"""One-command, read-only Folklore dialogue diagnosis for a local game copy.

Finds etc.bin_ + etc.fht_ below an explicitly supplied game folder, then
runs the existing source-byte probe and produces a separate redacted structural
summary. No binary writes, no uploads, no translation patch.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path

import dialogue_probe
import dialogue_summary

ROOT = Path(__file__).resolve().parents[1]
IGNORED_DIRS = {".git", "local-data", "dist", "work", "__pycache__"}
MAX_DEPTH = 8


def discover_archive_dirs(game_root: Path, *, max_depth: int = MAX_DEPTH) -> list[Path]:
    """Find only directories containing BOTH archive files; do not follow links."""
    root = game_root.resolve()
    if not root.is_dir():
        raise ValueError(f"Game root is not a directory: {root}")
    found: list[Path] = []
    for base, dirs, files in os.walk(root, followlinks=False):
        current = Path(base)
        depth = len(current.relative_to(root).parts)
        if depth >= max_depth:
            dirs[:] = []
        else:
            dirs[:] = sorted(d for d in dirs if d not in IGNORED_DIRS
                             and not (current / d).is_symlink())
        if {"etc.bin_", "etc.fht_"}.issubset(files):
            found.append(current)
    return found


def choose_archive_dir(game_root: Path | None, bin_dir: Path | None) -> Path:
    if (game_root is None) == (bin_dir is None):
        raise ValueError("Choose exactly one of --game-root or --bin-dir")
    if bin_dir is not None:
        folder = bin_dir.resolve()
        if not folder.is_dir() or not all(
                (folder / name).is_file() for name in ("etc.bin_", "etc.fht_")):
            raise ValueError("--bin-dir must contain both etc.bin_ and etc.fht_")
        return folder
    matches = discover_archive_dirs(game_root)
    if not matches:
        raise ValueError("Cannot find an original etc.bin_ + etc.fht_ pair under "
                         f"{game_root}. Use --bin-dir for the exact directory.")
    if len(matches) > 1:
        raise ValueError("Multiple archive pairs found; select one with --bin-dir: "
                         + "; ".join(str(p) for p in matches))
    return matches[0]


def diagnose(game_root: Path | None = None, bin_dir: Path | None = None, *,
             verify_all: bool = False, max_samples: int = 24) -> tuple[dict, dict]:
    """Run existing fail-closed tools; all outputs remain ignored and local."""
    if not 1 <= max_samples <= 100:
        raise ValueError("--max-samples must be between 1 and 100")
    archive_folder = choose_archive_dir(game_root, bin_dir)
    private_path = ROOT / "local-data" / "dialogue-probe.json"
    shareable_path = ROOT / "local-data" / "dialogue-structure-summary.json"
    if verify_all:
        index = dialogue_probe.folklore.read_json(ROOT / "translations" / "index.json")
        names = dialogue_probe.select_names(index, None, True)
    else:
        names = dialogue_probe.DEFAULT_FILES
    raw = dialogue_probe.run(
        archive_folder, names, private_path, max_samples=max_samples,
        verify_only=verify_all,
    )
    summary = dialogue_summary.run(private_path, shareable_path)
    if len(raw["reports"]) != len(summary["files"]):
        raise ValueError("Redacted summary file count differs from original probe")
    return raw, summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--game-root", type=Path,
                        help="Game folder; searches nested subfolders for etc files")
    source.add_argument("--bin-dir", type=Path,
                        help="Exact folder containing both etc.bin_ and etc.fht_")
    parser.add_argument("--verify-all", action="store_true",
                        help="Verify all dialogue source strings; no raw pointer-pattern scan")
    parser.add_argument("--max-samples", type=int, default=24,
                        help="Up to 100 examples per file in focused inspection")
    args = parser.parse_args(argv)
    try:
        raw, summary = diagnose(args.game_root, args.bin_dir,
                                verify_all=args.verify_all, max_samples=args.max_samples)
    except (ValueError, OSError, KeyError, TypeError) as exc:
        parser.exit(1, f"Diagnosis refused: {exc}\n")
    print(f"Verified source bytes in {len(raw['reports'])} original assets "
          f"({raw['verified_candidate_total']} candidates).")
    print(f"STRUCTURAL SUMMARY ONLY: {ROOT / 'local-data' / 'dialogue-structure-summary.json'}")
    print(f"PRIVATE raw/hex evidence: {ROOT / 'local-data' / 'dialogue-probe.json'}")
    print("No game files modified; no data uploaded. "
          "Pattern matches are not verified pointers; no repacker exists.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
