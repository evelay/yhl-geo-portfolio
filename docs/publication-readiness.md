# 发布准备报告

更新日期：2026-07-19

分支：`refactor/portfolio-v2`

本文件反映阶段 0.4C P1 作品集质量与发布一致性修复后的状态，并追加阶段 07B3 公开 manifest 本地路径清理结果。本阶段未修改外部 canonical 工作簿、原始 AI 回答、人工评分、核心指标、sitemap、robots 或 canonical 设置。

## 状态定义

- `yes`：当前公开范围可继续发布。
- `mitigated`：公开风险已隔离，但完整内容仍需人工审核。
- `internal-review`：已移出公开下载范围，等待人工审核。
- `not-in-scope`：本阶段不处理。

## 页面发布准备

| 页面/路由 | 当前状态 | 是否可以公开 | 当前公开内容 | 暂缓或内部审核内容 | 相关问题 |
| --- | --- | --- | --- | --- | --- |
| `/` | 已补全项目身份与数据版本说明 | yes | 独立 GEO 研究首页、baseline 指标、人工评分说明、未复测说明、内容资产入口 | 不展示复测提升结果，不提供内部下载 | `CS-006`、`CS-007`、`CS-014` |
| `/facts` | P0 内容页边界保持 | yes | 品牌事实分层、来源边界和核验路径 | 待补品牌事实不写成确定结论 | `CS-005`、`CS-006` |
| `/disambiguation` | P0 内容页边界保持 | yes | 同名主体消歧和主体核验路径 | 不补造工商号码、股权关系或跨行业关联 | `CS-005`、`CS-006` |
| `/materials` | P0 内容页边界保持 | yes | 材质标准、品牌公开范围和单件证据边界 | 不替单件产品下材质、真伪或价值结论 | `CS-006` |
| `/jingzuo` | P0 内容页边界保持 | yes | 京作、明清风格和产品资料的表达边界 | 不恢复使用待补信源支持的 FAQ-08 | `CS-001`、`CS-005` |
| `/buying-guide` | P0 内容页边界保持 | yes | 购买核验清单和动态信息边界 | 不承诺价格、门店、售后或投资结果 | `CS-006` |
| `/faq` | 仅展示已通过来源与发布检查的 FAQ | yes | 13 条公开 FAQ；source_id 使用品牌事实知识库 `内容FAQ映射`；页面含项目声明 | FAQ-08、FAQ-10 继续 hold，记录见 `docs/faq-publication-reconciliation.csv` | `CS-001`、`CS-002` |
| `/strategy` | 已撤下阻塞下载件并补 baseline 说明 | yes | 模拟品牌提案摘要、P0/P1/P2 内容架构、90 天路线图、公开下载状态 | PDF/DOCX、90 天执行工作簿进入内部复核，不公开下载 | `CS-006`、`CS-007`、`CS-008` |
| `/knowledge-base` | 使用安全过滤版公开 JSON | yes | 36 条公开事实、24 条公开信源、13 条公开 FAQ 映射；页面含项目声明 | 5 条被排除事实、3 条不可用信源和完整 XLSX 工作簿进入内部复核 | `CS-005`、`CS-008` |
| `/prompt-system` | 改为公开说明页 | mitigated | 设计目标、工作流程、输入字段类别、输出结构、人工审核节点、脱敏短示例、使用边界、项目声明 | 完整企业提示词体系 Markdown 和可复制提示词正文继续内部复核，不公开下载 | `CS-003`、`CS-013` |
| `/geo-articles` | 改为文章审核状态页 | mitigated | 页面说明示范稿、非官方内容、基于公开资料和项目研究、未经品牌官方审核；只展示标题、研究目的和审核状态 | 文章矩阵和完整文章样稿 Markdown 继续内部复核；不展示未审核完整正文 | `CS-004`、`CS-013`、`CS-015` |
| `/method` | 已补数据版本、测试日期和人工评分说明 | yes | 样本量、平台范围、测试日期、人工评分、原始数据主源和未复测限制 | 不展示长期趋势或优化后增长 | `CS-007`、`CS-009` |

## 公开下载文件

| 文件 | 状态 | 审核状态 | 说明 |
| --- | --- | --- | --- |
| `public/downloads/yhl-geo-knowledge-base-public.json` | public | approved | 从品牌事实知识库工作簿只读生成的安全过滤版公开快照；SHA-256 `379fbec902654f6daabd5cf5eb5ff856cd418f78e09ba5c772f6e69b8895c991` |
| `public/downloads/manifest.json` | public | approved | 机器可读下载清单；使用逻辑来源 ID/标签/范围，不含本地绝对路径；SHA-256 `dbfeca4ad231a0ad04a6a2d7d9a7e8d73a41a66e2952627121bea06f8a1d6932` |

## 内部审核下载文件

| 文件 | 状态 | 原因 |
| --- | --- | --- |
| `internal-review/downloads/yhl-geo-brand-content-optimization-plan.pdf` | internal-review | 只读审计发现旧 `chatgpt.site` 地址，需重新制作并复核 |
| `internal-review/downloads/yhl-geo-brand-content-optimization-plan.docx` | internal-review | 只读审计发现旧 `chatgpt.site` 地址，需重新制作并复核 |
| `internal-review/downloads/yhl-geo-enterprise-prompt-system.md` | internal-review | 完整提示词体系不再公开展示或下载 |
| `internal-review/downloads/yhl-geo-article-matrix.md` | internal-review | 文章矩阵需继续审核来源与发布状态 |
| `internal-review/downloads/yhl-geo-full-article-samples.md` | internal-review | 完整文章样稿未通过公开发布检查 |
| `internal-review/downloads/yhl-geo-knowledge-base-public.json` | internal-review | 旧版未过滤公开快照，已由安全版本替换 |
| `internal-review/downloads/yhl-geo-brand-fact-knowledge-base.xlsx` | internal-review | 完整工作簿含待复核记录，不作为公开下载 |
| `internal-review/downloads/yhl-geo-90-day-content-execution.xlsx` | internal-review | 工作簿发布状态语义需后续人工复核 |

## 后续人工审核

- 重新制作 14 页 PDF/DOCX，移除旧站地址，并再次检查官方委托、实施状态、未经确认事实和效果承诺。
- 对 FAQ-08、FAQ-10 完成来源和事实等级复核后，才能决定是否恢复公开。
- 对完整提示词体系进行 internal-review / public-summary / publishable excerpt 分级。
- 对 7 个 GEO 文章样稿逐篇核对 source_id、fact_id、非官方边界和效果承诺。
- 对品牌事实完整 XLSX 和 90 天执行 XLSX 决定是否需要生成公开删减版。
