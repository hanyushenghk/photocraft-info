"""Validate generated SEO, language pairs, static content and local links."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin,urlsplit,unquote
import json,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]/'dist'
class Page(HTMLParser):
 def __init__(self,path):
  super().__init__();self.tags=[];self.json=[];self.collect=False;self.feed(path.read_text())
 def handle_starttag(self,t,a):
  d=dict(a);self.tags.append((t,d))
  if t=='script' and d.get('type')=='application/ld+json':self.collect=True
 def handle_data(self,data):
  if self.collect:self.json.append(json.loads(data))
 def handle_endtag(self,t):
  if t=='script':self.collect=False
 def attrs(self,t):return [a for tag,a in self.tags if tag==t]
pages={'/'+str(p.relative_to(ROOT)):Page(p) for p in ROOT.rglob('*.html')}
canonicals=set()
for path,p in pages.items():
 ids=[a['id'] for _,a in p.tags if 'id' in a];assert len(ids)==len(set(ids)),path
 assert len(p.attrs('h1'))==1,path
 canonical=[a['href'] for a in p.attrs('link') if a.get('rel')=='canonical'];assert len(canonical)==1,path
 canonicals.add(canonical[0]);alts={a['hreflang']:a['href'] for a in p.attrs('link') if a.get('rel')=='alternate'}
 assert set(alts)=={'en','zh-CN','x-default'} and alts['en']==alts['x-default'],path
 assert canonical[0]==alts['zh-CN' if path.startswith('/zh/') else 'en'],path
 assert len([a for a in p.attrs('meta') if a.get('name')=='description'])==1,path
 assert p.json[0]['@graph'][1]['url']==canonical[0],path
 for a in p.attrs('img'):assert all(a.get(k) for k in ['alt','width','height','decoding']), (path,a)
 for _,a in p.tags:
  for key in ['href','src']:
   if key not in a:continue
   u=urlsplit(urljoin('https://local'+path,a[key]))
   if u.netloc!='local':continue
   target=unquote(u.path);target=target+'index.html' if target.endswith('/') else target
   assert (ROOT/target.lstrip('/')).is_file(),(path,a[key])
   if u.fragment and target in pages:assert any(d.get('id')==u.fragment for _,d in pages[target].tags),(path,a[key])
 for code in ['en','zh-CN']:
  target=urlsplit(alts[code]).path+'index.html';other={a['hreflang']:a['href'] for a in pages[target].attrs('link') if a.get('rel')=='alternate'};assert other==alts,path
for home in ['index.html','en/index.html','zh/index.html']:
 s=(ROOT/home).read_text();assert s.count('class="keyrow"')>=12,home
 assert '<ol class="steps" id="installation"><li>' in s,home
 assert 'fetchpriority="high"' in s,home
sitemap={e.text for e in ET.parse(ROOT/'sitemap.xml').findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')}
assert sitemap==canonicals,(sitemap,canonicals)
print(f'PASS: {len(pages)} HTML pages, {len(canonicals)} canonical URLs; metadata, schema, hreflang, sitemap, images, static content and local links.')
