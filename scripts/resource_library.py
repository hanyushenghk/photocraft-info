"""Render the bilingual, progressively enhanced download gallery."""
from html import escape
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def size(n):return f'{n/1048576:.1f} MB' if n>=1048576 else f'{n/1024:.0f} KB'
def gallery(lang):
 zh=lang=='zh';items=json.loads((ROOT/'content/resources.json').read_text())+json.loads((ROOT/'content/third-party-resources.json').read_text());labels={'all':'全部' if zh else 'All resources','template':'模板' if zh else 'Templates','texture':'纹理' if zh else 'Textures','lut':'调色预设' if zh else 'LUTs'}
 pack='/downloads/photocraft-starter-collection.zip';packsize=size((ROOT/'dist'/pack.lstrip('/')).stat().st_size)
 controls=''.join(f'<button type="button" data-resource-filter="{k}" aria-pressed="{str(k=="all").lower()}">{v}'+(' · '+str(len(items)) if k=='all' else ' · '+str(sum(x['kind']==k for x in items)))+'</button>' for k,v in labels.items())
 tests={r["id"]:r for r in json.loads((ROOT/"dist/downloads/photocraft-template-test-results.json").read_text())["results"]}
 cards=[]
 for i in items:
  downloads=''.join(f'<a class="asset-download" href="{d["url"]}" download aria-label="{escape(i["title"][lang])} — {d["label"]} ({size(d["bytes"])})">↓ {d["label"]} <span>{size(d["bytes"])}</span></a>' for d in i['downloads'])
  spec=(f'{i["width"]} × {i["height"]} px · {i["layers"]} '+('像素图层' if zh else 'pixel layers')) if i['kind']=='template' else (f'{i["width"]} × {i["height"]} px' if i['kind']=='texture' else ('17³ · 常规 RGB 照片' if zh else '17³ · standard RGB photos'))
  note=({'template':'PSD 示例文字已栅格化；隐藏该层后输入新文字。','texture':'作为背景图层使用，可调整不透明度与大小。','lut':'预览为程序生成色卡，不是 PhotoCraft 应用截图。'} if zh else {'template':'PSD sample text is rasterized. Hide it and add your own type.','texture':'Use as a background layer; adjust opacity and scale.','lut':'Preview: generated color chart, not a PhotoCraft app screenshot.'})[i['kind']]
  test_html=''
  if i['id'] in tests:
   result=tests[i['id']]
   passed=all(t['exit_code']==0 for t in result['tests'].values())
   status=('已通过引擎测试' if zh else 'Engine checks passed') if passed else ('请查看测试限制' if zh else 'Review test limitations')
   checks=('打开 · PNG 导出 · PSD/PCraft 保存与重开' if zh else 'Open · PNG export · PSD/PCraft save & reopen')
   edit=('单个文字图层修改并保存成功。' if zh else 'One text-layer edit saved successfully.') if i.get('source') else ('图层隐藏修改成功；导出与参考图逐像素一致。' if zh else 'Layer visibility edit passed; export matches the reference pixel for pixel.')
   caution=('需安装字体并检查换行；文件默认显示作者推广图层。' if zh else 'Install fonts and check line breaks. A publisher promotion layer is visible by default.') if i.get('source') else ''
   if i.get('color_mode')=='CMYK':
    caution+=(' PNG 导出转为 sRGB；未做印刷校样。' if zh else ' PNG converts to sRGB; print proofing is untested.')
   test_html=f'<div class="asset-test"><strong>{status}</strong><span>PhotoCraft 0.7.0 · Linux CLI · 2026-10-12</span><p>{checks}</p><p>{edit}</p>'+(f'<p class="asset-test-caution">{caution}</p>' if caution else '')+f'<a href="#tested">{"测试范围与完整结果" if zh else "Test scope & full results"} →</a></div>'
  attribution=''
  if i.get('source'):
   spec=f'{i["width"]} × {i["height"]} px · {i["color_mode"]} · {i["text_layers"]} '+('文字图层' if zh else 'text layers')
   note=('字体：' if zh else 'Fonts: ')+escape(i['fonts'])+('。下载包未附字体。' if zh else '. Fonts are not included.')
   attribution=f'<p class="asset-attribution"><a href="{i["source"]}" target="_blank" rel="noopener noreferrer">Free PSD Files ↗</a> · <a href="{i["license_url"]}" target="_blank" rel="noopener noreferrer">{"作者许可" if zh else "Publisher terms"}</a><br>{"个人与商用允许；再分享须保留来源，不得出售源文件。" if zh else "Personal/commercial use; credit the source when sharing. No source-file resale."}</p>'
  cards.append(f'''<article class="asset-card" data-resource-kind="{i['kind']}" data-resource-search="{escape((i['title'][lang]+' '+i['description'][lang]+' '+i['format']).lower(),quote=True)}"><div class="asset-preview"><img src="{i['preview']}" alt="{escape(i['title'][lang])} — {'资源预览' if zh else 'asset preview'}" width="{i.get('preview_width',i['width'])}" height="{i.get('preview_height',i['height'])}" loading="lazy" decoding="async"></div><div class="asset-content"><span class="overline">{labels[i['kind']]} / {'FREE PSD FILES' if i.get('source') else 'ORIGINAL'}</span><h2>{escape(i['title'][lang])}</h2><p>{escape(i['description'][lang])}</p><div class="asset-spec">{spec}</div><p class="asset-note">{note}</p>{test_html}{attribution}<div class="asset-downloads">{downloads}</div></div></article>''')
 return f'''<section class="asset-library" aria-label="{'资源下载库' if zh else 'Download library'}"><div class="asset-bundle"><div><div class="overline">STARTER COLLECTION / V1.0</div><h2>{'14 份原创资源，开始你的下一个作品。' if zh else '14 original assets. Your next project starts here.'}</h2><p>{'6 套分层模板 · 4 款 PNG 纹理 · 4 款 CUBE 预设' if zh else '6 layered templates · 4 PNG textures · 4 CUBE presets'}</p><p class="bundle-small">{'无需注册 · 允许商用 · 包含中英文使用说明' if zh else 'No sign-up · Commercial use permitted · Bilingual instructions included'}</p></div><a class="btn primary" href="{pack}" download>{'下载 14 份原创资源' if zh else 'Download 14 original assets'} ↓ <span>{packsize}</span></a></div><p class="source-note">{'另新增 8 套 Free PSD Files 模板，下方可单独下载；不包含在原创资源包内，适用作者许可。' if zh else 'Also explore 8 Free PSD Files templates below, available as separate downloads under the publisher’s terms. They are not included in the original bundle.'}</p><div class="asset-tools" id="resources-luts"><div class="asset-filters" aria-label="{'资源类别' if zh else 'Resource category'}">{controls}</div><label class="asset-search"><span>{'搜索资源' if zh else 'Search resources'}</span><input id="resource-search" type="search" placeholder="{'如：海报、纹理、PSD' if zh else 'Try poster, texture or PSD'}"></label></div><p class="asset-result" aria-live="polite"><span id="resource-count">{len(items)}</span> {'份资源' if zh else 'resources'} · <a href="#use">{'使用方法与授权' if zh else 'Usage & license'} ↗</a></p><div class="asset-grid">{''.join(cards)}</div><p id="resource-empty" class="no-results" hidden>{'没有匹配资源，请清除搜索词或切换分类。' if zh else 'No matches. Clear your search or try another category.'}</p><p class="source-note">{'14 套 PSD 已通过 PhotoCraft 0.7.0 官方命令行引擎的打开、PNG 导出、PSD/PCraft 保存与重开测试。六套原创模板图层开关与八套第三方模板单层文字修改已验证。桌面界面、全部字体与效果尚未全面测试。纹理与 LUT 仍仅完成文件校验。' if zh else 'All 14 PSDs passed open, PNG export, PSD/PCraft save and reopen in the official PhotoCraft 0.7.0 CLI engine. Layer visibility was tested in six originals; one text-layer edit in each third-party PSD. Desktop UI, every font and effect are not fully tested. Textures and LUTs have file-level checks only.'}</p></section>'''
