# 阶段 07D1 首页 Schema 人工审核清单

日期：2026-07-19

状态：`approved-for-injection`

本记录已根据 07D2 人工确认决定更新，允许仅将首页 `WebSite + WebPage` @graph 注入首页。

## 07D2 人工批准决定

- selected option：`WebSite + WebPage`
- approval：`approved`
- injection status：`injected`
- validation status：`valid`
- page audit status：`passed`
- 标记：`approved-for-injection`

## 已确认事项

1. 最终使用哪一种 Schema 方案？
   - 采用：`WebSite + WebPage`
   - 使用一个 `@graph`，同时包含 `WebSite` 与 `WebPage`。

2. `name` 是否使用当前首页 H1？
   - 确认值：`元亨利红木家具 GEO 诊断与可核验内容体系`
   - 当前状态：已确认

3. `description` 是否使用当前首页摘要原文？
   - 确认值：`本页呈现基于公开资料完成、未受元亨利委托且不代表品牌官方立场的独立 GEO 研究案例，围绕 AI 回答基线、品牌事实治理、内容体系和页面技术优化，诊断认知与证据缺口。`
   - 当前状态：已确认

4. 是否同意不设置 `publisher`？
   - 决定：不设置
   - 当前状态：已确认

5. 是否同意不设置 `Organization`、`Brand`、`Person`？
   - 决定：不设置 `Organization`、`Brand`、`Person`
   - 当前状态：已确认

6. 是否同意不设置 `SearchAction`？
   - 当前首页没有真实站内搜索功能。
   - 决定：不设置
   - 当前状态：已确认

7. 是否允许下一阶段 07D2 注入首页？
   - 决定：允许 07D2 注入首页。
   - 当前状态：已批准

8. URL 和 canonical 是否保持不变？
   - 确认保持：`https://evelay.github.io/yhl-geo-portfolio/`
   - 当前状态：已确认

## 禁用字段与主体

07D2 注入不得生成或关联：

- `Organization`
- `Brand`
- `Person`
- `author`
- `creator`
- `copyrightHolder`
- `accountablePerson`
- `publisher`
- `logo`
- `sameAs`
- `SearchAction`
- 首页 `BreadcrumbList`

## 07D2 实施结果

- 注入文件：`app/page.tsx`
- 注入方式：固定对象 + `JSON.stringify` + `<` 转义 + 静态 `application/ld+json`
- 最终 Schema：一个 `@graph`，包含 `WebSite` 与 `WebPage`
- 构建状态：GitHub Pages 等效构建成功，14 个静态页面生成成功
- 验证状态：`valid`
- 页面审计状态：`passed`
- 复测报告：`tools/geo-skill/reports/page-audit-pilot-after-home-schema/report.json`
- finding：`06B-PA-001` 已更新为 `resolved`
