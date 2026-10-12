"""Analyze Folklore diagnostic sample gaps without exposing original bytes or text.

Consumes the private local-data/dialogue-probe.json produced by dialogue_diagnose.
Outputs numeric data only: offsets, gap lengths, and byte CLASS counts. This is
NOT a message parser, opcode detector, pointer validator or patching tool.
Python 3.10+, stdlib only. Does not read or modify game archives.
"""
from __future__ import annotations
import argparse
from collections import Counter
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAX_GAP_BYTES = 32   # Avoid characterizing long regions that may contain text.


def local_path(path: Path) -> Path:
    result = path.resolve()
    if not any(result.is_relative_to((ROOT / x).resolve()) for x in ('local-data', 'dist')):
        raise ValueError('Input/output must stay under ignored local-data/ or dist/')
    return result


def byte_class(b: int) -> str:
    if b == 0:
        return 'zero'
    if b < 0x20 or b == 0x7f:
        return 'control'
    if b == 0x20:
        return 'space'
    if b < 0x7f:
        return 'printable'
    return 'high'


def analyze(payload: dict) -> dict:
    if not isinstance(payload, dict) or payload.get('schema') != 1 \
            or payload.get('game_id') != 'BCUS98147' \
            or payload.get('mode') != 'READ_ONLY_FORENSICS' \
            or not isinstance(payload.get('reports'), list):
        raise ValueError('Not a Folklore read-only probe')
    files = []
    for f in payload['reports']:
        name = f['file']
        if not isinstance(name, str) or not name.startswith(('talk/en/', 'cmc/en/')):
            raise ValueError('Unexpected file name')
        sections = f['sections']
        samples = sorted(f['samples'], key=lambda s: s['file_offset'])
        if not isinstance(sections, list) or not isinstance(samples, list):
            raise ValueError('Malformed report')
        summaries: list[dict] = []
        histogram: Counter[int] = Counter()
        classhist: Counter[str] = Counter()
        gap_count = 0
        skipped_long = 0
        missed_windows = 0
        for a, b in zip(samples, samples[1:]):
            start = a['nul_at'] + 1
            stop = b['file_offset']
            if stop < start:
                raise ValueError('Overlapping sample candidate ranges')
            # Only compare immediately consecutive samples within the SAME talk section.
            sa, sb = a['section'], b['section']
            if sa != sb:
                continue
            if not any(s['name'] == sa and s['is_talk'] and
                       s['start'] <= a['file_offset'] < start <= stop < s['end']
                       for s in sections):
                raise ValueError('Sample boundaries outside a named talk section')
            gap = stop - start
            gap_count += 1
            histogram[gap] += 1
            if gap > MAX_GAP_BYTES:
                skipped_long += 1
                continue
            before = bytes.fromhex(a['bytes_after_hex'])
            if len(before) < gap:
                missed_windows += 1
                continue
            # This window is restricted to bytes BETWEEN validated NUL-text ranges.
            # Never emit raw bytes, hashes, byte values, text previews, or hex.
            classes = Counter(byte_class(ch) for ch in before[:gap])
            classhist.update(classes)
            summaries.append({
                'left_nul_at': a['nul_at'],
                'right_text_at': b['file_offset'],
                'gap_size': gap,
                'first_gap_byte_alignment4': start % 4,
                'class_counts': dict(sorted(classes.items())),
            })
        files.append({
            'file': name,
            'sampled_candidates': len(samples),
            'adjacent_pairs_in_section': gap_count,
            'gap_lengths': {str(k): v for k, v in sorted(histogram.items())},
            'gap_class_counts_short_only': dict(sorted(classhist.items())),
            'long_gaps_omitted': skipped_long,
            'gaps_window_unavailable': missed_windows,
            'short_gap_samples': summaries,
        })
    return {
        'schema': 1, 'game_id': 'BCUS98147',
        'kind': 'REDACTED_GAP_CLASS_STATISTICS',
        'contains_original_text_or_hex': False,
        'scope': ('Numeric lengths and byte-class aggregates only for short gaps '
                  'between sampled candidate ranges; not proven opcodes, pointers, '
                  'message order, or all unscanned text.'),
        'message_parser_proven': False,
        'repacker_available': False,
        'files': files,
    }


def run(source: Path, dest: Path) -> dict:
    src, dst = local_path(source), local_path(dest)
    if src == dst:
        raise ValueError('Input and output paths must differ')
    report = json.loads(src.read_text(encoding='utf-8'))
    summary = analyze(report)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return summary


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--in', dest='source', type=Path,
                   default=ROOT/'local-data/dialogue-probe.json')
    p.add_argument('--out', dest='dest', type=Path,
                   default=ROOT/'local-data/dialogue-gap-fingerprint.json')
    a = p.parse_args()
    try:
        r = run(a.source, a.dest)
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        p.exit(1, f'Refused: {exc}\n')
    print(f'Redacted short-gap class stats: {len(r["files"])} files -> {a.dest}')
    print('No game files modified. Not proof of opcode layout or pointer format.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
