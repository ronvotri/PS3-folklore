"""Synthetic, read-only boundary tests. Does not need original game files."""
import unittest
import types
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import cmc_exception_ids as subject


def row(offset, source='HELLO!'):
    name = 'cmc/en/test.bi5_'
    return {'id': f'{name}@{offset:08x}', 'file_offset': offset, 'source': source}


class ExceptionLocatorTests(unittest.TestCase):
    def test_matching_control_and_printable_frames(self):
        data = bytearray(128)
        data[32:36] = b'\0\x04\0\x18'
        data[36:43] = b'HELLO!\0'
        data[48:52] = b'\0\x04\0$'
        data[51:59] = b'$WORLD!\0'
        self.assertIsNone(subject.candidate_reason(bytes(data), row(36), [(16,128)]))
        self.assertIsNone(subject.candidate_reason(bytes(data), row(51,'$WORLD!'), [(16,128)]))

    def test_misaligned_and_newline_leading_candidates(self):
        data = bytes(128)
        self.assertEqual(subject.candidate_reason(data,row(41),[(16,128)]),'unexpected_mod1')
        self.assertEqual(subject.candidate_reason(data,row(42),[(16,128)]),'unexpected_mod2')
        self.assertEqual(subject.candidate_reason(data,row(43,'\nHELLO'),[(16,128)]),
                         'mod3_nonprintable_source_prefix')

    def test_missing_signature_and_out_of_bounds(self):
        data = bytes(128)
        self.assertEqual(subject.candidate_reason(data,row(36),[(16,128)]),
                         'not_000400_frame')
        self.assertEqual(subject.candidate_reason(data,row(4),[(16,128)]),
                         'frame_outside_talk_bounds')
        bad = bytearray(data)
        bad[32:36] = b'\0\x04\0\xff'
        self.assertEqual(subject.candidate_reason(bytes(bad),row(36),[(16,128)]),
                         'noncontrol_marker_before_text')

    def test_fail_closed_on_inconsistent_counts_and_changed_roundtrip(self):
        binary = b'ORIGINAL_BLOB'
        catalog = {'file':'cmc/en/test.bi5_', 'entries':[row(41)]}
        class Good:
            matched_candidates=0
            opaque_candidates=1
            total_bytes=len(binary)
            def serialize(self): return binary
        audit = types.SimpleNamespace(
            audit_catalog=lambda *args: {
                'matching_frame_count':0,'nonmatching_reasons':{'unexpected_mod1':1}},
            cmc_talk_bounds=lambda data:[(0,128)])
        tokens = types.SimpleNamespace(tokenize=lambda *args:Good())
        got = subject.locate_one(binary,catalog,'sha',audit,tokens)
        self.assertEqual(got['opaque_candidate_count'],1)
        self.assertEqual(got['exceptions'][0]['id'],row(41)['id'])
        audit.audit_catalog=lambda *args: {
            'matching_frame_count':1,'nonmatching_reasons':{}}
        with self.assertRaisesRegex(ValueError,'disagrees'):
            subject.locate_one(binary,catalog,'sha',audit,tokens)
        audit.audit_catalog=lambda *args: {
            'matching_frame_count':0,'nonmatching_reasons':{'unexpected_mod1':1}}
        class Bad(Good):
            def serialize(self): return b'MODIFIED'
        tokens.tokenize=lambda *args:Bad()
        with self.assertRaisesRegex(ValueError,'Byte-exact'):
            subject.locate_one(binary,catalog,'sha',audit,tokens)


if __name__ == '__main__':
    unittest.main()
