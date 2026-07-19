# 阶段 06B 页面审计方法

## Skill 来源

本阶段参考 `yao-geo-skills` 仓库中的 `skills/yao-geo-page-audit`。

- 来源仓库：`https://github.com/yaojingang/yao-geo-skills`
- 来源 commit：`dc10716d97c40fed0a0a08e538a236b5e16b4822`
- 原许可证：MIT
- 本地裁剪目录：`tools/geo-skill/upstream/yao-geo-page-audit/`

Git 根目录未发现 `AGENTS.md`，因此本阶段以现有 `docs/` 治理文件和 `public/downloads/manifest.json` 作为项目规则来源。

## 原 Skill 方法

原 Skill 将页面 GEO 诊断拆成发现入口、检索候选、主内容抽取、证据质量和生成引用五段链路，并要求覆盖：

- 可抓取性、robots、sitemap、canonical、meta robots 和静态 HTML 正文。
- H1-H3、`main`、`article`、FAQ、表格、列表、面包屑、内链和锚文本。
- 结论前置、实体全称、来源、更新时间、事实/判断/建议边界和效果承诺风险。
- 原子事实、key-value 信息、问答结构、步骤结构、比较维度和区块引用准备度。
- JSON-LD 是否存在、类型、正文一致性和缺失字段。

原 Skill 默认输出 Markdown、HTML、Word、PDF 和 `quality-report.json`，并可在有公开材料时进行 Web 取证。

## 当前项目适配

本阶段只保留页面审计方法、证据分层和报告清单，不接入原 Skill 的四件套渲染链路。

适配层位于 `tools/geo-skill/adapters/page-audit/`，使用 Python 标准库实现：

- 只读取当前分支构建后的 `out/` 静态 HTML。
- 不联网，不调用模型或 API。
- 不运行 crawler。
- 不修改 HTML。
- 不写入 `app/` 或 `public/`。
- 输出进入 `tools/geo-skill/reports/page-audit-pilot/` 和 `docs/06b-page-audit-findings.csv`。

上游 `scripts/polish_docx.py` 与 `scripts/review_report_layout.py` 已读取，但未复制、未运行，因为本阶段禁止生成 Word/PDF。

## 审计范围

本阶段只审计三个代表页面：

- `/`：首页，代表作品集整体叙事和项目身份。
- `/facts`：品牌事实页，代表品牌事实与证据表达。
- `/buying-guide`：购买指南页，代表决策型 GEO 内容。

不得扩展到其他页面。

## 输入边界

允许输入：

- `out/index.html`
- `out/facts/index.html`
- `out/buying-guide/index.html`
- `out/robots.txt`
- `out/sitemap.xml`

禁止输入：

- `internal-review/`
- `first_setup/`
- `final/`
- archive 或 outdated 文件
- 外部 canonical 工作簿
- raw AI answers
- 人工评分工作簿
- `app/data.ts`
- TSX 页面源码
- `public/` 下载副本作为事实主源

`app/data.ts` 在本项目中只是 website-copy，不作为审计事实裁决来源。外部 canonical 工作簿不得修改，也不得作为本阶段脚本输入。

## 不分析的内容

本阶段不分析也不输出：

- AI 平台排名。
- AI 平台召回率。
- AI 引用概率。
- AI 收录概率。
- 品牌召回率。
- 引用份额。
- 优化后提升预测。
- 原始 AI 回答质量。
- 人工评分正确性。
- 平台内部权重或日志级抓取频率。

页面审计结论不得解释为 AI 排名、品牌召回率、引用份额或引用概率；Schema、结构完整度和可读性也不得解释为 AI 引用概率。

## 评分与证据规则

本阶段不生成单一 GEO 总分，也不把缺失字段自动视为零分。

每条 finding 必须包含：

- `evidence_status`：`observed`、`source-confirmed`、`inferred`、`input-gap` 或 `not-applicable`。
- `severity`：`high`、`medium` 或 `low`。
- `priority`：`P0`、`P1`、`P2` 或 `P3`。
- `owner`：`content`、`development`、`data`、`research` 或 `design`。
- `acceptance_test`：明确验收方式。
- `status`：初始统一为 `open`。

`inferred` 只能表示基于页面证据和方法规则的推断，不得写成事实。

## 人工审核节点

以下动作必须在后续阶段进入人工审核，不由本阶段自动修复：

- 修改页面正文、标题、模块或样式。
- 修正 canonical、robots、sitemap 或 basePath。
- 增加 JSON-LD 或 Schema。
- 新增 source_id、事实卡、来源映射或 key-value 模块。
- 解释品牌事实、荣誉、排名、门店、价格、售后或投资相关内容。
- 从 `internal-review`、外部 canonical 或公开下载副本同步任何事实。

## 与原 GEO Content Optimizer 的差异

本阶段不是接入旧的 GEO Content Optimizer。

关键差异：

- 不运行可见度测试脚本，不调用 Perplexity、Kimi、OpenAI 或其他 API。
- 不使用关键词密度或传统 SEO 总分作为核心结论。
- 不生成 AI 排名、引用率、召回率或趋势预测。
- 不自动生成 Schema；只记录 Schema 存在性和正文一致性检查结果。
- 不把 `app/data.ts`、TSX 页面或构建 HTML 反向当作 canonical。
- 不读取 `internal-review`、外部工作簿、raw answers 或人工评分。
- 输出是隔离审计报告和 open findings，不触发页面修复。
