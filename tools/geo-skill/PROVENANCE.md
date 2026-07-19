# 阶段 06B GEO Skill 来源记录

## 来源

- 来源仓库：`https://github.com/yaojingang/yao-geo-skills`
- 来源 Skill：`skills/yao-geo-page-audit`
- 来源 commit SHA：`dc10716d97c40fed0a0a08e538a236b5e16b4822`
- 获取日期：2026-07-19
- 原许可证：MIT License
- 本地裁剪目录：`tools/geo-skill/upstream/yao-geo-page-audit/`

## 已复制文件

- `LICENSE`
- `SKILL.md`
- `manifest.json`
- `agents/interface.yaml`
- `templates/brief-template.md`
- `evals/trigger_cases.json`
- `evals/expected_artifacts.json`
- `evals/quality_cases.json`
- `references/research-foundation.md`
- `references/authority-reference-model.md`
- `references/report-module-taxonomy.md`
- `references/quality-gates.md`
- `references/report-formatting-spec.md`
- `references/output-layout-policy.md`
- `references/page-audit-method.md`

## 已读取但未复制

- `scripts/polish_docx.py`
- `scripts/review_report_layout.py`
- `templates/report.css`
- `reports/output-risk-profile.md`
- `reports/artifact-design-profile.md`

未复制原因：上述文件主要服务原 Skill 的 Word/PDF/HTML 四件套渲染、排版质检和示例交付。本阶段禁止生成 Word/PDF，且只需要 Markdown/JSON/CSV 离线审计报告。

## 未复制内容

- 未复制整个 `yao-geo-skills` 仓库。
- 未复制 examples、PDF、DOCX、HTML 示例报告或预览素材。
- 未复制 crawler、GEOFlow 文件或其他无关 Skill。
- 未复制依赖锁文件、图片或示例运行输出。

## 修改说明

上游文件在 `upstream/` 下保持原样复制，未修改版权、许可证或内容。

本项目新增的适配文件位于：

- `tools/geo-skill/adapters/page-audit/README.md`
- `tools/geo-skill/adapters/page-audit/audit-config.json`
- `tools/geo-skill/adapters/page-audit/run_local_page_audit.py`
- `tools/geo-skill/adapters/page-audit/tests/test_run_local_page_audit.py`

这些文件是本项目离线适配层，不是对上游 Skill 文件的修改。

## 使用边界

- 只读取当前分支构建后的 `out/` 静态 HTML、`out/robots.txt` 和 `out/sitemap.xml`。
- 不读取 `internal-review/`。
- 不读取 `first_setup/`、`final/`、archive 或 outdated 文件。
- 不读取外部 canonical 工作簿、raw AI answers 或人工评分。
- 不调用外部模型、外部 API 或 crawler。
- 不把页面审计结论解释为 AI 排名、品牌召回率、引用份额、AI 引用概率或收录概率。
- 不把 Schema、结构完整度或可读性解释为 AI 引用概率。
- 不自动写入 `app/`、`public/`、Schema、robots、sitemap 或 canonical。

## 网络记录

为获取指定上游仓库，本阶段使用 GitHub 只读网络克隆。页面审计脚本本身不联网，`run-metadata.json` 中 `network_used=false`、`api_used=false` 表示审计运行阶段没有网络或 API 使用。

---

# 阶段 07A GEO Skill 来源记录

## 来源

- 来源仓库：`https://github.com/yaojingang/yao-geo-skills`
- 来源 Skill：`skills/yao-geo-brand-graph`
- 来源 commit SHA：`dc10716d97c40fed0a0a08e538a236b5e16b4822`
- 获取日期：2026-07-19
- 原许可证：MIT License
- 本地裁剪目录：`tools/geo-skill/upstream/yao-geo-brand-graph/`

Git 根目录未发现 `AGENTS.md`，因此 07A 以现有 `docs/` 治理文件和 `public/downloads/manifest.json` 作为项目规则来源。

## 已复制文件

- `LICENSE`
- `SKILL.md`
- `manifest.json`
- `agents/interface.yaml`
- `templates/brief-template.md`
- `evals/trigger_cases.json`
- `evals/expected_artifacts.json`
- `references/skill-method.md`
- `references/real-data-acquisition.md`
- `references/entity-schema.md`
- `references/evidence-policy.md`
- `references/quality-gates.md`
- `references/research-backed-framework.md`
- `reports/output-risk-profile.md`
- `reports/artifact-design-profile.md`
- `scripts/collect_source_validation.py`
- `scripts/render_yao_geo_brand_graph.py`

## 已读取但未复制

- `evals/rubric.md`
- `evals/failure_cases.md`
- `examples/hubspot-domestic-ai-test/*`

未复制原因：examples 包含示例输入、生成报告、Word/PDF/HTML 和质量报告，和本项目数据无关；07A 禁止复制大量 examples、截图、其他 Skill 或示例运行输出。

## 未复制内容

