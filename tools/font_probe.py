"""Fetch the pinned open-source font and check Vietnamese glyph coverage.

Requires fonttools for checking only; this does not install a Windows font or
modify PS3 files. Downloaded fonts/reports belong in ignored local-data/.
"""
import argparse
import hashlib
import json
import unicodedata
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VIETNAMESE_LOWER = 'àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ'


def probe(font_path, choice):
    try:
        from fontTools.ttLib import TTFont
    except ImportError as exc:
        raise ValueError('Install optional fonttools dependency: python -m pip install fonttools') from exc
    raw = font_path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != choice['font_sha256']:
        raise ValueError('Font SHA-256 differs from the pinned source')
    letters = set(VIETNAMESE_LOWER + VIETNAMESE_LOWER.upper())
    marks = {c for c in unicodedata.normalize('NFD', ''.join(letters)) if unicodedata.combining(c)}
    ascii_printable = {chr(i) for i in range(32, 127)}
    required = letters | marks | ascii_printable | set('…“”‘’–—')
    with TTFont(font_path) as font:
        cmap = font.getBestCmap()
        missing = [c for c in sorted(required) if not cmap.get(ord(c)) or cmap.get(ord(c)) == '.notdef']
        axes = {a.axisTag: {'min': a.minValue, 'default': a.defaultValue, 'max': a.maxValue}
                for a in font['fvar'].axes} if 'fvar' in font else {}
    return {
        'family': choice['family'], 'weight': choice['weight'], 'sha256': digest,
        'precomposed_vietnamese_letters': len(letters), 'combining_marks': len(marks),
        'required_codepoints': len(required), 'missing': missing,
        'coverage_ok': not missing, 'variable_axes': axes,
        'scope': 'source_font_glyph_coverage_only; PS3 rendering is not yet verified'
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--font', type=Path, default=ROOT / 'local-data/fonts/Merienda-variable.ttf')
    parser.add_argument('--download', action='store_true')
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    choice = json.loads((ROOT / 'fonts/choice.json').read_text(encoding='utf-8'))
    try:
        if args.download:
            data = urllib.request.urlopen(choice['font_url'], timeout=30).read()
            if hashlib.sha256(data).hexdigest() != choice['font_sha256']:
                raise ValueError('Downloaded font does not match the pinned hash; existing file kept')
            args.font.parent.mkdir(parents=True, exist_ok=True)
            args.font.write_bytes(data)
        report = probe(args.font, choice)
        result = json.dumps(report, ensure_ascii=False, indent=2) + '\n'
        print(result)
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(result, encoding='utf-8')
        if not report['coverage_ok']:
            parser.exit(1, 'Font is missing required glyphs\n')
    except (OSError, ValueError) as exc:
        parser.exit(1, f'Error: {exc}\n')


if __name__ == '__main__':
    main()
