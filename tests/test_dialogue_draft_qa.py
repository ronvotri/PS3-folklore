"""Synthetic safety tests for the non-destructive draft review queue."""
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import dialogue_draft_qa as qa


def row(name, offset, source, vi, status='draft'):
    return {'id': f'{name}@{offset:08x}', 'file_offset': offset,
            'source': source, 'source_sha256': hashlib.sha256(source.encode()).hexdigest(),
            'vi': vi, 'status': status, 'source_review': 'candidate', 'notes': ''}


class DraftQATests(unittest.TestCase):
    def setup_catalog(self, root: Path, items):
        name = 'cmc/en/LCmc999_en.bi5_'
        path = root / 'catalogs/cmc/LCmc999_en.bi5_.json'
        path.parent.mkdir(parents=True)
        content = {'file': name, 'entries': items}
        path.write_text(json.dumps(content, ensure_ascii=False), encoding='utf-8')
        index = {'game_id': 'BCUS98147', 'total_entries': len(items),
                 'files': [{'catalog': 'catalogs/cmc/LCmc999_en.bi5_.json',
                            'file': name, 'entries': len(items)}]}
        (root / 'index.json').write_text(json.dumps(index), encoding='utf-8')
        return path

    def test_flags_fragment_newlines_marker_and_preserves_catalog(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            name = 'cmc/en/LCmc999_en.bi5_'
            rows = [row(name, 2, '$Please\nhelp.', 'Xin hãy\ngiúp.'),
                    row(name, 20, '\n who lives here,', '\n đang sống ở đây,'),
                    row(name, 45, 'Hello', 'Xin chào')]
            path = self.setup_catalog(root, rows)
            original = path.read_bytes()
            report = qa.audit(root)
            kinds = [x['kind'] for x in report['issues']]
            self.assertIn('leading_marker_review', kinds)
            self.assertIn('fragment_context_review', kinds)
            self.assertNotIn('newline_mismatch', kinds)
            self.assertEqual(report['summary']['entries'], 3)
            self.assertEqual(path.read_bytes(), original)

    def test_conflicts_are_warnings_not_automatic_edits(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            name = 'cmc/en/LCmc999_en.bi5_'
            self.setup_catalog(root, [row(name, 1, 'Where is she?!?', 'Cô ấy đâu?!'),
                                      row(name, 99, 'Where is she?!?', 'Nó đâu?!')])
            report = qa.audit(root)
            matches = [x for x in report['issues'] if x['kind'] == 'duplicate_source_variants']
            self.assertEqual(len(matches), 1)
            self.assertEqual(len(matches[0]['uses']), 2)
            self.assertIn('context', matches[0]['warning'])

    def test_oversized_and_hash_changes_are_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            name = 'cmc/en/LCmc999_en.bi5_'
            bad = row(name, 1, 'Hello, friend.', 'Bản dịch siêu dài cần kiểm tra nếu vượt quá bốn mươi ký tự nhé.')
            bad['source_sha256'] = 'bad'
            self.setup_catalog(root, [bad])
            kinds = [x['kind'] for x in qa.audit(root)['issues']]
            self.assertIn('very_long_line', kinds)
            self.assertIn('source_hash_mismatch', kinds)

    def test_refuses_manifest_discrepancy(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.setup_catalog(root, [row('cmc/en/LCmc999_en.bi5_', 1, 'Hi!', 'Chào!')])
            j = json.loads((root / 'index.json').read_text())
            j['total_entries'] = 2
            (root / 'index.json').write_text(json.dumps(j))
            with self.assertRaisesRegex(ValueError, 'total mismatch'):
                qa.audit(root)


if __name__ == '__main__':
    unittest.main()
