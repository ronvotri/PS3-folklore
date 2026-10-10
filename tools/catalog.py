"""Extract text-only translation drafts locally; validate them without ROM on cloud.

Offsets identify original source bytes, never destinations for variable-length writes.
Dialogue extraction is conservative ASCII candidate scanning, NOT a repacker.
"""
import argparse
import collections
import hashlib
import json
import re
import unicodedata
from pathlib import Path
import folklore as f

ROOT=Path(__file__).resolve().parents[1]
TOKEN=re.compile(r'<[^<>\n]+>|%(?:\d+\$)?[sdif]|\{\d+\}|\$')
def digest(text):return hashlib.sha256(text.encode('utf-8')).hexdigest()

def candidate_runs(data,start=0,end=None):
    end=len(data) if end is None else end
    for match in re.finditer(rb'[\x20-\x7e\t\r\n]{4,}',data[start:end]):
        stop=start+match.end();text=match.group().decode('ascii')
        if stop>=end or data[stop]!=0:continue
        if not re.search(r'[A-Za-z]{3}',text):continue
        if not (' ' in text or '?' in text or '!' in text):continue
        if len(text)>3000:continue
        yield start+match.start(),text

def cmc_ranges(data):
    declared,count=__import__('struct').unpack_from('>II',data)
    if declared!=len(data) or not 1<=count<=64:raise ValueError('Unsupported CMC header')
    name_base=0x30+4*(count+1)
    offsets=__import__('struct').unpack_from(f'>{count+1}I',data,0x30)
    if any(a>b for a,b in zip(offsets,offsets[1:])) or offsets[-1]>len(data):
        raise ValueError('Invalid CMC offsets')
    for i in range(count):
        name=data[name_base+i*24:name_base+i*24+24].split(b'\0',1)[0]
        if name.startswith(b'talk'):yield offsets[i],offsets[i+1]

def make_row(filename,offset,source,vi='',verified=False):
    return {'id':f'{filename}@{offset:08x}','file_offset':offset,'source':source,
            'source_sha256':digest(source),'vi':vi,'status':'draft' if vi else 'todo',
            'source_review':'verified_menu' if verified else 'candidate','notes':''}

def extract(root,out,original_package):
    entries=f.read_index(root);files=[]
    translations=f.read_json(ROOT/'translations/menu_vi.json')
    old=f.read_json(original_package)
    recovered={p['name']:__import__('base64').b64decode(p['original_base64']) for p in old['patches']}
    baseline=f.read_json(ROOT/'docs/baseline.json')
    spec=next(s for s in baseline['menu_files'] if s['name']=='lang_en.bi5_')
    menu=recovered['lang_en.bi5_']
    if f.sha256(menu)!=spec['original_sha256']:raise ValueError('Original menu hash mismatch')
    selected=['lang_en.bi5_']+sorted(n for n in entries if n.startswith('talk/en/'))+sorted(n for n in entries if n.startswith('cmc/en/') and n.endswith('_en.bi5_'))
    with (root/'etc.bin_').open('rb') as archive:
        for filename in selected:
            e=entries[filename]
            if filename=='lang_en.bi5_':
                data=menu;rows=[];start=f.system_layout(data)[0]
                for rel,raw,_ in f.system_layout(data)[4]:
                    try:source=raw.decode('utf-8')
                    except UnicodeDecodeError:continue
                    if not re.search(r'[A-Za-z]',source):continue
                    rows.append(make_row(filename,start+rel,source,translations.get(source,''),True))
                section='system';kind='menu'
            else:
                archive.seek(e['offset']);data=archive.read(e['size'])
                ranges=list(cmc_ranges(data)) if filename.startswith('cmc/') else [(0,len(data))]
                rows=[make_row(filename,pos,text) for start,end in ranges for pos,text in candidate_runs(data,start,end)]
                section='talk sections' if filename.startswith('cmc/') else 'ASCII NUL candidates';kind='dialogue'
            if not rows:continue
            folder='menu' if kind=='menu' else 'talk' if filename.startswith('talk/') else 'cmc'
            path=Path('catalogs')/folder/(Path(filename).name+'.json')
            f.write_json(out/path,{'schema':1,'game_id':'BCUS98147','file':filename,'file_sha256':f.sha256(data),'extraction':section,'repacker':'menu_only' if kind=='menu' else 'not_implemented','entries':rows})
            files.append({'catalog':path.as_posix(),'file':filename,'source_sha256':f.sha256(data),'entries':len(rows),'kind':kind})
    f.write_json(out/'index.json',{'schema':1,'game_id':'BCUS98147','files':files,'total_entries':sum(v['entries'] for v in files)})
    print(f'Extracted {len(files)} text catalogs; {sum(v["entries"] for v in files)} rows')

def validate(root):
    index=f.read_json(root/'index.json');seen=set();counts=collections.Counter()
    for item in index['files']:
        data=f.read_json(root/item['catalog'])
        if data['file']!=item['file'] or data['file_sha256']!=item['source_sha256'] or len(data['entries'])!=item['entries']:
            raise ValueError('Catalog manifest mismatch')
        for row in data['entries']:
            label=row['id'];source=row['source'];target=row['vi'];status=row['status']
            if label in seen or label!=f'{data["file"]}@{row["file_offset"]:08x}':raise ValueError('Invalid/duplicate ID')
            seen.add(label)
            if digest(source)!=row['source_sha256']:raise ValueError('Source changed: '+label)
            if status not in ('todo','draft','reviewed','tested','skip'):raise ValueError('Unknown status: '+label)
            if row['source_review'] not in ('candidate','verified_menu','reviewed'):raise ValueError('Unknown source review')
            if not isinstance(target,str) or '\0' in target or target!=unicodedata.normalize('NFC',target):raise ValueError('Invalid/NFD target: '+label)
            if any(0x500<=ord(c)<0x580 for c in target):raise ValueError('Reserved game aliases in human translation')
            if status in ('draft','reviewed','tested') and not target:raise ValueError('Missing target: '+label)
            if status=='tested' and row['source_review']=='candidate':raise ValueError('Candidate cannot be runtime-tested')
            if target and collections.Counter(TOKEN.findall(source))!=collections.Counter(TOKEN.findall(target)):
                raise ValueError('Control tag or placeholder changed: '+label)
            counts[status]+=1
    if len(seen)!=index['total_entries']:raise ValueError('Total mismatch')
    print(f'Validated {len(seen)} rows: '+', '.join(f'{k}={v}' for k,v in sorted(counts.items())))
    return counts

def main():
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='command',required=True)
    x=sub.add_parser('extract');x.add_argument('--bin-dir',type=Path,required=True);x.add_argument('--out',type=Path,default=ROOT/'translations');x.add_argument('--original-package',type=Path,required=True)
    v=sub.add_parser('validate');v.add_argument('--root',type=Path,default=ROOT/'translations')
    args=p.parse_args()
    if args.command=='extract':extract(args.bin_dir,args.out,args.original_package)
    else:validate(args.root)

if __name__=='__main__':main()
