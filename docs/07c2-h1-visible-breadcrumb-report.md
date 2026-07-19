# 阶段 07C2 H1、页面摘要与可见 Breadcrumb 实施报告

日期：2026-07-19  
分支：`refactor/portfolio-v2`

## 1. 人工确认决定

`docs/07c1-human-review.md` 已标记为 `approved-for-implementation`。

- 首页 H1：`元亨利红木家具 GEO 诊断与可核验内容体系`
- `/facts` H1：`元亨利品牌事实、来源与信息边界`
- `/buying-guide` H1：`元亨利红木家具购买核验指南`
- 三页均增加或调整上下文独立摘要。
- 可见 breadcrumb 使用短导航名：`首页 -> 品牌事实与定位`、`首页 -> 购买核验指南`。
- 现有 BreadcrumbList JSON-LD name 保持：`品牌事实与定位`、`购买核验指南`。
- URL、canonical、sitemap、robots、品牌事实和核心指标均保持不变。
- 首页不添加可见 breadcrumb，不生成首页 Schema，不增加“知识中心”等中间层级。

## 2. 修改范围

页面与组件：

- `app/page.tsx`
- `app/facts/page.tsx`
- `app/buying-guide/page.tsx`
- `app/components.tsx`
- `app/globals.css`

测试、审计与记录：

- `tests/rendered-html.test.mjs`
- `tools/geo-skill/adapters/schema-draft/tests/test_breadcrumb_injection_html.py`
- `tools/geo-skill/adapters/page-audit/run_local_page_audit.py`
- `tools/geo-skill/adapters/page-audit/tests/test_run_local_page_audit.py`
- `tools/geo-skill/reports/page-audit-pilot-after-h1-visible-breadcrumb/`
- `docs/07c1-human-review.md`
- `docs/06b-page-audit-findings.csv`
- `docs/07c2-before-after.csv`
- `docs/07c2-h1-visible-breadcrumb-report.md`

未修改：`app/data.ts`、`app/layout.tsx`、`public/`、sitemap 源文件、robots 源文件、公开知识库 JSON、下载文件、其他页面。

## 3. H1 前后对比

| route | before | after |
| --- | --- | --- |
| `/` | `让红木家具信息变得可回答、可核验` | `元亨利红木家具 GEO 诊断与可核验内容体系` |
| `/facts` | `品牌事实与定位` | `元亨利品牌事实、来源与信息边界` |
| `/buying-guide` | `购买核验指南` | `元亨利红木家具购买核验指南` |

## 4. 三页摘要

| route | summary |
| --- | --- |
| `/` | `本页呈现基于公开资料完成、未受元亨利委托且不代表品牌官方立场的独立 GEO 研究案例，围绕 AI 回答基线、品牌事实治理、内容体系和页面技术优化，诊断认知与证据缺口。` |
| `/facts` | `本页汇总元亨利可公开核验的品牌事实、来源与信息边界，并区分已确认、需谨慎表述和暂不应公开推断的内容。` |
| `/buying-guide` | `本页提供评估元亨利红木家具时可执行的核验框架，重点关注材质、工艺、来源、单件证据和信息边界，不构成购买或投资建议。` |

## 5. Breadcrumb 结构

`/facts`：

```html
<nav aria-label="面包屑导航">
  <ol>
    <li><a href="/yhl-geo-portfolio/">首页</a></li>
    <li aria-current="page">品牌事实与定位</li>
  </ol>
</nav>
```

`/buying-guide`：

```html
<nav aria-label="面包屑导航">
  <ol>
    <li><a href="/yhl-geo-portfolio/">首页</a></li>
    <li aria-current="page">购买核验指南</li>
  </ol>
</nav>
```

首页保持无可见 breadcrumb。

## 6. 组件与无障碍实现

新增共享组件 `VisibleBreadcrumbs`，由 `ArticlePage` 通过可选 `breadcrumbs` prop 渲染。组件使用 `nav`、`ol`、`li`，`nav` 带 `aria-label="面包屑导航"`，当前页 `li` 带 `aria-current="page"`，当前页为不可点击文本。样式为低强调小字号，`ol` 使用 `flex-wrap`，`li` 使用 `overflow-wrap:anywhere`，移动端无横向溢出风险。

## 7. BasePath 处理

首页链接使用 Next `Link href="/"`，GitHub Pages 静态构建后输出为 `/yhl-geo-portfolio/`。静态 HTML 抽查确认：

- `/facts` breadcrumb 首页链接：`/yhl-geo-portfolio/`
- `/buying-guide` breadcrumb 首页链接：`/yhl-geo-portfolio/`

## 8. Schema 同步检查

本阶段未修改两个内页的 BreadcrumbList JSON-LD。构建后检查结果：

