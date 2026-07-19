# 发布准备报告

审计日期：2026-07-19

分支：`refactor/portfolio-v2`

数据版本：以 `docs/data-governance-decisions.md` 已确认 canonical 数据源为准。
结论口径：本文件只判断发布准备状态，不修改任何页面、下载件或数据源。

## 状态定义

- `yes`：当前可继续公开，但仍可做低风险质量优化。
- `conditional`：需要人工确认或完成指定修正后公开。
- `no`：公开前必须修复阻塞问题。

## 页面发布准备

| 页面/路由 | 当前状态 | 是否可以公开 | 阻塞问题 | 必须修复项 | 建议修复项 | 数据版本 | 来源完整性 | 建议免责声明 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `/` | 首页公开，展示 225 条 AI 回答、30/30 覆盖、24/6 回答等指标 | conditional | `CS-006` | 区分结构验收、内容审核、公开发布状态 | 在核心指标区补测试日期、测试模式和联网状态摘要；关联 `CS-007` | 主工作簿 2026-07-13；策略工作簿 2026-07-17 | 指标可溯源；状态语义需修正 | 保留“不代表官方、不承诺 AI 引用/推荐/效果提升” |
| `/facts` | P0 品牌事实页面公开 | yes | 无直接阻塞 | 确认页面没有使用 L3/pending 事实作为确定性主张 | 增加数据版本或来源更新时间 | 品牌事实知识库 2026-07-17 | 需持续映射到 fact_id/source_id | 页面内继续声明基于公开资料和主体核验，不代表官方 |
| `/disambiguation` | P0 同名混淆页面公开 | yes | 无直接阻塞 | 保持同名边界，不扩写为唯一官方结论 | 增加来源更新时间 | 品牌事实知识库 2026-07-17 | 可映射公开知识库 | 强调用于消除公开信息混淆，不代表官方认证 |
| `/materials` | P0 材质页面公开 | yes | 无直接阻塞 | 保持材质名、边界和核验清单，不写收藏价值承诺 | 增加 GB/T 18107 等依据说明的版本日期 | 品牌事实知识库 2026-07-17 | 可映射公开知识库 | 强调不构成材质鉴定或购买承诺 |
| `/jingzuo` | P0 京作与风格页面公开 | conditional | `CS-005` 如引用 L3/pending | 人工确认京作关系、风格边界是否只使用可用来源 | 明确“京作风格/关系”不能扩大为官方唯一身份 | 品牌事实知识库 2026-07-17 | 部分京作边界关联 B-007 待补 | 强调公开资料研究，不作官方流派认定 |
| `/buying-guide` | P0 购买决策页面公开 | yes | 无直接阻塞 | 避免价格、收藏、保值、售后保证等承诺 | 增加“以合同、发票、材质标识和单件核验为准” | 品牌事实知识库 2026-07-17 | 可映射公开知识库 | 不构成购买建议、投资建议或鉴定意见 |
| `/faq` | FAQ 页面公开，15 条问答 | no | `CS-001`、`CS-002` | 改为 `publication-review-required`；以知识库 FAQ 映射修正 source_id；逐条人工审核 | 增加作者、审核状态、更新时间和版本 | 品牌事实知识库 2026-07-17；FAQ 映射表 | 当前 source_id 存在漂移 | 每条答案需显示“非官方、公开资料、审核状态” |
| `/strategy` | 90 天策略页面公开，展示 KPI 和下载入口 | conditional | `CS-006`、`CS-008` | 区分计划目标、结构完成、内容审核、公开发布状态 | 增加下载 manifest 和数据版本说明 | 90 天策略工作簿 2026-07-17 | 指标可溯源；发布状态语义需修正 | 不承诺 AI 收录、曝光、推荐、销售提升 |
| `/knowledge-base` | 知识库页面公开，展示 41 条 publicFacts、24 可用/3 待补来源 | conditional | `CS-005` | 人工决定 L3/pending 是否允许保留公开 | 若保留，增加更醒目的 pending 和不可作为确定事实引用说明 | 品牌事实知识库 2026-07-17；公开 JSON 2026-07-17 | 事实和来源可溯源，但 pending 公开边界需决定 | 明确待补条目仅为审计线索，不是已确认事实 |
| `/prompt-system` | 提示词体系页面公开，可复制提示词 | no | `CS-003`、`CS-013` | 改为 `publication-review-required`；人工决定内部字段和完整提示词是否公开 | 可改为公开摘要 + 内部下载受控 | 提示词 Markdown 2026-07-17 | 与 canonical Markdown 一致，但发布审核字段不足 | 明确不是品牌官方提示词，不代表实施交付 |
| `/geo-articles` | 文章矩阵和 1+6 文章样稿公开 | no | `CS-004`、`CS-013`、`CS-015` | 改为 `publication-review-required`；处理 B-006/B-007 待补来源；审核样稿身份边界 | 每篇样稿补 fact_id/source_id 摘要 | 文章矩阵/样稿 Markdown 2026-07-17 | 部分来源待补，样稿追溯入口不足 | 明确为个人作品集样稿，不是品牌官方文章 |
| `/method` | 方法页公开，展示样本、评分、来源和限制 | yes | 无直接阻塞 | 保留历史测试元数据缺失说明 | 补测试日期；将来源表标题改为精选来源子集；关联 `CS-007`、`CS-009` | 主工作簿 2026-07-13；品牌事实知识库 2026-07-17 | 方法数据可溯源；来源表为子集 | 明确单轮诊断，不代表稳定趋势 |
| site metadata | `app/layout.tsx` metadata / Open Graph 已公开 | yes | 无直接阻塞 | 无 | 在 description 中补非官方和公开研究边界；关联 `CS-014` | 网站 V2 当前分支 | 页面内声明充分，metadata 边界不足 | “个人公开研究案例，不代表元亨利官方或品牌委托” |

