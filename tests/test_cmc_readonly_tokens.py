"""Synthetic only. Never requires or changes real Folklore binaries."""
import json
from pathlib import Path
import sys
import unittest
from unittest import mock
import tempfile
import struct
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
import cmc_readonly_tokens as target


def example():
    name='cmc/en/LCmc000_en.bi5_'
    payload=bytearray(b'\0'*288)
    struct.pack_into('>II',payload,0,len(payload),2)
    struct.pack_into('>3I',payload,0x30,0x80,0xa0,0x120)
    payload[0x3c:0x3c+5]=b'talk0'
    payload[0x54:0x54+4]=b'anim'
    # confirmed text at mod0, marker control=24
    payload[0x80:0x84]=b'\0\x04\0\x18'
    payload[0x84:0x89]=b'HEY!\0'
    # Printable marker begins at 0x8f, frame starts at aligned 0x8c.
    payload[0x8c:0x90]=b'\0\x04\0$'
    payload[0x8f:0x97]=b'$HELLO!\0'
    raw=bytes(payload)
    rows=[]
    for at,src in [(0x84,'HEY!'),(0x8f,'$HELLO!')]:
        rows.append({'id':f'{name}@{at:08x}', 'file_offset':at,
            'source':src,'source_sha256':target.audit.digest(src.encode()),
            'vi':'nháp','status':'draft'})
    catalog={'file':name,'file_sha256':target.audit.digest(raw),'entries':rows}
    return raw,catalog


class TokenizationTests(unittest.TestCase):
    def test_parse_serialize_byte_identical_and_separate_selector(self):
        raw,cat=example()
        result=target.tokenize(raw,cat,target.audit.digest(raw))
        self.assertEqual(result.serialize(),raw)
        self.assertEqual(result.matched_candidates,2)
        frames=[t for t in result.tokens if isinstance(t,target.FrameCandidate)]
        self.assertEqual([f.selector for f in frames],[24,36])
        self.assertEqual([f.text_ascii for f in frames],[b'HEY!',b'HELLO!'])
        self.assertEqual([f.selector_in_source for f in frames],[False,True])
        self.assertTrue(any(isinstance(t,target.Opaque) for t in result.tokens))

    def test_nonmatching_candidate_remains_opaque(self):
        raw,cat=example(); mod=bytearray(raw)
        # original text's prefix can fail the 00 04 00 signature yet remain a verified source
        mod[0x80:0x84]=b'\x55\x66\x77\x18'
        raw=bytes(mod);cat['file_sha256']=target.audit.digest(raw)
        r=target.tokenize(raw,cat,target.audit.digest(raw))
        self.assertEqual((r.matched_candidates,r.opaque_candidates),(1,1))
        self.assertEqual(r.serialize(),raw)

    def test_mismatch_source_fails_closed(self):
        raw,cat=example()
        with self.assertRaisesRegex(ValueError,'SHA-256 mismatch'):
            target.tokenize(raw,cat,'f'*64)
        cat['entries'][0]['source']='CHANGED'
        with self.assertRaises(ValueError):
            target.tokenize(raw,cat,target.audit.digest(raw))

    def test_tokens_cannot_be_used_to_add_nul(self):
        with self.assertRaisesRegex(ValueError,'Invalid frame token'):
            target.FrameCandidate(24,b'A\0B',False).serialize()
        self.assertFalse(hasattr(target,'apply_patch'))

if __name__=='__main__':unittest.main()