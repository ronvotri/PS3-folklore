"""Read-only CMC exception ID locator with byte-exact opaque roundtrip checks.

No game bytes or dialogue source text are exported. This is NOT a message parser
or a repacker. Python >=3.10, standard library only.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path


def candidate_reason(data: bytes, row: dict, bounds: list[tuple[int, int]]) -> str | None:
    """Classify a source-verified candidate; None means matching 00 04 00 XX.

    Caller MUST validate source SHA, ASCII/NUL and CMC section bounds first.
    """
    at = row['file_offset']
    raw = row['source'].encode('ascii')
    end = at + len(raw)
    mod = at % 4
    if mod == 3:
        if not 32 <= raw[0] <= 126:
            return 'mod3_nonprintable_source_prefix'
        start = at - 3
    elif mod == 0:
        start = at - 4
    else:
        return f'unexpected_mod{mod}'
    if start < 0 or not any(lo <= start and end < hi for lo, hi in bounds):
        return 'frame_outside_talk_bounds'
    if data[start:start + 3] != b'\x00\x04\x00':
        return 'not_000400_frame'
    if mod == 0 and not 1 <= data[at - 1] <= 31:
        return 'noncontrol_marker_before_text'
    return None


def locate_one(data: bytes, catalog: dict, sha: str, audit, tokens) -> dict:
    """Independently cross-check the V6 audit with byte-exact tokenization."""
    result = tokens.tokenize(data, catalog, sha)
    verified = audit.audit_catalog(data, catalog, sha)
    bounds = audit.cmc_talk_bounds(data)
    exceptions = []
    for row in catalog['entries']:
        reason = candidate_reason(data, row, bounds)
        if reason is not None:
            exceptions.append({'id': row['id'],
                               'file_offset': row['file_offset'], 'reason': reason})
    exceptions.sort(key=lambda item: item['file_offset'])
    reasons = dict(Counter(e['reason'] for e in exceptions))
    if reasons != verified['nonmatching_reasons']:
        raise ValueError('Independent exception locator disagrees with V6 audit')
    if (result.matched_candidates != verified['matching_frame_count']
            or result.opaque_candidates != len(exceptions)
            or result.total_bytes != len(data) or result.serialize() != data):
        raise ValueError('Byte-exact tokenizer/exception counts disagree')
    return {'file': catalog['file'], 'candidate_count': len(catalog['entries']),
            'matching_frame_count': result.matched_candidates,
            'opaque_candidate_count': len(exceptions), 'exceptions': exceptions}


def survey(bin_dir: Path, root: Path, output: Path) -> dict:
    import cmc_frame_audit as audit
    import cmc_readonly_tokens as tokens

    baseline = audit.load_json(root / 'docs/baseline.json')
    index = audit.load_json(root / 'translations/index.json')
    if baseline.get('game_id') != 'BCUS98147' or index.get('game_id') != 'BCUS98147':
        raise ValueError('Wrong Folklore game baseline')
    archive = bin_dir / 'etc.bin_'
    archive_size = archive.stat().st_size
    if archive_size != baseline['archive_size']:
        raise ValueError('Archive size differs from original baseline')
    fht = audit.read_fht(bin_dir, archive_size)
    specs = [x for x in index['files'] if x['kind'] == 'dialogue'
             and x['file'].startswith('cmc/en/')]
    out = audit.safe_output(output, root)
    files = []
    with archive.open('rb') as stream:
        for spec in specs:
            name = spec['file']
            if name not in fht:
                raise ValueError('Missing original CMC: ' + name)
            at, length = fht[name]
            if not 0 < length <= audit.MAX_FILE_BYTES:
                raise ValueError('Invalid CMC size: ' + name)
            stream.seek(at)
            data = stream.read(length)
            if len(data) != length:
                raise ValueError('Truncated original CMC: ' + name)
            catalog = audit.load_json(root / 'translations' / spec['catalog'])
            if catalog['file'] != name or len(catalog['entries']) != spec['entries']:
                raise ValueError('Catalog manifest mismatch: ' + name)
            files.append(locate_one(data, catalog, spec['source_sha256'], audit, tokens))
    exceptions = [e for x in files for e in x['exceptions']]
    candidates = sum(x['candidate_count'] for x in files)
    matched = sum(x['matching_frame_count'] for x in files)
    if candidates != sum(x['entries'] for x in specs) or matched + len(exceptions) != candidates:
        raise ValueError('Incomplete CMC candidate accounting')
    report = {
        'schema': 1, 'game_id': 'BCUS98147',
        'kind': 'REDACTED_CMC_BYTE_EXACT_ROUNDTRIP_AND_EXCEPTION_IDS',
        'contains_game_bytes_or_source_text': False,
        'scope': 'Cataloged frame spans only; not parsed messages or all game text.',
        'files_roundtripped': len(files), 'candidates_verified': candidates,
        'candidate_frames_recognized': matched, 'candidates_opaque': len(exceptions),
        'exception_reasons': dict(sorted(Counter(e['reason'] for e in exceptions).items())),
        'exceptions': exceptions,
        'message_parser_proven': False, 'repacker_available': False,
    }
    # No report is written until the entire original archive has passed.
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n',
                   encoding='utf-8')
    return report


def main() -> int:
    import cmc_frame_audit as audit

    p = argparse.ArgumentParser(description=__doc__)
    paths = p.add_mutually_exclusive_group(required=True)
    paths.add_argument('--game-root', type=Path)
    paths.add_argument('--bin-dir', type=Path)
    p.add_argument('--out', type=Path,
                   default=audit.ROOT / 'local-data/cmc-exception-ids.json')
    args = p.parse_args()
    try:
        folder = audit.archive_folder(args.game_root, args.bin_dir)
        result = survey(folder, audit.ROOT, args.out)
    except (ValueError, OSError, KeyError, UnicodeError, TypeError) as exc:
        p.exit(1, f'CMC read-only exception scan refused: {exc}\n')
    print(f"Byte-exact CMC candidate roundtrip: {result['files_roundtripped']} files; "
          f"{result['candidate_frames_recognized']}/{result['candidates_verified']} "
          f"frames, {result['candidates_opaque']} opaque exception IDs.")
    print(f'Redacted report: {args.out}')
    print('No game files modified. Not a message parser or repacker.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
