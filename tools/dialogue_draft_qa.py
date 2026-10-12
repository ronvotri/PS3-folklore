"""Read-only review queue for Folklore's translated dialogue candidates.

All findings are *review prompts*, not proof of in-game formatting or speaker.
Never changes a catalog, the original game archive, status or Merienda V3.
Python 3.10+, standard library only.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOKEN = re.compile(r'<[^<>\n]+>|%(?:\d+\$)?[sdif]|\{\d+\}|\$')
# Scanned ASCII sometimes includes a control-like leading byte as a printable char.
# Unproven prefix semantics: these are only warnings, never automatic edits.
LEAD = frozenset('$@<,(') | frozenset('0123456789')


def issue(kind: str, file: str, row: dict, detail: object) -> dict:
    return {'kind': kind, 'file': file, 'id': row.get('id'), 'detail': detail}


def audit(root: Path) -> dict:
    """Read manifest and candidate catalogs, preserving all source bytes on disk."""
    index = json.loads((root / 'index.json').read_text(encoding='utf-8'))
    if index.get('game_id') != 'BCUS98147' or not isinstance(index.get('files'), list):
        raise ValueError('Unsupported/malformed Folklore index')
    files = index['files']
    issues = []
    seen_ids: set[str] = set()
    duplicates: dict[str, list[tuple[str, str, str]]] = collections.defaultdict(list)
    counts = collections.Counter()
    for spec in files:
        path = spec['catalog']
        if not isinstance(path, str) or not path.startswith('catalogs/') or '..' in Path(path).parts:
            raise ValueError('Invalid catalog manifest path')
        doc = json.loads((root / path).read_text(encoding='utf-8'))
        rows = doc.get('entries')
        if not isinstance(rows, list) or len(rows) != spec['entries'] or doc.get('file') != spec['file']:
            raise ValueError('Manifest/catalog mismatch: ' + path)
        counts['catalogs'] += 1
        for row in rows:
            counts['entries'] += 1
            source, target = row['source'], row['vi']
            name, offset = doc['file'], row['file_offset']
            if not isinstance(source, str) or not isinstance(target, str):
                raise ValueError('Non-string candidate in ' + path)
            if type(offset) is not int or offset < 0 or row.get('id') != f'{name}@{offset:08x}':
                issues.append(issue('invalid_id', path, row, offset))
            if row.get('id') in seen_ids:
                issues.append(issue('duplicate_id', path, row, 'duplicate key'))
            seen_ids.add(row.get('id'))
            if hashlib.sha256(source.encode('utf-8')).hexdigest() != row['source_sha256']:
                issues.append(issue('source_hash_mismatch', path, row, 'Source changed'))
            if target and unicodedata.normalize('NFC', target) != target:
                issues.append(issue('target_not_nfc', path, row, 'Target is not NFC'))
            if row['status'] in ('draft', 'reviewed', 'tested') and not target:
                issues.append(issue('missing_target', path, row, 'Missing translated text'))
            if not target:
                counts['empty_targets'] += 1
                continue
            counts['nonempty_targets'] += 1
            if source.count('\n') != target.count('\n'):
                issues.append(issue('newline_mismatch', path, row, [source.count('\n'), target.count('\n')]))
            if collections.Counter(TOKEN.findall(source)) != collections.Counter(TOKEN.findall(target)):
                issues.append(issue('token_mismatch', path, row, 'Check control tokens'))
            if source and source[0] in LEAD and (not target or target[0] != source[0]):
                issues.append(issue('leading_marker_review', path, row, source[0]))
            if source.startswith((' ', '\n')) or source.endswith(('...', ',')):
                issues.append(issue('fragment_context_review', path, row, 'Original is likely sentence fragment'))
            for lineno, (english, translated) in enumerate(zip(source.split('\n'), target.split('\n')), start=1):
                if len(translated) > 40:
                    issues.append(issue('very_long_line', path, row, {'line': lineno,
                                'source_chars': len(english), 'vi_chars': len(translated)}))
                elif len(translated) > 32 and len(translated) > len(english) * 1.4:
                    issues.append(issue('expanded_line', path, row, {'line': lineno,
                                'source_chars': len(english), 'vi_chars': len(translated)}))
            duplicates[source].append((path, row['id'], target))
    if counts['entries'] != index.get('total_entries'):
        raise ValueError('Manifest total mismatch')
    for source, uses in duplicates.items():
        if len({t for _, _, t in uses}) > 1:
            issues.append({'kind': 'duplicate_source_variants',
                           'source': source, 'uses': [
                               {'file': path, 'id': rid, 'vi': t} for path, rid, t in uses
                           ], 'warning': 'May be intentional due to speaker/context; do not auto-replace.'})
    types = collections.Counter(i['kind'] for i in issues)
    return {'schema': 1, 'game_id': 'BCUS98147', 'scope': 'STATIC_DRAFT_REVIEW_ONLY',
            'does_not_validate': ['speaker', 'message order', 'binary pointers',
                                  'glyph width', 'runtime rendering', 'playability'],
            'summary': {**dict(counts), 'total_issues': len(issues),
                        'issue_types': dict(sorted(types.items()))},
            'issues': issues}


def safe_output(path: Path) -> Path:
    dest = path.resolve()
    if not dest.is_relative_to((ROOT / 'local-data').resolve()) and not dest.is_relative_to((ROOT / 'dist').resolve()):
        raise ValueError('QA reports must stay in ignored local-data/ or dist/')
    return dest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT / 'translations')
    parser.add_argument('--out', type=Path,
                        default=ROOT / 'local-data' / 'dialogue-draft-qa.json')
    args = parser.parse_args()
    try:
        result = audit(args.root)
        dest = safe_output(args.out)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        parser.exit(1, f'QA refused: {exc}\n')
    print(f"Inspected {result['summary']['entries']} entries in "
          f"{result['summary']['catalogs']} catalogs")
    print('Review flags:', json.dumps(result['summary']['issue_types'], ensure_ascii=False))
    print('Report:', dest)
    print('Warnings are not automatic translation errors. No catalog/game files changed.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
