# 阶段 0.4A 内容与数据安全审计

审计日期：2026-07-19

审计分支：`refactor/portfolio-v2`
审计结论：本阶段只识别问题并生成报告，未修改页面正文、`app/data.ts`、下载文件或外部 canonical 数据源。

## 1. 审计范围

本次审计覆盖当前网站仓库中用户可看到或下载的内容：

- `app/data.ts`
- `app/layout.tsx`
- `app/` 下所有公开页面：`/`、`/facts`、`/disambiguation`、`/materials`、`/jingzuo`、`/buying-guide`、`/faq`、`/strategy`、`/knowledge-base`、`/prompt-system`、`/geo-articles`、`/method`
- `app/components.tsx` 中展示项目身份和页脚声明的组件
- `public/data/`
- `public/downloads/`
- `public` 中 JSON、Markdown、PDF、XLSX、DOCX
- `docs/` 中已有治理说明
- 项目交付目录中的 `reports/` 报告文件，只读检查，不修改
- 构建脚本与数据生成逻辑的公开输出关系

本次未发现仓库内存在 `components/` 或 `reports/` 目录；显示组件集中在 `app/components.tsx`，项目报告位于仓库父级交付目录。

## 2. 审计方法

1. 先确认 Git 工作目录、Git 根目录、分支、工作区状态和本地/远程同步状态。
2. 读取数据治理文档，确认 canonical 数据源和已锁定的发布治理规则。
3. 只读解析主工作簿、品牌事实知识库、问题库、90 天策略工作簿、公开 JSON、Markdown、PDF、DOCX、XLSX 下载件。
4. 将网站页面、展示副本、下载副本和外部报告中的事实、指标、发布状态与 canonical 数据源比对。
5. 对问题按 A-F 六类审计类型归档，输出 `docs/content-safety-issues.csv`。
6. 对网站主要指标逐项建立溯源记录，输出 `docs/metric-provenance-audit.csv`。
7. 按页面和下载文件给出发布准备判断，输出 `docs/publication-readiness.md`。
8. 仅制定修复计划，不执行任何内容修复。

## 3. Canonical 依据

本次优先采用以下治理文档：

- `docs/data-governance-decisions.md`
- `docs/data-sync-policy.md`
- `docs/data-source-inventory.csv`
- `docs/data-source-map.md`
- `docs/question-bank-reconciliation.md`
- `docs/app-data-audit.md`

本次只读使用的 canonical 数据源：

- `元亨利GEO_投递版数据与分析.xlsx`：原始回答、人工评分、核心指标
- `redwood_question_bank_30.csv`：问题库
- `元亨利GEO品牌事实知识库.xlsx`：品牌事实、信源、FAQ 映射
- `public/downloads/yhl-geo-enterprise-prompt-system.md`：提示词体系 canonical Markdown
- `public/downloads/yhl-geo-article-matrix.md`：文章矩阵 canonical Markdown
- `public/downloads/yhl-geo-full-article-samples.md`：文章样稿 canonical Markdown
- `元亨利红木家具GEO_90天内容执行工作簿.xlsx`：90 天策略

下载副本哈希核验显示，公开下载目录中的品牌事实知识库、公开 JSON、90 天工作簿、PDF、DOCX 与登记的外部来源逐字节一致。问题集中在发布状态、审核状态、来源同步和公开边界，不是下载副本被意外改写。

## 4. 项目身份风险

总体判断：网站正文和页脚已经多处声明“个人公开研究和作品集执行版”“不代表元亨利官方或品牌委托”“不声称 AI 收录、曝光、推荐或销售提升”。未发现把项目直接写成元亨利官方委托、品牌内部权限或已代表品牌正式实施的高风险表达。

发现的边界问题：

- `CS-014`：`app/layout.tsx` 的 metadata / Open Graph description 没有非官方、公开研究、基于公开信息的边界。正文和 footer 有声明，因此为低风险，但搜索结果或社交预览可能脱离页面正文展示。

建议安全表达：

- “个人公开研究案例，不代表元亨利官方或品牌委托。”
- “基于公开信息、公开信源和模拟 AI 测试结果形成。”
- “不包含品牌内部后台数据，不代表品牌官方立场。”

## 5. 品牌事实风险

总体判断：公开知识库已经保留 evidence level、source status 和免责声明，未发现大量无来源品牌事实扩写。但存在来源状态与页面展示不同步、待补来源进入公开视图、来源子集呈现不够清晰等风险。

主要问题：

