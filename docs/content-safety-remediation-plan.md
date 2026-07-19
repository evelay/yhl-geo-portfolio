# 内容与数据安全修复计划

审计日期：2026-07-19

适用阶段：阶段 0.4A 之后的修复阶段
执行状态：阶段 0.4B 已隔离 P0 公开风险；阶段 0.4C 已完成 P1 作品集质量与发布一致性修复；阶段 07B3 已清理公开 manifest 本地路径。本文件保留原计划，并追加当前完成状态。

## P0：公开前必须修复

| 目标文件 | 问题 ID | 需要修改的内容 | 应参考的 canonical | 是否需要人工决定 | 验收标准 |
| --- | --- | --- | --- | --- | --- |
| `app/data.ts`; `app/faq/page.tsx` | `CS-001` | 将 FAQ 发布状态从“已发布”调整为 `publication-review-required` 或等价审核中状态；页面显示审核状态、更新时间和边界 | 治理规则；`docs/data-source-map.md`; 品牌事实知识库 `内容FAQ映射` | yes | 15 条 FAQ 均有发布审核状态；公开页不再暗示 FAQ 已完成最终发布审核 |
| `app/data.ts`; FAQ 展示数据生成链路 | `CS-002` | 以品牌事实知识库 FAQ 映射为准修正 `sourceIds`；重点核对 FAQ-01、FAQ-02、FAQ-10、FAQ-11、FAQ-13 | `元亨利GEO品牌事实知识库.xlsx` 的 `内容FAQ映射`; `public/data/yhl-geo-knowledge-base-public.json` | yes | FAQ 页面 source_id 与 canonical FAQ 映射逐条一致，或有人工批准的差异说明 |
| `app/prompt-system/page.tsx`; `public/downloads/yhl-geo-enterprise-prompt-system.md` | `CS-003` | 决定完整提示词、路由字段、内部判断字段是否公开；不可公开部分改为摘要或 internal-only | 提示词 Markdown canonical；治理规则 | yes | 页面和下载件均有审核状态；公开内容不暴露不适合公开的内部操作提示词 |
| `app/geo-articles/page.tsx`; `public/downloads/yhl-geo-article-matrix.md`; `public/downloads/yhl-geo-full-article-samples.md` | `CS-004` | 将文章样稿标为 `publication-review-required`；处理 B-006/B-007 待补来源；避免把样稿写成品牌官方内容 | 文章矩阵 Markdown；完整文章样稿 Markdown；品牌事实知识库 `信源主表` | yes | 每篇文章有审核状态；待补 source_id 不被当作已确认事实依据；样稿身份边界清楚 |
| `app/knowledge-base/page.tsx`; `app/knowledge-base/KnowledgeBaseExplorer.tsx`; public JSON/XLSX 下载件 | `CS-005` | 决定 L3 待补事实和 3 条待补信源是否保留公开；若保留，增强 pending 提示 | 品牌事实知识库 `事实原子库`; `信源主表`; public JSON summary | yes | 公开知识库中 pending/L3 条目有明确状态和不可作为确认事实引用的提示，或已从公开版本移除 |
| `app/data.ts`; `app/page.tsx`; `app/strategy/page.tsx`; `public/downloads/yhl-geo-90-day-content-execution.xlsx` | `CS-006` | 区分“结构已生成/数据已映射/内容已审核/公开已发布”；修正已完成和已发布的语义 | 90 天策略工作簿 `KPI看板`; `90天排期`; `发布质检`; 治理规则 | yes | 页面不再把 review-required 内容写成已通过公开发布审核；KPI 说明不构成效果承诺 |

## P1：作品集质量关键修复

| 目标文件 | 问题 ID | 需要修改的内容 | 应参考的 canonical | 是否需要人工决定 | 验收标准 |
| --- | --- | --- | --- | --- | --- |
| `app/page.tsx`; `app/method/page.tsx`; `app/strategy/page.tsx` | `CS-007` | 在方法说明或指标区补充测试日期、`test_mode`、`web_search_status`、模型版本缺失说明 | 主工作簿 `Baseline150`; `UserIntent75` | no | 指标旁或方法页能看到数据日期和缺失元数据说明；不把单轮测试写成稳定趋势 |
| `public/downloads/`; 发布文档或 manifest 文件 | `CS-008` | 建立下载 manifest，记录文件名、逻辑来源 ID/标签/范围、版本日期、复制时间、哈希、公开状态；真实 canonical 路径只保留在内部治理文档 | `docs/data-sync-policy.md`; 本次哈希核验结果 | yes | 每个公开下载件可追溯来源、版本和哈希；公开 manifest 不暴露本地绝对路径 |
| 外部报告 `reports/元亨利GEO_全面诊断报告_作品集版.md` | `CS-010` | 将数据来源更新为投递版主工作簿；早期 CSV 标为历史或 derived，不作为当前公开口径主来源 | `docs/data-governance-decisions.md`; `docs/data-source-inventory.csv`; 主工作簿 | yes | 报告数据源与当前 canonical 治理一致 |
| 外部报告 `reports/元亨利GEO_全面诊断报告_作品集版.md` | `CS-011` | 统一 Schema、FAQ、页面实施状态与当前 V2 网站实现；未完成项改为建议或后续计划 | 当前网站路由；构建脚本；治理文档 | yes | 报告不再暗示未实施功能已经部署 |
| 外部报告 `reports/元亨利GEO_摘要结论与方法论.md` | `CS-012` | 将“提高品牌被准确引用的概率”改为“降低无来源扩写风险”或“提升事实可核验性” | 主工作簿；网站非效果承诺声明 | yes | 报告不包含 AI 引用概率、收录率或推荐提升承诺 |
| `public/downloads/yhl-geo-enterprise-prompt-system.md`; `public/downloads/yhl-geo-article-matrix.md`; `public/downloads/yhl-geo-full-article-samples.md` | `CS-013` | 为三份 Markdown canonical 增加 publication status、author、reviewer、review date、source version | 治理规则；三份 Markdown canonical | yes | Markdown 文件具备明确审核字段，且默认状态符合 `publication-review-required` |

