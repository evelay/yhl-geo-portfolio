# 阶段 07B2 BreadcrumbList 注入与复测报告

日期：2026-07-19

## 1. 本阶段范围

本阶段只把已验证并经人工确认的两个 `BreadcrumbList` JSON-LD 草稿注入：

- `/facts`
- `/buying-guide`

未修改 H1、页面正文、可见 breadcrumb、视觉设计、canonical、title、description、`app/data.ts`、`globals.css`、`public/`、sitemap 或 robots。

## 2. 人工批准决定

人工审核状态已在 `docs/07b-breadcrumb-human-review.md` 标记为 `approved-for-injection`。

- 根节点名称：`首页`
- `/facts` 页面名称：`品牌事实与定位`
- `/buying-guide` 页面名称：`购买核验指南`
- `/facts` 层级：`首页 > 品牌事实与定位`
- `/buying-guide` 层级：`首页 > 购买核验指南`
- 当前网站没有真实存在的“知识中心”中间路由，因此未增加该层级。
- 不为首页生成 `BreadcrumbList`。
- 不生成 Organization、Brand、Person、Article、FAQPage、Product、Offer、Review 或 AggregateRating。

## 3. 修改文件

网站页面文件：

- `app/facts/page.tsx`
- `app/buying-guide/page.tsx`

审计、测试和记录文件：

- `docs/07b-breadcrumb-human-review.md`
- `docs/06b-page-audit-findings.csv`
- `docs/07b-schema-draft-ledger.csv`
- `docs/07b2-breadcrumb-injection-report.md`
- `docs/07b2-schema-before-after.csv`
- `tools/geo-skill/adapters/schema-draft/tests/test_breadcrumb_injection_html.py`
- `tools/geo-skill/adapters/page-audit/run_local_page_audit.py`
- `tools/geo-skill/adapters/page-audit/tests/test_run_local_page_audit.py`
- `tools/geo-skill/reports/page-audit-pilot-after-breadcrumb-schema/`

## 4. 注入方式

两个页面均使用 server component 中的固定安全数据对象，并通过：

```tsx
JSON.stringify(breadcrumbSchema).replace(/</g, "\\u003c")
```

生成 JSON-LD 字符串，再输出：

```tsx
<script type="application/ld+json" dangerouslySetInnerHTML={{ __html: breadcrumbSchemaJson }} />
```

未从 `tools/` 或外部文件运行时读取草稿，未引入新依赖，未添加共享视觉组件。

## 5. BreadcrumbList 内容

`/facts`：

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "首页",
      "item": "https://evelay.github.io/yhl-geo-portfolio/"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "品牌事实与定位",
      "item": "https://evelay.github.io/yhl-geo-portfolio/facts/"
    }
  ]
}
```

`/buying-guide`：

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "首页",
      "item": "https://evelay.github.io/yhl-geo-portfolio/"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "购买核验指南",
      "item": "https://evelay.github.io/yhl-geo-portfolio/buying-guide/"
    }
  ]
}
```

## 6. Canonical 对齐验证

- `/facts` canonical 保持 `https://evelay.github.io/yhl-geo-portfolio/facts/`，与 position 2 item 完全一致。
- `/buying-guide` canonical 保持 `https://evelay.github.io/yhl-geo-portfolio/buying-guide/`，与 position 2 item 完全一致。
- 首页根节点 item 为 `https://evelay.github.io/yhl-geo-portfolio/`。

## 7. H1 对齐验证

- `/facts` H1 保持 `品牌事实与定位`，与 position 2 name 一致。
- `/buying-guide` H1 保持 `购买核验指南`，与 position 2 name 一致。
- 首页 H1 保持 `让红木家具信息变得可回答、可核验`，未注入首页 `BreadcrumbList`。

## 8. 构建验证

系统 PATH 中没有 `npm` 或 `node`。本阶段使用 bundled Node 执行 `package.json` 中 `build:github` 的等效步骤：

```bash
GITHUB_PAGES=true GITHUB_REPOSITORY=evelay/yhl-geo-portfolio NEXT_PUBLIC_BASE_PATH=/yhl-geo-portfolio NEXT_PUBLIC_SITE_URL=https://evelay.github.io/yhl-geo-portfolio node node_modules/next/dist/bin/next build
GITHUB_REPOSITORY=evelay/yhl-geo-portfolio NEXT_PUBLIC_SITE_URL=https://evelay.github.io/yhl-geo-portfolio node scripts/prepare-github-pages.mjs
```

结果：

- `next build` 成功。
- 14 个静态页面生成成功。
- `out/facts/index.html` 已生成。
- `out/buying-guide/index.html` 已生成。
- `out/index.html` 已生成。
- `out/facts/index.html` 解析到 1 个 `application/ld+json` script，类型为 `BreadcrumbList`。
- `out/buying-guide/index.html` 解析到 1 个 `application/ld+json` script，类型为 `BreadcrumbList`。
- 首页解析到 0 个 `BreadcrumbList`。
- 三个审计页面 canonical 与 H1 保持不变。

