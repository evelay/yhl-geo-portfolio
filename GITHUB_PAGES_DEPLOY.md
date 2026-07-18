# GitHub Pages 发布说明

这个目录已经补齐 GitHub Pages 发布配置，适合把元亨利 GEO 作品集从 `chatgpt.site` 迁移到更容易公开访问的 `github.io` 地址。

## 推荐发布方式

1. 在 GitHub 新建一个公开仓库，例如 `yhl-geo-portfolio`。
2. 把本目录的全部文件上传到该仓库，或用 Git 推送到仓库的 `main` 分支。
3. 进入仓库 `Settings → Pages`，确认发布来源为 `GitHub Actions`。
4. 等待 `Actions` 里的 `Deploy to GitHub Pages` 跑完。
5. 访问 GitHub Pages 给出的地址，通常是：
   - 普通项目仓库：`https://你的用户名.github.io/yhl-geo-portfolio/`
   - 用户主页仓库：`https://你的用户名.github.io/`

## 已经为 GitHub Pages 做好的适配

- `npm run build:github` 会生成静态网站到 `out/`。
- `.github/workflows/github-pages.yml` 会在推送到 `main` 后自动构建并发布。
- 普通项目仓库会自动加上仓库名路径，例如 `/yhl-geo-portfolio`，避免页面资源 404。
- `robots.txt` 和 `sitemap.xml` 会在构建后自动替换成 GitHub Pages 地址。
- `.nojekyll` 会自动生成，避免 GitHub Pages 忽略 `_next` 静态资源。

## 本地预览静态版

```bash
npm run build:github
npx serve out
```

如果本地预览普通项目仓库路径，可以模拟仓库名：

```bash
GITHUB_REPOSITORY=你的用户名/yhl-geo-portfolio npm run build:github
```

## 如果使用自定义域名

在 GitHub Actions 的构建环境里设置：

```bash
GITHUB_PAGES_CNAME=你的域名
NEXT_PUBLIC_SITE_URL=https://你的域名
```

构建脚本会自动写入 `CNAME`，并把 `robots.txt`、`sitemap.xml` 换成自定义域名。
