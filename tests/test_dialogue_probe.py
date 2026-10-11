"""Synthetic fixtures: PS3 game files are NOT needed for these tests."""
import json
import struct
from dataclasses import replace
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import dialogue_probe as probe


def row(name, offset, source, *, status='draft'):
    return {'id': f'{name}@{offset:08x}', 'file_offset': offset, 'source': source,
            'source_sha256': probe.sha256(source.encode('utf-8')),
            'vi': 'nháp' if status == 'draft' else '', 'status': status,
            'source_review': 'candidate', 'notes': ''}


def talk_fixture():
    name = 'talk/en/tk100_en.bin_'
    data = bytearray(b'\xff' * 192)
    data[48:48 + 13] = b'Hello there!\0'
    data[112:112 + 15] = b'\nHello again!!\0'
    struct.pack_into('>I', data, 8, 48)
    struct.pack_into('<I', data, 12, 112)
    original = bytes(data)
    catalog = {'file': name, 'file_sha256': probe.sha256(original),
               'entries': [row(name, 48, 'Hello there!'),
                           row(name, 112, '\nHello again!!')]}
    return original, catalog


def cmc_fixture():
    name = 'cmc/en/LCmc000_en.bi5_'
    data = bytearray(b'\0' * 288)
    struct.pack_into('>II', data, 0, len(data), 2)
    struct.pack_into('>3I', data, 0x30, 0x80, 0xa0, 0x120)
    data[0x3c:0x3c + 5] = b'talk0'
    data[0x54:0x54 + 4] = b'anim'
    data[0x84:0x84 + 13] = b'Hello there!\0'
    data[0xa0:0xa0 + 13] = b'Hello there!\0'  # same text, NOT a talk section
    struct.pack_into('>I', data, 0x70, 0x84 - 0x80)
    original = bytes(data)
    catalog = {'file': name, 'file_sha256': probe.sha256(original),
               'entries': [row(name, 0x84, 'Hello there!')]}
    return original, catalog


