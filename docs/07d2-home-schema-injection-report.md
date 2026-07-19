# 阶段 07D2 首页 Schema 注入报告

日期：2026-07-19  
分支：`refactor/portfolio-v2`

## 1. 本阶段范围

本阶段只处理首页 `/` 的结构化数据注入，将 07D1 已评估并经人工确认的 `WebSite + WebPage` @graph 写入首页静态 HTML。

未处理 Organization、Brand、Person、SearchAction、Article、FAQPage、BreadcrumbList 或其他 Schema。

## 2. 人工批准决定

- 方案：`WebSite + WebPage`
- 结构：一个 `@graph`，包含 `WebSite` 与 `WebPage`
- `name`：使用当前首页 H1
- `description`：使用当前首页可见摘要原文
- canonical：保持 `https://evelay.github.io/yhl-geo-portfolio/`
- 不设置 `publisher`
- 不生成或关联 `Organization`、`Brand`、`Person`、`author`、`creator`、`copyrightHolder`、`accountablePerson`、`logo`、`sameAs`
- 不设置 `SearchAction`
- 不给首页生成 `BreadcrumbList`

## 3. 推荐方案

采用 `docs/07d1-home-schema-options.csv` 中的推荐方案 `07D1-B`：`WebSite + WebPage`。该方案能表达站点入口和首页页面事实，同时不引入未确认的品牌主体、发布方、作者、搜索动作或官方关系。

## 4. 修改文件

- `app/page.tsx`
- `tests/rendered-html.test.mjs`
- `tools/geo-skill/adapters/schema-draft/build_home_schema_drafts.py`
- `tools/geo-skill/adapters/schema-draft/tests/test_breadcrumb_injection_html.py`
- `tools/geo-skill/adapters/page-audit/run_local_page_audit.py`
- `tools/geo-skill/adapters/page-audit/tests/test_run_local_page_audit.py`
- `docs/07d1-home-schema-human-review.md`
- `docs/07d1-home-schema-options.csv`
- `docs/06b-page-audit-findings.csv`
- `tools/geo-skill/reports/page-audit-pilot-after-home-schema/`
- `docs/07d2-home-schema-injection-report.md`
- `docs/07d2-home-schema-before-after.csv`

## 5. 最终 JSON-LD

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "WebSite",
      "@id": "https://evelay.github.io/yhl-geo-portfolio/#website",
      "url": "https://evelay.github.io/yhl-geo-portfolio/",
      "name": "元亨利红木家具 GEO 诊断与可核验内容体系",
      "description": "本页呈现基于公开资料完成、未受元亨利委托且不代表品牌官方立场的独立 GEO 研究案例，围绕 AI 回答基线、品牌事实治理、内容体系和页面技术优化，诊断认知与证据缺口。",
      "inLanguage": "zh-CN"
    },
    {
      "@type": "WebPage",
      "@id": "https://evelay.github.io/yhl-geo-portfolio/#webpage",
      "url": "https://evelay.github.io/yhl-geo-portfolio/",
      "name": "元亨利红木家具 GEO 诊断与可核验内容体系",
      "description": "本页呈现基于公开资料完成、未受元亨利委托且不代表品牌官方立场的独立 GEO 研究案例，围绕 AI 回答基线、品牌事实治理、内容体系和页面技术优化，诊断认知与证据缺口。",
      "inLanguage": "zh-CN",
      "isPartOf": {
        "@id": "https://evelay.github.io/yhl-geo-portfolio/#website"
      }
    }
  ]
}
```

## 6. 字段来源

- `@context`：Schema.org 固定上下文。
- `@type`：07D1 推荐方案与 07D2 人工批准决定。
- `@id`：首页 canonical 加稳定 fragment。
- `url`：首页 canonical。
- `name`：首页 H1 `元亨利红木家具 GEO 诊断与可核验内容体系`。
- `description`：首页可见摘要原文。
- `inLanguage`：`app/layout.tsx` 渲染的 `<html lang="zh-CN">`。
- `WebPage.isPartOf`：指向同一 @graph 内的 WebSite `@id`。

## 7. 为什么未使用 Organization

07A2 已将 `Organization` 延后。当前公开证据不足以安全合并品牌、企业主体、官网主体、账号、法律责任或官方委托关系。首页是独立 GEO 研究作品集，不是元亨利官方网站或官方项目，因此本阶段不生成 `Organization`。

## 8. 为什么未设置 publisher

把元亨利或任何未确认主体设为 `publisher` 会暗示页面由该主体发布或承担责任，与首页“未受元亨利委托且不代表品牌官方立场”的声明冲突。当前也没有经确认的发布组织或个人作者字段，因此不设置 `publisher`。

## 9. 为什么未设置 SearchAction

当前网站没有真实站内搜索功能。设置 `SearchAction` 会声明不存在的搜索能力，因此本阶段不生成 `potentialAction` 或 `SearchAction`。

## 10. 静态构建验证

当前环境无系统 `npm` 或 `node`。真实执行命令为 bundled Node 等效命令：

```bash
env PATH=/Users/lay/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin:/usr/bin:/bin:/usr/sbin:/sbin GITHUB_PAGES=true GITHUB_REPOSITORY=evelay/yhl-geo-portfolio NEXT_PUBLIC_BASE_PATH=/yhl-geo-portfolio NEXT_PUBLIC_SITE_URL=https://evelay.github.io/yhl-geo-portfolio /Users/lay/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node node_modules/next/dist/bin/next build
env GITHUB_REPOSITORY=evelay/yhl-geo-portfolio NEXT_PUBLIC_SITE_URL=https://evelay.github.io/yhl-geo-portfolio /Users/lay/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node scripts/prepare-github-pages.mjs
```

结果：`next build` 成功，14 个静态页面生成成功；`prepare-github-pages.mjs` 成功。

## 11. Schema 解析验证

`out/index.html` 验证结果：

- JSON-LD script 数量：1
- `@context`：`https://schema.org`
- `@graph` 节点数量：2
- `WebSite`：1
- `WebPage`：1
- `WebPage.isPartOf`：指向 `https://evelay.github.io/yhl-geo-portfolio/#website`
- `Organization`、`Brand`、`Person`、`SearchAction`、`BreadcrumbList`、`Article`、`FAQPage`、`Product`、`Offer`、`Review`、`AggregateRating`：0

