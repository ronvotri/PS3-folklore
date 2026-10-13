"""Synthetic tests only. They do NOT prove Folklore in-game dialogue renders."""
from pathlib import Path
import hashlib
import importlib.util
import struct
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'tools'))
import cmc_alpha01 as alpha


def synthetic_cmc():
    # 1 section, 256 bytes. Header table begins 0x30, name begins 0x38.
    data = bytearray(0x200)
    struct.pack_into('>II', data, 0, len(data), 1)
    struct.pack_into('>2I', data, 0x30, 0x80, len(data))
    data[0x38:0x38+5] = b'talk0'
    data[0x80:0x84] = b'\x00\x04\x00\x18'
    data[0x84:0x84+17] = b'Say something...\0'
    return bytes(data)


class TrialPatchTests(unittest.TestCase):
    def test_same_length_alias_source_and_one_text_slot_only(self):
        source = synthetic_cmc()
        with patch.object(alpha, 'CMC_SHA', alpha.sha(source)), patch.object(
            alpha, 'PATCHES', ((0x84, 'Say something...', 'Lên tiếng đi!'),)):
            patched = alpha.build_trial(source)
        self.assertEqual(len(patched), len(source))
        self.assertEqual(patched[0x80:0x84], source[0x80:0x84])
        self.assertEqual(patched[0x84+16], 0)
        self.assertEqual(patched[0x84:0x84+16], alpha.encode_target('Lên tiếng đi!'))
        self.assertEqual(patched[:0x84],source[:0x84])
        self.assertEqual(patched[0x84+16:],source[0x84+16:])

    def test_wrong_sha_frame_length_and_missing_alias_fail(self):
        original = synthetic_cmc()
        with self.assertRaisesRegex(ValueError, 'SHA differs'):
            alpha.build_trial(original)
        with patch.object(alpha,'CMC_SHA',alpha.sha(original)),patch.object(
                alpha,'PATCHES',((0x84,'Say something...','Nói!'),)):
            with self.assertRaisesRegex(ValueError,'Not same byte length'):
                alpha.build_trial(original)
        with patch.object(alpha,'CMC_SHA',alpha.sha(original)),patch.object(
                alpha,'PATCHES',((0x84,'Say something...','Mẹ'),)):
            with self.assertRaisesRegex(ValueError,'font aliases'):
                alpha.build_trial(original)
        broken = bytearray(original)
        broken[0x81] = 3
        with patch.object(alpha,'CMC_SHA',alpha.sha(broken)),patch.object(
                alpha,'PATCHES',((0x84,'Say something...','Lên tiếng đi!'),)):
            with self.assertRaisesRegex(ValueError,'Unrecognized CMC frame'):
                alpha.build_trial(bytes(broken))

    def test_check_apply_restore_and_wrong_modified_archive_refused(self):
        original = synthetic_cmc()
        with tempfile.TemporaryDirectory() as d:
            dir = Path(d)
            archive = dir/'etc.bin_'
            base_offset=0x100
            archive.write_bytes(b'\x00'*base_offset+original+b'\xFF'*160)
            name = alpha.CMC_NAME.encode('ascii').ljust(32,b'\x00')
            (dir/'etc.fht_').write_bytes(name+struct.pack('>II',len(original),base_offset))
            archive_bytes=archive.read_bytes()
            with patch.object(alpha,'ARCHIVE_SIZE',len(archive_bytes)),patch.object(
                 alpha,'CMC_SHA',alpha.sha(original)),patch.object(
                 alpha,'PATCHES',((0x84,'Say something...','Lên tiếng đi!'),)):
                self.assertFalse(alpha.action(dir,'check')['archive_modified'])
                self.assertEqual(archive.read_bytes(),archive_bytes)
                assert alpha.action(dir,'apply')['mode']=='installed'
                after=archive.read_bytes()
                self.assertEqual(len(after),len(archive_bytes))
                self.assertEqual(after[:base_offset],archive_bytes[:base_offset])
                self.assertEqual(after[base_offset+len(original):],archive_bytes[base_offset+len(original):])
                self.assertTrue(alpha.original_backup(dir).is_file())
                with self.assertRaisesRegex(ValueError,'already installed'):
                    alpha.action(dir,'apply')
                self.assertEqual(alpha.action(dir,'restore')['mode'],'restored')
                self.assertEqual(archive.read_bytes(),archive_bytes)

    def test_modified_archive_rejected_and_backup_tampering_rejected(self):
        original = synthetic_cmc()
        with tempfile.TemporaryDirectory() as d:
            directory=Path(d)
            offset=40
            archive=directory/'etc.bin_'
            archive.write_bytes(b'\0'*offset+original)
            (directory/'etc.fht_').write_bytes(alpha.CMC_NAME.encode().ljust(32,b'\0')+struct.pack('>II',len(original),offset))
            with patch.object(alpha,'ARCHIVE_SIZE',archive.stat().st_size), patch.object(
                 alpha,'CMC_SHA',alpha.sha(original)),patch.object(
                 alpha,'PATCHES',((0x84,'Say something...','Lên tiếng đi!'),)):
                blob=bytearray(archive.read_bytes());blob[-1]=55;archive.write_bytes(blob)
                with self.assertRaisesRegex(ValueError,'not original'):
                    alpha.action(directory,'apply')
                archive.write_bytes(b'\0'*offset+original)
                backup=alpha.original_backup(directory);backup.parent.mkdir(parents=True)
                backup.write_bytes(b'WRONG')
                with self.assertRaisesRegex(ValueError,'backup conflicts'):
                    alpha.action(directory,'apply')

if __name__=='__main__':
    unittest.main()
