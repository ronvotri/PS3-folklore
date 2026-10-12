"""Create a structural-only handoff from Folklore's local read-only probe.

Never reads the game, never writes patches, and deliberately discards source
strings, hex byte windows, ASCII previews, and filenames from section names.
Only numerical candidate offsets / raw u32 pattern sightings are retained.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HEX32 = re.compile(r"0x[0-9a-fA-F]{8}\Z")
MAX_SAMPLES = 100


def local_report_path(path: Path) -> Path:
    candidate = path.resolve()
    if not any(candidate.is_relative_to((ROOT / name).resolve())
               for name in ("local-data", "dist")):
        raise ValueError("Report paths must stay within ignored local-data/ or dist/")
    return candidate


def checked_int(value: object, label: str) -> int:
    if type(value) is not int or value < 0:
        raise ValueError(f"Invalid nonnegative integer: {label}")
    return value


def summarize(payload: dict) -> dict:
    """Explicit allowlist: none of the source/hex byte-window fields survive."""
    if (not isinstance(payload, dict) or payload.get("schema") != 1
            or payload.get("mode") != "READ_ONLY_FORENSICS"
            or payload.get("game_id") != "BCUS98147"
            or not isinstance(payload.get("reports"), list)):
        raise ValueError("Unsupported or malformed probe JSON")
    out = []
    for report in payload["reports"]:
        name = report["file"]
        if not isinstance(name, str) or not name.startswith(("talk/en/", "cmc/en/")):
            raise ValueError("Unexpected archive file identifier")
        sections = []
        for i, section in enumerate(report["sections"]):
            start = checked_int(section["start"], "section start")
            end = checked_int(section["end"], "section end")
            # Empty sections are valid; a sample must still lie in a nonempty talk section.
            if start > end or type(section["is_talk"]) is not bool:
                raise ValueError("Invalid section bounds/type")
            sections.append({"index": i, "start": start, "end": end,
                             "is_talk": section["is_talk"]})
        samples = report["samples"]
        if not isinstance(samples, list) or len(samples) > MAX_SAMPLES:
            raise ValueError("Invalid number of samples")
        redacted = []
        for sample in samples:
            offset = checked_int(sample["file_offset"], "candidate offset")
            end = checked_int(sample["nul_at"], "NUL offset")
            if end < offset:
                raise ValueError("Invalid candidate range")
            section_index = next((s["index"] for s in sections
                                  if s["is_talk"] and s["start"] <= offset <= end < s["end"]), None)
            if section_index is None:
                raise ValueError("Sample outside talk section")
            patterns = []
            for pattern in sample["u32_byte_patterns"]:
                kind = pattern["kind"]
                if kind not in ("file_relative_offset", "section_relative_offset"):
                    raise ValueError("Unknown u32 pattern type")
                candidates = []
                for hit in pattern["candidates"]:
                    if (hit["endianness"] not in ("big", "little")
                            or not isinstance(hit["value_hex"], str)
                            or HEX32.fullmatch(hit["value_hex"]) is None):
                        raise ValueError("Malformed u32 pattern")
                    locations = []
                    for loc in hit["locations"]:
                        if type(loc["aligned4"]) is not bool:
                            raise ValueError("Invalid alignment flag")
                        locations.append({"at": checked_int(loc["at"], "hit offset"),
                                          "aligned4": loc["aligned4"]})
                    candidates.append({
                        "endianness": hit["endianness"],
                        "value_hex": hit["value_hex"],
                        "hit_count": checked_int(hit["hit_count"], "hit count"),
                        "locations": locations,
                    })
                patterns.append({"kind": kind, "matches": candidates})
            redacted.append({"file_offset": offset, "nul_at": end,
                             "section_index": section_index,
                             "u32_pattern_sightings": patterns})
        stats = report["stats"]
        out.append({
            "file": name,
            "archive_offset": checked_int(report["archive_offset"], "archive offset"),
            "size": checked_int(report["size"], "file size"),
            "candidate_count": checked_int(stats["entries_verified"], "candidate count"),
            "sections": sections,
            "samples": redacted,
        })
    return {
        "schema": 1, "game_id": "BCUS98147",
        "kind": "STRUCTURAL_METADATA_ONLY",
        "raw_text_or_hex_windows_included": False,
        "scope": "Observed offsets and u32 byte-pattern sightings; NOT validated pointers.",
        "parser_validated": False, "repacker_available": False,
        "files": out,
    }


def run(source: Path, dest: Path) -> dict:
    src, dst = local_report_path(source), local_report_path(dest)
    if src == dst:
        raise ValueError("Input and output must be different paths")
    report = json.loads(src.read_text(encoding="utf-8"))
    summarized = summarize(report)
    # Validate everything before creating the destination.
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(json.dumps(summarized, ensure_ascii=False, indent=2) + "\n",
                   encoding="utf-8")
    return summarized


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--in", dest="source", type=Path,
                        default=ROOT / "local-data/dialogue-probe.json")
    parser.add_argument("--out", dest="target", type=Path,
                        default=ROOT / "local-data/dialogue-structure-summary.json")
    args = parser.parse_args()
    try:
        report = run(args.source, args.target)
    except (ValueError, OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
        parser.exit(1, f"Refused: {exc}\n")
    print(f"Saved structural-only summary of {len(report['files'])} files: {args.target}")
    print("No game, ISO, source dialogue or hex byte windows are included.")


if __name__ == "__main__":
    main()
