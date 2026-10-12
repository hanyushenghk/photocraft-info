"""Apply canonical metadata and progressive enhancement to generated HTML."""
from pathlib import Path
from html import escape, unescape
import json,re
TITLES={
'':('PhotoCraft Downloads, Tutorials & Shortcuts | Resource Hub','PhotoCraft 下载、安装教程与快捷键 | 独立资源站'),
'guides':('PhotoCraft Tutorials & Installation Guides','PhotoCraft 教程中心：安装、入门与问题排查'),
'guide':('PhotoCraft Beginner Tutorial: Your First Project','PhotoCraft 入门教程：完成第一个作品'),
'download':('PhotoCraft Download Guide: Windows, macOS & Linux','PhotoCraft 官方下载指引：Windows、macOS 与 Linux'),
'download/windows':('PhotoCraft Windows Installation Guide: MSI & ZIP','PhotoCraft Windows 安装教程：MSI 与便携 ZIP'),
'download/mac':('PhotoCraft macOS Installation Guide: Universal DMG','PhotoCraft macOS 安装教程：通用 DMG'),
'download/linux':('PhotoCraft Linux Installation: AppImage, DEB & RPM','PhotoCraft Linux 安装教程：AppImage、DEB 与 RPM'),
'compatibility/psd':('PhotoCraft PSD Compatibility: Layers & Round-Trip Checks','PhotoCraft PSD 兼容性：图层与往返保存检查'),
'releases':('PhotoCraft Release Notes: v0.6.0 Snapshot & Upgrade Tips','PhotoCraft 更新记录：v0.6.0 快照与升级检查'),
'troubleshooting':('PhotoCraft Troubleshooting: Startup, Fonts & Saving','PhotoCraft 常见问题：启动、字体与保存排查')}
HOME_DESCS=('Find official PhotoCraft downloads, Windows, macOS and Linux installation guides, beginner tutorials, keyboard shortcuts and Photoshop comparisons.','PhotoCraft 独立中文资源站：官方软件下载指引、Windows/macOS/Linux 安装教程、入门操作、快捷键速查、PSD 兼容性与 Photoshop 功能对比。')
IMAGE_ALTS={
'adjustments':('PhotoCraft editor with Curves adjustment controls and layers','PhotoCraft 编辑器中的曲线调整控件与图层'),
'masks':('PhotoCraft editor showing layer masks','PhotoCraft 编辑器中的图层蒙版示例'),
'export-light':('PhotoCraft image export interface in the light theme','PhotoCraft 浅色主题下的图像导出界面')}
def optimize(root,origin):
 dist=root/'dist';data=json.loads((root/'content/home-data.json').read_text())
 for path in dist.rglob('*.html'):
  relative=path.parent.relative_to(dist).as_posix();relative='' if relative=='.' else relative
  lang='zh' if relative=='zh' or relative.startswith('zh/') else 'en';idx=lang=='zh'
  slug=relative.removeprefix('zh/');slug='' if relative in ['', 'en','zh'] else slug
  url=origin+('/zh/' if idx else '/')+(slug+'/' if slug else '')
  title=TITLES[slug][idx];s=path.read_text()
  desc=HOME_DESCS[idx] if not slug else unescape(re.search(r'<meta name="description" content="([^"]*)"',s)[1])
  if not slug:
   s=re.sub(r'<h1>.*?</h1>','<h1>PhotoCraft.<br><span>'+('让创作自由发生。' if idx else 'Create freely.')+'</span></h1>',s,count=1,flags=re.S)
   d=data[lang];shortcuts=d['shortcuts'];steps=d['installs']['windows']['steps']
   keys=''.join('<div class="keyrow"><span>'+escape(x[0])+'</span><span>'+('' if len(x)>3 and x[3] else '<kbd>Ctrl</kbd>')+'<kbd>'+escape(x[2])+'</kbd></span></div>' for x in shortcuts)
   install=''.join('<li><div><b>'+escape(x[0])+'</b><p>'+escape(x[1])+'</p></div></li>' for x in steps)
   s=s.replace('<div class="keygrid" id="keygrid" aria-live="polite"></div>','<div class="keygrid" id="keygrid" aria-live="polite">'+keys+'</div>')
   s=s.replace('<ol class="steps" id="installation"></ol>','<ol class="steps" id="installation">'+install+'</ol>')
   s=re.sub(r'const installs=.*?;\nconst tabButtons',lambda _: 'const installs='+json.dumps(d['installs'],ensure_ascii=False)+';\nconst tabButtons',s,count=1,flags=re.S)
   s=re.sub(r'const shortcuts=.*?;\nlet keyOS',lambda _: 'const shortcuts='+json.dumps(shortcuts,ensure_ascii=False)+';\nlet keyOS',s,count=1,flags=re.S)
   # Ordinary language links avoid query-string duplicates; legacy ?lang URLs still work.
   s=s.replace('/?lang=en','/').replace('/zh/?lang=zh','/zh/')
   label='教程中心' if idx else 'Guides'
   s=re.sub(r'(<nav class="mobile-nav"[^>]*>)',lambda m:m[0]+f'<a href="'+('/zh/guides/' if idx else '/guides/')+f'">{label}</a>',s,count=1)
  elif slug=='guides':
   s=re.sub(r'<h1>.*?</h1>','<h1>'+('PhotoCraft 教程中心' if idx else 'PhotoCraft tutorials & guides')+'</h1>',s,count=1)
  # Replace only SEO tags, preserving charset, viewport, styles and application scripts.
  s=re.sub(r'<title>.*?</title>','',s,flags=re.S)
  s=re.sub(r'<meta\s+(?:name="(?:description|robots|twitter:[^"]+)"|property="og:[^"]+")[^>]*>','',s)
  s=re.sub(r'<link rel="(?:canonical|alternate)"[^>]*>','',s)
  s=re.sub(r'<script type="application/ld\+json">.*?</script>','',s,flags=re.S)
  image=origin+'/photocraft-hero.webp';imagealt='PhotoCraft 编辑器官方截图' if idx else 'Official PhotoCraft editor screenshot'
  def meta(name,value,prop=False):return '<meta '+('property' if prop else 'name')+'="'+name+'" content="'+escape(value,quote=True)+'">'
  head='<title>'+escape(title)+'</title>'+meta('description',desc)+meta('robots','index,follow,max-image-preview:large')
  head+='<link rel="canonical" href="'+url+'">'
  for code,prefix in [('en','/'),('zh-CN','/zh/'),('x-default','/')]:head+='<link rel="alternate" hreflang="'+code+'" href="'+origin+prefix+(slug+'/' if slug else '')+'">'
  for name,value in {'og:title':title,'og:description':desc,'og:url':url,'og:type':'website' if slug in ['', 'guides'] else 'article','og:site_name':'PhotoCraft Resource Hub','og:locale':'zh_CN' if idx else 'en_US','og:locale:alternate':'en_US' if idx else 'zh_CN','og:image':image,'og:image:alt':imagealt}.items():head+=meta(name,value,True)
  for name,value in {'twitter:card':'summary_large_image','twitter:title':title,'twitter:description':desc,'twitter:image':image,'twitter:image:alt':imagealt}.items():head+=meta(name,value)
  website={'@type':'WebSite','@id':origin+'/#website','url':origin+'/','name':'PhotoCraft Resource Hub','inLanguage':['en','zh-CN']}
  page={'@type':'CollectionPage' if slug=='guides' else 'WebPage','@id':url+'#webpage','url':url,'name':title,'description':desc,'inLanguage':'zh-CN' if idx else 'en','isPartOf':{'@id':origin+'/#website'}}
  graph=[website,page]
  if slug:
   crumbs=[('首页' if idx else 'Home',origin+('/zh/' if idx else '/')),('教程中心' if idx else 'Guides',origin+('/zh/guides/' if idx else '/guides/'))]
   if slug!='guides':crumbs.append((unescape(re.sub('<[^>]+>','',re.search('<h1>(.*?)</h1>',s,re.S)[1])),url))
   graph.append({'@type':'BreadcrumbList','@id':url+'#breadcrumb','itemListElement':[{'@type':'ListItem','position':i+1,'name':n,'item':u} for i,(n,u) in enumerate(crumbs)]});page['breadcrumb']={'@id':url+'#breadcrumb'}
  head+='<script type="application/ld+json">'+json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False).replace('<','\\u003c')+'</script>'
  s=s.replace('</head>',head+'</head>')
  def img(m):
   tag=m[0]
   if 'photocraft-hero.webp' in tag:
    tag=tag[:-1]+' fetchpriority="high" decoding="async">'
   elif '/assets/photocraft-' in tag:
    if 'loading=' not in tag:tag=tag[:-1]+' loading="lazy">'
    if 'decoding=' not in tag:tag=tag[:-1]+' decoding="async">'
    if 'width=' not in tag:tag=tag[:-1]+' width="2400" height="1500">'
    name=re.search(r'photocraft-([^"/]+)\.jpg',tag)
    if name and name[1] in IMAGE_ALTS:tag=re.sub('alt="[^"]*"','alt="'+IMAGE_ALTS[name[1]][idx]+'"',tag)
   return tag
  s=re.sub(r'<img\b[^>]*>',img,s)
  path.write_text(s)
