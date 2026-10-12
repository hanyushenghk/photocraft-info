"""Generate original downloadable assets. Requires Pillow, numpy and psd-tools."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from psd_tools import PSDImage
from psd_tools.api.layers import PixelLayer
from psd_tools.constants import Compression
import numpy as np
import json,zipfile,hashlib,html,io
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'dist/downloads';PRE=ROOT/'dist/assets/resources'
OUT.mkdir(exist_ok=True);PRE.mkdir(exist_ok=True)
LICENSE='''PhotoCraft Resource Hub — Original Starter Assets, version 1.0 (2026-10-12)

Permission is granted to use, copy, modify and redistribute these original layouts,
geometric graphics, textures and LUT files for personal and commercial projects,
including client work and finished products. Attribution is appreciated, not required.
No third-party photographs or font files are included. This permission applies only
to files in this pack, not to linked external resources or third-party software.
Assets are provided as-is, without warranty. Do not imply endorsement by ArtCraft,
Adobe or the creators of PhotoCraft. This is an independent resource collection.

本站原创资源：允许个人与商业使用、修改、再分发及客户项目使用，无需署名。
不包含第三方照片或字体文件。本授权不适用于外部链接的素材或第三方软件。
按现状提供，不作兼容性保证；请勿暗示获得 ArtCraft 或 Adobe 官方背书。
'''
(OUT/'LICENSE.txt').write_text(LICENSE)
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
items=[];sheet=[]
def zipwrite(path,files):
 with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for name,data in files.items():
   info=zipfile.ZipInfo(name,date_time=(2026,10,12,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
   z.writestr(info,data.encode() if isinstance(data,str) else data)
def metadata(id,kind,names,descs,w,h,files,extra):
 entry=dict(id=id,kind=kind,title=dict(zip(['en','zh'],names)),description=dict(zip(['en','zh'],descs)),width=w,height=h,preview=f'/assets/resources/{id}.webp',downloads=[] ,**extra)
 for label,file in files:
  p=OUT/file;entry['downloads'].append(dict(label=label,url='/downloads/'+file,bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
 items.append(entry)
def preview(im,id):
 im=im.convert('RGB');im.thumbnail((760,760));im.save(PRE/(id+'.webp'),quality=86)
 thumb=Image.new('RGB',(340,270),'#edece5');p=im.copy();p.thumbnail((320,240));thumb.paste(p,((340-p.width)//2,(250-p.height)//2));ImageDraw.Draw(thumb).text((10,251),id,fill='#252723',font=ImageFont.truetype(FONT,12));sheet.append(thumb)
class Canvas:
 def __init__(self,w,h,bg):
  self.w=w;self.h=h;self.layers=[];self.svg=[];self.layer('Background');self.rect((0,0,w,h),bg)
 def layer(self,name):
  self.layers.append((name,Image.new('RGBA',(self.w,self.h))));self.d=ImageDraw.Draw(self.layers[-1][1])
 def rect(self,b,c,r=0):
  (self.d.rounded_rectangle if r else self.d.rectangle)(b,**({'radius':r} if r else {}),fill=c)
  x,y,x2,y2=b;self.svg.append(f'<rect x="{x}" y="{y}" width="{x2-x}" height="{y2-y}" rx="{r}" fill="{c}"/>')
 def ellipse(self,b,c):
  self.d.ellipse(b,fill=c);x,y,x2,y2=b;self.svg.append(f'<ellipse cx="{(x+x2)/2}" cy="{(y+y2)/2}" rx="{(x2-x)/2}" ry="{(y2-y)/2}" fill="{c}"/>')
 def text(self,x,y,t,size,c,bold=False):
  f=ImageFont.truetype(BOLD if bold else FONT,size);self.d.text((x,y),t,font=f,fill=c,anchor='lt')
  # SVG is an optional vector source, not a claim of native PhotoCraft SVG support.
  self.svg.append(f'<text x="{x}" y="{y+size*.78}" font-family="DejaVu Sans, sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" fill="{c}">{html.escape(t)}</text>')
 def export(self,id,names,descs):
  psd=PSDImage.new('RGBA',(self.w,self.h));flat=Image.new('RGBA',(self.w,self.h))
  for name,im in self.layers:
   box=im.getbbox()
   if box: PixelLayer.frompil(im.crop(box),psd,name=name,left=box[0],top=box[1],compression=Compression.RLE)
   flat=Image.alpha_composite(flat,im)
  p=OUT/(id+'.psd');psd._record.image_data.compression=Compression.RLE;psd.save(p)
  flat.convert('RGB').save(OUT/(id+'.png'),optimize=True)
  svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}">'+''.join(self.svg)+'</svg>'
  (OUT/(id+'.svg')).write_text(svg)
  readme=f'''{names[0]} / {names[1]}
{self.w} × {self.h} pixels · RGB 8-bit · {len(psd)} pixel layers

1. Open the PSD in PhotoCraft using File > Open.
2. Background, decoration, placeholder and sample lettering are separate pixel layers.
3. To change words, hide the layer named "Sample lettering - hide and replace" and
   add your own text with the Type tool. PSD sample lettering is rasterized, NOT live text.
4. Replace the decorative image/shape placeholder with your own image on a new layer.
5. Save a copy, reopen it, then export PNG or JPEG. PNG is a ready-to-use flattened image.
6. Optional SVG source keeps text elements editable in a vector editor. Font substitution
   can alter layout; SVG support in PhotoCraft is not asserted. No font files are included.

Checks: PSD decoded and layers/composite checked with psd-tools; PNG decoded with Pillow.
Not tested inside the PhotoCraft desktop app. No smart objects or live text are promised.

使用：在 PhotoCraft 打开 PSD。背景、装饰、占位图和示例文字各自分层。
修改文字时隐藏“Sample lettering - hide and replace”图层，再用文字工具输入。
PSD 示例文字是像素图层，不是可直接编辑的文字图层。PNG 为可直接使用的平面图。
SVG 为可选矢量源文件，可在矢量编辑器中修改文字，本站不宣称 PhotoCraft 支持 SVG。
检查：已用程序读取 PSD 图层与合成图、解码 PNG；尚未在 PhotoCraft 应用内实测。
请阅读 LICENSE.txt。
'''
  zipwrite(OUT/(id+'.zip'),{id+'.psd':p.read_bytes(),id+'.png':(OUT/(id+'.png')).read_bytes(),id+'.svg':svg,'README.txt':readme,'LICENSE.txt':LICENSE})
  preview(flat,id)
  # Verify file structure and rendered output against the source composition.
  reopened=PSDImage.open(p);assert len(reopened)==len(psd)
  actual=np.asarray(reopened.composite().convert('RGB')).astype(int);expected=np.asarray(flat.convert('RGB')).astype(int)
  assert np.abs(actual-expected).max()<=2,(id,np.abs(actual-expected).max())
  with Image.open(OUT/(id+'.png')) as test: test.verify()
  metadata(id,'template',names,descs,self.w,self.h,[('ZIP',id+'.zip'),('PSD',id+'.psd'),('PNG',id+'.png')],dict(layers=len(psd),format='PSD + PNG + SVG'))
# Original composition 1: square editorial launch.
c=Canvas(1080,1080,'#f3eee4');c.layer('Decorative shapes');c.ellipse((635,50,1160,575),'#e97846');c.rect((635,565,1010,950),'#273f36',26);c.ellipse((740,680,925,865),'#d5e0bd');c.layer('Layout rules');c.rect((70,920,560,924),'#293e35');c.layer('Sample lettering - hide and replace');c.text(70,70,'STUDIO / 001',23,'#293e35');c.text(70,230,'A fresh',91,'#293e35',True);c.text(70,344,'perspective.',78,'#293e35',True);c.text(74,520,'MAKE ROOM FOR YOUR NEXT IDEA.',20,'#53614f');c.text(74,962,'YOUR BRAND',22,'#293e35',True);c.export('social-launch',('Fresh Perspective · Social Post','全新视角 · 社交帖子'),('An editorial square with separate color blocks and a generous headline area.','编辑风格方形版式，独立色块与宽敞标题区域。'))
# 2: video cover.
c=Canvas(1280,720,'#203b32');c.layer('Image placeholder');c.rect((810,72,1200,650),'#d6dfbb',30);c.ellipse((870,130,1160,420),'#e98753');c.rect((862,468,1144,492),'#203b32');c.rect((862,528,1080,544),'#536e4e');c.layer('Accent');c.rect((70,72,248,112),'#d6dfbb',20);c.layer('Sample lettering - hide and replace');c.text(91,82,'THE CREATIVE EDIT',13,'#203b32',True);c.text(70,183,'MAKE',114,'#f5f0e6',True);c.text(70,319,'SOMETHING',87,'#f5f0e6',True);c.text(70,430,'GREAT.',114,'#f5f0e6',True);c.text(75,634,'YOUR CHANNEL  /  NEW EPISODE',20,'#d6dfbb');c.export('video-cover',('The Creative Edit · Video Cover','创意时刻 · 视频封面'),('A bold 16:9 thumbnail with a replaceable illustration panel.','醒目的 16:9 视频缩略图，带可替换插图区域。'))
# 3: vertical story.
c=Canvas(1080,1920,'#e9eedc');c.layer('Decorative panels');c.rect((64,760,1016,1590),'#284339',36);c.ellipse((245,866,835,1456),'#e58453');c.ellipse((397,1018,683,1304),'#e9eedc');c.rect((64,1660,1016,1790),'#284339',65);c.layer('Sample lettering - hide and replace');c.text(70,140,'A LITTLE INSPIRATION',24,'#284339');c.text(64,280,'YOUR NEXT',115,'#284339',True);c.text(64,430,'CHAPTER.',132,'#284339',True);c.text(70,628,'Start with one good idea.',38,'#65725d');c.text(312,1701,'EXPLORE MORE',34,'#e9eedc',True);c.export('vertical-story',('Next Chapter · Story','下一章 · 竖版故事'),('A 9:16 vertical layout with a large art panel and call-to-action area.','9:16 竖版布局，大幅视觉区与行动按钮区域。'))
# 4: square product image with geometric mock product.
c=Canvas(1200,1200,'#efebe5');c.layer('Product placeholder - replace with your photo');c.ellipse((285,962,945,1047),'#d0c5b9');c.rect((370,486,830,998),'#b6c4a6',56);c.rect((448,416,752,502),'#2e4238',12);c.rect((412,632,788,830),'#f6f0e6',8);c.layer('Accent');c.ellipse((920,130,1080,290),'#df7950');c.layer('Sample lettering - hide and replace');c.text(75,74,'THE DAILY COLLECTION',22,'#2e4238');c.text(75,170,'Everyday',88,'#2e4238',True);c.text(75,279,'essentials.',88,'#2e4238',True);c.text(465,701,'YOUR LABEL',27,'#2e4238',True);c.text(75,1090,'Thoughtfully made. Simply yours.',27,'#586150');c.export('product-square',('Everyday Essentials · Product','日常精选 · 产品主图'),('A clean product layout with a separate geometric bottle placeholder.','简洁产品版式，附独立几何瓶身占位图层。'))
# 5: wide banner.
c=Canvas(1600,600,'#213545');c.layer('Decorative geometry');c.ellipse((1030,-100,1690,560),'#ec8657');c.ellipse((1190,60,1530,400),'#213545');c.rect((1080,455,1520,520),'#d8e1bf',32);c.layer('Sample lettering - hide and replace');c.text(68,58,'YOUR STUDIO',19,'#d8e1bf',True);c.text(64,151,'Ideas into',97,'#f4f0e7',True);c.text(64,272,'impact.',115,'#f4f0e7',True);c.text(70,457,'Design a better first impression.',25,'#d8e1bf');c.export('website-banner',('Ideas Into Impact · Banner','创意成效 · 网站横幅'),('A panoramic hero banner for a studio, business or portfolio.','适合工作室、企业与作品集的宽幅首屏横幅。'))
# 6: event poster.
c=Canvas(1080,1350,'#edc760');c.layer('Decorative geometry');c.ellipse((62,560,525,1023),'#243a31');c.ellipse((554,560,1017,1023),'#f5edd6');c.rect((0,1090,1080,1350),'#243a31');c.layer('Sample lettering - hide and replace');c.text(65,68,'AN OPEN INVITATION',23,'#243a31');c.text(58,193,'CREATIVE',130,'#243a31',True);c.text(58,349,'SESSION',130,'#243a31',True);c.text(64,1140,'YOUR DATE  /  YOUR VENUE',33,'#f5edd6',True);c.text(64,1227,'Ideas. Conversation. New possibilities.',24,'#f5edd6');c.export('creative-poster',('Creative Session · Poster','创意聚会 · 活动海报'),('A 4:5 event poster with clear type hierarchy and a separate footer.','4:5 活动海报，清晰标题层级与独立底栏。'))
# Four deterministic original texture tiles. Geometric patterns are edge-periodic.
for id,names in [('linen-grid',('Linen Grid','亚麻网格')),('paper-grain',('Warm Paper','暖色纸纹')),('dot-matrix',('Dot Matrix','点阵纹理')),('diagonal-lines',('Diagonal Lines','斜线纹理'))]:
 n=1024;y,x=np.mgrid[:n,:n]
 if id=='linen-grid':
  v=232+5*np.sin(2*np.pi*x/8)+5*np.sin(2*np.pi*y/8);arr=np.stack([v+6,v+3,v-8],-1)
 elif id=='paper-grain':
  rng=np.random.default_rng(42);v=238+rng.normal(0,2.2,(n,n));arr=np.stack([v+4,v,v-12],-1)
 elif id=='dot-matrix':
  v=np.where(((x%32)-16)**2+((y%32)-16)**2<10,194,245);arr=np.stack([v,v,v-8],-1)
 else:
  v=np.where((x+y)%48<3,208,244);arr=np.stack([v,v+2,v-2],-1)
 im=Image.fromarray(np.clip(arr,0,255).astype('uint8'),'RGB');im.save(OUT/(id+'.png'),optimize=True);preview(im,id)
 metadata(id,'texture',names,('Original 1024 px background. Import as an image layer and adjust opacity.','原创 1024 像素背景，导入为图像图层后调整不透明度。'),1024,1024,[('PNG',id+'.png')],dict(format='PNG'))
# Original display-referred creative LUTs: 17^3 points, red changes fastest.
# Preview uses a generated color chart, not a photograph or PhotoCraft screenshot.
luts=[('warm-editorial',('Warm Editorial','暖调编辑')),('cool-slate',('Cool Slate','冷调青灰')),('soft-matte',('Soft Matte','柔和哑光')),('mono-contrast',('Monochrome Contrast','黑白对比'))]
def transform(a,id):
 lum=a@np.array([.2126,.7152,.0722]);l=lum[...,None]
 if id=='warm-editorial':b=(a-l)*.92+l;b=b*np.array([1.035,1.0,.955])+np.array([.012,.002,0])
 elif id=='cool-slate':b=(a-l)*.83+l;b=b*np.array([.955,1.0,1.035])+np.array([0,.008,.017])
 elif id=='soft-matte':b=(a-l)*.85+l;b=b*.88+.06
 else:b=np.repeat(np.clip((l-.5)*1.12+.5,0,1),3,-1)
 return np.clip(b,0,1)
for id,names in luts:
 lines=[f'TITLE "PhotoCraft Resource Hub - {names[0]}"','LUT_3D_SIZE 17','DOMAIN_MIN 0.0 0.0 0.0','DOMAIN_MAX 1.0 1.0 1.0']
 for b in range(17):
  for g in range(17):
   for red in range(17):lines.append(' '.join(f'{v:.6f}' for v in transform(np.array([red,g,b])/16,id)))
 (OUT/(id+'.cube')).write_text('\n'.join(lines)+'\n')
 ramp=np.zeros((360,720,3));colors=np.array([[.88,.43,.26],[.83,.68,.48],[.39,.57,.37],[.31,.56,.72],[.69,.43,.62],[.6,.6,.6]])
 for i,col in enumerate(colors):ramp[:,i*120:(i+1)*120,:]=np.linspace(.25,1,360)[:,None,None]*col[None,None,:]
 comparison=ramp.copy();comparison[:,360:]=transform(ramp[:,360:],id)
 # Use identical full-width charts stacked before/after for honest comparison.
 chart=Image.fromarray((np.concatenate([ramp,transform(ramp,id)],axis=0)*255).astype('uint8'),'RGB');d=ImageDraw.Draw(chart);d.rectangle((8,8,168,42),fill='#ffffff');d.text((16,16),'BEFORE / 原图' .split(' / ')[0],font=ImageFont.truetype(BOLD,16),fill='#203b32');d.rectangle((8,368,168,402),fill='#ffffff');d.text((16,376),'AFTER',font=ImageFont.truetype(BOLD,16),fill='#203b32');preview(chart,id)
 metadata(id,'lut',names,('17³ creative LUT for standard RGB photos; not a LOG conversion. Chart preview only.','17³ 创意 LUT，适用于常规 RGB 照片；非 LOG 转换。预览为色卡示意。'),720,720,[('CUBE',id+'.cube')],dict(format='CUBE · 17³'))
# Pack each category and the full collection with bilingual instructions and permission.
README='''PhotoCraft Resource Hub — Starter Collection v1.0

6 templates: PSD + PNG + optional SVG source. Sample PSD text is rasterized.
Hide its layer and use PhotoCraft's Type tool to enter your own words.
4 textures: PNG; open, copy and paste into your project, then adjust opacity/scale.
4 LUTs: .cube 17³; use the documented Color Lookup adjustment if your build supports it.
Use standard RGB photos. These are creative looks, not LOG-to-Rec.709 conversions.

Programmatically validated: PSD layers and composite, PNG decoding, LUT syntax,
size/range and ZIP integrity. NOT tested inside the PhotoCraft app. Back up originals.
Each template ZIP contains specific instructions. License permits commercial use.

6 套模板：PSD 分层稿 + PNG 成品 + 可选 SVG 源码。PSD 示例文字已栅格化，
修改时请隐藏该图层，使用 PhotoCraft 文字工具重新输入。
4 款 PNG 纹理：打开后复制粘贴进项目，调整大小与不透明度。
4 款 CUBE 调色预设：在支持的版本中使用 Color Lookup 加载，用于常规 RGB 照片。
已完成文件结构与读取校验，尚未在 PhotoCraft 应用内实测。授权允许商业使用。
'''
(OUT/'README.txt').write_text(README)
for kind,filename in [('template','templates-starter.zip'),('texture','textures-starter.zip'),('lut','luts-starter.zip'),('all','photocraft-starter-collection.zip')]:
 files={'README.txt':README,'LICENSE.txt':LICENSE}
 for i in items:
  if kind not in [i['kind'],'all']:continue
  if i['kind']=='template':
   for ext in ['psd','png','svg']:files[i['id']+'/'+i['id']+'.'+ext]=(OUT/(i['id']+'.'+ext)).read_bytes()
  else:
   ext='png' if i['kind']=='texture' else 'cube';files[i['kind']+'/'+i['id']+'.'+ext]=(OUT/(i['id']+'.'+ext)).read_bytes()
 zipwrite(OUT/filename,files)
 for name in files:
  assert name not in ['../','/']
 with zipfile.ZipFile(OUT/filename) as z: assert z.testzip() is None
(ROOT/'content/resources.json').write_text(json.dumps(items,ensure_ascii=False,indent=2)+'\n')
board=Image.new('RGB',(340*4,270*4),'#edece5')
for j,im in enumerate(sheet):board.paste(im,((j%4)*340,(j//4)*270))
board.save('/workspace/scratch/71096d64bfa7/resources-contact-sheet.jpg')
print(f'Generated {len(items)} resources. Collection: {(OUT/"photocraft-starter-collection.zip").stat().st_size:,} bytes')
