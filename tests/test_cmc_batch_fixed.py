"""Synthetic CMC-only tests; no original Folklore assets, no RPCS3."""
from __future__ import annotations
import hashlib, importlib.util, json, pathlib, re, struct, sys, tempfile, types, unittest
from unittest import mock
from pathlib import Path

# Stand-in dependencies with the same source SHA/Catalog checks to exercise the
# batch writer without downloading the repo or using copyrighted game binaries.
audit=types.ModuleType('cmc_frame_audit')
class AuditFns:
    @staticmethod
    def digest(b): return hashlib.sha256(b).hexdigest()
    @staticmethod
    def load_json(p): return json.loads(Path(p).read_text())
    @staticmethod
    def safe_output(p, root):
        p=Path(p).resolve()
        if not p.is_relative_to((root/'dist').resolve()): raise ValueError('unsafe output')
        return p
    @staticmethod
    def cmc_talk_bounds(data):
        declared,count=struct.unpack_from('>II',data)
        if declared!=len(data): raise ValueError('invalid CMC size')
        edges=struct.unpack_from('>'+str(count+1)+'I',data,0x30)
        return [(edges[i],edges[i+1]) for i in range(count)]
    @staticmethod
    def audit_catalog(data,cat,expected):
        if hashlib.sha256(data).hexdigest()!=expected or cat['file_sha256']!=expected:
            raise ValueError('Original CMC SHA mismatch')
        bounds=AuditFns.cmc_talk_bounds(data)
        for r in cat['entries']:
            source=r['source'].encode('ascii');at=r['file_offset']
            assert data[at:at+len(source)+1]==source+b'\x00'
            assert r['source_sha256']==hashlib.sha256(source).hexdigest()
            assert any(lo<=at and at+len(source)<hi for lo,hi in bounds)
            assert r['id']==f"{cat['file']}@{at:08x}"
        return {'matching_frame_count':len(cat['entries'])}
    @staticmethod
    def read_fht(bin_dir,archive_size):
        b=(bin_dir/'etc.fht_').read_bytes();r={}
        for start in range(0,len(b),40):
            entry=b[start:start+40];r[entry[:32].split(b'\0')[0].decode()]=struct.unpack('>II',entry[32:40])[::-1]
        return r

audit.digest=AuditFns.digest; audit.load_json=AuditFns.load_json
audit.cmc_talk_bounds=AuditFns.cmc_talk_bounds; audit.audit_catalog=AuditFns.audit_catalog
audit.read_fht=AuditFns.read_fht;audit.safe_output=AuditFns.safe_output
# read_fht returns (offset,size)
audit.MAX_FILE_BYTES=128*1024*1024
sys.modules['cmc_frame_audit']=audit
codec=types.ModuleType('text_codec')
codec.load_mapping=lambda path:{'ế':'Ԉ'}
codec.encode_text=lambda text,mapping: ''.join(mapping.get(c,c) for c in text).encode('utf-8')
sys.modules['text_codec']=codec
spec=importlib.util.spec_from_file_location('batch',Path(__file__).resolve().parents[1]/'tools'/'cmc_batch_fixed.py')
batch=importlib.util.module_from_spec(spec);sys.modules['batch']=batch;spec.loader.exec_module(batch)


def fixture():
    name='cmc/en/LCmc000_en.bi5_';raw=bytearray(0x200)
    struct.pack_into('>II',raw,0,len(raw),1)
    struct.pack_into('>2I',raw,0x30,0x80,len(raw))
    raw[0x38:0x3d]=b'talk0'
    raw[0x80:0x84]=b'\0\x04\0\x18'
    raw[0x84:0x95]=b'Say something...\0'
    raw[0xa0:0xa4]=b'\0\x04\0$'
    raw[0xa3:0xa9]=b'$Hi!!\0'
    rows=[]
    for at,src,vi in [(0x84,'Say something...','Lên tiếng đi!'),(0xa3,'$Hi!!','$Ôi!')]:
        rows.append({'id':f'{name}@{at:08x}','file_offset':at,
                     'source':src,'source_sha256':hashlib.sha256(src.encode()).hexdigest(),
                     'vi':vi,'status':'draft'})
    data=bytes(raw)
    return data,{'file':name,'file_sha256':hashlib.sha256(data).hexdigest(),'entries':rows}