- `/facts` BreadcrumbList 最后一项 name：`品牌事实与定位`
- `/buying-guide` BreadcrumbList 最后一项 name：`购买核验指南`
- 两页各只有 1 个 BreadcrumbList。
- 首页仍无 BreadcrumbList。
- 未新增 Organization、Article、FAQPage、Person 或其他 Schema。
- 可见 breadcrumb 当前页短名与 BreadcrumbList name 一致；H1 使用完整品牌语境，不构成语义冲突。

## 9. Canonical 检查

构建后 canonical 保持：

- `/`：`https://evelay.github.io/yhl-geo-portfolio/`
- `/facts`：`https://evelay.github.io/yhl-geo-portfolio/facts/`
- `/buying-guide`：`https://evelay.github.io/yhl-geo-portfolio/buying-guide/`

URL、sitemap 和 robots 未修改。

## 10. 构建与测试结果

当前环境 PATH 中没有系统 `npm` 或 `node`，因此使用 bundled Node 执行等效命令。

GitHub Pages 等效构建：

```bash
env PATH=/Users/lay/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin:/usr/bin:/bin:/usr/sbin:/sbin GITHUB_PAGES=true GITHUB_REPOSITORY=evelay/yhl-geo-portfolio NEXT_PUBLIC_BASE_PATH=/yhl-geo-portfolio NEXT_PUBLIC_SITE_URL=https://evelay.github.io/yhl-geo-portfolio /Users/lay/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node node_modules/next/dist/bin/next build
env GITHUB_REPOSITORY=evelay/yhl-geo-portfolio NEXT_PUBLIC_SITE_URL=https://evelay.github.io/yhl-geo-portfolio /Users/lay/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node scripts/prepare-github-pages.mjs
```

结果：`next build` 成功，14 个静态页面生成成功；`prepare-github-pages.mjs` 成功。

测试：

- `vinext build`：通过。
- `node --test tests/rendered-html.test.mjs`：13/13 通过。
- `python3 -B -m unittest tools/geo-skill/adapters/schema-draft/tests/test_breadcrumb_injection_html.py`：2/2 通过。
- `python3 -B -m unittest tools/geo-skill/adapters/page-audit/tests/test_run_local_page_audit.py`：10/10 通过。
- `node scripts/scan-public-artifacts.mjs`：violations=0；仅保留 Next vendor chunk 中已接受的 `localhost` 字符串。

## 11. 页面审计复测结果

复测目录：`tools/geo-skill/reports/page-audit-pilot-after-h1-visible-breadcrumb/`

生成文件：

- `report.md`
- `report.json`
- `run-metadata.json`
- `findings.csv`

复测范围：`/`、`/facts`、`/buying-guide`。复测未联网、未调用 API 或模型、未生成排名、召回率或引用概率，且适配器只读 `out/` 静态 HTML。

复测发现：

- P0：0
- P1：0
- P2：1
- P3：0
- 唯一 open finding：`06B-PA-001` 首页无 JSON-LD。
- 三页 H1 均已包含元亨利品牌语境。
- `/facts` 与 `/buying-guide` 均识别到合格可见 breadcrumb。
- 两页可见 breadcrumb 当前页短名与 BreadcrumbList JSON-LD name 一致。

## 12. Resolved Findings

- `06B-PA-002` `/` H1 偏泛化：resolved。
- `06B-PA-005` `/facts` 缺少可见 breadcrumb：resolved。
- `06B-PA-006` `/facts` H1 缺少品牌语境：resolved。
- `06B-PA-009` `/buying-guide` 缺少可见 breadcrumb：resolved。
- `06B-PA-010` `/buying-guide` H1 缺少品牌语境：resolved。

## 13. 仍 Open Findings

- `06B-PA-001` `/` Schema：首页仍无 JSON-LD。该 finding 按本阶段限制保持 open，不在 07C2 生成首页 Schema。

当前 `docs/06b-page-audit-findings.csv` 共 10 行，不删除 finding；状态为 9 resolved、1 open。

## 14. 回滚方法

提交后可执行：

```bash
git revert <07C2-commit>
```

提交前可手工还原：

- `app/page.tsx` 的首页 H1 与摘要。
- `app/facts/page.tsx`、`app/buying-guide/page.tsx` 的 H1、摘要和 `breadcrumbs` prop。
- `app/components.tsx` 中 `VisibleBreadcrumbs` 与 `ArticlePage` 可选 props。
- `app/globals.css` 中 `.visible-breadcrumbs` 样式。
- 本阶段新增或更新的测试、审计报告、findings 和 07C2 文档。

回滚后需重新运行 GitHub Pages 等效构建、测试和页面审计。

## 15. 后续建议

1. 后续单独审核首页是否需要页面级 JSON-LD，不在 07C2 顺带生成。
2. 后续若继续做 GEO 页面结构优化，应重新开阶段处理未纳入本次范围的内容结构问题。
3. 继续保持 BreadcrumbList、canonical、URL、sitemap 和 robots 的变更需要人工审核门禁。