- 未复制整个 `yao-geo-skills` 仓库。
- 未复制 examples、PDF、DOCX、HTML 示例报告或预览素材。
- 未复制 crawler、GEOFlow 文件或其他无关 Skill。
- 未复制依赖锁文件、图片或示例运行输出。
- 未安装为全局 Codex Skill。
- 未写入 `.codex/skills`、`.agents/skills`、`~/.codex/skills` 或 `~/.agents/skills`。

## 修改说明

上游文件在 `upstream/` 下保持原样复制，未修改版权、许可证或内容。

本项目新增的适配文件位于：

- `tools/geo-skill/adapters/brand-graph/README.md`
- `tools/geo-skill/adapters/brand-graph/graph-config.json`
- `tools/geo-skill/adapters/brand-graph/build_brand_graph.py`
- `tools/geo-skill/adapters/brand-graph/tests/test_build_brand_graph.py`

这些文件是本项目离线适配层，不是对上游 Skill 文件的修改。

## 使用边界

- 只读取 `public/downloads/yhl-geo-knowledge-base-public.json` 作为品牌数据输入。
- 治理文档只作为规则依据，不从中重新提取未公开品牌事实。
- 不读取 `internal-review/`。
- 不读取 `first_setup/`、`yhl_geo_portfolio_final/`、archive 或 outdated 文件。
- 不读取外部 canonical 工作簿、PDF/DOCX、完整文章、完整提示词、raw AI answers 或人工评分。
- 不调用外部模型、外部 API、URL 连通核验、crawler 或浏览器自动化。
- 不把实体关系推断写成确认事实。
- 不把内容主题关系写成经营事实。
- 不把材料关系写成产品全量事实。
- 不自动写入 `app/`、`public/`、生产 Schema、JSON-LD、RDF、页面正文、H1、breadcrumb 或 canonical。

## 网络记录

为获取指定上游仓库，本阶段使用 GitHub 只读网络克隆。品牌图谱构建脚本本身不联网，`run-metadata.json` 中 `network_used=false`、`api_used=false`、`model_used=false`、`crawler_used=false` 表示图谱生成阶段没有网络、API、模型或 crawler 使用。

---

# 阶段 07C1 GEO Skill 来源记录

## 来源

- 来源仓库：`https://github.com/yaojingang/yao-geo-skills`
- 来源 Skill：`skills/yao-geo-page-blueprint`
- 来源 commit SHA：`eabfde0f0bdf53f84559bdfcba2595fcac1ad50f`
- 获取日期：2026-07-19
- 原许可证：MIT License
- 本地裁剪目录：`tools/geo-skill/upstream/yao-geo-page-blueprint/`

Git 根目录未发现 `AGENTS.md`，因此 07C1 以现有 `docs/` 治理文件、三页源码和构建后的 `out/` HTML 作为项目规则来源。

## 已复制文件

- `LICENSE`
- `SKILL.md`
- `manifest.json`
- `agents/interface.yaml`
- `templates/brief-template.md`
- `evals/trigger_cases.json`
- `evals/expected_artifacts.json`
- `evals/quality_cases.json`
- `evals/rubric.md`
- `evals/failure_cases.md`
- `references/page-blueprint-method.md`
- `references/research-foundation.md`
- `references/cn-ai-platform-adaptation.md`
- `references/schema-html-cms-contract.md`
- `references/real-data-workflow.md`
- `references/artifact-layout.md`
- `references/quality-gates.md`
- `references/output-file-workflow.md`
- `reports/output-risk-profile.md`
- `reports/artifact-design-profile.md`
- `scripts/render_yao_geo_page_blueprint.py`

## 已读取但未复制

无。上游 examples、示例报告、截图和其他 Skill 未读取文件内容，也未作为本阶段输入复制。

## 未复制内容

- 未复制整个 `yao-geo-skills` 仓库。
- 未复制 examples、PDF、DOCX、HTML 示例报告、截图或预览素材。
- 未复制 crawler、GEOFlow 文件或其他无关 Skill。
- 未复制依赖锁文件、图片或示例运行输出。
- 未安装为全局 Codex Skill。
- 未写入 `.codex/skills`、`.agents/skills`、`~/.codex/skills` 或 `~/.agents/skills`。

## 修改说明

上游文件在 `upstream/` 下保持原样复制，未修改版权、许可证或内容。

本阶段新增的项目文件位于：

- `docs/07c1-page-blueprint-method.md`
- `docs/07c1-h1-options.csv`
- `docs/07c1-breadcrumb-options.csv`
- `docs/07c1-human-review.md`
- `tools/geo-skill/reports/page-blueprint-pilot/`

这些文件是本项目页面蓝图报告，不是对上游 Skill 文件的修改。

## 使用边界

- 只为 `/`、`/facts` 和 `/buying-guide` 生成 H1、页面摘要和用户可见 breadcrumb 蓝图。
- 只读取当前分支相关源码、构建后 HTML 和治理报告；`app/data.ts` 仅作为 website-copy 观察导航与页面标签，不作为品牌事实主源。
- 不读取 `internal-review/` 文件内容。
- 不读取 `first_setup/`、`final/`、archive 或 outdated 文件。
- 不读取外部 canonical 工作簿、raw AI answers 或人工评分。
- 不调用外部模型、外部 API、crawler 或浏览器自动化。
- 不把 H1、breadcrumb 或摘要建议解释为 AI 排名、收录、引用概率或优化增长。
- 不自动写入 `app/`、`public/`、生产 Schema、JSON-LD、页面正文、H1、title、description、canonical、sitemap 或 robots。