class BatchTests(unittest.TestCase):
    def test_two_full_line_replacements_byte_exact_and_fourth_byte_preserved(self):
        raw,cat=fixture()
        # Local mock codec doesn't map 'ê' and 'ế' correctly; use basic Unicode exact
        # length by constructing matching-length targets in this synthetic test.
        cat['entries'][0]['vi']='Go and speak now'  # 16 ASCII bytes
        cat['entries'][1]['vi']='$Go!!'
        plan,counts=batch.make_file_plan(raw,cat,hashlib.sha256(raw).hexdigest(),
                                         codec.load_mapping(None),name=cat['file'],offset=0)
        self.assertEqual(counts['eligible'],2)
        self.assertEqual(len(plan.patched),len(raw))
        self.assertEqual(plan.patched[0x80:0x84],raw[0x80:0x84])
        self.assertEqual(plan.patched[0xa0:0xa4],raw[0xa0:0xa4])
        self.assertEqual(plan.patched[0x94],0)
        self.assertEqual(plan.patched[0xa8],0)
        self.assertEqual(set(i for i,(x,y) in enumerate(zip(plan.patched,raw)) if x!=y).issubset(
                         set(range(0x84,0x94))|set(range(0xa3,0xa8))),True)

    def test_unpatchable_translation_skipped_without_rewriting(self):
        raw,cat=fixture()
        cat['entries'][0]['vi']='Long long long long sentence'
        cat['entries'][1]['vi']='Changed prefix'
        plan,reasons=batch.make_file_plan(raw,cat,hashlib.sha256(raw).hexdigest(),
                                          codec.load_mapping(None),name=cat['file'],offset=0)
        self.assertIsNone(plan)
        self.assertEqual(reasons['different_encoded_length'],1)
        self.assertEqual(reasons['special_tokens_changed'],1)

    def test_source_hash_and_control_mismatch_fail_closed(self):
        raw,cat=fixture()
        with self.assertRaisesRegex(ValueError,'SHA mismatch'):
            batch.make_file_plan(raw,cat,'x'*64,{},name=cat['file'],offset=0)
        mutated=bytearray(raw);mutated[0x81]=3
        cat['file_sha256']=hashlib.sha256(mutated).hexdigest()
        plan,counts=batch.make_file_plan(bytes(mutated),cat,hashlib.sha256(mutated).hexdigest(),
                                         codec.load_mapping(None),name=cat['file'],offset=0)
        self.assertEqual(counts['unrecognized_frame'],1)


    def test_tokens_lines_and_non_nfc_are_skipped_not_broken(self):
        raw,cat=fixture()
        cat['entries'][0]['vi']='Lên\ntố thêm'
        cat['entries'][1]['vi']='$O\u0302i!'
        plan,counts=batch.make_file_plan(raw,cat,hashlib.sha256(raw).hexdigest(),
                                         codec.load_mapping(None),name=cat['file'],offset=0)
        self.assertIsNone(plan)
        self.assertEqual(counts['linebreak_count_changed'],1)
        self.assertEqual(counts['invalid_text'],1)

    def test_full_plan_apply_restore_and_backup_tamper(self):
        raw,cat=fixture()
        cat['entries'][0]['vi']='Go and speak now';cat['entries'][1]['vi']='$Go!!'
        name=cat['file']; h=hashlib.sha256(raw).hexdigest()
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)/'repo';bin_dir=Path(td)/'game';bin_dir.mkdir();
            (root/'docs').mkdir(parents=True);(root/'translations/catalogs/cmc').mkdir(parents=True);(root/'fonts').mkdir(parents=True)
            catpath='catalogs/cmc/LCmc000_en.bi5_.json'
            (root/'docs/baseline.json').write_text(json.dumps({'game_id':'BCUS98147','archive_size':0x100+len(raw)}))
            (root/'translations/index.json').write_text(json.dumps({'game_id':'BCUS98147','files':[
                {'file':name,'kind':'dialogue','catalog':catpath,'source_sha256':h,'entries':2}]}))
            (root/'translations'/catpath).write_text(json.dumps(cat))
            (root/'fonts/aliases.json').write_text('{}')
            archive=bin_dir/'etc.bin_';archive.write_bytes(b'X'*0x100+raw)
            (bin_dir/'etc.fht_').write_bytes(name.encode().ljust(32,b'\0')+struct.pack('>II',len(raw),0x100))
            before=archive.read_bytes()
            plans,summary=batch.get_plan(bin_dir,root)
            self.assertEqual((summary['translated_candidates_eligible'],summary['files_to_patch']),(2,1))
            self.assertEqual(archive.read_bytes(),before)
            with self.assertRaisesRegex(ValueError,'confirm-test-copy'):
                batch.apply(bin_dir,plans,summary)
            patched=batch.apply(bin_dir,plans,summary,confirm_test_copy=True)
            self.assertEqual(patched['files_patched'],1)
            self.assertNotEqual(archive.read_bytes(),before)
            with self.assertRaisesRegex(ValueError,'backup folder'):
                batch.apply(bin_dir,plans,summary,confirm_test_copy=True)
            self.assertEqual(batch.restore(bin_dir,confirm_test_copy=True)['mode'],'restored')
            self.assertEqual(archive.read_bytes(),before)
            backup=bin_dir/batch.BACKUP_FOLDER/'cmc_original_0000.bin'
            backup.write_bytes(b'INVALID')
            with self.assertRaisesRegex(ValueError,'checksum mismatch'):
                batch.restore(bin_dir,confirm_test_copy=True)
            self.assertEqual(archive.read_bytes(),before)

if __name__=='__main__':unittest.main()
