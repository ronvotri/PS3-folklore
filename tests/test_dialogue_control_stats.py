"""Synthetic safeguards for non-sensitive V4 aggregate. No original binary."""
import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
import dialogue_control_stats as control


def fixture():
    a={'file_offset':40,'nul_at':44,'section':'talk0','bytes_after_hex':'00 01 00 00 03 00 20 00'}
    b={'file_offset':51,'nul_at':58,'section':'talk0','bytes_after_hex':'00 00 04 20 00'}
    c={'file_offset':63,'nul_at':70,'section':'talk0','bytes_after_hex':''}
    return {'schema':1,'game_id':'BCUS98147','mode':'READ_ONLY_FORENSICS','reports':[
        {'file':'cmc/en/LCmc000_en.bi5_', 'samples':[a,b,c]}]}


class V4ControlAggregateTests(unittest.TestCase):
    def test_counts_low_byte_values_but_not_text_or_raw_hex(self):
        report=fixture()
        x=control.analyze(report)
        f=x['files'][0]
        self.assertEqual(f['eligible_short_nontext_gaps'],1)
        self.assertEqual(f['control_value_histogram_decimal'],{'1':1,'3':1})
        self.assertEqual(f['next_text_mod4_histogram'],{'3':1})
        content=json.dumps(x)
        self.assertNotIn('bytes_after_hex',content)
        self.assertNotIn('file_offset',content)
        self.assertNotIn('00 01 00 00 03',content)
        self.assertFalse(x['message_parser_proven'])

    def test_excludes_printable_and_long_gaps(self):
        report=fixture()
        report['reports'][0]['samples'][1]['bytes_after_hex']='41 00 01 00'
        r=control.analyze(report)
        self.assertEqual(r['files'][0]['eligible_short_nontext_gaps'],1)
        self.assertEqual(r['files'][0]['other_pairs_not_classified'],1)
        report['reports'][0]['samples'][0]['bytes_after_hex']='20 01 00 00 03 00'
        r=control.analyze(report)
        self.assertEqual(r['files'][0]['eligible_short_nontext_gaps'],0)

    def test_rejects_invalid_schema_and_overlapping_sources(self):
        report=fixture();report['mode']='PATCH'
        with self.assertRaises(ValueError):control.analyze(report)
        report=fixture();report['reports'][0]['samples'][1]['file_offset']=44
        with self.assertRaisesRegex(ValueError,'Overlapping'):control.analyze(report)

    def test_report_stays_local_and_input_unmodified(self):
        report=fixture()
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);(root/'local-data').mkdir()
            old=control.ROOT;control.ROOT=root
            try:
                src=root/'local-data'/'raw.json';dst=root/'local-data'/'out.json'
                src.write_text(json.dumps(report),encoding='utf-8')
                before=src.read_bytes()
                x=control.run(src,dst)
                self.assertEqual(src.read_bytes(),before)
                self.assertTrue(dst.exists())
                self.assertEqual(x['kind'],'REDACTED_AGGREGATE_CONTROL_STATS')
                with self.assertRaises(ValueError): control.run(src,root/'out.json')
                with self.assertRaises(ValueError): control.run(root/'outside.json',dst)
            finally:control.ROOT=old

if __name__=='__main__':unittest.main()
