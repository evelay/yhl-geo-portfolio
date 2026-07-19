# 元亨利 GEO 作品集｜数据治理决定

阶段：0.3B 确认并锁定唯一可信数据源
日期：2026-07-19
范围：只记录数据治理决定；不迁移、不覆盖、不删除任何数据文件。

## 1. 数据治理目标

本项目的数据治理目标是把“主源、网站展示副本、交付副本、派生文件、归档文件”分开管理，避免网站正文、下载文件、早期测试文件或构建产物反向成为事实来源。

核心原则：

- canonical 只能存在于明确指定的主源文件中。
- website-copy 只能服务网站展示，不承担事实、评分或指标裁决职责。
- delivery 只能作为交付或下载副本，不在副本中直接修改事实。
- derived 必须能从 canonical 或经确认的工作源重新生成。
- archive 和 outdated 文件不得进入当前计算、网站同步和 GEO Skill 正式输入链路。

## 2. 已确认 canonical

| 数据类别 | canonical 文件 | 外部绝对路径 | 本阶段决定 |
|---|---|---|---|
| 原始回答、人工评分、核心指标 | 投递版数据与分析工作簿 | `/Users/lay/Documents/New project/outputs/yhl_geo_portfolio_delivery/元亨利GEO_投递版数据与分析.xlsx` | canonical |
| 问题库 | Redwood 30 题问题库 CSV | `/Users/lay/Documents/New project/redwood_geo/data/redwood_question_bank_30.csv` | canonical |
| 品牌事实、信源、FAQ 映射 | 品牌事实知识库工作簿 | `/Users/lay/Documents/New project/outputs/yhl_geo_portfolio_delivery/knowledge_base/元亨利GEO品牌事实知识库.xlsx` | canonical |
| 企业提示词体系 | Markdown 源文件 | `/Users/lay/Documents/New project/outputs/yhl_geo_portfolio_delivery/website/internal-review/downloads/yhl-geo-enterprise-prompt-system.md` | canonical，当前 internal-review，不公开下载 |
| GEO 文章矩阵 | Markdown 源文件 | `/Users/lay/Documents/New project/outputs/yhl_geo_portfolio_delivery/website/internal-review/downloads/yhl-geo-article-matrix.md` | canonical，当前 internal-review，不公开下载 |
| GEO 完整文章样稿 | Markdown 源文件 | `/Users/lay/Documents/New project/outputs/yhl_geo_portfolio_delivery/website/internal-review/downloads/yhl-geo-full-article-samples.md` | canonical，当前 internal-review，不公开下载 |
| 90 天内容执行计划 | 90 天内容执行工作簿 | `/Users/lay/Documents/New project/outputs/yhl_geo_portfolio_delivery/strategy/元亨利红木家具GEO_90天内容执行工作簿.xlsx` | canonical |

## 3. 每类数据的主从角色

### 原始回答、人工评分和核心指标

- canonical：`/Users/lay/Documents/New project/outputs/yhl_geo_portfolio_delivery/元亨利GEO_投递版数据与分析.xlsx`
- website-copy：`/Users/lay/Documents/New project/outputs/yhl_geo_portfolio_delivery/website/app/data.ts` 中的指标、诊断、FAQ 引用和展示摘要
- delivery：`public/downloads` 中面向下载的交付副本
- derived：平台汇总、图表、`.inspect.ndjson`、报告中的指标摘录、网站展示图表数据
- archive 或 outdated：早期 batch1、old10、first_setup、final 版本中的测试文件和汇总文件

不得修改投递版数据与分析工作簿；原始回答、人工评分、风险标签、缺失标签和核心指标只能以该工作簿为正式依据。

### 问题库

- canonical：`/Users/lay/Documents/New project/redwood_geo/data/redwood_question_bank_30.csv`
- working / duplicate：投递版数据与分析工作簿中的 `CategoryMap`
- derived：由问题库和评分数据生成的分类汇总、页面展示表和图表
- archive 或 outdated：早期 batch1、old10、first_setup、final 版本中的问题模板或复测模板

只读比对显示 CSV 与 `CategoryMap` 的 `question_id` 和问题文本完全一致，均为 30 条；CSV 可以确定为问题库 canonical。`CategoryMap` 的分类字段是作品集展示用分组，作为 working / duplicate 保留。

### 品牌事实、信源和 FAQ

- canonical：`/Users/lay/Documents/New project/outputs/yhl_geo_portfolio_delivery/knowledge_base/元亨利GEO品牌事实知识库.xlsx`
- derived：公开知识库 JSON，包括外部快照和网站内 JSON 副本
- website-copy：`app/data.ts` 中的品牌事实、FAQ、来源子集，以及相关 TSX 页面展示文案
- delivery：`public/downloads/yhl-geo-brand-fact-knowledge-base.xlsx`、`public/downloads/yhl-geo-knowledge-base-public.json`

当前四份公开知识库 JSON 内容一致，但它们仍然是公开快照副本，不得分别标记为 canonical。

### 提示词体系和 GEO 文章样稿

角色规则：

- Markdown 源文件：canonical，当前位于 `internal-review/downloads`，不得作为公开下载素材
- TSX 页面内容：website-copy 或 presentation
- 构建后的 HTML：derived

当前对应关系：

| 内容 | Markdown canonical | TSX website-copy / presentation | 状态 |
|---|---|---|---|
| 企业提示词体系 | `internal-review/downloads/yhl-geo-enterprise-prompt-system.md` | `app/prompt-system/page.tsx` | 已确认对应；完整版本不公开 |
| GEO 文章矩阵 | `internal-review/downloads/yhl-geo-article-matrix.md` | `app/geo-articles/page.tsx` | 已确认对应；继续审核 |
| GEO 完整文章样稿 | `internal-review/downloads/yhl-geo-full-article-samples.md` | `app/geo-articles/page.tsx` | 已确认对应；完整正文不公开 |

