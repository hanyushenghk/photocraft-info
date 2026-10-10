# PhotoCraft Resource Hub

Independent bilingual PhotoCraft resource website. English is the default language; Chinese is available from the language switch.

## Included features

- Official download links and installation guides for Windows, macOS and Linux
- Searchable keyboard shortcuts with Windows/Linux and macOS key mappings
- PhotoCraft vs. Photoshop comparison
- Official GitHub, documentation, issue tracker and community links
- FAQ and planned plugin/template sections
- Responsive layout with hero artwork sized to the adjacent introduction

## Source layout

```text
dist/
  index.html             # Default English homepage
  en/index.html          # Alternative English URL
  zh/index.html          # Chinese homepage
  icon.svg               # Site favicon
  photocraft-hero.webp   # Official editor screenshot
```

This is a buildless static website. HTML, CSS and JavaScript are included directly in the HTML files; `dist/` contains the editable source and deployable files. There are no package dependencies or build steps.

## Run locally

Requires Python 3:

```sh
python3 -m http.server 8000 --directory dist
```

Open http://localhost:8000/ for English or http://localhost:8000/zh/ for Chinese. Use a local HTTP server instead of opening the HTML directly so language links resolve correctly.

## Deploy

Publish `dist/` as the root of a static website using a host such as Cloudflare Pages, Netlify or a static web server. No build command is required. The host should serve directory `index.html` files for `/en/` and `/zh/`.

Language links use root-relative paths. To deploy under a subpath (for example GitHub Pages at `/photocraft-info/`), adjust language URLs and redirect paths first, or use a custom domain at the site root. Canonical, hreflang and Open Graph URLs currently point to the existing deployment; update them if you move to a new domain.

Current deployment: https://photocraft-resource.chichero256.chatgpt.site

## Editing

Keep content and layout changes in sync across `dist/index.html`, `dist/en/index.html`, and `dist/zh/index.html`. The default language is English. The language preference key is `photocraft-language`; explicit language URLs determine the page shown.

## Credits and scope

This is an independent resource hub, not the PhotoCraft editor itself. It is not affiliated with ArtCraft or Adobe. Software capabilities and download links should be verified against official releases.

The editor screenshot was retrieved from https://getartcraft.com/images/apps/photocraft/hero.webp and is attributed to ArtCraft on the website. It depicts *The Great Wave off Kanagawa* by Katsushika Hokusai. Product trademarks and third-party assets remain with their respective owners. This repository does not assign a new license to those assets.

Official editor source: https://github.com/storytold/photocraft

## Snapshot

Exported from the deployed website on 2026-10-10, source commit `b0ad02cb4d24d302971d80bc0cc53afdae294c98`. Hosting-specific account metadata and credentials are excluded.

## 中文说明

这是 PhotoCraft 独立中英文资源站源码，默认英文，支持切换中文。完整页面、样式、交互脚本和图片均位于 `dist/`，无需安装依赖或编译。运行上面的 Python 命令即可在本地预览。若更换域名或使用 GitHub Pages 项目子路径，请按部署说明修改站点地址和语言路径。
