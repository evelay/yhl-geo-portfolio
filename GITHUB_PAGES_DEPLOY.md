# GitHub Pages 发布说明

这个目录已经补齐 GitHub Pages 发布配置。元亨利 GEO 作品集的主站地址统一为 `https://evelay.github.io/yhl-geo-portfolio/`。

## 推荐发布方式

1. 在 GitHub 使用公开仓库 `evelay/yhl-geo-portfolio`。
2. 把本目录的全部文件上传到该仓库，或用 Git 推送到仓库的 `main` 分支。
3. 进入仓库 `Settings → Pages`，确认发布来源为 `GitHub Actions`。
4. 等待 `Actions` 里的 `Deploy to GitHub Pages` 跑完。
5. 访问 GitHub Pages 主站地址：`https://evelay.github.io/yhl-geo-portfolio/`。

## 已经为 GitHub Pages 做好的适配

- `npm run build:github` 会生成静态网站到 `out/`。
- `.github/workflows/github-pages.yml` 会在推送到 `main` 后自动构建并发布。
- GitHub Pages basePath 固定为 `/yhl-geo-portfolio`，避免页面资源 404。
- `robots.txt` 和 `sitemap.xml` 会在构建后写入 GitHub Pages 主站地址。
- `.nojekyll` 会自动生成，避免 GitHub Pages 忽略 `_next` 静态资源。
- `.openai/hosting.json` 和 OpenAI Sites 构建文件作为历史或备用预览保留，不作为 canonical、metadataBase、sitemap 或 robots 的主站地址。

## 本地预览静态版

```bash
npm run build:github
npx serve out
```

如果需要手动模拟普通项目仓库路径：

```bash
GITHUB_REPOSITORY=evelay/yhl-geo-portfolio npm run build:github
```

## 如果使用自定义域名

在 GitHub Actions 的构建环境里设置：

```bash
GITHUB_PAGES_CNAME=你的域名
NEXT_PUBLIC_SITE_URL=https://你的域名
```

构建脚本会自动写入 `CNAME`，并把 `robots.txt`、`sitemap.xml` 换成自定义域名。