class DialogueProbeTests(unittest.TestCase):
    def test_raw_talk_verifies_every_candidate_and_pointer_patterns(self):
        original, cat = talk_fixture()
        report = probe.probe_binary(original, cat, radius=16, max_samples=12)
        self.assertEqual(report['stats']['entries_verified'], 2)
        self.assertEqual(len(report['samples']), 2)
        self.assertEqual(report['stats']['begins_newline'], 1)
        self.assertEqual(report['samples'][0]['file_offset'], 48)
        hits = report['samples'][0]['u32_byte_patterns'][0]['candidates']
        self.assertTrue(any(x['endianness'] == 'big' and
                            x['locations'][0]['at'] == 8 for x in hits))
        self.assertEqual(original, talk_fixture()[0])  # strictly read-only

    def test_cmc_sections_limit_context_and_report_relative_patterns(self):
        data, cat = cmc_fixture()
        report = probe.probe_binary(data, cat, radius=64)
        self.assertEqual([x['is_talk'] for x in report['sections']], [True, False])
        self.assertEqual(report['samples'][0]['section'], 'talk0')
        self.assertLessEqual(len(bytes.fromhex(report['samples'][0]['bytes_before_hex'])), 4)
        patterns = report['samples'][0]['u32_byte_patterns'][1]
        self.assertEqual(patterns['kind'], 'section_relative_offset')
        self.assertTrue(any(x['locations'][0]['at'] == 0x70 for x in patterns['candidates']))

    def test_source_only_audit_checks_bytes_without_pointer_search(self):
        original, cat = talk_fixture()
        with mock.patch.object(probe, 'hits_for_u32', side_effect=AssertionError('no scans')):
            report = probe.probe_binary(original, cat, verify_only=True)
        self.assertEqual(report['stats']['entries_verified'], 2)
        self.assertEqual(report['samples'], [])
        self.assertFalse(report['u32_pattern_scan'])
        self.assertEqual(report['sha256'], probe.sha256(original))

    def test_all_dialogue_selects_index_order_and_rejects_conflict(self):
        index = {'files': [
            {'file': 'lang_en.bi5_', 'kind': 'menu'},
            {'file': 'talk/en/tk100_en.bin_', 'kind': 'dialogue'},
            {'file': 'cmc/en/LCmc000_en.bi5_', 'kind': 'dialogue'},
        ]}
        self.assertEqual(probe.select_names(index, None, True),
                         ('talk/en/tk100_en.bin_', 'cmc/en/LCmc000_en.bi5_'))
        self.assertEqual(probe.select_names(None, ['talk/en/tk100_en.bin_'], False),
                         ('talk/en/tk100_en.bin_',))
        with self.assertRaisesRegex(ValueError, 'cannot be combined'):
            probe.select_names(index, ['talk/en/tk100_en.bin_'], True)
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            probe.select_names({'files': index['files'][1:] * 2}, None, True)

    def test_opaque_cmc_roundtrip_preserves_header_padding_commands_and_trailer(self):
        original, _ = cmc_fixture()
        modified = bytearray(original)
        modified[0x2b] = 0x8c  # unknown bytes in the header
        modified[0x6c] = 0x53  # padding before first section
        modified[0xc0] = 0xf0  # opaque command bytes
        struct.pack_into('>I', modified, 0x38, 0x110)  # leave trailer
        modified[0x11a] = 0xe1  # trailing unknown bytes
        data = bytes(modified)
        envelope = probe.parse_opaque_cmc(data)
        self.assertEqual(envelope.edges, (0x80, 0xa0, 0x110))
        self.assertEqual(len(envelope.trailer), 0x10)
        self.assertEqual(envelope.serialize(), data)
        probe.check_opaque_cmc_roundtrip(data)

    def test_opaque_cmc_rejects_changed_section_or_padding_length(self):
        original, _ = cmc_fixture()
        envelope = probe.parse_opaque_cmc(original)
        with self.assertRaisesRegex(ValueError, 'payload length changed'):
            replace(envelope, payloads=(envelope.payloads[0] + b'!', *envelope.payloads[1:])).serialize()
        with self.assertRaisesRegex(ValueError, 'first section boundary changed'):
            replace(envelope, padding=envelope.padding[:-1]).serialize()
        with self.assertRaisesRegex(ValueError, 'section count changed'):
            replace(envelope, header=envelope.header[:4] + struct.pack('>I', 3)
                    + envelope.header[8:]).serialize()

    def test_cmc_probe_reports_only_opaque_container_roundtrip(self):
        original, catalog = cmc_fixture()
        report = probe.probe_binary(original, catalog, verify_only=True)
        self.assertTrue(report['opaque_cmc_container_roundtrip'])
        self.assertFalse(report['u32_pattern_scan'])
        self.assertEqual(report['stats']['entries_verified'], 1)
        raw_talk, talk_catalog = talk_fixture()
        self.assertIsNone(probe.probe_binary(raw_talk, talk_catalog, verify_only=True)[
            'opaque_cmc_container_roundtrip'])

    def test_rejects_tampered_content_without_treating_offset_as_patch_destination(self):
        original, cat = talk_fixture()
        modified = bytearray(original)
        modified[50] ^= 1
        with self.assertRaisesRegex(ValueError, 'SHA-256 differs'):
            probe.probe_binary(bytes(modified), cat)
        wrong = dict(cat)
        wrong['file_sha256'] = probe.sha256(bytes(modified))
        with self.assertRaisesRegex(ValueError, 'Original bytes/NUL differ'):
            probe.probe_binary(bytes(modified), wrong)
        broken_nul = bytearray(original)
        broken_nul[60] = 1
        wrong['file_sha256'] = probe.sha256(bytes(broken_nul))
        with self.assertRaisesRegex(ValueError, 'Original bytes/NUL differ'):
            probe.probe_binary(bytes(broken_nul), wrong)

    def test_rejects_cmc_candidate_outside_named_talk_section(self):
        original, cat = cmc_fixture()
        cat['entries'].append(row(cat['file'], 0xa0, 'Hello there!'))
        with self.assertRaisesRegex(ValueError, 'outside named talk section'):
            probe.verify_candidates(original, cat)

    def test_rejects_invalid_sample_size_and_malformed_cmc(self):
        orig, cat = talk_fixture()
        with self.assertRaises(ValueError):
            probe.probe_binary(orig, cat, radius=9999)
        cmc, _ = cmc_fixture()
        malformed = bytearray(cmc)
        struct.pack_into('>I', malformed, 0x38, 0x70)  # overlapping sections
        with self.assertRaisesRegex(ValueError, 'section bounds'):
            probe.cmc_sections(bytes(malformed))

    def test_run_stays_local_and_writes_no_report_on_failure(self):
        orig, cat = talk_fixture()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'docs').mkdir()
            (root / 'translations' / 'catalogs' / 'talk').mkdir(parents=True)
            (root / 'local-data').mkdir()
            (root / 'game').mkdir()
            (root / 'docs' / 'baseline.json').write_text(json.dumps({
                'game_id': 'BCUS98147', 'archive_size': 512}), encoding='utf-8')
            (root / 'translations' / 'index.json').write_text(json.dumps({
                'game_id': 'BCUS98147', 'files': [{
                    'catalog': 'catalogs/talk/tk100_en.bin_.json',
                    'file': cat['file'], 'kind': 'dialogue',
                    'source_sha256': cat['file_sha256']}]}), encoding='utf-8')
            (root / 'translations' / 'catalogs' / 'talk' / 'tk100_en.bin_.json').write_text(
                json.dumps(cat), encoding='utf-8')
            binary = bytearray(b'X' * 512)
            binary[128:128 + len(orig)] = orig
            (root / 'game' / 'etc.bin_').write_bytes(binary)
            (root / 'game' / 'etc.fht_').write_bytes(
                cat['file'].encode().ljust(32, b'\0') + struct.pack('>II', len(orig), 128))
            dest = root / 'local-data' / 'audit.json'
            saved_root = probe.ROOT
            try:
                probe.ROOT = root
                report = probe.run(root / 'game', (cat['file'],), dest,
                                   verify_only=True)
                self.assertEqual(report['mode'], 'READ_ONLY_FORENSICS')
                self.assertEqual(report['scan_mode'], 'SOURCE_ONLY')
                self.assertEqual(report['verified_candidate_total'], 2)
                self.assertFalse(report['parser_validated'])
                self.assertTrue(dest.exists())
                self.assertEqual((root / 'game' / 'etc.bin_').read_bytes(), binary)
                dest.unlink()
                with self.assertRaises(ValueError):
                    probe.run(root / 'game', (cat['file'],), root / 'unsafe.json')
                self.assertFalse((root / 'unsafe.json').exists())
                # Strict hash mismatch aborts before generating any file.
                tampered = bytearray(binary)
                tampered[180] ^= 1
                (root / 'game' / 'etc.bin_').write_bytes(tampered)
                with self.assertRaisesRegex(ValueError, 'SHA-256 differs'):
                    probe.run(root / 'game', (cat['file'],), dest)
                self.assertFalse(dest.exists())
            finally:
                probe.ROOT = saved_root


if __name__ == '__main__':
    unittest.main()
