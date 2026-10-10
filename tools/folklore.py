"""Portable tools for the verified BCUS98147 ASCII menu prototype.

Game assets and generated patch packages stay local. Python 3.10+, stdlib only.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_index(bin_dir: Path):
    raw = (bin_dir / "etc.fht_").read_bytes()
    if len(raw) % 40:
        raise ValueError("FHT length is not a multiple of 40")
    archive_size = (bin_dir / "etc.bin_").stat().st_size
    entries = {}
    for pos in range(0, len(raw), 40):
        record = raw[pos:pos + 40]
        name = record[:32].split(b"\0", 1)[0].decode("ascii")
        size, offset = struct.unpack(">II", record[32:])
        if not name or name in entries or offset + size > archive_size:
            raise ValueError(f"Invalid or duplicate FHT entry: {name!r}")
        entries[name] = {"name": name, "size": size, "offset": offset}
    return entries


def system_layout(data: bytes):
    if len(data) < 0x38:
        raise ValueError("BI5 header is too short")
    declared_size, section_count = struct.unpack_from(">II", data)
    if declared_size != len(data) or section_count != 13:
        raise ValueError("Unsupported menu BI5 header")
    section, limit = struct.unpack_from(">II", data, 0x30)
    if not 0x38 <= section < limit <= len(data):
        raise ValueError("Invalid system section bounds")
    table_size = struct.unpack_from(">I", data, section)[0]
    if not 4 <= table_size < limit - section or table_size % 4:
        raise ValueError("Invalid string table length")
    pointers = list(struct.unpack_from(f">{table_size // 4}I", data, section))
    unique = sorted(set(pointers))
    if min(unique) != table_size or max(unique) >= limit - section:
        raise ValueError("String pointer outside system pool")
    segments = []
    for idx, rel in enumerate(unique):
        pos = section + rel
        next_pos = section + unique[idx + 1] if idx + 1 < len(unique) else limit
        end = data.find(b"\0", pos, next_pos)
        if end < 0:
            raise ValueError("String has no terminator before next pointer")
        segments.append((rel, data[pos:end], data[end:next_pos]))
    return section, limit, table_size, pointers, segments


def rebuild_menu(data: bytes, translations: dict[str, str]):
    if not isinstance(translations, dict):
        raise ValueError("Translations must be an object of source/target strings")
    for source, target in translations.items():
        if not isinstance(source, str) or not isinstance(target, str):
            raise ValueError("Each translation must contain strings")
        if "\0" in source or "\0" in target:
            raise ValueError("Embedded NUL is not allowed")
        try:
            source.encode("ascii")
            target.encode("ascii")
        except UnicodeEncodeError as exc:
            raise ValueError("This prototype accepts ASCII only; accented font support is pending") from exc
    section, limit, table_size, pointers, segments = system_layout(data)
    pool = bytearray()
    relocated = {}
    expected = {}
    changes = []
    for rel, raw, suffix in segments:
        relocated[rel] = table_size + len(pool)
        try:
            source = raw.decode("ascii")
        except UnicodeDecodeError:
            source = None
        replacement = translations[source].encode("ascii") if source in translations else raw
        expected[rel] = replacement
        if source in translations and replacement != raw:
            changes.append({"original_offset": section + rel, "source": source,
                            "target": translations[source]})
        pool.extend(replacement)
        # The last string's all-NUL tail is section slack, not string data.
        if rel == segments[-1][0] and not any(suffix):
            suffix = b"\0"
        pool.extend(suffix)
    if table_size + len(pool) > limit - section:
        raise ValueError("Translated pool exceeds original section capacity; archive resizing is pending")
    table = b"".join(struct.pack(">I", relocated[rel]) for rel in pointers)
    block = table + pool
    result = data[:section] + block + b"\0" * (limit - section - len(block)) + data[limit:]
    if len(result) != len(data) or result[:section] != data[:section] or result[limit:] != data[limit:]:
        raise ValueError("Rebuild changed data outside the system section")
    _, _, _, new_pointers, _ = system_layout(result)
    for old, new in zip(pointers, new_pointers):
        pos = section + new
        end = result.find(b"\0", pos, limit)
        if result[pos:end] != expected[old]:
            raise ValueError("Rebuilt string reference mismatch")
    return result, changes


def extract_menu(bin_dir: Path, out: Path, baseline: dict, original_package: Path | None):
    entries = read_index(bin_dir)
    legacy = read_json(original_package) if original_package else None
    recovered = {p["name"]: p for p in legacy["patches"]} if legacy else {}
    if (bin_dir / "etc.bin_").stat().st_size != baseline["archive_size"]:
        raise ValueError("Archive size differs from the supported BCUS98147 baseline")
    extracted = []
    with (bin_dir / "etc.bin_").open("rb") as archive:
        for spec in baseline["menu_files"]:
            entry = entries.get(spec["name"])
            if not entry or any(entry[key] != spec[key] for key in ("size", "offset")):
                raise ValueError(f"Baseline index mismatch: {spec['name']}")
            archive.seek(entry["offset"])
            data = archive.read(entry["size"])
            if sha256(data) != spec["original_sha256"]:
                old = recovered.get(spec["name"])
                if not old or sha256(data) != old["patched_sha256"]:
                    raise ValueError("Menu is modified. Supply the matching local --original-package; do not use modified menus as a new baseline")
                data = base64.b64decode(old["original_base64"], validate=True)
            if len(data) != entry["size"] or sha256(data) != spec["original_sha256"]:
                raise ValueError("Original menu hash mismatch")
            _, _, _, pointers, segments = system_layout(data)
            out.mkdir(parents=True, exist_ok=True)
            (out / entry["name"]).write_bytes(data)
            strings = [{"relative_offset": rel, "text": raw.decode("ascii", errors="backslashreplace")}
                       for rel, raw, _ in segments]
            write_json(out / (entry["name"] + ".strings.json"), strings)
            extracted.append(entry)
            print(f"Extracted original {entry['name']}: {len(pointers)} references")
    write_json(out / "source.json", {"game_id": baseline["game_id"],
               "archive_size": baseline["archive_size"], "entries": extracted})


def build_package(data_dir: Path, translation_path: Path, out: Path, baseline: dict):
    translations = read_json(translation_path)
    patches = []
    report = []
    for spec in baseline["menu_files"]:
        original = (data_dir / spec["name"]).read_bytes()
        if sha256(original) != spec["original_sha256"] or len(original) != spec["size"]:
            raise ValueError(f"Expected verified original file: {spec['name']}")
        modified, changes = rebuild_menu(original, translations)
        patches.append({"name": spec["name"], "offset": spec["offset"], "size": len(original),
                        "changes": len(changes), "original_sha256": sha256(original),
                        "patched_sha256": sha256(modified),
                        "original_base64": base64.b64encode(original).decode(),
                        "patched_base64": base64.b64encode(modified).decode()})
        report.extend({"file": spec["name"], **change} for change in changes)
        print(f"Built {spec['name']}: {len(changes)} translations")
    write_json(out / "menu-patch.json", {"game_id": baseline["game_id"],
               "archive_size": baseline["archive_size"], "patches": patches})
    write_json(out / "translation-report.json", report)


def apply_package(bin_dir: Path, package_path: Path, restore: bool = False, check: bool = False):
    package = read_json(package_path)
    entries = read_index(bin_dir)
    if package.get("game_id") != "BCUS98147":
        raise ValueError("Unsupported package game ID")
    if (bin_dir / "etc.bin_").stat().st_size != package["archive_size"]:
        raise ValueError("Archive size mismatch")
    operations = []
    seen = set()
    # Preflight every region before opening the archive for writing.
    with (bin_dir / "etc.bin_").open("rb") as archive:
        for patch in package["patches"]:
            name = patch["name"]
            entry = entries.get(name)
            if name in seen or name not in ("lang_en.bi5_", "lang_uk.bi5_"):
                raise ValueError("Unexpected or duplicate patch region")
            seen.add(name)
            if not entry or any(entry[k] != patch[k] for k in ("size", "offset")):
                raise ValueError("Patch index mismatch")
            payloads = {}
            for key in ("original", "patched"):
                data = base64.b64decode(patch[key + "_base64"], validate=True)
                if len(data) != entry["size"] or sha256(data) != patch[key + "_sha256"]:
                    raise ValueError("Package payload/hash mismatch")
                payloads[key] = data
            system_layout(payloads["original"])
            system_layout(payloads["patched"])
            archive.seek(entry["offset"])
            current = archive.read(entry["size"])
            if current not in payloads.values():
                raise ValueError(f"Unknown menu contents: {name}; no changes written")
            desired = payloads["original" if restore else "patched"]
            operations.append((entry, current, desired))
            print(f"Verified {name}")
    if check:
        print("Check passed; no changes written")
        return
    # Close RPCS3 before applying. A concurrent writer can invalidate the preflight.
    with (bin_dir / "etc.bin_").open("r+b") as archive:
        for entry, current, _ in operations:
            archive.seek(entry["offset"])
            if archive.read(entry["size"]) != current:
                raise ValueError("Menu changed after preflight; no changes written")
        for entry, current, desired in operations:
            if current != desired:
                archive.seek(entry["offset"])
                archive.write(desired)
        archive.flush()
        for entry, _, desired in operations:
            archive.seek(entry["offset"])
            if archive.read(entry["size"]) != desired:
                raise ValueError("Post-write verification failed; keep package for recovery")
    print("Original menu restored" if restore else "ASCII Vietnamese menu applied")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    inspect = sub.add_parser("inspect")
    inspect.add_argument("--bin-dir", type=Path, required=True)
    extract = sub.add_parser("extract-menu")
    extract.add_argument("--bin-dir", type=Path, required=True)
    extract.add_argument("--out", type=Path, default=ROOT / "local-data")
    extract.add_argument("--original-package", type=Path)
    build = sub.add_parser("build-menu")
    build.add_argument("--data-dir", type=Path, default=ROOT / "local-data")
    build.add_argument("--translations", type=Path, default=ROOT / "translations/menu_ascii.json")
    build.add_argument("--out", type=Path, default=ROOT / "dist/menu")
    apply = sub.add_parser("apply-menu")
    apply.add_argument("--bin-dir", type=Path, required=True)
    apply.add_argument("--package", type=Path, required=True)
    apply.add_argument("--restore", action="store_true")
    apply.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        if args.command == "inspect":
            entries = read_index(args.bin_dir)
            print(f"{len(entries)} validated archive entries")
            for name in ("lang_en.bi5_", "lang_uk.bi5_", "lang_tex_a.bi5_", "lang_tex_e.bi5_"):
                print(entries.get(name))
        elif args.command == "extract-menu":
            extract_menu(args.bin_dir, args.out, read_json(ROOT / "docs/baseline.json"), args.original_package)
        elif args.command == "build-menu":
            build_package(args.data_dir, args.translations, args.out, read_json(ROOT / "docs/baseline.json"))
        else:
            apply_package(args.bin_dir, args.package, args.restore, args.check)
    except (ValueError, OSError, KeyError, struct.error) as exc:
        parser.exit(1, f"Error: {exc}\n")


if __name__ == "__main__":
    main()
