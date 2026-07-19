# 阶段 0.4C P1 作品集质量修复报告

修复日期：2026-07-19

分支：`refactor/portfolio-v2`

## 1. 本阶段范围

本阶段只处理 P1 作品集质量与发布一致性问题：旧测试口径、公开下载一致性、PDF/DOCX 公开审计、项目身份声明、baseline 数据版本披露和发布准备文档。未重新公开 FAQ-08、FAQ-10、完整提示词、7 篇完整文章、完整知识库 XLSX 或 90 天执行工作簿；未接入 GEO Skill，未重构首页视觉。

## 2. 测试修复情况

`tests/rendered-html.test.mjs` 已从旧公开物料预期改为当前发布规则验证：

- 全部公开路由必须可渲染，并包含非官方/独立研究边界。
- 内部文件不得存在于 `public/downloads`。
- 内部文件必须存在于 `internal-review/downloads`。
- manifest 中 public 文件必须实际存在、哈希匹配、状态为 approved 或 conditional。
- manifest 中 internal-review 文件必须哈希匹配、public_url 为空、review_status 为 blocked。
- 页面下载链接只能指向 public 且 approved/conditional 的文件。
- FAQ 页面只渲染 13 条公开 FAQ，不出现 FAQ-08 或 FAQ-10。
- Prompt 页面不包含完整提示词、内部字段或 Markdown 下载链接。
- Articles 页面不包含未审核完整正文、文章矩阵或完整样稿 Markdown 下载链接。
- 安全知识库 JSON 仍公开，并验证 36 条公开事实、24 条可用信源、13 条 FAQ 映射，且无 L3 事实或不可用信源。

旧的 `yhl-geo-brand-fact-knowledge-base.xlsx`、`yhl-geo-enterprise-prompt-system.md`、`yhl-geo-full-article-samples.md` 公开存在性断言已被替换，没有通过 skip 掩盖。

## 3. 公开 PDF/DOCX 审计结果

审计对象：

- `yhl-geo-brand-content-optimization-plan.pdf`
- `yhl-geo-brand-content-optimization-plan.docx`

审计方式：使用可提取文本进行只读检查，未使用 OCR。PDF 可读取 14 页文本；DOCX 可读取 139 个段落和 33 个表格。两者内容结构基本同源，均包含相同旧站链接风险。

结果：

| 检查项 | 结果 |
| --- | --- |
| 是否包含旧 `chatgpt.site` 地址 | 是，PDF 和 DOCX 各 3 处 |
| 是否表述为官方委托 | 未发现；文本写有“不构成品牌委托” |
| 是否暗示正式实施 | 未发现正式实施完成表述，但包含旧公开案例链接 |
| 是否包含未经确认品牌事实 | 未逐项重制，因旧域名已触发阻塞处理 |
| 是否包含“保证 AI 引用”“提升收录率”等效果承诺 | 未发现这两类直接承诺 |
| 是否展示未完成复测提升结果 | 未发现已完成复测提升结果；复测多为后续要求 |
| 是否与当前 canonical 指标一致 | 核心 baseline 指标未发现明显冲突，但 FAQ 数量仍有旧“15 个直接答案”口径 |
| 是否包含已下线公开下载链接 | 未发现旧 Markdown/XLSX 下载文件名，但包含旧公开站地址 |
| 是否缺少独立研究声明 | 不缺少，已有个人公开资料研究声明 |
| PDF 和 DOCX 是否一致 | 基本同源，风险项一致；因已阻塞，不再继续做发布级视觉一致性修复 |

处理：PDF 和 DOCX 已从 `public/downloads` 移到 `internal-review/downloads`，manifest 标记为 `internal-review` / `blocked`，公开页面下载链接已移除。

重新制作建议：

- 使用当前 GitHub Pages 或最终发布 URL，移除旧 `chatgpt.site` 地址。
- 将 FAQ 口径更新为 13 条公开、FAQ-08/FAQ-10 hold。
- 明确 baseline、尚未复测和人工评分，不写优化后增长。
- 保留独立研究、基于公开资料、非官方委托、不代表官方立场声明。
- 重新导出 PDF/DOCX 后记录哈希、审核日期、来源版本和公开免责声明。

## 4. 项目身份说明统一情况

