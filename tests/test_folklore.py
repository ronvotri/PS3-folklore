import base64
import json
import struct
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import folklore


def temp_workspace():
    root = Path(__file__).resolve().parents[1] / 'work'
    root.mkdir(exist_ok=True)
    return tempfile.TemporaryDirectory(dir=root)


def fixture():
    data = bytearray(b'\0' * 320)
    struct.pack_into('>II', data, 0, len(data), 13)
    struct.pack_into('>II', data, 0x30, 64, 256)
    struct.pack_into('>4I', data, 64, 16, 25, 16, 35)
    data[80:100] = b'New Game\0Load Game\0\0'
    data[256:] = b'Z' * 64
    return bytes(data)


class MenuTests(unittest.TestCase):
    def test_relocation_preserves_aliases_and_other_sections(self):
        original = fixture()
        modified, changes = folklore.rebuild_menu(original, {'New Game': 'Bat dau choi moi', 'Load Game': 'Tai game'})
        s, e, _, pointers, segments = folklore.system_layout(modified)
        texts = {rel: raw for rel, raw, _ in segments}
        self.assertEqual(pointers[0], pointers[2])
        self.assertEqual(texts[pointers[0]], b'Bat dau choi moi')
        self.assertEqual(texts[pointers[1]], b'Tai game')
        self.assertEqual(texts[pointers[3]], b'')
        self.assertEqual(modified[:s], original[:s])
        self.assertEqual(modified[e:], original[e:])
        self.assertEqual(len(modified), len(original))
        self.assertEqual(len(changes), 2)

    def test_rejects_unsupported_encoding_and_overflow(self):
        for value in ['Tiếng Việt', 'X' * 500, 'abc\0def']:
            with self.subTest(value=value), self.assertRaises(ValueError):
                folklore.rebuild_menu(fixture(), {'New Game': value})

    def test_rejects_corrupt_pointer(self):
        data = bytearray(fixture())
        struct.pack_into('>I', data, 68, 99999)
        with self.assertRaises(ValueError):
            folklore.rebuild_menu(bytes(data), {})

    def archive(self, root):
        original = fixture()
        modified, changes = folklore.rebuild_menu(original, {'New Game': 'Choi moi'})
        names = ['lang_en.bi5_', 'lang_uk.bi5_']
        archive = bytearray(b'Q' * 1024)
        index = bytearray()
        patches = []
        for name, offset in zip(names, [16, 400]):
            archive[offset:offset + len(original)] = original
            index += name.encode().ljust(32, b'\0') + struct.pack('>II', len(original), offset)
            patches.append({'name': name, 'offset': offset, 'size': len(original),
                            'original_sha256': folklore.sha256(original),
                            'patched_sha256': folklore.sha256(modified),
                            'original_base64': base64.b64encode(original).decode(),
                            'patched_base64': base64.b64encode(modified).decode()})
        (root / 'etc.bin_').write_bytes(archive)
        (root / 'etc.fht_').write_bytes(index)
        package = root / 'patch.json'
        package.write_text(json.dumps({'game_id': 'BCUS98147', 'archive_size': len(archive), 'patches': patches}))
        return bytes(archive), package

    def test_apply_idempotent_restore_and_check(self):
        with temp_workspace() as tmp:
            root = Path(tmp)
            original, package = self.archive(root)
            folklore.apply_package(root, package, check=True)
            self.assertEqual((root / 'etc.bin_').read_bytes(), original)
            folklore.apply_package(root, package)
            applied = (root / 'etc.bin_').read_bytes()
            self.assertNotEqual(applied, original)
            folklore.apply_package(root, package)
            self.assertEqual((root / 'etc.bin_').read_bytes(), applied)
            folklore.apply_package(root, package, restore=True)
            self.assertEqual((root / 'etc.bin_').read_bytes(), original)

    def test_second_region_mismatch_prevents_first_write(self):
        with temp_workspace() as tmp:
            root = Path(tmp)
            _, package = self.archive(root)
            data = bytearray((root / 'etc.bin_').read_bytes())
            data[500] ^= 1
            (root / 'etc.bin_').write_bytes(data)
            with self.assertRaises(ValueError):
                folklore.apply_package(root, package)
            self.assertEqual((root / 'etc.bin_').read_bytes(), data)

    def test_tampered_payload_prevents_write(self):
        with temp_workspace() as tmp:
            root = Path(tmp)
            original, package = self.archive(root)
            payload = json.loads(package.read_text())
            payload['patches'][0]['patched_base64'] = base64.b64encode(b'bad').decode()
            package.write_text(json.dumps(payload))
            with self.assertRaises(ValueError):
                folklore.apply_package(root, package)
            self.assertEqual((root / 'etc.bin_').read_bytes(), original)


if __name__ == '__main__':
    unittest.main()
