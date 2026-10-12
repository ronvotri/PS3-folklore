"""Synthetic tests: no game data and no real dialogue strings."""
from __future__ import annotations
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import dialogue_frame_hypothesis as frame


def fake_probe(*, printable=False, signature=True, bad_pad=False):
    section = {'name':'talk0','start':64,'end':192,'is_talk':True}
    # First source string is 'FIRST' ending in NUL at 100.
    left = {'source':'FIRST','file_offset':95,'nul_at':100,'section':'talk0'}
    if printable:
        # next text begins at 107: gap 101..106 (6 bytes), then printed marker at 107.
        nxt = {'source':'(NEXT','file_offset':107,'nul_at':112,'section':'talk0'}
        # gap expected from 101: [0 0 0 0 04 00], starts next-3 == 104
        gap = b'\x01\0\0\0\x04\0' if bad_pad else b'\0\0\0\0\x04\0'
        # However next=107, frame-start=104, gap start=101 => byte indices 3,4,5.
    else:
        # next text begins at 108; frame starts 104. gap 101..107 = 7 bytes.
        nxt = {'source':'NEXT','file_offset':108,'nul_at':112,'section':'talk0'}
        gap = b'\x01\0\0\0\x04\0\x18' if bad_pad else b'\0\0\0\0\x04\0\x18'
    if not signature:
        gap = gap.replace(b'\x04', b'\x05')
    left['bytes_after_hex'] = gap.hex(' ')
    nxt['bytes_after_hex'] = ''
    return {'schema':1,'game_id':'BCUS98147','mode':'READ_ONLY_FORENSICS',
            'reports':[{'file':'cmc/en/fake.bi5_', 'sections':[section],
                        'samples':[left,nxt]}]}


class FrameHypothesisTests(unittest.TestCase):
    def test_four_byte_aligned_control_frame(self):
        report=frame.analyze(fake_probe())
        f=report['files'][0]
        self.assertEqual(f['short_gap_pairs_checked'],1)
        self.assertEqual(f['matching_000400xx_frames'],1)
        self.assertEqual(f['matching_prefix_classes'],
                         {'nonprintable_leading_byte_at_mod0':1})
        self.assertFalse(report['contains_original_text_or_hex'])

    def test_printable_prefix_is_part_of_four_byte_frame_hypothesis(self):
        report=frame.analyze(fake_probe(printable=True))
        self.assertEqual(report['files'][0]['matching_000400xx_frames'],1)
        self.assertEqual(report['files'][0]['matching_prefix_classes'],
                         {'printable_leading_byte_at_mod3':1})
        text=json.dumps(report)
        self.assertNotIn('FIRST',text)
        self.assertNotIn('(NEXT',text)
        self.assertNotIn('bytes_after_hex',text)

    def test_invalid_signature_and_padding_are_not_accepted(self):
        wrong=frame.analyze(fake_probe(signature=False))['files'][0]
        self.assertEqual(wrong['matching_000400xx_frames'],0)
        self.assertEqual(wrong['nonmatching_reasons']['missing_000400_signature'],1)
        padded=frame.analyze(fake_probe(bad_pad=True))['files'][0]
        self.assertEqual(padded['matching_000400xx_frames'],0)
        self.assertEqual(padded['nonmatching_reasons']['nonzero_padding_before_frame'],1)

    def test_input_validation_and_local_output_only(self):
        with self.assertRaisesRegex(ValueError,'Not a Folklore'):
            frame.analyze({'mode':'PATCH'})
        with tempfile.TemporaryDirectory() as td:
            old=frame.ROOT
            try:
                frame.ROOT=Path(td)
                (frame.ROOT/'local-data').mkdir()
                src=frame.ROOT/'local-data/raw.json'
                dest=frame.ROOT/'local-data/out.json'
                src.write_text(json.dumps(fake_probe()),encoding='utf-8')
                before=src.read_bytes()
                got=frame.run(src,dest)
                self.assertEqual(got['files'][0]['matching_000400xx_frames'],1)
                self.assertEqual(src.read_bytes(),before)
                self.assertNotIn('FIRST',dest.read_text())
                with self.assertRaisesRegex(ValueError,'ignored'):
                    frame.run(src,frame.ROOT/'outside.json')
            finally:
                frame.ROOT=old

if __name__ == '__main__':
    unittest.main()
