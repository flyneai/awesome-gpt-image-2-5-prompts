#!/usr/bin/env python3
"""Optional: rebuild committed previews with Pillow 12.3.0; originals are untouched."""
import hashlib, json
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
rows=[]
for a in json.loads((ROOT/'assets/manifest.json').read_text())['assets']:
    source=ROOT/a['path']; target=ROOT/'assets/previews'/source.with_suffix('.jpg').name
    target.parent.mkdir(exist_ok=True)
    with Image.open(source) as im:
        im.thumbnail((720,720),Image.Resampling.LANCZOS)
        rgba=im.convert('RGBA'); bg=Image.new('RGB',im.size,'white'); bg.paste(rgba,mask=rgba.getchannel('A'))
        bg.save(target,quality=76,optimize=True,progressive=True)
        rows.append(dict(source=a['path'],source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),path=str(target.relative_to(ROOT)),sha256=hashlib.sha256(target.read_bytes()).hexdigest(),bytes=target.stat().st_size,width=bg.width,height=bg.height))
(ROOT/'assets/previews.json').write_text(json.dumps({'max_edge':720,'format':'JPEG; white background for preview only','previews':rows},indent=2)+'\n')
print(f'Built {len(rows)} previews: {sum(r["bytes"] for r in rows):,} bytes')