## 下载文件发布准备

| 文件 | 当前状态 | 是否可以公开 | 阻塞问题 | 必须修复项 | 建议修复项 | 数据版本 | 来源完整性 | 建议免责声明 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `public/data/yhl-geo-knowledge-base-public.json` | 公开 JSON 数据 | conditional | `CS-005` | 决定 L3/pending 是否进入公开 JSON | 增加 manifest/hash 记录 | JSON updatedAt 2026-07-17 | 与下载 JSON 和 app JSON 哈希一致 | 待补条目仅作审计线索 |
| `public/downloads/yhl-geo-knowledge-base-public.json` | 可下载公开 JSON | conditional | `CS-005`、`CS-008` | 决定 L3/pending 是否继续公开 | 增加下载 manifest/hash 记录 | JSON updatedAt 2026-07-17 | 与外部公开 JSON 哈希一致 | 不代表官方，不含未公开资料 |
| `public/downloads/yhl-geo-brand-fact-knowledge-base.xlsx` | 可下载品牌事实知识库 XLSX | conditional | `CS-005`、`CS-008` | 人工确认待补信源/事实是否适合公开下载 | 增加版本、来源路径、哈希、复制时间记录 | 知识库 2026-07-17 | 与外部 canonical XLSX 哈希一致 | 待补来源不得作为确认事实引用 |
| `public/downloads/yhl-geo-enterprise-prompt-system.md` | 可下载提示词体系 Markdown | no | `CS-003`、`CS-013` | 人工审核可公开模块；补 publication status、author、reviewer | 可拆分公开摘要版和内部完整版 | Markdown 2026-07-17 | 与页面展示内容一致；发布审核字段不足 | 不是品牌官方提示词，不代表正式实施 |
| `public/downloads/yhl-geo-article-matrix.md` | 可下载文章矩阵 Markdown | no | `CS-004`、`CS-013` | 处理 B-006/B-007 待补 source_id；补审核状态 | 增加每篇文章的发布状态和审核人 | Markdown 2026-07-17 | 与页面文章矩阵一致；部分来源待补 | 文章为样稿，不是品牌官方内容 |
| `public/downloads/yhl-geo-full-article-samples.md` | 可下载完整文章样稿 Markdown | no | `CS-004`、`CS-013`、`CS-015` | 逐篇审核事实、边界、营销承诺和官方身份风险 | 每篇补 source_id/fact_id 摘要 | Markdown 2026-07-17 | 需结合文章矩阵追溯 | 个人作品集样稿，不代表品牌官方发布 |
| `public/downloads/yhl-geo-90-day-content-execution.xlsx` | 可下载 90 天策略工作簿 | conditional | `CS-006`、`CS-008` | 区分已完成、已发布、待审核等状态 | 增加 manifest/hash 记录 | 策略工作簿 2026-07-17 | 与外部 canonical XLSX 哈希一致 | 策略为内容治理计划，不承诺 AI 效果 |
| `public/downloads/yhl-geo-brand-content-optimization-plan.pdf` | 可下载 PDF 报告 | yes | 无直接阻塞 | 无 | 抽检是否仍代表当前 V2 发布状态；加入 manifest/hash | PDF 2026-07-17 | 与外部 PDF 哈希一致，可正常解析 | 已含非官方和非效果承诺声明 |
| `public/downloads/yhl-geo-brand-content-optimization-plan.docx` | 可下载 DOCX 报告 | yes | 无直接阻塞 | 无 | 确认是否需要公开可编辑版本；加入 manifest/hash | DOCX 2026-07-17 | 与外部 DOCX 哈希一致，可正常解析 | 已含非官方和非效果承诺声明 |

## 暂不适合公开的页面

- `/faq`
- `/prompt-system`
- `/geo-articles`

## 条件公开页面

- `/`
- `/jingzuo`
- `/strategy`
- `/knowledge-base`

这些页面的核心事实或指标不一定错误，但需要先完成发布状态、pending 来源和审核状态的人工决策。

## 需要人工复核的下载文件

- `public/downloads/yhl-geo-enterprise-prompt-system.md`
- `public/downloads/yhl-geo-article-matrix.md`
- `public/downloads/yhl-geo-full-article-samples.md`
- `public/downloads/yhl-geo-knowledge-base-public.json`
- `public/downloads/yhl-geo-brand-fact-knowledge-base.xlsx`
- `public/downloads/yhl-geo-90-day-content-execution.xlsx`

PDF 和 DOCX 当前不列为阻塞下载件，但建议进入发布前抽检和 manifest 登记。
