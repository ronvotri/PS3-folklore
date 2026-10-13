"""Folklore BCUS98147: guarded CMC *same-byte-length* multi-line patch builder.

Interim, opt-in test-copy patch. No relocation, no resizing, no script grammar claim.
All noneligible candidates remain untouched. Uses original SHA/catalog and font
V3 alias mapping; backs up every changed CMC before modifying the archive.
Requires Python 3.10+, stdlib only. NEVER run against your only game copy.
"""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import unicodedata

import cmc_frame_audit as audit
import text_codec

BACKUP_FOLDER = 'Folklore-CMC-FixedBatch-Backup'
BACKUP_MANIFEST = 'manifest.json'
# Cannot assume the byte at mod3 is text or metadata. Preserve it identically.
TOKENS = re.compile(r'<[^<>\n]+>|%(?:\d+\$)?[sdif]|\{\d+\}|\$')


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def json_dump(obj: dict) -> bytes:
    return (json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode('utf-8')


def changed_runs(a: bytes, b: bytes):
    if len(a) != len(b):
        raise ValueError('Changed sizes are forbidden')
    begin = None
    for i, (x, y) in enumerate(zip(a, b)):
        if x != y and begin is None:
            begin = i
        elif x == y and begin is not None:
            yield begin, i
            begin = None
    if begin is not None:
        yield begin, len(a)


def check_runtime():
    if sys.platform == 'win32':
        import subprocess
        result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq rpcs3.exe', '/FO', 'CSV', '/NH'],
                                capture_output=True, text=True, timeout=10, check=False)
        if result.returncode == 0 and 'rpcs3.exe' in result.stdout.lower():
            raise ValueError('Close RPCS3 before writing game files')


def row_decision(row: dict, raw: bytes, bounds: list[tuple[int, int]], mapping: dict) -> tuple[str, bytes | None]:
    source, target = row['source'], row['vi']
    at = row['file_offset']
    if not isinstance(target, str) or not target or row.get('status') not in ('draft', 'reviewed', 'tested'):
        return 'missing_translation', None
    if source == target:
        return 'unchanged_translation', None
    if not unicodedata.is_normalized('NFC', target) or '\0' in target:
        return 'invalid_text', None
    if TOKENS.findall(source) != TOKENS.findall(target):
        return 'special_tokens_changed', None
    if source.count('\n') != target.count('\n'):
        return 'linebreak_count_changed', None
    sbytes = source.encode('ascii')
    at_mod = at % 4
    if at_mod == 3:
        start = at-3
        if target[0] != source[0]:
            return 'uncertain_fourth_byte_changed', None
    elif at_mod == 0:
        start = at-4
        if start < 0 or not 1 <= raw[at-1] <= 31:
            return 'unrecognized_control', None
    else:
        return 'unrecognized_alignment', None
    if start < 0 or raw[start:start+3] != b'\0\x04\0' or not any(lo <= start and at+len(sbytes) < hi for lo,hi in bounds):
        return 'unrecognized_frame', None
    try:
        encoded = text_codec.encode_text(target, mapping)
    except (ValueError, UnicodeError):
        return 'needs_font_glyph_or_alias', None
    if len(encoded) != len(sbytes):
        return 'different_encoded_length', None
    if b'\0' in encoded or raw[at:at+len(sbytes)+1] != sbytes + b'\0':
        raise ValueError('Original byte mismatch after SHA validation')
    return 'eligible', encoded


@dataclass(frozen=True)
class Change:
    at: int
    source: bytes
    target: bytes


@dataclass(frozen=True)
class FilePlan:
    name: str
    offset: int
    original: bytes
    patched: bytes
    changes: tuple[Change, ...]


def make_file_plan(data: bytes, cat: dict, expected_sha: str, mapping: dict,
                   *, name: str, offset: int) -> tuple[FilePlan | None, Counter]:
    if cat['file'] != name:
        raise ValueError('Catalog name mismatch: ' + name)
    audit.audit_catalog(data, cat, expected_sha)  # Source SHA, text+NUL, sections.
    bounds = audit.cmc_talk_bounds(data)
    reasons: Counter[str] = Counter()
    changes: list[Change] = []
    out = bytearray(data)
    occupied = set()
    for row in cat['entries']:
        reason, target_bytes = row_decision(row, data, bounds, mapping)
        reasons[reason] += 1
        if reason != 'eligible':
            continue
        at = row['file_offset']
        src = row['source'].encode('ascii')
        assert target_bytes is not None
        for k in range(at,at+len(src)):
            if k in occupied:
                raise ValueError(f'Overlapping translation slots in {name}')
            occupied.add(k)
        out[at:at+len(src)] = target_bytes
        changes.append(Change(at,src,target_bytes))
    if not changes:
        return None, reasons
    patched = bytes(out)
    if len(patched) != len(data):
        raise ValueError('CMC file length changed')
    diff = {i for i,(x,y) in enumerate(zip(data,patched)) if x!=y}
    if not diff.issubset(occupied) or not diff:
        raise ValueError('Patch changed outside authorized source bytes')
    for change in changes:
        if data[change.at-1] != patched[change.at-1] or data[change.at+len(change.source)] != 0:
            raise ValueError('Record boundary changed')
    return FilePlan(name,offset,data,patched,tuple(changes)),reasons


