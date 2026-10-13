"""Encode responsive delivery assets; retain original screenshots and download files."""
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];DIST=ROOT/'dist'
for name in ['adjustments','masks','export-light']:
 source=DIST/f'assets/photocraft-{name}.jpg'
 with Image.open(source) as original:
  for width in [640,1280]:
   img=original.copy();img.thumbnail((width,10000),Image.Resampling.LANCZOS)
   target=DIST/f'assets/photocraft-{name}-{width}.webp';img.save(target,'WEBP',quality=82,method=6)
   print(target.name,original.size,'->',img.size,source.stat().st_size,'->',target.stat().st_size)
with Image.open(DIST/'photocraft-hero.webp') as original:
 img=original.copy();img.thumbnail((800,10000),Image.Resampling.LANCZOS)
 img.save(DIST/'assets/photocraft-hero-800.webp','WEBP',quality=82,method=6)
 print('hero 800:',(DIST/'assets/photocraft-hero-800.webp').stat().st_size)