本次检查未发现“只有 TSX、没有 Markdown”的提示词体系或 GEO 文章样稿项；因此本类当前没有 `missing-canonical-source` 项。

### 90 天策略计划

- canonical：`/Users/lay/Documents/New project/outputs/yhl_geo_portfolio_delivery/strategy/元亨利红木家具GEO_90天内容执行工作簿.xlsx`
- website-copy：网站策略页面和 `app/data.ts` 中的策略、路线图、内容资产摘要
- delivery 或 derived：PDF、DOCX、截图、渲染预览、public 下载副本

### first_setup

目录：`/Users/lay/Documents/New project/outputs/yhl_geo_first_setup_20260718`

统一角色：archive。

不得作为以下内容的数据来源：

- 当前问题库
- 当前品牌事实
- 当前指标
- 当前网站展示
- 当前 GEO Skill 正式输入

### final 早期版本

目录：`/Users/lay/Documents/New project/outputs/yhl_geo_portfolio_final`

统一角色：archive。

只有经过明确人工确认的内容，才能迁移到当前 delivery 体系。

## 4. 网站仓库如何引用外部主源

网站仓库不直接运行时读取外部主源文件。外部 canonical 文件通过人工审核、导出快照、重新计算派生指标和更新网站副本的流程同步到仓库。

当前网站仓库内引用关系：

- `app/data.ts`：展示副本，承载指标、FAQ、信源子集、诊断卡、路线图和下载链接。
- `app/knowledge-base/knowledge-base-public.json`：公开知识库 JSON 的网站内派生副本。
- `public/data/yhl-geo-knowledge-base-public.json`：公开知识库 JSON 的 public 数据副本。
- `public/downloads/*`：仅存放 approved / conditional 的公开下载副本和下载清单。
- `internal-review/downloads/*`：存放 blocked / internal-review 下载件和完整 Markdown canonical。
- TSX 页面：展示副本或 presentation，不作为核心数据 canonical。

## 5. 需要人工确认的数据

以下数据仍需要人工确认或人工审核后才能发布更新：

- 原始 AI 回答是否对应当时冻结输出，以及历史模型、联网状态、产品端环境缺失时的标注方式。
- 人工评分、确认错误、确认幻觉、疑似幻觉、风险标签、缺失标签、证据备注。
- 品牌事实新增、删除、事实等级调整、信源状态和允许表述。
- FAQ 直接回答、边界文案和页面归属。
- 提示词体系和 GEO 文章样稿的正式发布口径。
- 从 `first_setup` 或 `final` 归档目录迁移任何内容。
- 当 `CategoryMap` 未来与问题库 CSV 出现 `question_id` 或问题文本差异时，问题库 canonical 决策需重新进入人工确认。

## 6. 不得作为正式输入的文件

以下文件或目录不得作为正式输入：

- `/Users/lay/Documents/New project/outputs/yhl_geo_first_setup_20260718`
- `/Users/lay/Documents/New project/outputs/yhl_geo_portfolio_final`
- `app/data.ts`
- 任意 TSX 页面
- 构建后的 HTML
- `.inspect.ndjson`、预览、公式错误扫描、截图和渲染产物
- batch1、old10、早期汇总 CSV 和早期复测模板
- 公开知识库 JSON 的任一副本
- `public/downloads` 中非 Markdown canonical 的下载副本

## 7. 数据版本更新规则

1. canonical 文件更新前必须记录更新原因、更新人、版本日期和影响范围。
2. 原始回答和人工评分不得在网站仓库中直接编辑。
3. 投递版数据工作簿更新后，必须重新计算 Dashboard、RiskTags、MissingTags、EvidenceIndex 等派生指标。
4. 品牌事实知识库更新后，必须重新导出公开知识库 JSON。
5. 90 天策略工作簿更新后，必须重新生成或复核网站策略页面、下载副本和相关截图/PDF。
6. Markdown canonical 更新后，必须同步检查对应 TSX 页面展示内容。
7. 每次导出 public 快照或下载副本后，必须记录来源路径、版本日期和哈希。

## 8. 网站同步规则

同步流程：

主源修改
→ 人工审核
→ 导出公开快照
→ 重新计算派生指标
→ 更新网站副本
→ 构建验证
→ 提交版本

同步约束：

- `app/data.ts` 只能接收已审核的展示副本，不得反向覆盖主工作簿。
- TSX 页面只能接收 Markdown、工作簿或公开 JSON 的展示同步内容。
- 下载文件必须来自明确主源或生成流程，不能在下载目录中手工改事实。
- 早期归档不得参与当前计算。

## 9. 冲突处理规则

- canonical 与 website-copy 冲突：以 canonical 为准，网站副本进入待同步状态。
- canonical 与 delivery 冲突：以 canonical 为准，delivery 副本重新导出或重新复制。
- canonical 与 derived 冲突：丢弃 derived 结果，重新计算或重新导出。
- 问题库 CSV 与 `CategoryMap` 的 `question_id` 或问题文本冲突：暂停确认，标记 `decision-pending`，输出完整差异清单等待人工决定。
- 品牌事实工作簿与公开 JSON 冲突：以工作簿为准，重新导出 JSON。
- Markdown canonical 与 TSX 页面冲突：以 Markdown 为准，TSX 进入展示同步状态。
- archive 与任何当前文件冲突：archive 不参与裁决，只能作为历史参考。