## P2：后续结构改进

| 目标文件 | 问题 ID | 需要修改的内容 | 应参考的 canonical | 是否需要人工决定 | 验收标准 |
| --- | --- | --- | --- | --- | --- |
| `app/data.ts`; `app/method/page.tsx` | `CS-009` | 将方法页来源表标题改为“精选第三方/权威来源子集”，或链接完整信源库 | 品牌事实知识库 `信源主表`; public JSON source summary | no | 读者能区分页面表格是精选来源而非完整来源库 |
| `public/downloads/yhl-geo-full-article-samples.md`; `app/geo-articles/page.tsx` | `CS-015` | 在每篇完整样稿下补 `fact_id/source_id` 摘要或链接到文章矩阵 | 文章矩阵 Markdown；品牌事实知识库 | yes | 每篇样稿可直接追溯到对应 source_id/fact_id，或明确需要查看文章矩阵 |

## P3：可选优化

| 目标文件 | 问题 ID | 需要修改的内容 | 应参考的 canonical | 是否需要人工决定 | 验收标准 |
| --- | --- | --- | --- | --- | --- |
| `app/layout.tsx` | `CS-014` | 在 metadata description / Open Graph description 中增加非官方、公开研究、基于公开资料的边界 | 网站页脚声明；主工作簿 README；治理规则 | no | 搜索结果或社交预览脱离页面正文时仍能看到非官方边界 |

## 修复执行顺序建议

1. 先由人工决定 FAQ、Prompt System、GEO Articles、L3/pending 知识库条目的公开范围。
2. 再根据人工决定修正 `app/data.ts`、公开页面和 Markdown canonical。
3. 然后建立下载 manifest，并对所有下载件重新做哈希与版本登记。
4. 最后修订外部报告，使报告口径与 V2 网站和 canonical 治理一致。

## 本阶段未执行的事项

- 未修改外部 canonical 工作簿
- 未修改原始 AI 回答
- 未修改人工评分
- 未修改核心指标
- 未修改外部 canonical 文件
- 未接入 GEO Skill
- 未创建 Pull Request

## 阶段 0.4B / 0.4C 完成状态

| 问题 ID | 当前状态 | 完成说明 |
| --- | --- | --- |
| `CS-001` | resolved | FAQ 页面保留公开，但只展示 13 条已通过来源与发布检查的 FAQ；FAQ-08、FAQ-10 继续 hold。 |
| `CS-002` | resolved | 公开 FAQ source_id 已使用品牌事实知识库 FAQ 映射，差异记录见 `docs/faq-publication-reconciliation.csv`。 |
| `CS-003` | mitigated | `/prompt-system` 只公开方法说明、流程、输入输出结构、审核节点和脱敏短示例；完整提示词继续在 `internal-review/downloads`。 |
| `CS-004` | mitigated | `/geo-articles` 只公开标题、研究目的和审核状态；文章矩阵和完整文章样稿继续在 `internal-review/downloads`。 |
| `CS-005` | resolved | 公开知识库 JSON 已过滤为 36 条公开事实、24 条可用信源和 13 条 FAQ 映射；完整 XLSX 继续内部复核。 |
| `CS-006` | mitigated | 首页和策略页已区分内容承接、公开发布状态和复测结果；90 天执行工作簿继续内部复核。 |
| `CS-007` | resolved | 首页、策略页和方法页已补充 baseline 数据版本、测试日期、平台范围、人工评分说明和主源说明。 |
| `CS-008` | resolved | `public/downloads/manifest.json` 和 `docs/download-manifest.md` 已同步实际目录、哈希、发布状态、审核状态和验证日期；07B3 已将公开来源追溯改为逻辑 ID/标签/范围，不再暴露本地路径。 |
| `CS-013` | mitigated | 三份 Markdown 已从公开下载范围移入内部复核；manifest 已记录 internal-review/blocked 状态。文件内审核字段仍待人工补齐后再决定是否公开。 |
| `CS-014` | resolved | 全站页脚和 metadata description 已补充独立研究、基于公开资料、非官方委托和不代表品牌官方立场。 |

## 阶段 0.4C 新增处理

- `yhl-geo-brand-content-optimization-plan.pdf` 和 `yhl-geo-brand-content-optimization-plan.docx` 经只读文本审计发现旧 `chatgpt.site` 地址，已移入 `internal-review/downloads`。
- 公开页面已撤下 PDF/DOCX 下载入口；当前公开下载仅保留安全知识库 JSON 和机器可读 manifest。
- 旧测试已替换为当前发布规则测试：内部文件不得进入 `public/downloads`；公开页面不得链接 blocked/internal-review 文件；manifest 校验不读取 `internal-review` 内容。
