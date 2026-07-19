# 阶段 07D1 首页 Schema 人工审核清单

日期：2026-07-19

状态：`pending-human-review`

本阶段只生成隔离草稿，不替用户批准注入。

## 待确认事项

1. 最终使用哪一种 Schema 方案？
   - `WebSite only`
   - `WebSite + WebPage`
   - `WebSite + CollectionPage`

2. `name` 是否使用当前首页 H1？
   - 建议值：`元亨利红木家具 GEO 诊断与可核验内容体系`
   - 当前状态：待确认

3. `description` 是否使用当前首页摘要原文？
   - 建议值：`本页呈现基于公开资料完成、未受元亨利委托且不代表品牌官方立场的独立 GEO 研究案例，围绕 AI 回答基线、品牌事实治理、内容体系和页面技术优化，诊断认知与证据缺口。`
   - 当前状态：待确认

4. 是否同意不设置 `publisher`？
   - 建议：同意不设置
   - 当前状态：待确认

5. 是否同意不设置 `Organization`、`Brand`、`Person`？
   - 建议：同意不设置
   - 当前状态：待确认

6. 是否同意不设置 `SearchAction`？
   - 当前首页没有真实站内搜索功能。
   - 建议：同意不设置
   - 当前状态：待确认

7. 是否允许下一阶段 07D2 注入首页？
   - 07D1 不注入。
   - 当前状态：待确认

8. URL 和 canonical 是否保持不变？
   - 建议保持：`https://evelay.github.io/yhl-geo-portfolio/`
   - 当前状态：待确认

## 07D2 前置提醒

若进入 07D2，需要重新检查分支、upstream、ahead/behind、工作区干净状态、首页 H1、description、canonical、JSON-LD 数量、禁用字段、禁用类型和 `06B-PA-001` 状态。
