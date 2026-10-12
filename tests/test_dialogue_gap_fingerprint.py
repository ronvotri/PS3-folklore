"""Synthetic tests for the read-only Folklore structural gap classifier."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import dialogue_gap_fingerprint as qa


def report():
    return {'schema': 1, 'game_id': 'BCUS98147', 'mode': 'READ_ONLY_FORENSICS',
            'reports': [{'file': 'cmc/en/LCmc000_en.bi5_',
                         'sections': [{'name': 'talk1', 'start': 80, 'end': 256,
                                       'is_talk': True}],
                         'samples': [
                             {'file_offset': 100, 'nul_at': 104, 'section': 'talk1',
                              'bytes_after_hex': '00 04 80 20 66 6f 6f'},
                             {'file_offset': 109, 'nul_at': 112, 'section': 'talk1',
                              'bytes_after_hex': '00 05 03 00 62 61 72'},
                             {'file_offset': 117, 'nul_at': 119, 'section': 'talk1',
                              'bytes_after_hex': ''}]}]}


class GapFingerprintTests(unittest.TestCase):
    def test_fingerprint_never_exports_source_bytes(self):
        result = qa.analyze(report())
        out = result['files'][0]
        self.assertEqual(out['gap_lengths'], {'4': 2})
        self.assertEqual(out['sampled_candidates'], 3)
        self.assertEqual(out['short_gap_samples'][0]['class_counts'],
                         {'control': 1, 'high': 1, 'space': 1, 'zero': 1})
        self.assertEqual(out['short_gap_samples'][1]['class_counts'],
                         {'control': 2, 'zero': 2})
        text = json.dumps(result)
        for prohibited in ('bytes_after_hex', 'foo', 'bar', '00 04 80 20',
                           'source', 'samples_before_hex'):
            self.assertNotIn(prohibited, text)
        self.assertFalse(result['message_parser_proven'])
        self.assertFalse(result['repacker_available'])

    def test_rejects_negative_gap_and_bad_metadata(self):
        p = report()
        p['reports'][0]['samples'][0]['nul_at'] = 110
        with self.assertRaisesRegex(ValueError, 'Overlapping'):
            qa.analyze(p)
        p = report()
        p['mode'] = 'PATCH_WRITER'
        with self.assertRaisesRegex(ValueError, 'Not a Folklore'):
            qa.analyze(p)

    def test_long_gaps_do_not_export_bytes(self):
        p = report()
        p['reports'][0]['samples'][1]['file_offset'] = 200
        p['reports'][0]['samples'][1]['nul_at'] = 204
        p['reports'][0]['samples'][2]['file_offset'] = 240
        p['reports'][0]['samples'][2]['nul_at'] = 242
        res = qa.analyze(p)['files'][0]
        self.assertEqual(res['long_gaps_omitted'], 2)
        self.assertEqual(res['short_gap_samples'], [])

    def test_output_stays_local_and_input_is_unchanged(self):
        old_root = qa.ROOT
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root/'local-data').mkdir()
            inp = root/'local-data/probe.json'
            out = root/'local-data/stats.json'
            inp.write_text(json.dumps(report()), encoding='utf-8')
            before = inp.read_bytes()
            try:
                qa.ROOT = root
                qa.run(inp,out)
                self.assertEqual(inp.read_bytes(),before)
                self.assertTrue(out.exists())
                with self.assertRaisesRegex(ValueError,'ignored'):
                    qa.run(inp,root/'exposed.json')
                self.assertFalse((root/'exposed.json').exists())
            finally:
                qa.ROOT = old_root


if __name__ == '__main__':
    unittest.main()