- `CS-002`：FAQ 展示的 `sourceIds` 与知识库 FAQ 映射不一致，至少 6 条存在差异。FAQ-01、FAQ-11、FAQ-13 缺少主体核验来源，FAQ-10 缺少 EV 证据引用。该问题阻止 FAQ 直接公开发布。
- `CS-005`：公开知识库包含 5 条 L3 待补事实和 3 条待补信源。页面有标签和筛选，但是否允许进入 publicFacts 需要人工决定。
- `CS-009`：`/method` 页面标题写“已核验第三方/权威来源”，但表格只展示 10 条 B 类来源子集，容易让读者误解为完整来源库。
- `CS-015`：完整文章样稿缺少每篇文章级别的 `fact_id/source_id` 入口，需结合文章矩阵才能完整追溯。

未发现的问题：

- 未发现“第一、顶级、最权威、国家级”等明显无证据绝对化品牌定位在网站正文中作为主张使用。
- 未发现把品牌内部数据、后台权限或官方授权作为事实来源。

## 6. AI 测试真实性

总体判断：网站主要 AI 测试指标可回溯到主工作簿，且页面已说明不把测试结果当作 AI 推荐、引用或曝光提升。但测试元数据披露仍不完整。

已核验一致的核心点：

- Baseline 样本量：150 条
- UserIntent 样本量：75 条
- 平台：豆包、文心一言、通义千问、Kimi、腾讯元宝
- 主指标：Baseline 平均总分 17.2，UserIntent 平均总分 14.9，均可由主工作簿重算
- 事实性风险、来源覆盖、自然提及、可靠性缺口等主要指标均可从主工作簿或策略工作簿追溯

主要问题：

- `CS-007`：关键图表旁未完整披露测试日期、`test_mode` 和 `web_search_status`。主工作簿显示历史测试的联网状态和测试模式为“未记录”；Baseline 日期为 Excel 序列值 46216，UserIntent 日期为 2026-07-13。

未发现的问题：

- 未发现人工评分被标成模型自动评分。
- 未发现空评分进入平均值或缺失回答被当成零分的证据。
- 未发现模拟 AI Overview 被描述为真实 Google AI Overview。
- 未发现单轮测试被直接描述为稳定趋势。

## 7. 指标与效果承诺

总体判断：网站核心展示指标大多能从 canonical 数据源重算或追溯。主要风险不是算术错误，而是“结构验收/计划完成/发布审核”之间的语义边界。

主要问题：

- `CS-006`：页面和策略工作簿将 P0 页面、FAQ、30/30 覆盖、24/6 回答和质检通过写成已完成或已发布。指标可溯源，但在内容安全审计与人工确认前，容易被理解为已经通过公开发布审核。
- `CS-010`：外部全面诊断报告仍把 archive/outdated 或 derived CSV 与主工作簿并列为数据来源。如继续分发，应改为以投递版工作簿为主来源。
- `CS-011`：外部全面诊断报告存在 Schema 已生成或待部署等旧实施状态，与当前 V2 网站实现不完全一致。
- `CS-012`：外部摘要报告中的“提高品牌被准确引用的概率”容易被理解为效果承诺，应改为“降低无来源扩写风险”或“提升事实可核验性”。

未发现的问题：

- 未发现网站主指标存在明显百分比与样本量不匹配。
- 未发现“保证被引用”“保证 AI 收录率”等直接承诺。
- 未发现把复测提升结果写成已经实现的成果。

## 8. FAQ、提示词和文章发布状态

根据本阶段治理规则，FAQ、提示词体系和 GEO 文章样稿统一应标记为 `publication-review-required`。本阶段不修改发布状态，只记录建议。

| 内容模块 | 当前公开状态 | 审计建议状态 | 主要问题 |
| --- | --- | --- | --- |
| FAQ | 页面公开，`app/data.ts` 标为已发布 | `publication-review-required` | `CS-001`、`CS-002` |
| Prompt System | 页面公开，可复制，Markdown 可下载 | `publication-review-required` 或部分 `internal-only` | `CS-003`、`CS-013` |
| GEO Articles | 页面公开，文章矩阵和样稿可下载 | `publication-review-required` | `CS-004`、`CS-013`、`CS-015` |
| Knowledge Base | 页面公开，JSON/XLSX 可下载 | `conditional`：待人工决定 L3/pending 是否公开 | `CS-005` |
| Strategy | 页面公开，XLSX/PDF/DOCX 可下载 | `conditional`：区分计划执行与发布审核 | `CS-006`、`CS-008` |

## 9. 下载文件风险

本次逐项检查 `public/downloads/`：

