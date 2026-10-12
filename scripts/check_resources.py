"""Validate published downloads against the catalog and generated source composites."""
from pathlib import Path
import hashlib,json,zipfile
from PIL import Image
from psd_tools import PSDImage
import numpy as np
ROOT=Path(__file__).resolve().parents[1];dist=ROOT/'dist';catalog=json.loads((ROOT/'content/resources.json').read_text())
assert len(catalog)==14
for item in catalog:
 for d in item['downloads']:
  p=dist/d['url'].lstrip('/');assert p.stat().st_size==d['bytes'];assert hashlib.sha256(p.read_bytes()).hexdigest()==d['sha256']
 if item['kind']=='template':
  path=dist/'downloads'/item['id'];psd=PSDImage.open(path.with_suffix('.psd'));png=Image.open(path.with_suffix('.png')).convert('RGB')
  assert psd.size==png.size==(item['width'],item['height']);assert len(psd)==item['layers']
  assert any(l.name=='Sample lettering - hide and replace' for l in psd)
  assert np.abs(np.asarray(psd.composite().convert('RGB')).astype(int)-np.asarray(png).astype(int)).max()<=2
 if item['kind']=='lut':
  lines=(dist/'downloads'/(item['id']+'.cube')).read_text().splitlines();assert 'LUT_3D_SIZE 17' in lines
  values=[list(map(float,l.split())) for l in lines if l and l[0].isdigit()]
  assert len(values)==17**3 and all(len(v)==3 and all(0<=x<=1 for x in v) for v in values)
for p in (dist/'downloads').glob('*.png'):
 with Image.open(p) as im:im.verify()
for p in (dist/'downloads').glob('*.zip'):
 with zipfile.ZipFile(p) as z:
  assert z.testzip() is None;assert 'LICENSE.txt' in z.namelist() and 'README.txt' in z.namelist()
  assert all(not n.startswith('/') and '..' not in Path(n).parts for n in z.namelist())
print('PASS: 14 assets; PSD layers/composites, PNG decoding, LUT size/range, ZIP integrity and catalog hashes.')
