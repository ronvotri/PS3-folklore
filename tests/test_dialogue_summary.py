"""Synthetic-only tests for the redacted structural Folklore handoff."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import dialogue_summary


def source_probe():
    return {
        "schema": 1, "game_id": "BCUS98147", "mode": "READ_ONLY_FORENSICS",
        "reports": [{
            "file": "cmc/en/LCmc000_en.bi5_", "archive_offset": 4096,
            "size": 256, "stats": {"entries_verified": 1},
            "sections": [{"name": "talk0", "start": 128, "end": 240, "is_talk": True}],
            "samples": [{
                "source": "PRIVATE_DIALOGUE_SHOULD_NEVER_LEAK",
                "bytes_before_hex": "PRIVATE_HEX_SHOULD_NEVER_LEAK",
                "bytes_after_ascii": "PRIVATE_ASCII_SHOULD_NEVER_LEAK",
                "file_offset": 132, "nul_at": 144, "section": "talk0",
                "u32_byte_patterns": [{
                    "kind": "section_relative_offset",
                    "candidates": [{"endianness": "big", "value_hex": "0x00000004",
                                    "hit_count": 1,
                                    "locations": [{"at": 64, "aligned4": True}]}],
                }],
            }],
        }],
    }


class DialogueSummaryTests(unittest.TestCase):
    def test_summary_never_reprints_dialogue_or_hex_windows(self):
        out = dialogue_summary.summarize(source_probe())
        text = json.dumps(out, ensure_ascii=False)
        for sentinel in ("PRIVATE_DIALOGUE_SHOULD_NEVER_LEAK",
                         "PRIVATE_HEX_SHOULD_NEVER_LEAK",
                         "PRIVATE_ASCII_SHOULD_NEVER_LEAK", "talk0"):
            self.assertNotIn(sentinel, text)
        self.assertFalse(out["raw_text_or_hex_windows_included"])
        self.assertEqual(out["files"][0]["samples"][0]["section_index"], 0)
        self.assertEqual(out["files"][0]["samples"][0]["u32_pattern_sightings"][0]
                         ["matches"][0]["locations"][0]["at"], 64)

    def test_verify_only_empty_samples_supported(self):
        data = source_probe()
        data["reports"][0]["samples"] = []
        self.assertEqual(dialogue_summary.summarize(data)["files"][0]["samples"], [])

    def test_bad_sample_and_nonprobe_refused(self):
        data = source_probe()
        data["reports"][0]["samples"][0]["nul_at"] = 260
        with self.assertRaisesRegex(ValueError, "outside talk section"):
            dialogue_summary.summarize(data)
        data = source_probe()
        data["mode"] = "WRITABLE_PATCH"
        with self.assertRaisesRegex(ValueError, "Unsupported"):
            dialogue_summary.summarize(data)
        data = source_probe()
        data["reports"][0]["samples"][0]["u32_byte_patterns"][0]["candidates"][0][
            "value_hex"] = "source text"
        with self.assertRaisesRegex(ValueError, "Malformed u32"):
            dialogue_summary.summarize(data)

    def test_output_is_local_and_source_unchanged(self):
        with tempfile.TemporaryDirectory() as tmp:
            old_root = dialogue_summary.ROOT
            root = Path(tmp)
            (root / "local-data").mkdir()
            (root / "dist").mkdir()
            inp = root / "local-data/input.json"
            out = root / "dist/safe.json"
            inp.write_text(json.dumps(source_probe()), encoding="utf-8")
            before = inp.read_bytes()
            try:
                dialogue_summary.ROOT = root
                result = dialogue_summary.run(inp, out)
                self.assertEqual(result["files"][0]["candidate_count"], 1)
                self.assertEqual(inp.read_bytes(), before)
                self.assertTrue(out.exists())
                with self.assertRaisesRegex(ValueError, "local-data/ or dist"):
                    dialogue_summary.run(inp, root / "outside.json")
                with self.assertRaisesRegex(ValueError, "different paths"):
                    dialogue_summary.run(inp, inp)
                self.assertFalse((root / "outside.json").exists())
            finally:
                dialogue_summary.ROOT = old_root


if __name__ == "__main__":
    unittest.main()
