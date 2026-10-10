"""Rebuild the locally tested Merienda V3 atlas from verified originals.
Optional dependencies: Pillow 12.3.0 and fonttools. No game bytes included.
Adding text can change the common baseline: inspect preview and retest locally.
"""
import argparse,hashlib,io,json,math,struct
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import text_codec
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--original',type=Path,required=True)
p.add_argument('--ttf',type=Path,default=ROOT/'local-data/fonts/Merienda-variable.ttf')
p.add_argument('--texts',type=Path,default=ROOT/'translations/menu_vi.json')
p.add_argument('--out',type=Path,required=True)
args=p.parse_args()
tr=json.loads(args.texts.read_text(encoding='utf-8-sig'))
choice=json.loads((ROOT/'fonts/choice.json').read_text(encoding='utf-8'))
if hashlib.sha256(args.ttf.read_bytes()).hexdigest()!=choice['font_sha256']:raise ValueError('Pinned Merienda font required')
accepted_hashes={r['original_sha256'] for r in json.loads((ROOT/'docs/font_baseline.json').read_text(encoding='utf-8'))['files']}
orig=args.original.read_bytes()
if hashlib.sha256(orig).hexdigest() not in accepted_hashes:raise ValueError('Expected supported ORIGINAL font file')
dds=orig[0x80260:0x1002e0];head=b''.join(dds[i:i+4][::-1] for i in range(0,128,4))
old_atlas=Image.open(io.BytesIO(head+dds[128:])).convert('RGB')
old={cp:struct.unpack_from('>4H',orig,0x1e0+cp*8) for cp in range(65536)}
codes=set(cp for cp,v in old.items() if v[1]!=0xfc00)|{ord(c) for v in tr.values() for c in v if c not in '\n\r\t'}
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
source_font=TTFont(args.ttf)
static_font=instantiateVariableFont(source_font,{'wght':400},inplace=False)
static_bytes=io.BytesIO();static_font.save(static_bytes);static_bytes.seek(0)
font=ImageFont.truetype(static_bytes,27)
from fontTools.ttLib import TTFont
cmap=TTFont(args.ttf).getBestCmap()
boxes={cp:font.getbbox(chr(cp),anchor='ls') for cp in codes if cp in cmap}
top=min(v[1] for v in boxes.values());bottom=max(v[3] for v in boxes.values());height=bottom-top
atlas=Image.new('RGB',(1024,1024));table=bytearray(orig[0x1e0:0x801e0]);x=y=0
coords={}
for cp in sorted(codes):
    if cp in boxes:
        left,t,right,b=boxes[cp];width=max(2,math.ceil(max(font.getlength(chr(cp)),right)-min(0,left))+2)
        tile=Image.new('RGB',(width,height));ImageDraw.Draw(tile).text((1-min(0,left),-top),chr(cp),font=font,fill='white',anchor='ls')
        if height>34:tile=tile.resize((width,34),Image.Resampling.LANCZOS)
        glyph=Image.new('RGB',(width,36));glyph.paste(tile,(0,1))
    else:
        ox,oy,width,_=old[cp];glyph=old_atlas.crop((ox,oy,ox+width,oy+36))
    if cp in boxes:
        # The engine takes lookup width as both crop width and pen advance.
        # Remove TTF side bearings already represented by the bitmap margins.
        # Use a modest word gap; runtime confirmation comes from user screenshots.
        if cp==32:
            width=5;glyph=Image.new('RGB',(width,36))
        else:
            ink=glyph.convert('L').point(lambda value:255 if value>=16 else 0).getbbox()
            if ink:
                width=ink[2]-ink[0]+2
                tight=Image.new('RGB',(width,36))
                tight.paste(glyph.crop((ink[0],0,ink[2],36)),(1,0));glyph=tight
    if x+width>1024:x=0;y+=37
    assert y+36<=1024
    atlas.paste(glyph,(x,y));struct.pack_into('>4H',table,cp*8,x,y,width,0);coords[cp]=(x,y,width)
    x+=width+1
buf=io.BytesIO();atlas.save(buf,format='DDS',pixel_format='DXT1');payload=buf.getvalue()[128:]
assert len(payload)==len(dds)-128
fontdata=bytearray(orig);fontdata[0x1e0:0x801e0]=table;fontdata[0x802e0:0x1002e0]=payload
assert fontdata[0x1002e0:]==orig[0x1002e0:]
modified=text_codec.alias_font(bytes(fontdata))
args.out.parent.mkdir(parents=True,exist_ok=True)
args.out.write_bytes(modified)
atlas.save(args.out.with_suffix('.atlas.png'))
print(f'Built {len(codes)} glyphs, extent {height}, SHA256 {hashlib.sha256(modified).hexdigest()}')