全量 `out/` 污染扫描说明：

- 三个审计 HTML 页面未发现 `chatgpt.site`、`localhost`、`/Users/` 或重复 basePath。
- 全量 `out/` 仍命中既有非本阶段项：`out/downloads/manifest.json` 由已存在的 `public/downloads/manifest.json` 复制而来，含两个 `/Users/` 标记；一个 Next 静态 chunk 含 vendor/polyfill 中的通用 `localhost` 字符串。
- 上述两项不是本阶段注入产生；由于本阶段禁止修改 `public/` 和非 Breadcrumb 范围，已记录但未处理。

## 9. Schema 解析验证

新增回归测试：

```bash
python3 -B -m unittest tools/geo-skill/adapters/schema-draft/tests/test_breadcrumb_injection_html.py
```

覆盖：

- `/facts` 和 `/buying-guide` 各有且只有一个实际 JSON-LD `BreadcrumbList`。
- JSON-LD 可解析。
- name 与 H1 一致。
- item 与 canonical 一致。
- 首页无 `BreadcrumbList`。
- 两个目标页无其他解析到的 Schema 类型。
- 目标 HTML 无本地绝对路径、旧域名、`localhost` 或重复 basePath。

## 10. 页面审计复测

复测目录：

- `tools/geo-skill/reports/page-audit-pilot-after-breadcrumb-schema/`

生成文件：

- `report.md`
- `report.json`
- `run-metadata.json`
- `findings.csv`

复测范围仍为：

- `/`
- `/facts`
- `/buying-guide`

复测结果：

- P0：0
- P1：0
- P2：4
- P3：2
- Schema finding：1，仅首页仍无 JSON-LD。
- `/facts` 已识别 `BreadcrumbList` 数量 1。
- `/buying-guide` 已识别 `BreadcrumbList` 数量 1。
- 两个内容页可见 breadcrumb 标记仍未处理，相关 P3 finding 保持 open。

复测未联网、未调用 API 或模型、未读取 `internal-review/`，也未生成 AI 排名、召回率、引用概率或提升预测。

## 11. Findings 修复前后对比

更新 `docs/06b-page-audit-findings.csv`：

- `06B-PA-004` `/facts` Schema：`open` -> `resolved`
- `06B-PA-008` `/buying-guide` Schema：`open` -> `resolved`

保持 open：

- `06B-PA-001` 首页 Schema：首页仍无 JSON-LD。
- `06B-PA-002` 首页 H1 语境。
- `06B-PA-005` `/facts` 可见 breadcrumb/面包屑标记。
- `06B-PA-006` `/facts` H1 语境。
- `06B-PA-009` `/buying-guide` 可见 breadcrumb/面包屑标记。
- `06B-PA-010` `/buying-guide` H1 语境。

未删除任何行，未修改 canonical 已 resolved finding。

## 12. 首页为什么仍不处理

07B 和 07B2 的人工决定明确：首页只作为 breadcrumb position 1 根节点，不为首页自身生成独立 `BreadcrumbList`。首页页面级 JSON-LD 是否需要生成，需后续独立审核，不能在本阶段顺带处理。

## 13. 为什么未生成其他 Schema

`BreadcrumbList` 只表达页面层级与 canonical URL，不声明品牌主体、企业主体、人物、材料、产品、价格、评价或背书关系。Organization、Brand、Person、Article、FAQPage、Product、Offer、Review 和 AggregateRating 都需要独立证据链、页面匹配和人工审核，因此本阶段不生成。

## 14. 回滚方式

提交后可执行：

```bash
git revert <07B2-commit>
```

提交前回滚可还原：

- `app/facts/page.tsx` 中新增的 `breadcrumbSchema`、`breadcrumbSchemaJson` 和 JSON-LD script。
- `app/buying-guide/page.tsx` 中新增的 `breadcrumbSchema`、`breadcrumbSchemaJson` 和 JSON-LD script。
- `docs/06b-page-audit-findings.csv` 中 `06B-PA-004`、`06B-PA-008` 的状态和 notes。
- `docs/07b-schema-draft-ledger.csv` 中两个草稿的 injected 状态。
- 本阶段新增报告、测试和复测目录。

## 15. 后续建议

1. 后续单独处理首页是否需要页面级 JSON-LD。
2. 后续单独处理可见 breadcrumb UI 或语义化面包屑标记。
3. 后续单独处理 H1 或紧邻摘要中的品牌实体可抽取性。
4. 后续在新的治理阶段处理 `public/downloads/manifest.json` 中既有本地路径来源字段。
5. 后续在独立 Schema 阶段评估 Organization、Article、FAQPage 等类型。
