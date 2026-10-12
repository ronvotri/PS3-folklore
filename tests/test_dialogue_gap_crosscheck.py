"""Synthetic consistency tests for redacted V3 crosscheck. No game binary."""
from __future__ import annotations
import copy
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import dialogue_gap_crosscheck as qa


def fixture():
    sections = [{'index': 0, 'start': 0, 'end': 128, 'is_talk': True}]
    samples = [
        {'file_offset': 40, 'nul_at': 43, 'section_index': 0},
        {'file_offset': 48, 'nul_at': 55, 'section_index': 0},
        {'file_offset': 59, 'nul_at': 67, 'section_index': 0},
    ]
    structure = {'schema':1, 'game_id':'BCUS98147', 'kind':'STRUCTURAL_METADATA_ONLY',
                 'raw_text_or_hex_windows_included': False,
                 'files':[{'file':'cmc/en/LCmc000_en.bi5_', 'samples':samples,'sections':sections}]}
    gap = {'schema':1, 'game_id':'BCUS98147', 'kind':'REDACTED_GAP_CLASS_STATISTICS',
           'contains_original_text_or_hex':False,
           'files':[{'file':'cmc/en/LCmc000_en.bi5_', 'sampled_candidates':3,
                     'adjacent_pairs_in_section':2,'gap_lengths':{'4':1, '3':1},
                     'gap_class_counts_short_only':{'control':3,'zero':4},
                     'long_gaps_omitted':0,'gaps_window_unavailable':0,
                     'short_gap_samples':[
                        {'left_nul_at':43,'right_text_at':48,'gap_size':4,
                         'first_gap_byte_alignment4':0,'class_counts':{'control':2,'zero':2}},
                        {'left_nul_at':55,'right_text_at':59,'gap_size':3,
                         'first_gap_byte_alignment4':0,'class_counts':{'control':1,'zero':2}}]}]}
    return gap,structure


class DialogueGapCrosscheckTests(unittest.TestCase):
    def test_valid_pair_and_alignment_hypothesis(self):
        gap, structure = fixture()
        result = qa.crosscheck(gap, structure)
        self.assertTrue(result['reports_consistent'])
        self.assertEqual(result['total_compact_gaps'],2)
        self.assertEqual(result['compact_gaps_matching_alignment_pattern'],2)
        self.assertFalse(result['message_parser_proven'])
        self.assertFalse(result['repacker_available'])

    def test_mismatched_gap_histogram_fails_closed(self):
        gap, structure = fixture()
        gap['files'][0]['gap_lengths']['3'] = 2
        with self.assertRaisesRegex(ValueError,'histogram'):
            qa.crosscheck(gap,structure)

    def test_class_length_and_alignment_tampering_fails_closed(self):
        gap,structure = fixture()
        changed=copy.deepcopy(gap)
        changed['files'][0]['short_gap_samples'][0]['class_counts']['zero'] = 3
        with self.assertRaisesRegex(ValueError,'classified gap'):
            qa.crosscheck(changed,structure)
        changed=copy.deepcopy(gap)
        changed['files'][0]['short_gap_samples'][1]['first_gap_byte_alignment4']=1
        with self.assertRaisesRegex(ValueError,'alignment'):
            qa.crosscheck(changed,structure)

    def test_rejects_unredacted_or_wrong_file_or_overlap(self):
        gap,structure=fixture()
        changed=copy.deepcopy(structure)
        changed['raw_text_or_hex_windows_included']=True
        with self.assertRaisesRegex(ValueError,'redacted'):
            qa.crosscheck(gap,changed)
        changed=copy.deepcopy(gap)
        changed['files'][0]['file']='another.bin_'
        with self.assertRaisesRegex(ValueError,'order/name'):
            qa.crosscheck(changed,structure)
        changed=copy.deepcopy(structure)
        changed['files'][0]['samples'][1]['file_offset']=43
        with self.assertRaisesRegex(ValueError,'Overlapping'):
            qa.crosscheck(gap,changed)


if __name__=='__main__':
    unittest.main()