## 12. 页面内容一致性

首页 H1、可见摘要、canonical、title 和 meta description 均未修改。Schema 中两个节点的 `url`、`name`、`description` 与静态 HTML 中的 canonical、H1 和可见摘要一致。

## 13. 页面审计复测

复测目录：`tools/geo-skill/reports/page-audit-pilot-after-home-schema/`

生成文件：

- `report.md`
- `report.json`
- `run-metadata.json`
- `findings.csv`

复测结果：

- P0：0
- P1：0
- P2：0
- P3：0
- total open findings：0

报告明确识别首页 `WebSite + WebPage` @graph，确认字段与首页可见页面一致，并确认 `/facts` 与 `/buying-guide` 的 `BreadcrumbList` 仍然存在。报告未因为首页有 JSON-LD 就判断整个项目 GEO 已完成。

## 14. Finding 前后变化

- `06B-PA-001`：`open` -> `resolved`
- 依据：首页 Schema 注入成功；静态构建成功；JSON-LD 可解析；字段与页面一致；测试通过；页面审计复测通过。
- 其他历史 finding 状态未改动。

## 15. 未修改事项

未修改：

- `app/layout.tsx`
- `app/data.ts`
- `app/components.tsx`
- `app/globals.css`
- `public/`
- sitemap
- robots
- canonical 配置
- 首页 H1、摘要、URL、title、meta description
- `/facts` 与 `/buying-guide` 的 BreadcrumbList
- 其他页面正文

未读取 `internal-review` 内容；未调用 API 或模型；未安装新依赖；未创建 PR；未 push。

## 16. 回滚方法

提交后可执行：

```bash
git revert <07D2-commit>
```

若提交前手工回滚，需移除 `app/page.tsx` 中的 `homeSchema`、`homeSchemaJson` 和首页 `<script type="application/ld+json">`，并还原本阶段新增或更新的测试、审计报告、finding 与文档。

## 17. 后续建议

1. 继续保持 Organization、Brand、Person 与 publisher 独立人工审核，不在首页 Schema 中顺带生成。
2. 若后续处理其他页面 Schema，继续采用字段白名单、页面可见证据和静态 HTML 解析测试。
3. 后续 GEO 内容结构优化应单独开阶段，不把首页 JSON-LD 注入解读为项目整体完成。
