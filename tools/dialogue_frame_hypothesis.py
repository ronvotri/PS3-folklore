"""Read-only, redacted Folklore CMC 4-byte frame hypothesis test.

Consumes the PRIVATE local-data/dialogue-probe.json from the original
read-only diagnostic. It never opens game archives or patches anything.
Output is only aggregate counts; no text, byte values, sample offsets or hex.
A matching frame is evidence of a record pattern, NOT a proven opcode/parser.
Requires Python 3.10+ and standard library only.
"""
from __future__ import annotations
import argparse
from collections import Counter
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAX_GAP = 8


def within_local(path: Path) -> Path:
    p = path.resolve()
    if not any(p.is_relative_to((ROOT / d).resolve()) for d in ('local-data', 'dist')):
        raise ValueError('Input/output must stay under ignored local-data/ or dist/')
    return p


def analyze(payload: dict) -> dict:
    if (not isinstance(payload, dict) or payload.get('schema') != 1
            or payload.get('game_id') != 'BCUS98147'
            or payload.get('mode') != 'READ_ONLY_FORENSICS'
            or not isinstance(payload.get('reports'), list)):
        raise ValueError('Not a Folklore read-only source probe')
    results = []
    for report in payload['reports']:
        name = report['file']
        if not isinstance(name, str) or not name.startswith(('cmc/en/', 'talk/en/')):
            raise ValueError('Unsupported archive name')
        samples = sorted(report['samples'], key=lambda r: r['file_offset'])
        sections = report['sections']
        if not isinstance(sections, list):
            raise ValueError('Malformed CMC section list')
        considered = 0
        matches = Counter()
        mismatches = Counter()
        ineligible = Counter()
        for a, b in zip(samples, samples[1:]):
            if a['section'] != b['section']:
                continue
            # This experiment applies to CMC sections only, not raw talk scripts.
            if not name.startswith('cmc/en/'):
                continue
            start = a['nul_at'] + 1
            target = b['file_offset']
            if target < start:
                raise ValueError('Overlapping sampled source ranges')
            if not any(s['name'] == a['section'] and s['is_talk']
                       and s['start'] <= a['file_offset'] < start <= target < s['end']
                       for s in sections):
                raise ValueError('Source sample lies outside named CMC talk section')
            length = target - start
            if length > MAX_GAP:
                ineligible['gap_gt_8'] += 1
                continue
            considered += 1
            after = bytes.fromhex(a['bytes_after_hex'])
            if len(after) < length:
                mismatches['missing_private_byte_window'] += 1
                continue
            gap = after[:length]
            if target % 4 == 3:
                # Candidate's first printable byte may itself be record metadata.
                source = b['source']
                if not isinstance(source, str) or not source or ord(source[0]) > 127:
                    raise ValueError('Missing/invalid ASCII candidate prefix')
                if length < 3:
                    mismatches['frame_not_contained_in_gap'] += 1
                    continue
                frame_start = target - 3
                candidate = gap[-3:] + source[0].encode('ascii')
                shape = 'printable_leading_byte_at_mod3'
            elif target % 4 == 0:
                if length < 4:
                    mismatches['frame_not_contained_in_gap'] += 1
                    continue
                frame_start = target - 4
                candidate = gap[-4:]
                shape = 'nonprintable_leading_byte_at_mod0'
            else:
                mismatches['unexpected_candidate_alignment'] += 1
                continue
            if frame_start % 4:
                mismatches['frame_start_unaligned'] += 1
                continue
            if candidate[:3] != b'\x00\x04\x00':
                mismatches['missing_000400_signature'] += 1
                continue
            if shape == 'nonprintable_leading_byte_at_mod0' and not (1 <= candidate[3] <= 31):
                mismatches['last_byte_not_control'] += 1
                continue
            if shape == 'printable_leading_byte_at_mod3' and not (32 <= candidate[3] <= 126):
                mismatches['last_byte_not_printable'] += 1
                continue
            before_frame = gap[:frame_start-start]
            if any(x != 0 for x in before_frame):
                mismatches['nonzero_padding_before_frame'] += 1
                continue
            matches[shape] += 1
        results.append({
            'file': name,
            'candidate_count_sampled': len(samples),
            'short_gap_pairs_checked': considered,
            'matching_000400xx_frames': sum(matches.values()),
            'matching_prefix_classes': dict(sorted(matches.items())),
            'nonmatching_reasons': dict(sorted(mismatches.items())),
            'long_gap_pairs_not_tested': ineligible['gap_gt_8'],
        })
    return {
        'schema': 1,
        'game_id': 'BCUS98147',
        'kind': 'REDACTED_CMC_FRAME_HYPOTHESIS',
        'contains_original_text_or_hex': False,
        'scope': 'Four-byte frame 00 04 00 XX signature near sampled CMC text; only gaps <=8 bytes.',
        'message_parser_proven': False,
        'repacker_available': False,
        'files': results,
    }


def run(source: Path, target: Path) -> dict:
    src, dst = within_local(source), within_local(target)
    if src == dst:
        raise ValueError('Input and output cannot be the same path')
    data = json.loads(src.read_text(encoding='utf-8'))
    summary = analyze(data)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    return summary


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--in', dest='src', type=Path,
                   default=ROOT / 'local-data/dialogue-probe.json')
    p.add_argument('--out', dest='dst', type=Path,
                   default=ROOT / 'local-data/dialogue-frame-hypothesis.json')
    args = p.parse_args()
    try:
        r = run(args.src, args.dst)
    except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
        p.exit(1, f'Refused: {exc}\n')
    for f in r['files']:
        if f['short_gap_pairs_checked']:
            print(f"{f['file']}: {f['matching_000400xx_frames']}/"
                  f"{f['short_gap_pairs_checked']} four-byte candidate frames")
    print(f'Redacted report: {args.dst}')
    print('No game files modified; this is NOT a validated message parser.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
