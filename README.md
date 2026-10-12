# PhotoCraft Resource Hub

Independent bilingual PhotoCraft resource website. English is the default; Chinese is available on every page. This is a resource hub, not the editor itself, and is not affiliated with ArtCraft or Adobe.

## Features

- Eight detailed guides in English and Chinese: first workflow, download center, Windows, macOS, Linux, PSD compatibility, troubleshooting, and release highlights
- Searchable guide hub and keyboard shortcuts
- PhotoCraft vs. Photoshop comparison, official resources, FAQ and planned plugin/template sections
- Official feature screenshots and responsive layout
- Corresponding-language article links, source references, canonical URLs and sitemap

## Edit and build

Requires only Python 3; no package installation is needed.

```sh
python3 scripts/build_content.py
python3 -m http.server 8000 --directory dist
```

Open http://localhost:8000/ or http://localhost:8000/zh/.

- `content/pages.json`: bilingual guide content and source references
- `content/templates/home-en.html` and `home-zh.html`: base homepages
- `scripts/build_content.py`: generates guides, guide hubs, enriched homepages and sitemap
- `dist/assets/`: shared styles, scripts and official screenshots
- `dist/`: complete generated static website, ready to host

Edit content/templates and rebuild; direct edits to generated HTML will be overwritten. Shared asset styles and scripts are edited directly in `dist/assets/`. The original homepage CSS is embedded in the templates; article pages use `dist/assets/site.css`.

## Deploy

Publish `dist/` at the root of a static host supporting directory index files. Committed output requires no build step. To regenerate during deployment, run `python3 scripts/build_content.py`.

Routes use root-relative paths. GitHub Pages project subpaths require URL adjustments or a custom domain. If moving domains, update `ORIGIN` in the builder and canonical/hreflang/Open Graph URLs in both home templates, then rebuild.

Current deployment: https://photocraft-resource.chichero256.chatgpt.site

## Sources and credits

Official editor: https://github.com/storytold/photocraft

The hero screenshot comes from https://getartcraft.com/images/apps/photocraft/hero.webp. Feature screenshots come from `docs/images/photocraft-adjustments.jpg`, `photocraft-masks.jpg` and `photocraft-export-light.jpg` in the official editor repository. They are attributed on the website. Product trademarks and third-party assets remain with their respective owners; this repository does not assign a new license to them.

Content snapshot: October 10, 2026. Release highlights are dated snapshots, not a live version feed. Guides distinguish official documentation from editorial recommendations and are not a cross-platform software compatibility test.

## 中文说明

PhotoCraft 独立中英文资源站，默认英文，包含 8 篇双语详细指南、可搜索教程中心、快捷键和功能对比。修改 `content/` 中的内容后运行 `python3 scripts/build_content.py`，再将 `dist/` 部署到静态网站根目录。新域名或 GitHub Pages 子路径需要相应修改 URL。

## SEO and validation

`python3 scripts/build_content.py` also runs `scripts/seo.py`, which provides unique bilingual titles, descriptions, canonical and reciprocal hreflang links, Open Graph/Twitter image metadata, and WebSite/WebPage/BreadcrumbList JSON-LD. The `/en/` alias canonicalizes to `/`. The sitemap lists only the 20 canonical URLs.

Homepage installation steps and all 12 shortcuts are pre-rendered from `content/home-data.json` and enhanced with the existing JavaScript controls. The hero image has high fetch priority; lower-page screenshots use lazy loading, explicit dimensions, descriptive alt text and asynchronous decoding.

Run `python3 scripts/check_site.py` after rebuilding to validate local links, language pairs, metadata, JSON-LD, sitemap coverage and static content. These checks do not substitute for browser rendering, live HTTP validation, Google Rich Results testing or Search Console inspection.

The Sites deployment was owner-private when checked on October 12, 2026. Public crawling requires the owner to explicitly enable public access. No Search Console verification token, sitemap submission or indexing guarantee is included. When publishing on another domain, update the configured origin and rebuild before submitting its sitemap.


## Original downloadable resource collection

The live site is public at https://photo-craft.io. `/templates/` and `/zh/templates/`
include 6 original layered PSD layouts, 4 PNG textures and 4 CUBE LUTs. Downloads
are self-hosted in `dist/downloads`, with permission and bilingual instructions.
PSD sample lettering is rasterized; optional SVG source retains text elements.
The 14 PSD templates were tested with the official PhotoCraft 0.7.0 Linux CLI engine on 2026-10-12. Desktop GUI testing is not included; textures, LUTs and optional SVGs still have file-level checks only.

To regenerate assets: install `scripts/requirements-resources.txt`, then run
`python scripts/build_resources.py`, `python scripts/build_content.py`,
`python scripts/check_resources.py` and `python scripts/check_site.py`.
The generator uses DejaVu Sans from the host; no font files are distributed.


## Third-party template collection

Eight PSD template packs from Free PSD Files are listed in
`content/third-party-resources.json` and hosted under `dist/downloads/third-party/`.
The original PSD bytes are preserved; each ZIP adds SOURCE-AND-LICENSE.txt with
the author, specific source URL, publisher terms and font/compatibility notes.
Publisher terms permit redistribution of its own resources with source backlinks;
these files are not covered by the original-assets license and cannot be resold.
They are intentionally excluded from the 14-original-asset starter ZIP.
Validation: ZIP integrity, PSD parsing, embedded composite decoding and SHA-256.
PhotoCraft application compatibility remains untested.

## PhotoCraft template integration tests

All 14 PSDs pass open/export/PSD and PCraft round trips. See `dist/downloads/photocraft-template-test-results.json` for version, input hashes, warnings, image differences and individual checks. Third-party fonts are missing in the test environment; cached unedited text does not prove font fidelity. CMYK reference metrics use Pillow RGB conversion and are not color-managed proofs. Every third-party PSD has a publisher promotion layer visible by default.

Reproduce using an official CLI release and an empty output path:

```bash
python scripts/test_photocraft_templates.py --cli /absolute/path/photocraft-cli --out /tmp/photocraft-template-tests-new
```
