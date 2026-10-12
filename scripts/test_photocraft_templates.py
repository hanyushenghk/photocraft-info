"""Integration checks; requires official photocraft-cli and requirements-resources.txt.
Reference diffs for CMYK are not color-managed proofs. Never modifies downloads.
"""
import json, pathlib, zipfile, subprocess, hashlib, time
import numpy as np
from PIL import Image
from psd_tools import PSDImage
import argparse
parser=argparse.ArgumentParser(description="Test all downloaded PSD templates using the official PhotoCraft CLI.")
parser.add_argument('--cli',required=True)
parser.add_argument('--out',required=True,help='New output directory outside the repository')
args=parser.parse_args()
ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=pathlib.Path(args.out).resolve();OUT.mkdir(parents=True,exist_ok=False)
CLI=str(pathlib.Path(args.cli).resolve())
items=[x for x in json.loads((ROOT/'content/resources.json').read_text()) if x['kind']=='template']+json.loads((ROOT/'content/third-party-resources.json').read_text())
def flat(ls):
 return [y for x in ls for y in [x,*flat(x.get('children',[]))]]
def run(args,prefix):
 start=time.time()
 try:
  r=subprocess.run([CLI,*map(str,args)],capture_output=True,text=True,timeout=120)
  res={'exit_code':r.returncode,'seconds':round(time.time()-start,3),'stderr':r.stderr}
  (prefix.with_suffix('.stdout.txt')).write_text(r.stdout);(prefix.with_suffix('.stderr.txt')).write_text(r.stderr)
  return res,r.stdout
 except subprocess.TimeoutExpired:
  return {'exit_code':124,'error':'120 second timeout'},''
def diff(a,b):
 a=np.asarray(a.convert('RGB')).astype(np.int16);b=np.asarray(b.convert('RGB')).astype(np.int16)
 if a.shape!=b.shape:return {'size_mismatch':True}
 d=np.abs(a-b);return {'mean_abs_8bit':round(float(d.mean()),4),'max_abs_8bit':int(d.max()),'pixels_delta_gt_10_pct':round(float((d.max(axis=2)>10).mean()*100),4)}
results=json.loads((OUT/"results.json").read_text()) if (OUT/"results.json").exists() else []
for item in items:
 id=item['id']
 if any(r['id']==id for r in results):continue
 d=OUT/id;d.mkdir(exist_ok=True)
 if id.startswith('external-'):
  z=zipfile.ZipFile(ROOT/'dist'/item['downloads'][0]['url'].lstrip('/'))
  src=d/'input.psd';src.write_bytes(z.read(next(n for n in z.namelist() if n.lower().endswith('.psd'))))
 else:src=ROOT/'dist/downloads'/f'{id}.psd'
 rec={'id':id,'title':item['title'],'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'tests':{}}
 t,s=run(['info',src,'--compact'],d/'info');rec['tests']['open']=t
 if t['exit_code']!=0:results.append(rec);continue
 info=json.loads(s);(d/'info.json').write_text(json.dumps(info,indent=2));layers=flat(info['layers']);types=[x for x in layers if x['kind']=='Type']
 rec.update(width=info['width'],height=info['height'],mode=info['mode'],layer_count=len(layers),text_layer_count=len(types),warnings=info['warnings'],expected_layer_count=item['layers'])
 ref=PSDImage.open(src).topil().convert('RGB');ref.save(d/'reference.png')
 t,_=run(['convert',src,d/'render.png'],d/'render');rec['tests']['png_export']=t
 if t['exit_code']==0:rec['reference_diff']=diff(ref,Image.open(d/'render.png'))
 for ext in ['psd','pcraft']:
  t,_=run(['convert',src,d/f'roundtrip.{ext}'],d/f'save-{ext}');rec['tests'][f'save_{ext}']=t
  if t['exit_code']==0:
   t,s=run(['info',d/f'roundtrip.{ext}','--compact'],d/f'reopen-{ext}');rec['tests'][f'reopen_{ext}']=t
   if t['exit_code']==0:
    ri=json.loads(s);rl=flat(ri['layers']);t.update(layer_count=len(rl),text_layer_count=sum(x['kind']=='Type' for x in rl),dimensions_match=(ri['width'],ri['height'])==(info['width'],info['height']),layer_names_match=[x['name'] for x in layers]==[x['name'] for x in rl])
   t,_=run(['convert',d/f'roundtrip.{ext}',d/f'roundtrip-{ext}.png'],d/f'render-{ext}');rec['tests'][f'roundtrip_render_{ext}']=t
   if t['exit_code']==0 and (d/'render.png').exists():t['diff_from_first_render']=diff(Image.open(d/'render.png'),Image.open(d/f'roundtrip-{ext}.png'))
 target=types[0] if types else layers[0]
 cmd='type.edit' if types else 'layer.setProps'
 params={'layer':target['id'],'text':'PhotoCraft template test'} if types else {'layer':target['id'],'visible':False}
 t,s=run(['run',src,'--cmd',cmd,'--params',json.dumps(params),'--out',d/'edited.pcraft'],d/'edit');rec['tests']['edit']=t;t['command']=cmd
 if t['exit_code']==0:
  t,s=run(['info',d/'edited.pcraft','--compact'],d/'edited-info');rec['tests']['edit_reopen']=t
  if t['exit_code']==0:
   el=flat(json.loads(s)['layers']);matches=[x for x in el if x['id']==target['id']];t['change_persisted']=bool(matches and (matches[0].get('text',{}).get('text')=='PhotoCraft template test' if types else matches[0]['visible']==False))
 t,_=run(['convert',d/'edited.pcraft',d/'edited.png'],d/'edited-render');rec['tests']['edited_render']=t
 if t['exit_code']==0:
  a=np.asarray(Image.open(d/'render.png').convert('RGB'));b=np.asarray(Image.open(d/'edited.png').convert('RGB'));t['changed_pixels']=int(np.any(a!=b,axis=2).sum())
 results.append(rec);(OUT/'results.json').write_text(json.dumps(results,indent=2));print(id,rec.get('reference_diff'), 'warnings',len(rec['warnings']),flush=True)
print('DONE',len(results),flush=True)
