"""Synthetic tests for the local Folklore diagnostic command; no PS3 files."""
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import dialogue_diagnose as diagnose


class DialogueDiagnoseTests(unittest.TestCase):
    def archive(self, base: Path) -> Path:
        folder = base / "PS3_GAME" / "USRDIR" / "DATA"
        folder.mkdir(parents=True)
        (folder / "etc.bin_").write_bytes(b"original copy placeholder")
        (folder / "etc.fht_").write_bytes(b"index placeholder")
        return folder

    def test_finds_nested_archive_pair_without_modification(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            folder = self.archive(root)
            before = (folder / "etc.bin_").read_bytes()
            self.assertEqual(diagnose.discover_archive_dirs(root), [folder])
            self.assertEqual(diagnose.choose_archive_dir(root, None), folder)
            self.assertEqual((folder / "etc.bin_").read_bytes(), before)

    def test_rejects_missing_or_multiple_archive_pairs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with self.assertRaisesRegex(ValueError, "Cannot find"):
                diagnose.choose_archive_dir(root, None)
            first = self.archive(root / "copy1")
            second = self.archive(root / "copy2")
            with self.assertRaisesRegex(ValueError, "Multiple archive pairs"):
                diagnose.choose_archive_dir(root, None)
            self.assertEqual(diagnose.choose_archive_dir(None, second), second)
            with self.assertRaisesRegex(ValueError, "exactly one"):
                diagnose.choose_archive_dir(root, first)
            with self.assertRaisesRegex(ValueError, "exactly one"):
                diagnose.choose_archive_dir(None, None)

    def test_diagnose_invokes_read_only_probe_and_redaction(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = self.archive(Path(tmp))
            report = {"reports": [{"file": "talk/en/tk100_en.bin_"}],
                      "verified_candidate_total": 15}
            sanitized = {"files": [{"file": "talk/en/tk100_en.bin_"}]}
            with mock.patch.object(diagnose.dialogue_probe, "run",
                                   return_value=report) as run, mock.patch.object(
                                       diagnose.dialogue_summary, "run",
                                       return_value=sanitized) as redact:
                raw, summary = diagnose.diagnose(game_root=Path(tmp))
            self.assertEqual(raw, report)
            self.assertEqual(summary, sanitized)
            arguments, kwargs = run.call_args
            self.assertEqual(arguments[0], folder)
            self.assertEqual(arguments[1], diagnose.dialogue_probe.DEFAULT_FILES)
            self.assertFalse(kwargs["verify_only"])
            self.assertEqual(kwargs["max_samples"], 24)
            self.assertEqual(redact.call_args.args[0],
                             diagnose.ROOT / "local-data" / "dialogue-probe.json")
            self.assertEqual(redact.call_args.args[1],
                             diagnose.ROOT / "local-data" /
                             "dialogue-structure-summary.json")

    def test_all_source_verification_skips_pointer_scans(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = self.archive(Path(tmp))
            index = {"files": [{"file": "talk/en/tk100_en.bin_", "kind": "dialogue"},
                               {"file": "lang_en.bi5_", "kind": "menu"}]}
            report = {"reports": [{"file": "talk/en/tk100_en.bin_"}],
                      "verified_candidate_total": 5}
            sanitized = {"files": [{}]}
            with mock.patch.object(diagnose.dialogue_probe.folklore, "read_json",
                                   return_value=index), mock.patch.object(
                                       diagnose.dialogue_probe, "run",
                                       return_value=report) as run, mock.patch.object(
                                           diagnose.dialogue_summary, "run",
                                           return_value=sanitized):
                diagnose.diagnose(bin_dir=folder, verify_all=True)
            self.assertEqual(run.call_args.args[1], ("talk/en/tk100_en.bin_",))
            self.assertTrue(run.call_args.kwargs["verify_only"])

    def test_rejects_mismatched_report_counts_and_invalid_samples(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = self.archive(Path(tmp))
            with self.assertRaisesRegex(ValueError, "max-samples"):
                diagnose.diagnose(bin_dir=folder, max_samples=101)
            with mock.patch.object(diagnose.dialogue_probe, "run",
                                   return_value={"reports": [{}],
                                                 "verified_candidate_total": 1}), mock.patch.object(
                                                     diagnose.dialogue_summary, "run",
                                                     return_value={"files": []}):
                with self.assertRaisesRegex(ValueError, "file count"):
                    diagnose.diagnose(bin_dir=folder)

    def test_directory_depth_and_ignored_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ignored = root / "local-data"
            ignored.mkdir()
            (ignored / "etc.bin_").write_bytes(b"x")
            (ignored / "etc.fht_").write_bytes(b"x")
            outside = root / "deep"
            outside.mkdir()
            found = self.archive(outside)
            self.assertEqual(diagnose.discover_archive_dirs(root), [found])
            self.assertEqual(diagnose.discover_archive_dirs(root, max_depth=1), [])


if __name__ == "__main__":
    unittest.main()
