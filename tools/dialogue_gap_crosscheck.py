"""Cross-check two REDACTED Folklore diagnostic reports. No game binaries used.

Reports validate numerical consistency and suggest hypotheses only; a matching
pattern does NOT validate command stream grammar or dialogue repacking.
Python 3.10+, standard library.
"""
from __future__ import annotations
import argparse
from collections import Counter
import json
from pathlib import Path

BYTE_CLASSES = frozenset({'zero', 'control', 'space', 'printable', 'high'})


def integer(v, label):
    if type(v) is not int or v < 0:
        raise ValueError(f'Invalid nonnegative integer: {label}')
    return v


def crosscheck(gap_report: dict, structure_report: dict) -> dict:
    if not isinstance(gap_report, dict) or not isinstance(structure_report, dict):
        raise ValueError('Invalid JSON report')
    if (gap_report.get('schema') != 1 or structure_report.get('schema') != 1
            or gap_report.get('game_id') != 'BCUS98147'
            or structure_report.get('game_id') != 'BCUS98147'
            or gap_report.get('kind') != 'REDACTED_GAP_CLASS_STATISTICS'
            or structure_report.get('kind') != 'STRUCTURAL_METADATA_ONLY'
            or gap_report.get('contains_original_text_or_hex') is not False
            or structure_report.get('raw_text_or_hex_windows_included') is not False):
        raise ValueError('Expected paired redacted BCUS98147 reports')
    gf, sf = gap_report['files'], structure_report['files']
    if not isinstance(gf, list) or not isinstance(sf, list) or len(gf) != len(sf):
        raise ValueError('Different file list lengths')
    files, total_pairs, small_pairs, model_hits = [], 0, 0, 0
    for a, b in zip(gf, sf):
        if a['file'] != b['file']:
            raise ValueError('File order/name mismatch')
        samples = b['samples']
        if not isinstance(samples, list) or integer(a['sampled_candidates'], 'candidate count') != len(samples):
            raise ValueError('Sample count mismatch')
        if samples != sorted(samples, key=lambda x: x['file_offset']):
            raise ValueError('Source samples must be sorted')
        sections = {s['index']: s for s in b['sections']}
        pairs = []
        for left, right in zip(samples, samples[1:]):
            i = left['section_index']
            if i != right['section_index']:
                continue
            section = sections[i]
            if not section['is_talk']:
                raise ValueError('Non-talk sample')
            first, last = integer(left['nul_at'], 'NUL offset'), integer(right['file_offset'], 'text offset')
            if (left['file_offset'] > first or first >= last
                    or not (section['start'] <= left['file_offset'] <= first < last < section['end'])):
                raise ValueError('Overlapping or out-of-section sources')
            pairs.append((first, last, last - first - 1))
        hist = Counter(str(gap) for _, _, gap in pairs)
        if hist != Counter(a['gap_lengths']):
            raise ValueError(f'{a["file"]}: gap histogram differs from source offsets')
        if integer(a['adjacent_pairs_in_section'], 'pair count') != len(pairs):
            raise ValueError('Adjacent pair count mismatch')
        shorts = a['short_gap_samples']
        known = Counter((left, last, n) for left, last, n in pairs if n <= 32)
        classes = Counter()
        compact, pure_nontext, regular, control_count = 0, 0, 0, 0
        for g in shorts:
            key = (integer(g['left_nul_at'], 'left NUL'), integer(g['right_text_at'], 'right text'), integer(g['gap_size'], 'gap size'))
            if key[2] > 32 or known[key] < 1:
                raise ValueError('Missing or invalid short gap')
            known[key] -= 1
            if g['first_gap_byte_alignment4'] != (key[0]+1) % 4:
                raise ValueError('Gap alignment mismatch')
            cc = g['class_counts']
            if not isinstance(cc, dict) or not set(cc).issubset(BYTE_CLASSES):
                raise ValueError('Invalid byte class')
            cc = Counter({k: integer(v, 'byte class count') for k, v in cc.items()})
            if sum(cc.values()) != key[2]:
                raise ValueError('Bad classified gap length')
            classes.update(cc)
            if not any(cc[x] for x in ('printable', 'space', 'high')):
                pure_nontext += 1
            if key[2] <= 8:
                compact += 1
                if cc['zero'] + cc['control'] == key[2] and (
                    (key[1] % 4 == 3 and cc['control'] == 1) or
                    (key[1] % 4 == 0 and cc['control'] == 2)
                ):
                    regular += 1
            control_count += cc['control']
        if classes != Counter(a['gap_class_counts_short_only']):
            raise ValueError('Byte-class aggregates differ')
        long_count = sum(n > 32 for _, _, n in pairs)
        if (integer(a['long_gaps_omitted'], 'long gaps') != long_count or
                integer(a['gaps_window_unavailable'], 'unavailable gaps') != sum(known.values())):
            raise ValueError('Gap reporting does not cover every sample pair')
        total_pairs += len(pairs)
        small_pairs += compact
        model_hits += regular
        files.append({
            'file': a['file'], 'sampled_candidates': len(samples),
            'adjacent_pairs': len(pairs), 'short_gaps_at_most_32': len(shorts),
            'gaps_at_most_8': compact, 'gaps_at_most_8_matching_alignment_pattern': regular,
            'short_gaps_only_zero_and_control': pure_nontext,
            'short_gaps_with_printable_or_space_or_high': len(shorts)-pure_nontext,
            'short_gap_class_counts': dict(sorted(classes.items())),
            'interpretation': 'Unproven structural regularity, not a decoded opcode or record format.',
        })
    return {
        'schema': 1, 'game_id': 'BCUS98147', 'kind': 'REDACTED_GAP_CROSSCHECK',
        'reports_consistent': True, 'total_compared_adjacent_pairs': total_pairs,
        'total_compact_gaps': small_pairs, 'compact_gaps_matching_alignment_pattern': model_hits,
        'message_parser_proven': False, 'repacker_available': False,
        'files': files,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--gap', required=True, type=Path)
    parser.add_argument('--structure', required=True, type=Path)
    parser.add_argument('--out', type=Path, default=None)
    args = parser.parse_args()
    try:
        g = json.loads(args.gap.read_text(encoding='utf-8'))
        s = json.loads(args.structure.read_text(encoding='utf-8'))
        result = crosscheck(g, s)
        content = json.dumps(result, indent=2, ensure_ascii=False) + '\n'
        if args.out is None:
            print(content, end='')
        else:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text(content, encoding='utf-8')
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        parser.exit(1, f'Crosscheck refused: {exc}\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
