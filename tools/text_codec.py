"""Font V3 aliases: human translations stay NFC; only game payloads use aliases."""
import json
import struct
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load_mapping(path=None):
    spec=json.loads(Path(path or ROOT/'fonts/aliases.json').read_text(encoding='utf-8'))
    mapping={r['vietnamese']:chr(int(r['slot'][2:],16)) for r in spec['mapping']}
    if len(set(mapping.values()))!=len(mapping):raise ValueError('Duplicate alias slots')
    for source,target in mapping.items():
        if not (len(source)==1 and 0x1ea0<=ord(source)<=0x1ef9 and 0x500<=ord(target)<0x580):
            raise ValueError('Unexpected alias character')
    return mapping

def encode_text(text,mapping=None):
    mapping=load_mapping() if mapping is None else mapping
    text=unicodedata.normalize('NFC',text)
    if '\0' in text:raise ValueError('NUL in translation')
    missing={c for c in text if 0x1ea0<=ord(c)<=0x1ef9 and c not in mapping}
    if missing:raise ValueError('Font alias extension required: '+', '.join(sorted(missing)))
    if any(c in mapping.values() for c in text):raise ValueError('Translation contains reserved alias slot')
    return ''.join(mapping.get(c,c) for c in text).encode('utf-8')

def decode_text(payload,mapping=None):
    mapping=load_mapping() if mapping is None else mapping
    reverse={v:k for k,v in mapping.items()}
    return ''.join(reverse.get(c,c) for c in payload.decode('utf-8'))

def alias_font(data,mapping=None):
    mapping=load_mapping() if mapping is None else mapping
    if len(data)!=1311584 or struct.unpack_from('>I',data,4)[0]!=15:
        raise ValueError('Unsupported BCUS98147 font layout')
    result=bytearray(data)
    for source,target in mapping.items():
        src=0x1e0+ord(source)*8;dst=0x1e0+ord(target)*8
        glyph=data[src:src+8]
        x,y,width,face=struct.unpack('>4H',glyph)
        if y==0xfc00 or not width or x+width>1024 or y+36>1024 or face!=0:
            raise ValueError('Missing or invalid Vietnamese source glyph: '+source)
        if data[dst:dst+8] not in (struct.pack('>4H',0,0xfc00,0,0),glyph):
            raise ValueError('Occupied alias slot')
        result[dst:dst+8]=glyph
    return bytes(result)
