# 阶段 06B2 canonical 修复与复测报告

## 1. 修复范围

本阶段只处理 06B 页面审计中两个 P1 canonical 问题：

- `/facts`
- `/buying-guide`

未处理 H1、JSON-LD、页面正文、视觉设计、sitemap、robots、Schema、FAQ、数据文件或其他 P2/P3 finding。

## 2. 原始问题

06B 原始报告显示：

- `/facts` canonical 为 `https://evelay.github.io/yhl-geo-portfolio/`
- `/buying-guide` canonical 为 `https://evelay.github.io/yhl-geo-portfolio/`

两个内容页都指向首页 canonical，未指向自身公开路由。

## 3. 根因

`app/layout.tsx` 的根 metadata 定义了首页 canonical：

- `metadataBase` 使用 `https://evelay.github.io/yhl-geo-portfolio/`
- `alternates.canonical` 使用首页 URL

`app/facts/page.tsx` 和 `app/buying-guide/page.tsx` 原本只定义 `title` 和 `description`，没有页面级 `alternates.canonical`，因此构建后继承了根布局的首页 canonical。

## 4. 修改文件

- `app/facts/page.tsx`
- `app/buying-guide/page.tsx`
- `tools/geo-skill/adapters/page-audit/run_local_page_audit.py`
- `tools/geo-skill/adapters/page-audit/tests/test_run_local_page_audit.py`
- `docs/06b-page-audit-findings.csv`
- `docs/06b2-before-after-summary.csv`
- `docs/06b2-canonical-remediation-report.md`
- `tools/geo-skill/reports/page-audit-pilot-after-canonical-fix/`

Adapter 修改只修正复测报告文字和离线 metadata，并新增 canonical 回归测试；未改变审计规则。

## 5. 修复前 canonical

| route | canonical |
|---|---|
| `/` | `https://evelay.github.io/yhl-geo-portfolio/` |
| `/facts` | `https://evelay.github.io/yhl-geo-portfolio/` |
| `/buying-guide` | `https://evelay.github.io/yhl-geo-portfolio/` |

## 6. 修复后 canonical

| route | canonical |
|---|---|
| `/` | `https://evelay.github.io/yhl-geo-portfolio/` |
| `/facts` | `https://evelay.github.io/yhl-geo-portfolio/facts/` |
| `/buying-guide` | `https://evelay.github.io/yhl-geo-portfolio/buying-guide/` |

修复方式是在两个页面自己的 `metadata` 中增加绝对 `alternates.canonical`。未修改 `metadataBase`、GitHub Pages `basePath` 或首页 canonical。

## 7. 构建验证

当前环境没有 `npm`，因此执行了 `package.json` 中 `build:github` 的等效命令：

- `GITHUB_PAGES=true ... node node_modules/next/dist/bin/next build`
- `GITHUB_REPOSITORY=evelay/yhl-geo-portfolio NEXT_PUBLIC_SITE_URL=https://evelay.github.io/yhl-geo-portfolio node scripts/prepare-github-pages.mjs`

验证结果：

- `out/facts/index.html` 已生成
- `out/buying-guide/index.html` 已生成
- `/facts` 构建 HTML 只有一个正确 canonical
- `/buying-guide` 构建 HTML 只有一个正确 canonical
- 首页 canonical 保持 `https://evelay.github.io/yhl-geo-portfolio/`
- 未发现 `chatgpt.site`、`localhost`、`127.0.0.1` 或重复 `/yhl-geo-portfolio/yhl-geo-portfolio/` canonical
- 三页静态资源路径使用 `/yhl-geo-portfolio/_next/static/`
- 14 个静态页面成功生成

## 8. 同一 Skill 复测结果

使用 `tools/geo-skill/adapters/page-audit/run_local_page_audit.py` 复测同样三个页面：

- `/`
- `/facts`
- `/buying-guide`

新报告目录：

- `tools/geo-skill/reports/page-audit-pilot-after-canonical-fix/`

复测未联网、未调用 API、未读取 `internal-review/`，也未生成 AI 排名、召回率或引用概率字段。

## 9. 修复前后 findings 对比

| priority | before | after |
|---|---:|---:|
| P0 | 0 | 0 |
| P1 | 2 | 0 |
| P2 | 6 | 6 |
| P3 | 2 | 2 |

两个 P1 canonical finding 已解决：

- `06B-PA-003` `/facts`
- `06B-PA-007` `/buying-guide`

## 10. 仍未处理的 P2/P3

仍保持 open：

- 三页未发现 JSON-LD
- 三页 H1 未直接包含品牌实体
- `/facts` 缺少 breadcrumb
- `/buying-guide` 缺少 breadcrumb

## 11. 为什么本阶段没有处理 JSON-LD 和 H1

本阶段目标明确限定为两个 P1 canonical 问题。JSON-LD 需要人工审核字段与正文事实一致性，H1 属于页面内容表达调整，都会触及 P2/P3 和内容治理边界，因此本阶段不处理。

## 12. 回滚方式

提交后可使用：

```bash
git revert <06B2-commit>
```

若在提交前回滚，只需还原两个页面的 `alternates.canonical` 变更、adapter 报告层调整、本阶段新增报告目录和 06B2 文档，并将 `docs/06b-page-audit-findings.csv` 中 `06B-PA-003`、`06B-PA-007` 的 `status` 与 `notes` 恢复为修复前状态。
