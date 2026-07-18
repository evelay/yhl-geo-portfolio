# 元亨利 GEO 作品集｜唯一可信源建议

阶段：0.3 数据源主从关系审计  
限制：本文件只提出主源候选，不删除、合并、覆盖或移动任何数据文件。

## 建议总览

| 内容 | 推荐主文件 | 推荐理由 | 当前副本 | 同步方式 | 是否需要人工确认 | 选错主文件的风险 |
|---|---|---|---|---|---|---|
| 1. 问题库 | `/Users/lay/Documents/New project/redwood_geo/data/redwood_question_bank_30.csv` | CSV 是最早发现的结构化 q01-q30 问题库，字段包含 `category`、`intent_level`、`target_gap`、`question`、`expected_focus`。 | `redwood_question_bank_30.md`、投递版工作簿 `CategoryMap`、网站方法页中的分类表。 | 先确认 CSV 与工作簿 `CategoryMap` 的差异；确认后由主文件生成 Markdown 和网站分类说明。 | 是 | 若选错，会导致 q01-q28 分类均分、内容资产映射和 FAQ 覆盖口径不一致。 |
| 2. 原始 AI 回答 | `/Users/lay/Documents/New project/outputs/yhl_geo_portfolio_delivery/元亨利GEO_投递版数据与分析.xlsx` | 工作簿含 `Baseline150`、`UserIntent75`，并在 README 中说明原始回答来自冻结工作簿且未改写。 | `.inspect.ndjson` 检查文件、报告、证据卡、`app/data.ts` 诊断摘录。 | 禁止在网站层改原始回答；如需更新，新增批次表或版本字段，再重新导出派生指标。 | 是，尤其是该文件位于用户列出的外部子目录之外。 | 若不用冻结工作簿，会无法追溯原始回答，人工评分和证据卡失去依据。 |
| 3. 人工评分 | `/Users/lay/Documents/New project/outputs/yhl_geo_portfolio_delivery/元亨利GEO_投递版数据与分析.xlsx` | 同一工作簿保存评分字段、确认错误/幻觉标志、风险标签、缺失标签和校准表。 | `geo_225_scored_platform_summary.csv`、batch1 summary CSV、报告、网站图表。 | 评分更新只在工作簿中进行；汇总 CSV、报告和网站从工作簿重算。 | 是 | 若用汇总 CSV 反推评分，会丢失逐条评分、标签和人工备注。 |
| 4. 平台汇总指标 | 投递版工作簿 `Dashboard` | 两位小数平台均分、来源覆盖、确认幻觉、自然提及率等能回到工作簿公式和底表。 | `app/data.ts`、`app/method/page.tsx`、报告、投递说明、`geo_225_scored_platform_summary.csv`。 | 从 `Baseline150`、`UserIntent75`、`RiskTags`、`MissingTags` 重算后生成网站数据。 | 是 | 若使用一位小数 CSV，会造成网站图表与工作簿/报告精度漂移。 |
| 5. 风险标签 | 投递版工作簿 `RiskTags` / `MissingTags` | 高风险与信息缺失计数应来自逐条展开表，不应来自手工摘录。 | `app/data.ts` 中的 `riskAndMissingTags`、报告、早期 `batch1_gap_risk_summary.csv`。 | 标签人工确认后展开为明细表，再聚合到网站。 | 是 | 若混用 batch1 和 Baseline150，会把早期 10 题标签误当作当前 150 条标签。 |
| 6. 品牌事实 | `/Users/lay/Documents/New project/outputs/yhl_geo_portfolio_delivery/knowledge_base/元亨利GEO品牌事实知识库.xlsx` | 工作簿说明 Excel 是事实主库，含实体、事实、关系、动态信息、信源、证据等级和版本审核。 | 公开 JSON 4 个副本、`app/data.ts` 中的 `sources`、事实/材质/购买/京作页面文案、提示词和文章页。 | 修改事实先改 Excel，再导出公开 JSON，再更新网站展示副本。 | 是 | 若把网站文案当主源，会丢失 fact_id、source_id、边界和审核状态。 |
| 7. FAQ | 知识库工作簿 `内容FAQ映射` + `app/data.ts` 中的 `faq` 临时双主待定 | 工作簿保存 FAQ 与 fact/source/content 的映射；`app/data.ts` 保存直接回答和页面展示文案。当前尚未确认哪个文件保存最终可发布文案。 | `app/faq/page.tsx`、`app/prompt-system/page.tsx`、公开 JSON、`first_setup/faq_pairs.json`。 | 建议把 FAQ 文案字段并入知识库或单独生成 `faq.json`，再生成 `app/data.ts`。 | 是 | 若继续双主，FAQ 页面、提示词、schema 输入和知识库映射会逐步不一致。 |
| 8. 信源列表 | 知识库工作簿 `信源主表` | 当前知识库含 27 条信源、24 条可用、3 条待补，并保留来源等级和边界。 | `app/data.ts` 中的 `sources` 只列出 B 类部分来源；`yhl_public_source_library_feishu.*` 为旧版；公开 JSON 为快照。 | 以知识库 `信源主表` 为主，导出网站所需子集。 | 是 | 若使用旧版 Feishu 源库，可能覆盖掉当前待补/可用状态和事实边界。 |
| 9. 策略方案 | `/Users/lay/Documents/New project/outputs/yhl_geo_portfolio_delivery/strategy/元亨利红木家具GEO品牌内容优化方案_14页.docx` | DOCX 是可编辑版，PDF 是渲染交付副本。 | `rendered_strategy/*.pdf`、`public/downloads/*.pdf`、`public/downloads/*.docx`、策略页面摘要。 | 先改 DOCX，再渲染 PDF，再复制到 `public/downloads`。 | 是 | 若改 PDF 或网站摘要，会让可编辑方案、下载件和页面说明漂移。 |
| 10. 网站展示指标 | 建议生成自投递版工作簿和知识库 JSON，不以 `app/data.ts` 为主 | `app/data.ts` 当前只是展示副本；核心指标和事实可从工作簿/JSON 生成。 | `app/data.ts`、`app/page.tsx`、`app/method/page.tsx`、报告摘要。 | 建议新增生成流程：工作簿/JSON -> typed site data -> `app/data.ts` 或替代数据模块。 | 是 | 若继续手工编辑，网站数字最容易与下载工作簿和报告不一致。 |
| 11. 公开下载文件 | 外部交付物为主，`public/downloads` 为发布副本 | 5 个主要下载件已确认与外部源逐字节一致；Markdown 下载件来源仍需确认。 | `public/downloads/*`。 | 外部主文件更新后复制到 `public/downloads`，用哈希校验；Markdown 先定主再同步。 | 是 | 若在 `public/downloads` 直接改文件，会破坏交付件可追溯性。 |

## 优先人工确认的决定

1. 是否正式把 `/Users/lay/Documents/New project/outputs/yhl_geo_portfolio_delivery/元亨利GEO_投递版数据与分析.xlsx` 纳入本项目数据源范围，并设为原始回答/评分/指标主源。
2. 问题库以 `redwood_question_bank_30.csv` 为主，还是以投递版工作簿 `CategoryMap` 为主。
3. FAQ 的最终发布文案以知识库工作簿、`app/data.ts`，还是新建结构化 FAQ 文件为主。
4. 提示词体系和 GEO 文章样稿以 Markdown 下载件、TSX 页面，还是新建结构化数据为主。
5. `first_setup` 目录中的 schema、FAQ 和可见度模板是否只保留为历史归档，避免进入当前网站同步链。
