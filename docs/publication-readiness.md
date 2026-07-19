# 发布准备报告

更新日期：2026-07-19

分支：`refactor/portfolio-v2`

本文件反映阶段 0.4B P0 公开阻塞修复后的状态；本阶段未修改外部 canonical 工作簿、原始 AI 回答、人工评分、核心指标、首页结构或 strategy 页面文件。

## 状态定义

- `yes`：当前公开范围可继续发布。
- `mitigated`：公开风险已隔离，但完整内容仍需人工审核。
- `internal-review`：已移出公开下载范围，等待人工审核。
- `not-in-scope`：本阶段不处理。

## 页面发布准备

| 页面/路由 | 修复后状态 | 是否可以公开 | 当前公开内容 | 暂缓或内部审核内容 | 相关问题 |
| --- | --- | --- | --- | --- | --- |
| `/faq` | 仅展示已通过来源与发布检查的 FAQ | yes | 13 条 FAQ；source_id 使用品牌事实知识库 `内容FAQ映射`；页面含项目声明 | FAQ-08、FAQ-10 暂缓公开，记录见 `docs/faq-publication-reconciliation.csv` | `CS-001`、`CS-002` |
| `/prompt-system` | 改为公开说明页 | mitigated | 设计目标、工作流程、输入字段类别、输出结构、人工审核节点、脱敏短示例、使用边界、项目声明 | 完整企业提示词体系 Markdown 和可复制提示词正文进入内部复核，不公开下载 | `CS-003` |
| `/geo-articles` | 改为文章审核状态页 | mitigated | 页面说明示范稿、非官方内容、基于公开资料和项目研究、未经品牌官方审核；只展示标题、研究目的和审核状态 | 文章矩阵和完整文章样稿 Markdown 进入内部复核；不展示未审核完整正文 | `CS-004` |
| `/knowledge-base` | 使用安全过滤版公开 JSON | yes | 36 条公开事实、24 条公开信源、13 条公开 FAQ 映射；页面含项目声明 | 5 条被排除事实、3 条不可用信源和完整 XLSX 工作簿进入内部复核 | `CS-005` |

## 公开下载文件

| 文件 | 状态 | 审核状态 | 说明 |
| --- | --- | --- | --- |
| `public/downloads/yhl-geo-knowledge-base-public.json` | public | approved | 从品牌事实知识库工作簿只读生成的安全过滤版公开快照 |
| `public/downloads/manifest.json` | public | approved | 机器可读下载清单 |
| `public/downloads/yhl-geo-brand-content-optimization-plan.pdf` | public | conditional | 阶段 0.4A 标记可继续公开，建议后续抽检 |
| `public/downloads/yhl-geo-brand-content-optimization-plan.docx` | public | conditional | 阶段 0.4A 标记可继续公开，建议后续抽检 |

## 内部审核下载文件

| 文件 | 状态 | 原因 |
| --- | --- | --- |
| `internal-review/downloads/yhl-geo-enterprise-prompt-system.md` | internal-review | 完整提示词体系不再公开展示或下载 |
| `internal-review/downloads/yhl-geo-article-matrix.md` | internal-review | 文章矩阵需继续审核来源与发布状态 |
| `internal-review/downloads/yhl-geo-full-article-samples.md` | internal-review | 完整文章样稿未通过公开发布检查 |
| `internal-review/downloads/yhl-geo-knowledge-base-public.json` | internal-review | 旧版未过滤公开快照，已由安全版本替换 |
| `internal-review/downloads/yhl-geo-brand-fact-knowledge-base.xlsx` | internal-review | 完整工作簿含待复核记录，不作为公开下载 |
| `internal-review/downloads/yhl-geo-90-day-content-execution.xlsx` | internal-review | 工作簿发布状态语义需后续人工复核 |

## 后续人工审核

- 对 FAQ-08、FAQ-10 完成来源和事实等级复核后，才能决定是否恢复公开。
- 对完整提示词体系进行 internal-only / public-summary / publishable excerpt 分级。
- 对 7 个 GEO 文章样稿逐篇核对 source_id、fact_id、非官方边界和效果承诺。
- 对品牌事实完整 XLSX 和 90 天执行 XLSX 决定是否需要生成公开删减版。
- PDF/DOCX 报告虽可继续公开，仍建议进入下一阶段抽检。
