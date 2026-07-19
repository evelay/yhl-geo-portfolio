# 阶段 07A 品牌实体图谱方法说明

## 1. 为什么先做实体图谱再做 Schema

Schema 会把页面事实变成机器可读声明。当前项目先做实体图谱，是为了在写入任何结构化数据前区分品牌、企业主体、材料、工艺风格、内容主题、证据和边界规则，避免把内容主题或推断关系写成确认事实。

## 2. Skill 来源

- 来源仓库：`https://github.com/yaojingang/yao-geo-skills`
- 来源 Skill：`skills/yao-geo-brand-graph`
- 来源 commit：`dc10716d97c40fed0a0a08e538a236b5e16b4822`
- 原许可证：`MIT`

本阶段只采用实体消歧、证据账本、方向性关系和质量门方法，不运行上游联网来源采样、Word/PDF/HTML 渲染、JSON-LD 或 RDF 输出。

## 3. 当前项目适配方式

适配层位于 `tools/geo-skill/adapters/brand-graph/`，使用 Python 标准库离线运行。输出只进入 `docs/` 与 `tools/geo-skill/reports/brand-graph-pilot/`。

## 4. 数据输入边界

唯一品牌数据输入为 `public/downloads/yhl-geo-knowledge-base-public.json`。治理文档只作为规则依据，不从中重新提取未公开品牌事实。禁止读取 `internal-review/`、外部工作簿、first_setup、yhl_geo_portfolio_final、旧版未过滤 JSON、完整文章样稿、完整提示词、PDF/DOCX、原始 AI 回答和人工评分工作簿。

## 5. 证据等级

关系证据状态限定为 `source-confirmed`、`snapshot-supported`、`inferred`、`evidence-gap`。`source-confirmed` 必须拥有明确 `evidence_id`；`inferred` 不能是 `public-safe`；`evidence-gap` 不能进入候选 Schema。

## 6. 实体和关系规则

实体账本记录 canonical name、display name、type、aliases、evidence、confidence、publication safety 和 ambiguity risk。关系账本记录 subject、predicate、object、evidence_ids、evidence_status、confidence、publication_safety、解释边界、禁止解释和人工审核要求。所有关系初始状态均为 `candidate`。

## 7. 消歧逻辑

重点处理品牌/企业主体、京作工艺/品牌身份、紫檀/全部产品、黄花梨/品牌定位、白酸枝/产品关系、明式/具体年代、清式/具体年代。缺少 evidence_id 时只记录缺口，不扩写成事实。

## 8. 人工审核节点

进入 07B 前，需人工确认品牌与企业主体关系、官网和公开账号关系、京作是否有公开 evidence_id、材料主题是否只作为内容主题、明式/清式是否只作为风格概念，以及哪些 public-safe 关系适合落到页面正文和 Schema。

## 9. 不允许推断的内容

不得推断创始人、成立年份、国家级资质、行业排名、第一/顶级/领先、奖项、销售额、客户数量、门店数量、所有产品材质、独家材料关系、收藏升值保证、投资回报、官方委托关系或已实施 GEO 增长结果。

## 10. 与品牌事实知识库的关系

公开 JSON 是从品牌事实知识库导出的安全过滤快照，不是事实 canonical。本阶段只用它做隔离试点，不反向修改主源，也不修改 `app/data.ts`。

## 11. 与后续 07B Schema 的关系

`docs/07a-schema-input-candidates.csv` 只是候选输入清单。只有 source-confirmed 或 snapshot-supported、public-safe、high/medium confidence、无消歧冲突且不属于禁止事实的项目，才可标记 `eligible_for_07b=yes`。

## 12. 回滚方式

本阶段只新增或修改 `docs/` 与 `tools/geo-skill/`。如需回滚，可 revert 本阶段 commit，或删除 `docs/07a-*` 与 `tools/geo-skill/adapters/brand-graph/`、`tools/geo-skill/upstream/yao-geo-brand-graph/`、`tools/geo-skill/reports/brand-graph-pilot/`，不会影响 `app/`、`public/` 或外部 canonical 工作簿。