def get_plan(bin_dir: Path, root: Path) -> tuple[list[FilePlan],dict]:
    baseline = audit.load_json(root/'docs/baseline.json')
    index = audit.load_json(root/'translations/index.json')
    if baseline.get('game_id') != 'BCUS98147' or index.get('game_id') != 'BCUS98147':
        raise ValueError('Unexpected game ID')
    archive = bin_dir/'etc.bin_'
    archive_size = archive.stat().st_size
    if archive_size != baseline['archive_size']:
        raise ValueError('Archive size not equal to BCUS98147 baseline')
    entries = audit.read_fht(bin_dir,archive_size)
    specs = [x for x in index['files'] if x['file'].startswith('cmc/en/') and x['kind']=='dialogue']
    mapping = text_codec.load_mapping(root/'fonts/aliases.json')
    plans: list[FilePlan] = []
    tally = Counter()
    by_file = []
    with archive.open('rb') as stream:
        for spec in specs:
            name = spec['file']
            if name not in entries:
                raise ValueError('Missing original CMC: '+name)
            offset,size = entries[name]
            if not 0<size<=audit.MAX_FILE_BYTES:
                raise ValueError('CMC size out of bounds: '+name)
            stream.seek(offset)
            data=stream.read(size)
            if len(data)!=size:
                raise ValueError('CMC truncated: '+name)
            cat=audit.load_json(root/'translations'/spec['catalog'])
            if len(cat['entries'])!=spec['entries']:
                raise ValueError('Catalog index count mismatch: '+name)
            plan,reasons=make_file_plan(data,cat,spec['source_sha256'],mapping,name=name,offset=offset)
            tally.update(reasons)
            if plan:
                plans.append(plan)
                by_file.append({'file':name,'eligible':len(plan.changes),'original_sha256':digest(data),
                                'patched_sha256':digest(plan.patched)})
    report={'schema':1,'game_id':'BCUS98147','kind':'FIXED_LENGTH_CMC_SAFE_BATCH_PLAN',
            'warning':'TEST COPY ONLY; not validated game dialogue parser/repacker',
            'catalogs_checked':len(specs),'candidates_checked':sum(tally.values()),
            'translated_candidates_eligible':tally['eligible'],
            'files_to_patch':len(plans),'skip_reasons':dict(sorted((k,v) for k,v in tally.items() if k!='eligible')),
            'files':by_file, 'font':'Merienda V3 (current 25 aliases only)',
            'scripts_talk_bin_supported':False,'allows_relocation':False}
    return plans,report


def _backup_path(bin_dir:Path)->Path:
    return bin_dir/BACKUP_FOLDER


def _write_runs(archive:Path, entries:list[FilePlan], *, restore:bool=False) -> None:
    if not entries:
        return
    # Double-check all regions before touching the first byte.
    with archive.open('r+b') as stream:
        for item in entries:
            current=item.patched if restore else item.original
            stream.seek(item.offset)
            if stream.read(len(current))!=current:
                raise ValueError('Prewrite original/patch mismatch: '+item.name)
        completed=[]
        try:
            for item in entries:
                old,new=(item.patched,item.original) if restore else (item.original,item.patched)
                for start,stop in changed_runs(old,new):
                    stream.seek(item.offset+start)
                    stream.write(new[start:stop])
                stream.flush()
                os.fsync(stream.fileno())
                stream.seek(item.offset)
                if stream.read(len(new))!=new:
                    raise ValueError('Postwrite mismatch: '+item.name)
                completed.append(item)
        except Exception:
            # Original backups remain on disk; attempt rollback for every planned span,
            # including the partly modified last item.
            for item in entries:
                original=item.patched if restore else item.original
                replacement=item.original if restore else item.patched
                for start,stop in changed_runs(original,replacement):
                    stream.seek(item.offset+start)
                    stream.write(original[start:stop])
            stream.flush()
            os.fsync(stream.fileno())
            raise


