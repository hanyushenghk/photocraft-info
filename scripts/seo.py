"""Apply canonical metadata and progressive enhancement to generated HTML."""
from pathlib import Path
from html import escape, unescape
import json,re
IMAGE_ALTS={
'adjustments':('PhotoCraft editor with Curves adjustment controls and layers','PhotoCraft 编辑器中的曲线调整控件与图层'),
'masks':('PhotoCraft editor showing layer masks','PhotoCraft 编辑器中的图层蒙版示例'),
'export-light':('PhotoCraft image export interface in the light theme','PhotoCraft 浅色主题下的图像导出界面')}
def breadcrumb_slugs(slug):
 if slug in ['', 'guides', 'plugins', 'templates', 'download', 'compare', 'community']:
  return ['', slug] if slug else ['']
 parent='download' if slug.startswith('download/') else 'guides'
 return ['', parent, slug]

def optimize(root,origin):
 dist=root/'dist';data=json.loads((root/'content/home-data.json').read_text())
 metadata=json.loads((root/'content/seo.json').read_text())
 pages={p['slug']:p for p in json.loads((root/'content/pages.json').read_text())}
 for path in dist.rglob('*.html'):
  relative=path.parent.relative_to(dist).as_posix();relative='' if relative=='.' else relative
  lang='zh' if relative=='zh' or relative.startswith('zh/') else 'en';idx=lang=='zh'
  slug=relative.removeprefix('zh/');slug='' if relative in ['', 'en','zh'] else slug
  url=origin+('/zh/' if idx else '/')+(slug+'/' if slug else '')
  settings=metadata[slug]
  title=settings['title'][idx];s=path.read_text()
  desc=settings['description'][idx]
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
  elif slug=='guides':
   s=re.sub(r'<h1>.*?</h1>','<h1>'+('PhotoCraft 教程中心' if idx else 'PhotoCraft tutorials & guides')+'</h1>',s,count=1)
  # Replace only SEO tags, preserving charset, viewport, styles and application scripts.
  s=re.sub(r'<title>.*?</title>','',s,flags=re.S)
  s=re.sub(r'<meta\s+(?:name="(?:description|keywords|robots|twitter:[^"]+)"|property="og:[^"]+")[^>]*>','',s)
  s=re.sub(r'<link rel="(?:canonical|alternate)"[^>]*>','',s)
  s=re.sub(r'<script type="application/ld\+json">.*?</script>','',s,flags=re.S)
  image=origin+'/photocraft-hero.webp';imagealt='PhotoCraft 编辑器官方截图' if idx else 'Official PhotoCraft editor screenshot'
  def meta(name,value,prop=False):return '<meta '+('property' if prop else 'name')+'="'+name+'" content="'+escape(value,quote=True)+'">'
  head='<title>'+escape(title)+'</title>'+meta('description',desc)+meta('keywords',', '.join(settings['keywords'][idx]))+meta('robots','index,follow,max-image-preview:large')
  head+='<link rel="canonical" href="'+url+'">'
  for code,prefix in [('en','/'),('zh-CN','/zh/'),('x-default','/')]:head+='<link rel="alternate" hreflang="'+code+'" href="'+origin+prefix+(slug+'/' if slug else '')+'">'
  for name,value in {'og:title':title,'og:description':desc,'og:url':url,'og:type':'website' if slug in ['', 'guides', 'plugins', 'templates', 'community', 'download'] else 'article','og:site_name':'PhotoCraft Resource Hub','og:locale':'zh_CN' if idx else 'en_US','og:locale:alternate':'en_US' if idx else 'zh_CN','og:image':image,'og:image:alt':imagealt}.items():head+=meta(name,value,True)
  for name,value in {'twitter:card':'summary_large_image','twitter:title':title,'twitter:description':desc,'twitter:image':image,'twitter:image:alt':imagealt}.items():head+=meta(name,value)
  website={'@type':'WebSite','@id':origin+'/#website','url':origin+'/','name':'PhotoCraft Resource Hub','inLanguage':['en','zh-CN']}
  page={'@type':'CollectionPage' if slug in ['', 'guides', 'plugins', 'templates', 'community', 'download'] else 'WebPage','@id':url+'#webpage','url':url,'name':title,'description':desc,'inLanguage':'zh-CN' if idx else 'en','isPartOf':{'@id':origin+'/#website'}}
  graph=[website,page]
  if settings.get('modified'):page['dateModified']=settings['modified']
  if slug:
   def crumb_title(key):
    if not key:return '首页' if idx else 'Home'
    if key=='guides':return '教程中心' if idx else 'Guides'
    return pages[key]['title'][lang]
   crumbs=[(crumb_title(key),origin+('/zh/' if idx else '/')+(key+'/' if key else '')) for key in breadcrumb_slugs(slug)]
   graph.append({'@type':'BreadcrumbList','@id':url+'#breadcrumb','itemListElement':[{'@type':'ListItem','position':i+1,'name':n,'item':u} for i,(n,u) in enumerate(crumbs)]});page['breadcrumb']={'@id':url+'#breadcrumb'}
  if slug=='guides':
   entries=[(p['title'][lang],origin+('/zh/' if idx else '/')+p['slug']+'/') for p in pages.values()]
  elif slug in ['plugins','templates','community']:
   entries=[(section['title'][lang],url+'#'+section['id']) for section in pages[slug]['sections']]
  else:entries=[]
  if entries:
   listing={'@type':'ItemList','@id':url+'#contents','name':'本页资源与指南' if idx else 'Resources and guides on this page','numberOfItems':len(entries),'itemListElement':[{'@type':'ListItem','position':i+1,'name':name,'url':href} for i,(name,href) in enumerate(entries)]}
   graph.append(listing);page['mainEntity']={'@id':listing['@id']}
  head+='<script type="application/ld+json">'+json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False).replace('<','\\u003c')+'</script>'
  s=s.replace('</head>',head+'</head>')
  def img(m):
   tag=m[0]
   if 'photocraft-hero.webp' in tag:
    tag=re.sub(r'src="[^"]*"','src="/photocraft-hero.webp"',tag)
    tag=tag[:-1]+' srcset="/assets/photocraft-hero-800.webp 800w, /photocraft-hero.webp 1600w" sizes="(max-width: 760px) 92vw, 50vw" fetchpriority="high" decoding="async">'
   elif '/assets/photocraft-' in tag:
    name=re.search(r'photocraft-([^"/]+)\.jpg',tag)
    if name and name[1] in IMAGE_ALTS:
     key=name[1];base='/assets/photocraft-'+key
     tag=re.sub(r'src="[^"]*"','src="'+base+'-1280.webp"',tag)
     tag=re.sub('alt="[^"]*"','alt="'+IMAGE_ALTS[key][idx]+'"',tag)
     sizes='(max-width: 760px) 92vw, 800px' if slug else '(max-width: 760px) 92vw, 33vw'
     tag=tag[:-1]+' srcset="'+base+'-640.webp 640w, '+base+'-1280.webp 1280w" sizes="'+sizes+'">'
    if 'loading=' not in tag:tag=tag[:-1]+' loading="lazy">'
    if 'decoding=' not in tag:tag=tag[:-1]+' decoding="async">'
    if 'width=' not in tag:tag=tag[:-1]+' width="2400" height="1500">'
   return tag
  s=re.sub(r'<img\b[^>]*>',img,s)
  path.write_text(s)
