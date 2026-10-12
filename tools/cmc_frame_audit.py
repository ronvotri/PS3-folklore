"""Read-only whole-catalog CMC 00 04 00 XX frame audit for Folklore BCUS98147.

Works only with a local original etc.bin_ / etc.fht_ pair plus the GitHub
translation catalogs. No patch, no replacement, no text or hex in reports.
A matching candidate frame is NOT a decoded speaker/message/opcode.
Python >=3.10; standard library only.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parents[1]
MAX_FILE_BYTES = 128 * 1024 * 1024
IGNORE_DIRS = {'.git', '__pycache__', 'local-data', 'dist', 'work'}


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding='utf-8-sig'))


def archive_folder(game_root: Path | None, bin_dir: Path | None) -> Path:
    if (game_root is None) == (bin_dir is None):
        raise ValueError('Supply exactly one of --game-root or --bin-dir')
    if bin_dir is not None:
        p = bin_dir.resolve()
        if not p.is_dir() or not all((p / f).is_file() for f in ('etc.bin_', 'etc.fht_')):
            raise ValueError('The --bin-dir folder must contain etc.bin_ and etc.fht_')
        return p
    root = game_root.resolve()
    if not root.is_dir():
        raise ValueError('Game folder does not exist')
    candidates = []
    for base, dirs, names in os.walk(root, followlinks=False):
        here = Path(base)
        depth = len(here.relative_to(root).parts)
        dirs[:] = [] if depth >= 8 else [
            d for d in dirs if d not in IGNORE_DIRS and not (here / d).is_symlink()]
        if {'etc.bin_', 'etc.fht_'}.issubset(names):
            candidates.append(here)
    if len(candidates) != 1:
        raise ValueError(f'Expected exactly one archive pair, found {len(candidates)}. '
                         'Use --bin-dir for the exact folder.')
    return candidates[0]


def read_fht(bin_dir: Path, archive_size: int) -> dict:
    raw = (bin_dir / 'etc.fht_').read_bytes()
    if len(raw) % 40:
        raise ValueError('FHT length not divisible by 40')
    out = {}
    for pos in range(0, len(raw), 40):
        rec = raw[pos:pos+40]
        name = rec[:32].split(b'\0', 1)[0].decode('ascii')
        size, offset = struct.unpack('>II', rec[32:])
        if not name or name in out or offset + size > archive_size:
            raise ValueError('Duplicate or invalid FHT entry')
        out[name] = (offset, size)
    return out


def cmc_talk_bounds(data: bytes) -> list[tuple[int, int]]:
    if len(data) < 0x38:
        raise ValueError('CMC file too short')
    declared, count = struct.unpack_from('>II', data, 0)
    if declared != len(data) or not 1 <= count <= 64:
        raise ValueError('CMC declared size or section count invalid')
    names_start = 0x30 + 4 * (count+1)
    names_end = names_start + count*24
    if names_end > len(data):
        raise ValueError('CMC name table outside file')
    edges = struct.unpack_from(f'>{count+1}I', data, 0x30)
    if edges[0] < names_end or edges[-1] > len(data) or any(a > b for a, b in zip(edges, edges[1:])):
        raise ValueError('CMC section bounds invalid')
    return [(edges[i], edges[i+1]) for i in range(count)
            if data[names_start+i*24:names_start+(i+1)*24].split(b'\0',1)[0].startswith(b'talk')]


def audit_catalog(data: bytes, catalog: dict, expected_sha: str) -> dict:
    name = catalog['file']
    if not isinstance(name, str) or not name.startswith('cmc/en/'):
        raise ValueError('Not a CMC catalog')
    if digest(data) != expected_sha or catalog['file_sha256'] != expected_sha:
        raise ValueError(f'{name}: original CMC SHA-256 mismatch')
    bounds = cmc_talk_bounds(data)
    if not bounds:
        raise ValueError(f'{name}: no named talk sections')
    rows = catalog['entries']
    seen = set()
    counts: Counter[str] = Counter()
    selectors: Counter[str] = Counter()
    for r in rows:
        at = r['file_offset']
        if type(at) is not int or at in seen or at < 0:
            raise ValueError(f'{name}: invalid or duplicate candidate offset')
        seen.add(at)
        if r['id'] != f'{name}@{at:08x}':
            raise ValueError(f'{name}: candidate ID differs')
        source = r['source']
        if not isinstance(source, str) or not source:
            raise ValueError(f'{name}: empty candidate source')
        try:
            ascii_raw = source.encode('ascii')
        except UnicodeEncodeError as exc:
            raise ValueError(f'{name}: non-ASCII source candidate') from exc
        if r['source_sha256'] != digest(source.encode('utf-8')):
            raise ValueError(f'{name}: source hash mismatch')
        end = at + len(ascii_raw)
        if end >= len(data) or data[at:end] != ascii_raw or data[end] != 0:
            raise ValueError(f'{name}: source bytes/NUL mismatch')
        if not any(start <= at and end < stop for start, stop in bounds):
            raise ValueError(f'{name}: candidate outside named talk bounds')
        mod = at % 4
        if mod == 3:
            frame_start = at-3
            expected = b'\x00\x04\x00' + ascii_raw[:1]
            label = 'printable_marker_in_candidate'
            if not 32 <= ascii_raw[0] <= 126:
                counts['mod3_nonprintable_source_prefix'] += 1
                continue
        elif mod == 0:
            frame_start = at-4
            expected = None
            label = 'control_marker_before_candidate'
        else:
            counts[f'unexpected_mod{mod}'] += 1
            continue
        if frame_start < 0 or not any(start <= frame_start and end < stop for start, stop in bounds):
            counts['frame_outside_talk_bounds'] += 1
            continue
        frame = data[frame_start:frame_start+4]
        if len(frame) != 4 or frame[:3] != b'\x00\x04\x00':
            counts['not_000400_frame'] += 1
            continue
        if expected is not None and frame != expected:
            counts['prefix_not_part_of_frame'] += 1
            continue
        if mod == 0 and not (1 <= frame[3] < 32):
            counts['noncontrol_marker_before_text'] += 1
            continue
        counts[label] += 1
        if mod == 0:
            selectors[f'control_{frame[3]}'] += 1
        else:
            # Do not report printable character values; these are only aggregate classes.
            selectors['printable_selector'] += 1
    total = len(rows)
    accepted = counts['printable_marker_in_candidate'] + counts['control_marker_before_candidate']
    return {'file': name, 'candidate_count': total,
            'matching_frame_count': accepted,
            'matching_forms': {k: counts[k] for k in (
                'printable_marker_in_candidate', 'control_marker_before_candidate')},
            'nonmatching_reasons': dict(sorted((k, v) for k, v in counts.items()
                                                 if k not in ('printable_marker_in_candidate',
                                                              'control_marker_before_candidate'))),
            'control_selector_value_histogram_decimal': dict(sorted(selectors.items()))}


def safe_output(path: Path, root: Path) -> Path:
    p = path.resolve()
    if not any(p.is_relative_to((root / part).resolve()) for part in ('local-data','dist')):
        raise ValueError('Report must be saved under local-data/ or dist/')
    return p


def audit(bin_dir: Path, root: Path = ROOT, *, limit: int | None = None,
          out: Path | None = None) -> dict:
    baseline = load_json(root / 'docs/baseline.json')
    index = load_json(root / 'translations/index.json')
    if baseline['game_id'] != 'BCUS98147' or index['game_id'] != 'BCUS98147':
        raise ValueError('Wrong game ID')
    archive = bin_dir / 'etc.bin_'
    size = archive.stat().st_size
    if size != baseline['archive_size']:
        raise ValueError('Original archive size differs from baseline')
    fht = read_fht(bin_dir, size)
    specs = [v for v in index['files'] if v['file'].startswith('cmc/en/')
             and v['kind'] == 'dialogue']
    if limit is not None:
        if type(limit) is not int or limit < 1:
            raise ValueError('--limit must be positive')
        specs = specs[:limit]
    reports = []
    with archive.open('rb') as stream:
        for v in specs:
            name = v['file']
            if name not in fht:
                raise ValueError(f'Missing CMC archive item {name}')
            offset, length = fht[name]
            if not 0 < length <= MAX_FILE_BYTES:
                raise ValueError(f'CMC size outside safe bounds: {name}')
            stream.seek(offset)
            data = stream.read(length)
            if len(data) != length:
                raise ValueError(f'Truncated archive item {name}')
            cat = load_json(root / 'translations' / v['catalog'])
            if len(cat['entries']) != v['entries'] or cat['file'] != name:
                raise ValueError(f'Catalog index mismatch: {name}')
            reports.append(audit_catalog(data, cat, v['source_sha256']))
    summary = {'schema': 1, 'game_id': 'BCUS98147',
               'kind': 'REDACTED_CMC_ALL_CATALOG_FRAME_AUDIT',
               'contains_game_bytes_or_source_text': False,
               'frame_pattern': '00 04 00 XX (unproven candidate record layout)',
               'scope': 'All cataloged CMC ASCII-NUL candidate offsets only; not all text or game messages',
               'message_parser_proven': False, 'repacker_available': False,
               'files_audited': len(reports),
               'candidates_audited': sum(x['candidate_count'] for x in reports),
               'frames_matching': sum(x['matching_frame_count'] for x in reports),
               'files': reports}
    if out is not None:
        target = safe_output(out, root)
        # Reports are written only after every source hash/byte has passed.
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(summary, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    return summary


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    choose = p.add_mutually_exclusive_group(required=True)
    choose.add_argument('--game-root', type=Path)
    choose.add_argument('--bin-dir', type=Path)
    p.add_argument('--limit', type=int, help='Inspect first N CMC catalogs only')
    p.add_argument('--out', type=Path, default=ROOT/'local-data/dialogue-cmc-frame-audit.json')
    args = p.parse_args()
    try:
        folder = archive_folder(args.game_root, args.bin_dir)
        result = audit(folder, limit=args.limit, out=args.out)
    except (ValueError, OSError, KeyError, UnicodeError, TypeError, struct.error) as exc:
        p.exit(1, f'CMC frame audit refused: {exc}\n')
    print(f'CMC {result["files_audited"]} files, '
          f'{result["frames_matching"]}/{result["candidates_audited"]} candidate frames match.')
    print(f'Redacted metadata report: {args.out}')
    print('Read-only: no game binaries or catalogs changed. No message parser/repacker.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())