"""Fixture-only safety tests for a read-only, entire-CMC-catalog frame survey."""
from pathlib import Path
import json
import struct
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import cmc_frame_audit as scan

NAME = 'cmc/en/LCmc_test_en.bi5_'


def fixture():
    data=bytearray(0x200)
    struct.pack_into('>II',data,0,0x200,2)
    struct.pack_into('>3I',data,0x30,0x80,0x180,0x200)
    data[0x3c:0x3c+5]=b'talk0'
    data[0x54:0x54+3]=b'img'
    a,b=0x90,0xa7
    t1,t2='Hello world','$Good bye!'
    data[a-4:a]=b'\0\4\0\x18'
    data[a:a+len(t1)+1]=t1.encode()+b'\0'
    data[b-3:b+1]=b'\0\4\0$'
    data[b+1:b+len(t2)+1]=t2[1:].encode()+b'\0'
    rows=[{'id':f'{NAME}@{p:08x}','file_offset':p,'source':t,
           'source_sha256':scan.digest(t.encode()),'vi':'nháp','status':'draft'}
          for p,t in [(a,t1),(b,t2)]]
    result=bytes(data)
    cat={'file':NAME,'file_sha256':scan.digest(result),'entries':rows}
    return result,cat


class CmcFrameAuditTests(unittest.TestCase):
    def test_two_original_candidate_forms_and_empty_section(self):
        raw,cat=fixture()
        info=scan.audit_catalog(raw,cat,scan.digest(raw))
        self.assertEqual(info['matching_frame_count'],2)
        self.assertEqual(info['matching_forms'],{
            'printable_marker_in_candidate':1,'control_marker_before_candidate':1})
        self.assertEqual(info['nonmatching_reasons'],{})
        self.assertEqual(scan.cmc_talk_bounds(raw),[(0x80,0x180)])
        self.assertNotIn('Good',json.dumps(info))
        bad=bytearray(raw)
        struct.pack_into('>3I',bad,0x30,0x80,0x200,0x200)
        self.assertEqual(scan.cmc_talk_bounds(bytes(bad)),[(0x80,0x200)])

    def test_wrong_frame_counts_anomaly_without_patching_game(self):
        raw,cat=fixture()
        bad=bytearray(raw)
        bad[0x8d]=5
        updated=bytes(bad)
        cat['file_sha256']=scan.digest(updated)
        info=scan.audit_catalog(updated,cat,scan.digest(updated))
        self.assertEqual(info['matching_frame_count'],1)
        self.assertEqual(info['nonmatching_reasons'],{'not_000400_frame':1})
        bad[0xa4]=1
        info=scan.audit_catalog(bytes(bad),dict(cat,file_sha256=scan.digest(bytes(bad))),scan.digest(bytes(bad)))
        self.assertEqual(info['matching_frame_count'],0)
        self.assertEqual(info['nonmatching_reasons'],{'not_000400_frame':2})
        self.assertEqual(raw,fixture()[0])

    def test_fail_closed_on_source_digest_and_bounds(self):
        raw,cat=fixture()
        with self.assertRaisesRegex(ValueError,'SHA-256 mismatch'):
            scan.audit_catalog(raw,cat,'0'*64)
        wrong=json.loads(json.dumps(cat))
        wrong['entries'][0]['source']='Hello worlds'
        with self.assertRaisesRegex(ValueError,'source hash mismatch'):
            scan.audit_catalog(raw,wrong,scan.digest(raw))
        malformed=bytearray(raw)
        struct.pack_into('>3I',malformed,0x30,0x80,0x70,0x200)
        with self.assertRaisesRegex(ValueError,'section bounds invalid'):
            scan.cmc_talk_bounds(bytes(malformed))

    def test_end_to_end_read_only_and_output_guard(self):
        raw,cat=fixture()
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); game=root/'game';game.mkdir()
            (root/'translations/catalogs/cmc').mkdir(parents=True)
            (root/'docs').mkdir()
            archive=bytearray(4096)
            archive[1024:1024+len(raw)]=raw
            (game/'etc.bin_').write_bytes(archive)
            name=NAME.encode().ljust(32,b'\0')
            (game/'etc.fht_').write_bytes(name+struct.pack('>II',len(raw),1024))
            (root/'docs/baseline.json').write_text(json.dumps({'game_id':'BCUS98147','archive_size':4096}))
            catalog_rel='catalogs/cmc/LCmc_test_en.bi5_.json'
            (root/'translations/index.json').write_text(json.dumps({'game_id':'BCUS98147','files':[
                {'file':NAME,'kind':'dialogue','catalog':catalog_rel,'source_sha256':scan.digest(raw),'entries':2}]}))
            (root/'translations'/catalog_rel).write_text(json.dumps(cat))
            original=(game/'etc.bin_').read_bytes()
            output=root/'local-data/summary.json'
            result=scan.audit(game,root,out=output)
            self.assertEqual(result['files_audited'],1)
            self.assertEqual(result['frames_matching'],2)
            self.assertEqual(result['candidates_audited'],2)
            self.assertFalse(result['message_parser_proven'])
            self.assertFalse(result['contains_game_bytes_or_source_text'])
            self.assertEqual((game/'etc.bin_').read_bytes(),original)
            self.assertNotIn('Hello world',output.read_text())
            with self.assertRaisesRegex(ValueError,'local-data/ or dist'):
                scan.audit(game,root,out=root/'unsafe.json')
            output.unlink()
            binary=bytearray(original);binary[1024+0x91]^=1
            (game/'etc.bin_').write_bytes(binary)
            with self.assertRaisesRegex(ValueError,'SHA-256 mismatch'):
                scan.audit(game,root,out=output)
            self.assertFalse(output.exists())

if __name__=='__main__':
    unittest.main()