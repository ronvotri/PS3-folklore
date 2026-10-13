"""Experimental read-only CMC frame tokenizer for Folklore BCUS98147.

This proves only that confidently recognized 00 04 00 XX *candidate spans*
can be separated and reassembled without changing any bytes. Everything
unrecognized stays opaque. It is NOT a message parser and NEVER patches game.
Only source-verified original files are accepted. Python 3.10+, stdlib.
"""
from __future__ import annotations
from dataclasses import dataclass
from collections import Counter
from pathlib import Path
import argparse
import json

import cmc_frame_audit as audit


@dataclass(frozen=True)
class Opaque:
    raw: bytes

    def serialize(self) -> bytes:
        return self.raw


@dataclass(frozen=True)
class FrameCandidate:
    # This is a four-byte boundary candidate, not proven semantic metadata.
    # DO NOT strip the fourth byte when generating visible dialogue without proof.
    # Neutral names: no speaker/metadata/display semantics have been proven.
    fourth_byte: int
    remaining_ascii: bytes
    # The scanner sometimes included the fourth byte as its first character.
    fourth_byte_in_source: bool

    def serialize(self) -> bytes:
        if not 0 <= self.fourth_byte <= 127 or b'\0' in self.remaining_ascii:
            raise ValueError('Invalid frame token')
        return b'\0\x04\0' + bytes([self.fourth_byte]) + self.remaining_ascii + b'\0'


@dataclass(frozen=True)
class Tokenization:
    tokens: tuple[Opaque | FrameCandidate, ...]
    matched_candidates: int
    opaque_candidates: int
    total_bytes: int

    def serialize(self) -> bytes:
        return b''.join(t.serialize() for t in self.tokens)


def tokenize(data: bytes, catalog: dict, expected_sha: str) -> Tokenization:
    # Mandatory source authenticity, all source hashes/NULs and section checks.
    checked = audit.audit_catalog(data, catalog, expected_sha)
    expected_match = checked['matching_frame_count']
    spans: list[tuple[int, int, FrameCandidate]] = []
    for row in sorted(catalog['entries'], key=lambda r: r['file_offset']):
        at = row['file_offset']
        source = row['source'].encode('ascii')
        mod = at % 4
        if mod == 3:
            start = at - 3
            if not 32 <= source[0] <= 126:
                continue
            fourth_byte = source[0]
            text = source[1:]
            from_source = True
        elif mod == 0:
            start = at - 4
            if start < 0:
                continue
            fourth_byte = data[at-1]
            if not 1 <= fourth_byte <= 31:
                continue
            text = source
            from_source = False
        else:
            continue
        if start < 0 or data[start:start+3] != b'\0\x04\0':
            continue
        frame = FrameCandidate(fourth_byte, text, from_source)
        end = at + len(source) + 1
        if data[start:end] != frame.serialize():
            raise ValueError('Unexpected candidate frame byte mismatch')
        spans.append((start, end, frame))

    if len(spans) != expected_match:
        raise ValueError('Tokenizer disagrees with audited matching-frame count')
    tokens: list[Opaque | FrameCandidate] = []
    pos = 0
    for start, end, frame in sorted(spans):
        if start < pos:
            raise ValueError('Overlapping candidate frame spans')
        tokens.append(Opaque(data[pos:start]))
        tokens.append(frame)
        pos = end
    tokens.append(Opaque(data[pos:]))
    result = Tokenization(tuple(tokens), len(spans),
                          len(catalog['entries']) - len(spans), len(data))
    if len(result.serialize()) != len(data) or result.serialize() != data:
        raise ValueError('Read-only token roundtrip is not byte-exact')
    return result


def survey(bin_dir: Path, root: Path, out: Path | None = None) -> dict:
    baseline = audit.load_json(root/'docs/baseline.json')
    index = audit.load_json(root/'translations/index.json')
    if baseline.get('game_id') != 'BCUS98147' or index.get('game_id') != 'BCUS98147':
        raise ValueError('Incorrect game ID')
    archive = bin_dir/'etc.bin_'
    size = archive.stat().st_size
    if size != baseline['archive_size']:
        raise ValueError('Archive size differs from baseline')
    entries = audit.read_fht(bin_dir, size)
    specs = [v for v in index['files'] if v['file'].startswith('cmc/en/')
             and v['kind'] == 'dialogue']
    totals = Counter()
    with archive.open('rb') as fh:
        for item in specs:
            name = item['file']
            if name not in entries:
                raise ValueError('Missing CMC: '+name)
            off, length = entries[name]
            if not 0 < length <= audit.MAX_FILE_BYTES:
                raise ValueError('Invalid file size: '+name)
            fh.seek(off)
            data = fh.read(length)
            if len(data) != length:
                raise ValueError('Archive read truncated: '+name)
            cat = audit.load_json(root/'translations'/item['catalog'])
            if cat['file'] != name or len(cat['entries']) != item['entries']:
                raise ValueError('Manifest mismatch: '+name)
            result = tokenize(data, cat, item['source_sha256'])
            totals['files'] += 1
            totals['matched'] += result.matched_candidates
            totals['opaque_candidate_count'] += result.opaque_candidates
            totals['bytes_verified'] += result.total_bytes
    report = {'schema': 1, 'game_id': 'BCUS98147',
              'kind': 'REDACTED_CMC_LOSSLESS_CANDIDATE_TOKENIZATION',
              'game_text_or_raw_bytes_included': False,
              'source_hashes_verified': True,
              'candidate_prefixes_tokenized': totals['matched'],
              'candidate_strings_left_opaque': totals['opaque_candidate_count'],
              'files_roundtripped': totals['files'],
              'bytes_reconstructed_exactly': totals['bytes_verified'],
              'message_parser_proven': False, 'repacker_available': False,
              'scope': 'Candidate prefix spans reconstructed byte-for-byte; full message grammar remains unknown.'}
    if out is not None:
        dest = audit.safe_output(out, root)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    return report


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument('--game-root', type=Path)
    group.add_argument('--bin-dir', type=Path)
    p.add_argument('--out', type=Path, default=audit.ROOT/'local-data/cmc-readonly-roundtrip.json')
    args = p.parse_args()
    try:
        folder = audit.archive_folder(args.game_root, args.bin_dir)
        r = survey(folder, audit.ROOT, args.out)
    except (ValueError, OSError, UnicodeError, TypeError, KeyError) as exc:
        p.exit(1, f'Read-only tokenizer refused: {exc}\n')
    print(f'{r["files_roundtripped"]} CMC files reassembled byte-exact; '
          f'{r["candidate_prefixes_tokenized"]} frame candidates recognized, '
          f'{r["candidate_strings_left_opaque"]} uncertain candidates preserved.')
    print('No binary files changed. This is NOT message parsing or game translation.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())