def apply(bin_dir:Path, plans:list[FilePlan], report:dict, *, confirm_test_copy:bool=False):
    if not confirm_test_copy:
        raise ValueError('Refused: --confirm-test-copy is required')
    check_runtime()
    archive=bin_dir/'etc.bin_'
    folder=_backup_path(bin_dir)
    if folder.exists():
        raise ValueError('Existing fixed-batch backup folder: restore first, or use clean game COPY')
    if not plans:
        raise ValueError('No exact-byte CMC replacements eligible. Archive unchanged')
    # Reserve backup folder atomically, then persist each original CMC before writing.
    folder.mkdir(exist_ok=False)
    manifest={'schema':1,'game_id':'BCUS98147','kind':'FIXED_LENGTH_CMC_BACKUP',
              'archive_size':archive.stat().st_size,'files':[]}
    try:
        for i,p in enumerate(plans):
            name=f'cmc_original_{i:04d}.bin'
            dest=folder/name
            with dest.open('xb') as fh:
                fh.write(p.original)
                fh.flush()
                os.fsync(fh.fileno())
            manifest['files'].append({'name':p.name,'offset':p.offset,'size':len(p.original),
                                      'original_sha256':digest(p.original),
                                      'patched_sha256':digest(p.patched), 'backup_file':name,
                                      'changes':[{'at':x.at,'source_hex':x.source.hex(),
                                                  'target_hex':x.target.hex()} for x in p.changes]})
        with (folder/BACKUP_MANIFEST).open('xb') as fh:
            fh.write(json_dump(manifest));fh.flush();os.fsync(fh.fileno())
        _write_runs(archive,plans)
    except Exception:
        # Keep backup folder for recovery. It is never deleted automatically.
        raise
    return {'mode':'installed','files_patched':len(plans),
            'candidate_lines_patched':report['translated_candidates_eligible'],
            'backup':str(folder)}


def restore(bin_dir:Path, *, confirm_test_copy:bool=False):
    if not confirm_test_copy:
        raise ValueError('Refused: --confirm-test-copy is required')
    check_runtime()
    folder=_backup_path(bin_dir)
    f=folder/BACKUP_MANIFEST
    if not f.is_file():
        raise ValueError('No fixed-batch manifest. Cannot restore unknown state')
    m=json.loads(f.read_text(encoding='utf-8'))
    if m.get('game_id')!='BCUS98147' or m.get('kind')!='FIXED_LENGTH_CMC_BACKUP':
        raise ValueError('Backup manifest unsupported')
    archive=bin_dir/'etc.bin_'
    if archive.stat().st_size != m['archive_size']:
        raise ValueError('Archive size changed')
    entries=audit.read_fht(bin_dir,archive.stat().st_size)
    plans=[]
    seen=set()
    for item in m['files']:
        name=item['name']
        if name in seen or name not in entries or entries[name]!=(item['offset'],item['size']):
            raise ValueError('Backup references invalid FHT entry')
        seen.add(name)
        if not re.fullmatch(r'cmc_original_\d{4}\.bin',item['backup_file']):
            raise ValueError('Unsafe backup file name')
        original=(folder/item['backup_file']).read_bytes()
        if len(original)!=item['size'] or digest(original)!=item['original_sha256']:
            raise ValueError('Original backup checksum mismatch')
        out=bytearray(original)
        for c in item['changes']:
            at=c['at'];source=bytes.fromhex(c['source_hex']);target=bytes.fromhex(c['target_hex'])
            if len(source)!=len(target) or original[at:at+len(source)]!=source:
                raise ValueError('Backup patch record invalid')
            out[at:at+len(source)]=target
        patched=bytes(out)
        if digest(patched)!=item['patched_sha256']:
            raise ValueError('Backup patched checksum mismatch')
        plans.append(FilePlan(name,item['offset'],original,patched,()))
    _write_runs(archive,plans,restore=True)
    return {'mode':'restored','files_restored':len(plans),'backup_retained':str(folder)}


def main()->int:
    p=argparse.ArgumentParser(description=__doc__)
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--game-root',type=Path)
    g.add_argument('--bin-dir',type=Path)
    p.add_argument('--action',choices=['plan','apply','restore'],default='plan')
    p.add_argument('--confirm-test-copy',action='store_true')
    p.add_argument('--out',type=Path,default=audit.ROOT/'dist/cmc-fixed-batch-plan.json')
    a=p.parse_args()
    try:
        folder=audit.archive_folder(a.game_root,None) if a.game_root else audit.archive_folder(None,a.bin_dir)
        if a.action=='restore':
            result=restore(folder,confirm_test_copy=a.confirm_test_copy)
        else:
            plans,report=get_plan(folder,audit.ROOT)
            if a.action=='apply':
                result=apply(folder,plans,report,confirm_test_copy=a.confirm_test_copy)
            else:
                dest=audit.safe_output(a.out,audit.ROOT)
                dest.parent.mkdir(parents=True,exist_ok=True)
                dest.write_bytes(json_dump(report))
                result={k:report[k] for k in ('catalogs_checked','candidates_checked','translated_candidates_eligible','files_to_patch','skip_reasons')}
                result['plan_file']=str(dest)
    except (ValueError,OSError,KeyError,UnicodeError,TypeError) as exc:
        p.exit(1,'CMC batch refused: '+str(exc)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0


if __name__=='__main__':
    raise SystemExit(main())
