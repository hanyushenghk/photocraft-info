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