| 文件 | 审计结论 | 风险 |
| --- | --- | --- |
| `yhl-geo-enterprise-prompt-system.md` | 需要人工复核 | 含可复制提示词和内部判断字段，缺少显式 publication status |
| `yhl-geo-article-matrix.md` | 需要人工复核 | 文章矩阵含 B-006/B-007 待补信源 |
| `yhl-geo-full-article-samples.md` | 需要人工复核 | 样稿需确认不被误解为品牌官方内容，且缺少篇章级 source_id/fact_id 入口 |
| `yhl-geo-knowledge-base-public.json` | 条件公开 | 与 canonical 一致，但包含 L3/pending 条目 |
| `yhl-geo-brand-fact-knowledge-base.xlsx` | 条件公开 | 与 canonical 一致，但包含待补信源和待补事实 |
| `yhl-geo-90-day-content-execution.xlsx` | 条件公开 | 与 canonical 一致，但包含“已完成/已进入公开站/已发布”等状态，需要结合安全审计解释 |
| `yhl-geo-brand-content-optimization-plan.pdf` | 可继续公开，建议抽检 | 已有非官方和非效果承诺声明；未发现旧域名或官方委托暗示 |
| `yhl-geo-brand-content-optimization-plan.docx` | 可继续公开，建议抽检 | 与 PDF 同源，已有声明；建议确认是否继续作为可编辑公开件 |

未发现旧域名、官方委托暗示、模拟 AI Overview 被当成真实 Google AI Overview、空评分或旧指标直接混入下载件的证据。二进制文件均可用正常解析工具读取；未使用 OCR。

## 10. 按严重程度统计

| 严重程度 | 数量 |
| --- | ---: |
| critical | 0 |
| high | 6 |
| medium | 7 |
| low | 2 |
| 合计 | 15 |

## 11. 阻止公开发布的问题

明确阻止公开发布的问题共 4 项：

- `CS-001`：FAQ 当前公开状态与 `publication-review-required` 规则冲突
- `CS-002`：FAQ source_id 与知识库 FAQ 映射不一致
- `CS-003`：提示词体系公开展示和下载前缺少人工审核
- `CS-004`：文章样稿公开且文章矩阵使用待补 source_id

条件阻止项共 7 项：

- `CS-005`：公开知识库包含 L3 待补事实和待补信源
- `CS-006`：发布状态、质检通过和内容审核边界混用
- `CS-008`：下载件缺少发布用 manifest
- `CS-010`：外部全面诊断报告仍引用 archive/outdated 或 derived 数据
- `CS-011`：外部全面诊断报告存在旧实施状态
- `CS-012`：外部摘要报告存在引用概率类表达
- `CS-013`：Markdown canonical 缺少显式发布审核字段

## 12. 不阻止发布但需要修正的问题

- `CS-007`：AI 测试元数据披露不足
- `CS-009`：方法页来源表标题未明确是精选子集
- `CS-014`：metadata 缺少非官方边界
- `CS-015`：完整文章样稿缺少篇章级 source_id/fact_id 入口

这些问题不一定阻止网站整体公开，但会影响审计透明度、搜索预览边界和后续维护效率。

## 13. 无法判断、需要人工确认的问题

以下问题需要人工决策，不应由同步脚本或自动修复直接决定：

- L3 待补事实和待补信源是否允许保留在公开知识库中。
- Prompt System 哪些部分适合公开，哪些应 internal-only 或只展示摘要。
- GEO 文章样稿是否作为作品集公开样稿、审核中草稿，还是仅作为内部样稿。
- FAQ 是否以知识库 FAQ 映射为唯一准绳自动同步，还是先人工逐条确认。
- 外部 `reports/` 是否仍作为公开交付材料；如公开，应先进入同一套内容安全修复流程。
- 下载文件是否需要新增公开免责声明页、下载 manifest 或文件内 review status。

## 14. 修复优先级建议

P0 公开前必须修复：

- FAQ 发布状态和 source_id 同步问题：`CS-001`、`CS-002`
- Prompt System 公开审核和内部字段暴露问题：`CS-003`
- GEO 文章样稿与待补 source_id 问题：`CS-004`
- 公开知识库 L3/pending 条目是否保留：`CS-005`
- 发布状态与内容审核状态混用：`CS-006`

P1 作品集质量关键修复：

- 下载 manifest 和哈希/来源版本记录：`CS-008`
- Markdown canonical 增加 publication status、作者、审核状态：`CS-013`
- AI 测试日期、模式、联网状态披露：`CS-007`
- 外部报告旧数据源和旧实施状态：`CS-010`、`CS-011`、`CS-012`

P2 后续结构改进：

- 方法页来源表明确为精选子集：`CS-009`
- 完整文章样稿补篇章级 source_id/fact_id 入口：`CS-015`

P3 可选优化：

- metadata / Open Graph 增加非官方和公开研究边界：`CS-014`
