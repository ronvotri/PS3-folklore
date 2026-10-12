"""Read-only V4 control-byte aggregate from a PRIVATE local Folklore raw probe.

Reads ONLY candidate-gap byte windows of at most 8 bytes containing zeros and
low control codes. Outputs histogram data (decimal control IDs, no byte strings,
no original text/hex/windows, no original offsets), NOT opcode interpretations.
Python 3.10+; standard library; no game binary access or writes.
"""
from __future__ import annotations
from collections import Counter, defaultdict
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAX_GAP = 8


def private_path(path: Path) -> Path:
    p=path.resolve()
    if not p.is_relative_to((ROOT/'local-data').resolve()):
        raise ValueError('Private raw probe must be under the local-data directory')
    return p


def output_path(path: Path) -> Path:
    p=path.resolve()
    if not any(p.is_relative_to((ROOT/x).resolve()) for x in ('local-data','dist')):
        raise ValueError('Output must stay under ignored local-data/ or dist/')
    return p


def analyze(source: dict) -> dict:
    if (not isinstance(source,dict) or source.get('schema') != 1
        or source.get('game_id') != 'BCUS98147'
        or source.get('mode') != 'READ_ONLY_FORENSICS'
        or not isinstance(source.get('reports'),list)):
        raise ValueError('Expected Folklore private read-only probe data')
    data=[]
    for f in source['reports']:
        if not f['file'].startswith(('cmc/en/','talk/en/')):
            raise ValueError('Invalid file kind')
        samples=sorted(f['samples'],key=lambda x:x['file_offset'])
        code_freq=Counter()
        align_freq=Counter()
        pos_freq=Counter()
        gap_shape=Counter()
        eligible=0
        omitted=0
        for a,b in zip(samples,samples[1:]):
            if a['section'] != b['section']:
                continue
            left_end=a['nul_at'] + 1
            gap_len=b['file_offset']-left_end
            if gap_len < 0:
                raise ValueError('Overlapping candidate ranges')
            if gap_len == 0 or gap_len > MAX_GAP:
                omitted += 1
                continue
            window=bytes.fromhex(a['bytes_after_hex'])
            if len(window)<gap_len:
                omitted+=1
                continue
            gap=window[:gap_len]
            if any(x>=32 for x in gap):
                omitted+=1
                continue
            controls=[(i,x) for i,x in enumerate(gap) if x]
            if not controls:
                omitted+=1
                continue
            eligible+=1
            alignment=b['file_offset']%4
            align_freq[str(alignment)]+=1
            gap_shape[f'gap{gap_len}_controls{len(controls)}_nextmod{alignment}']+=1
            for i,x in controls:
                # Numbers 1..31 ONLY; no raw byte sequence, no source text.
                code_freq[str(x)]+=1
                pos_freq[f'value{x}_distance_before_next_text{gap_len-i}']+=1
        data.append({
            'file':f['file'], 'sampled_candidates':len(samples),
            'eligible_short_nontext_gaps':eligible,
            'other_pairs_not_classified':omitted,
            'control_value_histogram_decimal':dict(sorted(code_freq.items(),key=lambda kv:int(kv[0]))),
            'next_text_mod4_histogram':dict(sorted(align_freq.items())),
            'gap_shape_histogram':dict(sorted(gap_shape.items())),
            'control_value_distance_to_next_text_counts':dict(sorted(pos_freq.items()))
        })
    return {'schema':1,'game_id':'BCUS98147','kind':'REDACTED_AGGREGATE_CONTROL_STATS',
            'source_text_or_hex_windows_included':False,'contains_game_binary':False,
            'message_parser_proven':False,'repacker_available':False,
            'scope':'Aggregate counts of decimal nonprintable control values in short isolated gaps only; not proven opcodes.',
            'files':data}


def run(source:Path, dest:Path) -> dict:
    src=private_path(source)
    dst=output_path(dest)
    if src==dst:raise ValueError('Input and output must differ')
    report=analyze(json.loads(src.read_text(encoding='utf-8')))
    dst.parent.mkdir(parents=True,exist_ok=True)
    dst.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return report


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--in',dest='source',type=Path,default=ROOT/'local-data/dialogue-probe.json')
    parser.add_argument('--out',dest='target',type=Path,default=ROOT/'local-data/dialogue-control-stats.json')
    args=parser.parse_args()
    try:
        report=run(args.source,args.target)
    except (ValueError,TypeError,KeyError,OSError,json.JSONDecodeError) as exc:
        parser.exit(1,f'Diagnostic refused: {exc}\n')
    print(f'Finished, {len(report["files"])} files. No game, dialogue text, or hex copied.')
    print(f'Redacted aggregation: {args.target}')
    return 0

if __name__=='__main__':
    raise SystemExit(main())
