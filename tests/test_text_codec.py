import json
import struct
import sys
import unittest
import tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
import text_codec as c
import catalog

class CodecTests(unittest.TestCase):
    def test_alias_roundtrip(self):
        text='Nhấn nút START — Chơi mới'
        encoded=c.encode_text(text)
        self.assertEqual(c.decode_text(encoded),text)
        for char in 'ấớ':self.assertNotIn(char.encode(),encoded)
        self.assertIn('ú'.encode(),encoded)

    def test_normalizes_accents(self):
        import unicodedata
        text='Nhấn nút START'
        self.assertEqual(c.encode_text(text),c.encode_text(unicodedata.normalize('NFD',text)))

    def test_missing_and_reserved_slots_fail(self):
        with self.assertRaises(ValueError):c.encode_text('Nhấn',{})
        with self.assertRaises(ValueError):c.encode_text('\u0500')

    def test_alias_font_preserves_textures(self):
        data=bytearray(1311584);struct.pack_into('>I',data,4,15)
        struct.pack_into('>4H',data,0x1e0+ord('ấ')*8,42,37,16,0)
        struct.pack_into('>4H',data,0x1e0+0x500*8,0,0xfc00,0,0)
        patched=c.alias_font(bytes(data),{'ấ':'\u0500'})
        self.assertEqual(patched[0x801e0:],data[0x801e0:])
        self.assertEqual(patched[0x1e0+0x500*8:0x1e0+0x500*8+8],data[0x1e0+ord('ấ')*8:0x1e0+ord('ấ')*8+8])
        with self.assertRaises(ValueError):c.alias_font(bytes(data),{'ớ':'\u0500'})

    def test_candidate_scanner_keeps_original_offset_and_markers(self):
        data=b'\x01$Hello there!\nStay here.\0junk\xff'
        self.assertEqual(list(catalog.candidate_runs(data)),[(1,'$Hello there!\nStay here.')])

    def test_catalog_rejects_changed_source_and_lost_control(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as folder:
            root=Path(folder)
            row=catalog.make_row('talk/en/test.bin_',4,'$Hello there!')
            data={'file':'talk/en/test.bin_','file_sha256':'original','entries':[row]}
            index={'files':[{'catalog':'test.json','file':data['file'],'source_sha256':'original','entries':1}],'total_entries':1}
            (root/'index.json').write_text(json.dumps(index),encoding='utf-8')
            def save(): (root/'test.json').write_text(json.dumps(data),encoding='utf-8')
            save();catalog.validate(root)
            row['vi']='Xin chào!';row['status']='draft';save()
            with self.assertRaisesRegex(ValueError,'Control'):catalog.validate(root)
            row['vi']='$Xin chào!';save();catalog.validate(root)
            row['source']='Changed';save()
            with self.assertRaisesRegex(ValueError,'Source changed'):catalog.validate(root)

if __name__=='__main__':unittest.main()
