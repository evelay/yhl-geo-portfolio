# 内容与数据安全修复计划

审计日期：2026-07-19

适用阶段：阶段 0.4A 之后的修复阶段
执行状态：本文件只制定计划，不执行修复，不修改页面、数据、下载件或外部 canonical。

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
| `public/downloads/`; 发布文档或 manifest 文件 | `CS-008` | 建立下载 manifest，记录文件名、来源 canonical 路径、版本日期、复制时间、哈希、公开状态 | `docs/data-sync-policy.md`; 本次哈希核验结果 | yes | 每个公开下载件可追溯来源、版本和哈希；人工审核者可确认是否最新 |
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

- 未修改 `app/data.ts`
- 未修改页面正文
- 未修改组件
- 未修改下载文件
- 未修改外部 canonical 文件
- 未创建同步脚本
- 未接入 GEO Skill
- 未创建 Pull Request
