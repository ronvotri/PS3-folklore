"""Folklore BCUS98147 CMC000 ALPHA 0.1 -- TWO SAME-BYTE-LENGTH TEST LINES.

EXPERIMENTAL in-game visibility test, not a verified game dialogue serializer.
Requires a *test game copy*, RPCS3 closed, and Python 3.10+ (stdlib only).
Never changes offsets, frame controls, end NULs, CMC length or FHT. Saves a
FULL ORIGINAL CMC region for rollback before touching etc.bin_.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import struct
import sys
import unicodedata

GAME_ID = 'BCUS98147'
ARCHIVE_SIZE = 2498514097
CMC_NAME = 'cmc/en/LCmc000_en.bi5_'
CMC_SHA = '4af80f46f6521b69248d8c7d7cc0cad7d7223f8a8eb89126c0c0fca36c8569a0'
BACKUP_NAME = 'CMC000_original_BCUS98147.bin'
PATCHES = (
    (12780, 'Say something...', 'Lên tiếng đi!'),
)
# User-confirmed 25 aliases. Keep synchronized with repo fonts/aliases.json.
ALIAS_FILE = Path(__file__).resolve().parents[1] / 'fonts' / 'aliases.json'


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def encode_target(text: str, alias_path: Path = ALIAS_FILE) -> bytes:
    if not text or '\0' in text or unicodedata.normalize('NFC', text) != text:
        raise ValueError('Translation must be nonempty NFC text without NUL')
    obj = json.loads(alias_path.read_text(encoding='utf-8'))
    mapping = {x['vietnamese']: chr(int(x['slot'][2:], 16)) for x in obj['mapping']}
    if len(mapping) != 25 or len(set(mapping.values())) != 25:
        raise ValueError('Unsupported font alias mapping; expected Merienda V3 25 aliases')
    if any(c in mapping.values() for c in text):
        raise ValueError('Human translation contains reserved alias character')
    missing = [c for c in text if 0x1EA0 <= ord(c) <= 0x1EF9 and c not in mapping]
    if missing:
        raise ValueError('Translation requires additional font aliases: ' + ''.join(missing))
    return ''.join(mapping.get(c, c) for c in text).encode('utf-8')


def locate(root: Path) -> Path:
    """Find a unique etc.bin_/etc.fht_ pair in an extracted TEST game folder."""
    root = root.resolve()
    if not root.is_dir():
        raise ValueError('Game copy folder not found: ' + str(root))
    matches = []
    for base, dirs, files in os.walk(root, followlinks=False):
        folder = Path(base)
        depth = len(folder.relative_to(root).parts)
        dirs[:] = [] if depth >= 8 else [d for d in dirs if d not in {'.git', 'local-data','dist','PS3_UPDATE'} and not (folder/d).is_symlink()]
        if {'etc.bin_', 'etc.fht_'} <= set(files):
            matches.append(folder)
    if len(matches) != 1:
        raise ValueError(f'Expected one etc.bin_/etc.fht_ pair, found {len(matches)}. Pass --bin-dir instead.')
    return matches[0]


def index_entry(bin_dir: Path, archive_size: int) -> tuple[int, int]:
    raw = (bin_dir / 'etc.fht_').read_bytes()
    if len(raw) == 0 or len(raw) % 40:
        raise ValueError('Invalid FHT size')
    hits = []
    for i in range(0, len(raw), 40):
        rec = raw[i:i+40]
        name = rec[:32].split(b'\0', 1)[0].decode('ascii')
        length, offset = struct.unpack('>II', rec[32:])
        if name == CMC_NAME:
            if offset + length > archive_size or length < 0x100:
                raise ValueError('Invalid CMC000 entry bounds')
            hits.append((offset, length))
    if len(hits) != 1:
        raise ValueError('CMC000 must appear exactly once in FHT')
    return hits[0]


def build_trial(original: bytes, alias_file: Path = ALIAS_FILE) -> bytes:
    """Fail closed on original SHA and source bytes. Never shift NUL or offsets."""
    if sha(original) != CMC_SHA:
        raise ValueError('CMC000 SHA differs from ORIGINAL; refusing to build/apply')
    if len(original) < 0x38:
        raise ValueError('Original CMC header too short')
    declared, count = struct.unpack_from('>II', original)
    if declared != len(original) or not 1 <= count <= 64:
        raise ValueError('Original CMC header invalid')
    names = 0x30 + 4 * (count+1)
    edges = struct.unpack_from(f'>{count+1}I', original, 0x30)
    bounds = [(edges[i],edges[i+1]) for i in range(count)
              if original[names+i*24:names+(i+1)*24].split(b'\0',1)[0].startswith(b'talk')]
    if not bounds:
        raise ValueError('CMC000 has no talk section')
    work = bytearray(original)
    for pos, source, target in PATCHES:
        en = source.encode('ascii')
        vi = encode_target(target, alias_file)
        if len(vi) != len(en):
            raise ValueError(f'Not same byte length at {pos}: {len(en)} vs {len(vi)}')
        if pos % 4 or pos < 4 or not any(a <= pos-4 and pos + len(en) < b for a,b in bounds):
            raise ValueError('Target not at supported mod0 CMC frame inside talk section')
        if original[pos-4:pos-1] != b'\0\x04\0' or not (1 <= original[pos-1] <= 31):
            raise ValueError('Unrecognized CMC frame before target')
        if original[pos:pos+len(en)+1] != en + b'\0':
            raise ValueError('Original source bytes/NUL mismatch')
        work[pos:pos+len(en)] = vi
        if work[pos+len(en)] != 0 or work[pos-4:pos] != original[pos-4:pos]:
            raise ValueError('NUL terminator/control header changed')
    patched = bytes(work)
    if len(patched) != len(original):
        raise ValueError('CMC data length changed')
    allowed = {p for pos, src, _ in PATCHES for p in range(pos, pos+len(src))}
    if any((a != b and i not in allowed) for i,(a,b) in enumerate(zip(original,patched))):
        raise ValueError('Changed a byte outside approved text slots')
    return patched


def read_entry(bin_dir: Path) -> tuple[int,bytes]:
    archive = bin_dir / 'etc.bin_'
    if archive.stat().st_size != ARCHIVE_SIZE:
        raise ValueError('Archive size differs from BCUS98147 original baseline')
    offset, length = index_entry(bin_dir, ARCHIVE_SIZE)
    with archive.open('rb') as fh:
        fh.seek(offset)
        data = fh.read(length)
    if len(data) != length:
        raise ValueError('CMC000 read truncated')
    return offset, data


def original_backup(bin_dir: Path) -> Path:
    return bin_dir / 'Folklore-Alpha01-Backup' / BACKUP_NAME


def _ensure_game_not_running():
    if sys.platform == 'win32':
        import subprocess
        cp = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq rpcs3.exe', '/FO', 'CSV', '/NH'],
                            capture_output=True, text=True, timeout=10, check=False)
        if cp.returncode == 0 and 'rpcs3.exe' in cp.stdout.lower():
            raise ValueError('Close RPCS3 before applying/restoring patch')


def action(bin_dir: Path, mode: str) -> dict:
    bin_dir = bin_dir.resolve()
    _ensure_game_not_running()
    offset, current = read_entry(bin_dir)
    backup = original_backup(bin_dir)
    if mode == 'restore':
        if not backup.is_file():
            raise ValueError('No Alpha01 backup; refusing to restore unknown game data')
        original = backup.read_bytes()
        if sha(original) != CMC_SHA or len(original) != len(current):
            raise ValueError('Backup not the validated original CMC000')
        wanted = build_trial(original)
        if current != wanted:
            raise ValueError('CMC000 is not the matching Alpha01 patch; refusing restore')
        write_verified(bin_dir/'etc.bin_', offset, current, original)
        return {'mode':'restored', 'archive_modified':True, 'backup':str(backup)}
    if mode not in ('check','apply'):
        raise ValueError('Unsupported action')
    if sha(current) != CMC_SHA:
        if backup.is_file() and sha(backup.read_bytes()) == CMC_SHA:
            old = backup.read_bytes()
            if current == build_trial(old):
                raise ValueError('Alpha01 is already installed; use restore or test the game')
        raise ValueError('CMC000 is not original (perhaps already patched); no changes')
    desired = build_trial(current)
    if mode == 'check':
        return {'mode':'ready', 'archive_modified':False, 'lines':len(PATCHES),
                'original_cmc_sha256':CMC_SHA, 'new_cmc_sha256':sha(desired)}
    if backup.exists():
        if sha(backup.read_bytes()) != CMC_SHA:
            raise ValueError('Existing backup conflicts with original; refusing')
    else:
        backup.parent.mkdir(parents=True, exist_ok=True)
        # Exclusive-create; flush before any write to archive.
        with backup.open('xb') as fh:
            fh.write(current)
            fh.flush()
            os.fsync(fh.fileno())
    if backup.read_bytes() != current:
        raise ValueError('Backup does not exactly match original; refusing')
    write_verified(bin_dir/'etc.bin_', offset, current, desired)
    return {'mode':'installed', 'archive_modified':True, 'lines':len(PATCHES),
            'backup':str(backup), 'new_cmc_sha256':sha(desired)}


def write_verified(archive: Path, offset: int, old: bytes, new: bytes) -> None:
    """One-region write; on an ordinary failure restore original region."""
    if len(old) != len(new):
        raise ValueError('Unsafe write: region size changed')
    with archive.open('r+b') as fh:
        fh.seek(offset)
        if fh.read(len(old)) != old:
            raise ValueError('Target changed between preflight and write')
        try:
            # Smallest modification footprint: ONLY changed byte ranges.
            changes = [(a,b) for a,b in _changed_runs(old,new)]
            for start,end in changes:
                fh.seek(offset+start)
                fh.write(new[start:end])
            fh.flush()
            os.fsync(fh.fileno())
            fh.seek(offset)
            if fh.read(len(old)) != new:
                raise ValueError('Post-write CMC validation failed')
        except Exception:
            # On an ordinary write failure restore all changed byte ranges.
            for start,end in _changed_runs(old,new):
                fh.seek(offset+start)
                fh.write(old[start:end])
            fh.flush()
            os.fsync(fh.fileno())
            raise


def _changed_runs(a: bytes,b: bytes):
    start = None
    for i,(x,y) in enumerate(zip(a,b)):
        if x != y and start is None:
            start = i
        elif x == y and start is not None:
            yield start,i
            start = None
    if start is not None:
        yield start,len(a)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    group=p.add_mutually_exclusive_group(required=True)
    group.add_argument('--game-root',type=Path)
    group.add_argument('--bin-dir',type=Path)
    p.add_argument('--action',choices=['check','apply','restore'],default='check')
    args=p.parse_args()
    try:
        bin_dir = locate(args.game_root) if args.game_root else args.bin_dir
        result=action(bin_dir,args.action)
    except (ValueError,OSError,UnicodeError,KeyError,struct.error) as exc:
        print('ALPHA01 REFUSED:',exc,file=sys.stderr)
        return 1
    print('RESULT:',json.dumps(result,ensure_ascii=False,indent=2))
    print('Only two CMC000 text byte ranges may be changed. Test RPCS3 separately.')
    return 0


if __name__=='__main__':
    raise SystemExit(main())