共享页脚已统一写明：本项目为基于公开资料完成的独立 GEO 研究与求职作品集，未受元亨利委托，不代表品牌官方立场，且不声称 AI 收录、引用、曝光、推荐或销售提升。

`app/layout.tsx` 的 metadata description 和 Open Graph description 已补充非官方和公开研究边界。首页第一屏也加入了基于公开资料、未受元亨利委托、不代表官方立场的说明。

## 5. 数据版本披露情况

首页指标区、策略页指标区和 `/method` 已补充：

- 数据版本：baseline / 基线；
- 样本量：Baseline150、UserIntent75；
- 平台范围：豆包、文心一言、通义千问、Kimi、腾讯元宝；
- 测试日期：2026-07-13，其中 Baseline 原始日期为 Excel 序列值 46216；
- 评分方式：人工四维评分，不是模型自动评分；
- 原始数据主源：《元亨利GEO_投递版数据与分析.xlsx》；
- 当前尚未完成复测，不展示优化后增长或长期趋势。

## 6. 下载 manifest 一致性

`public/downloads/manifest.json` 与 `docs/download-manifest.md` 已同步。

07B3 追加清理：公开 manifest 的来源追溯字段已改为逻辑来源 ID/标签/范围，真实本地路径只保留在内部治理文档。

当前公开下载范围：

- `public/downloads/yhl-geo-knowledge-base-public.json`
- `public/downloads/manifest.json`

公开文件哈希：

- `yhl-geo-knowledge-base-public.json`：`379fbec902654f6daabd5cf5eb5ff856cd418f78e09ba5c772f6e69b8895c991`
- `manifest.json`：`dbfeca4ad231a0ad04a6a2d7d9a7e8d73a41a66e2952627121bea06f8a1d6932`

当前 internal-review 下载范围：

- `internal-review/downloads/yhl-geo-brand-content-optimization-plan.pdf`
- `internal-review/downloads/yhl-geo-brand-content-optimization-plan.docx`
- `internal-review/downloads/yhl-geo-enterprise-prompt-system.md`
- `internal-review/downloads/yhl-geo-article-matrix.md`
- `internal-review/downloads/yhl-geo-full-article-samples.md`
- `internal-review/downloads/yhl-geo-knowledge-base-public.json`
- `internal-review/downloads/yhl-geo-brand-fact-knowledge-base.xlsx`
- `internal-review/downloads/yhl-geo-90-day-content-execution.xlsx`

页面下载链接只指向安全公开知识库 JSON。PDF/DOCX、完整知识库 XLSX、90 天执行 XLSX、完整提示词和完整文章样稿均不再有公开下载链接。

## 7. 仍处于 hold/internal-review 的内容

- FAQ-08、FAQ-10：继续 hold。
- 完整企业提示词体系 Markdown：继续 internal-review / blocked。
- GEO 文章矩阵 Markdown：继续 internal-review / blocked。
- 7 篇完整文章样稿 Markdown：继续 internal-review / blocked。
- 完整品牌事实知识库 XLSX：继续 internal-review / blocked。
- 90 天内容执行工作簿 XLSX：继续 internal-review / blocked。
- 旧版未过滤知识库 JSON：继续 internal-review / blocked。
- 14 页 PDF/DOCX：因旧站地址继续 internal-review / blocked。

## 8. 尚未解决的 P2/P3 问题

- `CS-009`：方法页来源表仍可进一步标注为“精选来源子集”，避免被误解为完整来源库。
- `CS-010`：外部全面诊断报告如继续分发，仍需把旧 CSV 数据源改为历史或 derived。
- `CS-011`：外部全面诊断报告仍需统一 Schema 和实施状态口径。
- `CS-012`：外部摘要报告仍需消除“引用概率提升”类表达。
- `CS-015`：完整文章样稿如果未来公开，需要补篇章级 fact_id/source_id 入口。

## 9. GEO Skill 前置条件

公开站点层面的前置条件基本满足：公开页面边界、测试口径、下载链接和 manifest 已与当前发布决定对齐。

限制条件：GEO Skill 接入时只能读取公开路由和安全知识库 JSON，不得把 `internal-review/downloads` 中的完整提示词、完整文章、完整工作簿或被阻塞 PDF/DOCX 作为输入。若下一阶段需要接入这些资产，必须先完成人工审核和重新发布决定。
