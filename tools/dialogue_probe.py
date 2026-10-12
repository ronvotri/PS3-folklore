"""Read-only forensic probe for Folklore BCUS98147 dialogue candidates.

This is NOT a parser, serializer, repacker, patcher or speaker detector. All
observations are hypotheses about binary layout, not relocation instructions.
Original game data are read from etc.bin_/etc.fht_ locally; NEVER committed.
Python >=3.10, standard library only.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import struct
from dataclasses import dataclass
from pathlib import Path

import folklore

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FILES = (
    'talk/en/tk100_en.bin_',
    'talk/en/tk101_en.bin_',
    'cmc/en/LCmc000_en.bi5_',
    'cmc/en/LCmc004_en.bi5_',
)
MAX_FILE_BYTES = 128 * 1024 * 1024
MAX_RADIUS = 256


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def cmc_sections(data: bytes) -> list[dict]:
    """Inventory section bounds/names; does NOT parse command stream."""
    if len(data) < 0x38:
        raise ValueError('CMC header too short')
    declared, count = struct.unpack_from('>II', data, 0)
    if declared != len(data) or not 1 <= count <= 64:
        raise ValueError('Unsupported CMC header')
    table_end = 0x30 + 4 * (count + 1)
    name_end = table_end + 24 * count
    if name_end > len(data):
        raise ValueError('CMC section names outside file')
    edges = struct.unpack_from(f'>{count + 1}I', data, 0x30)
    # Zero-length CMC sections are legal (and were accepted by catalog.py).
    # Only descending, overlapping or out-of-file boundaries are invalid.
    if edges[0] < name_end:
        raise ValueError(
            f'Invalid CMC section bounds: first edge 0x{edges[0]:x} '
            f'overlaps section-name table ending at 0x{name_end:x}')
    if edges[-1] > len(data):
        raise ValueError(
            f'Invalid CMC section bounds: last edge 0x{edges[-1]:x} '
            f'exceeds file length 0x{len(data):x}')
    for i, (start, end) in enumerate(zip(edges, edges[1:])):
        if start > end:
            raise ValueError(
                f'Invalid CMC section bounds: section {i} descends '
                f'from 0x{start:x} to 0x{end:x}')
    result = []
    for i in range(count):
        raw = data[table_end + i * 24:table_end + (i + 1) * 24]
        name = raw.split(b'\0', 1)[0].decode('ascii', errors='backslashreplace')
        result.append({'name': name, 'start': edges[i], 'end': edges[i + 1],
                       'is_talk': name.startswith('talk')})
    return result


@dataclass(frozen=True)
class OpaqueCMCContainer:
    """Immutable section envelope; section payloads are NOT decoded messages."""
    header: bytes
    edges: tuple[int, ...]
    name_table: bytes
    padding: bytes
    payloads: tuple[bytes, ...]
    trailer: bytes

    def serialize(self) -> bytes:
        """Reassemble every byte and refuse size/offset changes (no editing)."""
        count = len(self.payloads)
        if (len(self.header) != 0x30 or not 1 <= count <= 64
                or len(self.edges) != count + 1
                or len(self.name_table) != 24 * count):
            raise ValueError('Invalid opaque CMC component lengths')
        declared, header_count = struct.unpack_from('>II', self.header)
        if header_count != count:
            raise ValueError('CMC section count changed')
        name_end = 0x30 + 4 * (count + 1) + 24 * count
        if name_end + len(self.padding) != self.edges[0]:
            raise ValueError('CMC first section boundary changed')
        for i, payload in enumerate(self.payloads):
            if self.edges[i + 1] < self.edges[i] or len(payload) != self.edges[i + 1] - self.edges[i]:
                raise ValueError('CMC section payload length changed')
        body = (self.header + struct.pack(f'>{count + 1}I', *self.edges)
                + self.name_table + self.padding + b''.join(self.payloads)
                + self.trailer)
        if len(body) != declared:
            raise ValueError('CMC declared size changed')
        return body


def parse_opaque_cmc(data: bytes) -> OpaqueCMCContainer:
    """Parse only known CMC envelope boundaries, preserving opaque bytes."""
    sections = cmc_sections(data)  # Fail closed on malformed header/edges.
    count = len(sections)
    names_at = 0x30 + 4 * (count + 1)
    names_end = names_at + 24 * count
    edges = struct.unpack_from(f'>{count + 1}I', data, 0x30)
    return OpaqueCMCContainer(
        header=data[:0x30],
        edges=tuple(edges),
        name_table=data[names_at:names_end],
        padding=data[names_end:edges[0]],
        payloads=tuple(data[s['start']:s['end']] for s in sections),
        trailer=data[edges[-1]:],
    )


def check_opaque_cmc_roundtrip(data: bytes) -> None:
    """Proof is limited to the outer section envelope, NOT talk commands."""
    if parse_opaque_cmc(data).serialize() != data:
        raise ValueError('CMC opaque section parse/serialize byte mismatch')



def verify_candidates(data: bytes, catalog: dict) -> tuple[list[dict], dict]:
    """Fail closed unless every catalog source is exact ASCII+NUL at its offset."""
    file_name = catalog['file']
    if sha256(data) != catalog['file_sha256']:
        raise ValueError(f'Original SHA-256 differs for {file_name}; no report written')
    if file_name.startswith('cmc/en/'):
        sections = cmc_sections(data)
    elif file_name.startswith('talk/en/'):
        sections = [{'name': '(raw talk file; structure unknown)', 'start': 0,
                     'end': len(data), 'is_talk': True}]
    else:
        raise ValueError(f'Unsupported binary kind: {file_name}')
    seen_offsets: set[int] = set()
    for row in catalog['entries']:
        offset = row['file_offset']
        if not isinstance(offset, int) or isinstance(offset, bool) or offset in seen_offsets:
            raise ValueError(f'Invalid/duplicate offset in {file_name}: {offset}')
        seen_offsets.add(offset)
        if row['id'] != f'{file_name}@{offset:08x}':
            raise ValueError(f'Catalog ID differs at offset {offset}')
        source = row['source']
        try:
            payload = source.encode('ascii')
        except UnicodeEncodeError as exc:
            raise ValueError(f'Catalog source is not ASCII at {offset:#x}') from exc
        if not payload or sha256(source.encode('utf-8')) != row['source_sha256']:
            raise ValueError(f'Catalog source digest mismatch at {offset:#x}')
        end = offset + len(payload)
        if offset < 0 or end >= len(data) or data[offset:end] != payload or data[end] != 0:
            raise ValueError(f'Original bytes/NUL differ at {file_name}@{offset:08x}')
        if not any(s['is_talk'] and s['start'] <= offset and end < s['end'] for s in sections):
            raise ValueError(f'Candidate outside named talk section at {offset:#x}')
    stats = {
        'entries_verified': len(catalog['entries']),
        'statuses': dict(sorted(collections.Counter(r['status'] for r in catalog['entries']).items())),
        'begins_newline': sum(r['source'].startswith('\n') for r in catalog['entries']),
        'begins_space': sum(r['source'].startswith(' ') for r in catalog['entries']),
        'begins_dollar': sum(r['source'].startswith('$') for r in catalog['entries']),
        'begins_paren': sum(r['source'].startswith('(') for r in catalog['entries']),
        'begins_choice': sum(r['source'].startswith('* ') for r in catalog['entries']),
    }
    return sections, stats


def hits_for_u32(data: bytes, value: int, *, max_hits: int = 16) -> list[dict]:
    """Raw byte-pattern sightings only; not validated references or pointers."""
    if value <= 0 or value > 0xffffffff:
        return []
    results = []
    for endian in ('big', 'little'):
        needle = value.to_bytes(4, endian)
        pos = data.find(needle)
        count = 0
        locations = []
        while pos != -1:
            count += 1
            if len(locations) < max_hits:
                locations.append({'at': pos, 'aligned4': pos % 4 == 0})
            pos = data.find(needle, pos + 1)
        if count:
            results.append({'endianness': endian, 'value_hex': f'0x{value:08x}',
                            'hit_count': count, 'locations': locations,
                            'truncated': count > max_hits})
    return results


def select_names(index: dict | None, names: list[str] | None,
                 all_dialogue: bool) -> tuple[str, ...]:
    """Select catalog sources in index order; do not invent archive paths."""
    if all_dialogue:
        if names is not None:
            raise ValueError('--all-dialogue and --files cannot be combined')
        if index is None:
            raise ValueError('Missing catalog index for all-dialogue selection')
        selected = tuple(row['file'] for row in index['files']
                         if row['kind'] == 'dialogue')
        if not selected or len(selected) != len(set(selected)):
            raise ValueError('No dialogue entries or duplicate dialogue names in index')
        return selected
    return tuple(names if names is not None else DEFAULT_FILES)


def sample_indices(entries: list[dict], limit: int) -> list[int]:
    """Deterministically cover leading labels, fragments and end-of-file."""
    if not entries or limit <= 0:
        return []
    categories = (
        lambda s: s.startswith('$'), lambda s: s.startswith('* '),
        lambda s: s.startswith('('), lambda s: s.startswith(' '),
        lambda s: s.startswith('\n'), lambda s: '\n' in s[1:],
        lambda s: not s.startswith((' ', '\n', '$', '*', '(')),
    )
    chosen = []
    def add(i):
        if i not in chosen and len(chosen) < limit:
            chosen.append(i)
    add(0)
    for predicate in categories:
        for i, row in enumerate(entries):
            if predicate(row['source']):
                add(i)
                break
    add(len(entries) // 2)
    add(len(entries) - 1)
    for i in range(len(entries)):
        add(i)
    return sorted(chosen)


def ascii_preview(data: bytes) -> str:
    return ''.join(chr(b) if 32 <= b <= 126 else '.' for b in data)


def probe_binary(data: bytes, catalog: dict, *, radius: int = 64,
                 max_samples: int = 12, verify_only: bool = False) -> dict:
    if not 0 <= radius <= MAX_RADIUS or not 1 <= max_samples <= 100:
        raise ValueError('radius must be 0..256 and max_samples 1..100')
    sections, stats = verify_candidates(data, catalog)
    is_cmc = catalog['file'].startswith('cmc/en/')
    if is_cmc:
        check_opaque_cmc_roundtrip(data)
    entries = catalog['entries']
    examples = []
    for i in ([] if verify_only else sample_indices(entries, max_samples)):
        row = entries[i]
        start = row['file_offset']
        end = start + len(row['source'].encode('ascii')) + 1
        section = next(s for s in sections if s['is_talk'] and s['start'] <= start and end <= s['end'])
        # Never inspect beyond the active talk section boundary for context.
        before = data[max(section['start'], start - radius):start]
        after = data[end:min(section['end'], end + radius)]
        patterns = [{'kind': 'file_relative_offset', 'candidates': hits_for_u32(data, start)}]
        delta = start - section['start']
        if section['start'] and delta:
            patterns.append({'kind': 'section_relative_offset', 'section': section['name'],
                             'candidates': hits_for_u32(data, delta)})
        examples.append({
            'id': row['id'], 'source': row['source'], 'status': row['status'],
            'file_offset': start, 'nul_at': end - 1, 'section': section['name'],
            'bytes_before_hex': before.hex(' '), 'bytes_before_ascii': ascii_preview(before),
            'bytes_after_hex': after.hex(' '), 'bytes_after_ascii': ascii_preview(after),
            'u32_byte_patterns': patterns,
        })
    return {
        'file': catalog['file'], 'size': len(data), 'sha256': sha256(data),
        'source_verification': 'all catalog ASCII+NUL bytes and file digest match original',
        'stats': stats, 'sections': sections, 'samples': examples,
        'u32_pattern_scan': not verify_only,
        'opaque_cmc_container_roundtrip': True if is_cmc else None,
        'limitations': ('Raw u32 matches are byte-pattern candidates, not proven pointers. '
                        'Opaque CMC roundtrip checks section envelopes only; '
                        'no command/speaker/control-flow parser, relocation or patch capability.'),
    }


def run(bin_dir: Path, names: tuple[str, ...], out: Path, *,
        radius: int = 64, max_samples: int = 12,
        verify_only: bool = False) -> dict:
    allowed_roots = (ROOT / 'local-data', ROOT / 'dist')
    resolved = out.resolve()
    if not any(resolved.is_relative_to(p.resolve()) for p in allowed_roots):
        raise ValueError('Report path must be under ignored local-data/ or dist/')
    if not names or len(names) != len(set(names)):
        raise ValueError('Specify distinct archive file names')
    baseline = folklore.read_json(ROOT / 'docs/baseline.json')
    index = folklore.read_json(ROOT / 'translations/index.json')
    if index['game_id'] != 'BCUS98147' or baseline['game_id'] != index['game_id']:
        raise ValueError('Unsupported game ID')
    fht = folklore.read_index(bin_dir)
    archive = bin_dir / 'etc.bin_'
    if archive.stat().st_size != baseline['archive_size']:
        raise ValueError('Archive size differs from verified BCUS98147 baseline')
    lookup = {f['file']: f for f in index['files']}
    reports = []
    with archive.open('rb') as stream:
        for name in names:
            spec = lookup.get(name)
            if not spec or spec['kind'] != 'dialogue' or name not in fht:
                raise ValueError(f'Not a supported catalog/archive item: {name}')
            location = fht[name]
            if not 0 < location['size'] <= MAX_FILE_BYTES:
                raise ValueError(f'Unexpected file size for {name}')
            stream.seek(location['offset'])
            data = stream.read(location['size'])
            if len(data) != location['size']:
                raise ValueError(f'Archive entry truncated: {name}')
            catalog = folklore.read_json(ROOT / 'translations' / spec['catalog'])
            if catalog['file'] != name or catalog['file_sha256'] != spec['source_sha256']:
                raise ValueError(f'Index/catalog mismatch for {name}')
            try:
                report = probe_binary(data, catalog, radius=radius,
                                      max_samples=max_samples,
                                      verify_only=verify_only)
            except (ValueError, UnicodeError, struct.error) as exc:
                raise ValueError(f'{name}: {exc}') from exc
            report['archive_offset'] = location['offset']
            reports.append(report)
    payload = {'schema': 1, 'game_id': 'BCUS98147', 'mode': 'READ_ONLY_FORENSICS',
               'parser_validated': False, 'repacker_available': False,
               'scan_mode': 'SOURCE_ONLY' if verify_only else 'SOURCE_AND_BYTE_PATTERNS',
               'verified_candidate_total': sum(r['stats']['entries_verified'] for r in reports),
               'reports': reports}
    # If *any* file fails verification, no report is written.
    resolved.parent.mkdir(parents=True, exist_ok=True)
    resolved.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return payload


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--bin-dir', required=True, type=Path,
                   help='Local folder containing original etc.bin_ and etc.fht_')
    p.add_argument('--files', nargs='+', default=None,
                   help='Exact archive entries with committed catalog JSON')
    p.add_argument('--all-dialogue', action='store_true',
                   help='Verify every dialogue catalog in index order (read-only)')
    p.add_argument('--verify-only', action='store_true',
                   help='Verify source SHA, offsets, NUL and CMC bounds; skip u32 scans')
    p.add_argument('--out', type=Path, default=ROOT/'local-data/dialogue-probe.json',
                   help='Ignored report path under local-data/ or dist/')
    p.add_argument('--radius', type=int, default=64)
    p.add_argument('--max-samples', type=int, default=12)
    args = p.parse_args()
    try:
        index = folklore.read_json(ROOT / 'translations/index.json') if args.all_dialogue else None
        names = select_names(index, args.files, args.all_dialogue)
        report = run(args.bin_dir, names, args.out,
                     radius=args.radius, max_samples=args.max_samples,
                     verify_only=args.verify_only)
    except (ValueError, OSError, KeyError, UnicodeError, struct.error) as exc:
        p.exit(1, f'Probe refused: {exc}\n')
    if args.all_dialogue:
        print(f"VERIFIED {len(report['reports'])} dialogue catalogs / "
              f"{report['verified_candidate_total']} ASCII-NUL candidates; "
              "no message parser or patch capability")
    else:
        for item in report['reports']:
            print(f"VERIFIED {item['file']}: {item['stats']['entries_verified']} sources, "
                  f"{len(item['samples'])} samples; raw pointer patterns NOT validated")
    print(f'Read-only report: {args.out}')


if __name__ == '__main__':
    main()