## 网络记录

为获取指定上游仓库，本阶段使用 GitHub 只读网络克隆。页面蓝图生成阶段不联网，`run-metadata.json` 中 `network_used=false`、`api_used=false`、`model_used=false`、`crawler_used=false` 表示蓝图生成阶段没有网络、API、模型或 crawler 使用。

---

# 阶段 08A GEO Skill 来源记录

## 来源

- 来源仓库：`https://github.com/yaojingang/yao-geo-skills`
- 来源 Skill：`skills/yao-geo-intent-miner`
- 来源 commit SHA：`eabfde0f0bdf53f84559bdfcba2595fcac1ad50f`
- 获取日期：2026-07-20
- 原许可证：MIT License
- 本地裁剪目录：`tools/geo-skill/upstream/yao-geo-intent-miner/`

Git 根目录未发现 `AGENTS.md`，因此 08A 以现有治理文档、canonical 问题库、安全公开知识库 JSON、07A 实体/消歧记录和 07A2 人工决定作为项目规则来源。

## 已复制文件

- `LICENSE`
- `SKILL.md`
- `manifest.json`
- `agents/interface.yaml`
- `templates/brief-template.md`
- `evals/trigger_cases.json`
- `evals/expected_artifacts.json`
- `evals/quality_cases.json`
- `references/research-foundation.md`
- `references/intent-mining-method.md`
- `references/cn-platform-adaptation.md`
- `references/scoring-and-mapping.md`
- `references/real-data-ingestion.md`
- `references/report-module-contract.md`
- `references/four-format-output.md`
- `references/quality-gates.md`
- `scripts/render_intent_miner_report.py`
- `scripts/check_report_layout.py`

## 未读取且未复制的相邻文件

- `evals/rubric.md`
- `evals/failure_cases.md`
- `examples/README.md`

未读取和未复制原因：上述文件为评测说明或示例入口；本阶段只需要触发、产物、方法、报告契约、质量门和脚本参考。examples 下的示例输入、示例输出、HTML、PDF、DOCX 和索引页未读取、未复制、未作为本阶段输入。

## 未复制内容

- 未复制整个 `yao-geo-skills` 仓库。
- 未复制 examples、PDF、DOCX、HTML 示例报告或预览素材。
- 未复制 crawler、GEOFlow 文件或其他无关 Skill。
- 未复制依赖锁文件、图片或示例运行输出。
- 未安装为全局 Codex Skill。
- 未写入 `.codex/skills`、`.agents/skills`、`~/.codex/skills` 或 `~/.agents/skills`。

## 修改说明

上游文件在 `upstream/` 下保持原样复制，未修改版权、许可证或内容。

本阶段新增的项目适配文件位于：

- `tools/geo-skill/adapters/intent-miner/README.md`
- `tools/geo-skill/adapters/intent-miner/intent-config.json`
- `tools/geo-skill/adapters/intent-miner/audit_question_intents.py`
- `tools/geo-skill/adapters/intent-miner/tests/test_audit_question_intents.py`

本阶段新增的审计输出位于：

- `docs/08a-question-intent-audit.csv`
- `docs/08a-follow-up-chains.csv`
- `docs/08a-candidate-questions.csv`
- `docs/08a-intent-coverage-matrix.csv`
- `docs/08a-question-route-map.csv`
- `docs/08a-intent-miner-method.md`
- `tools/geo-skill/reports/intent-miner-pilot/`

这些文件是本项目离线适配层和审计报告，不是对上游 Skill 文件的修改。

## 使用边界

- 只读 canonical 30 题问题库，保留原 `question_id`、原问题文本和原分类。
- 安全公开知识库 JSON 只用于证据需求和页面映射判断，不作为问题库主源。
- 不读取 `internal-review/`。
- 不读取 `first_setup/`、`yhl_geo_portfolio_final/`、archive 或 outdated 文件。
- 不读取外部完整工作簿、raw AI answers、人工评分、未审核 FAQ、完整提示词、完整文章样稿或 PDF/DOCX。
- 不调用外部模型、外部 API、URL 连通核验、crawler 或浏览器自动化。
- 不生成正式答案、文章、FAQ 正文、新页面或生产 Schema。
- 不自动写入 canonical、`app/`、`public/`、`app/data.ts` 或网站页面。
- 不把候选问题、页面映射或覆盖状态解释为市场规模、平台热度、排名或效果预测。

## 网络记录

为获取指定上游仓库，本阶段使用 GitHub 只读网络克隆。Intent Miner 审计脚本本身不联网，`run-metadata.json` 中 `audit_network_used=false`、`api_used=false`、`model_api_used=false`、`crawler_used=false` 表示审计运行阶段没有网络、API、模型 API 或 crawler 使用。
