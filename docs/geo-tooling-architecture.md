# 阶段 06A GEO 工具架构评估

## 四个仓库定位

| 仓库 | 定位 | 对当前项目的结论 |
| --- | --- | --- |
| `GEO-Content-Optimizer-Skill` | 单体 GEO prompt 和脚本包，覆盖 Schema、可读性、Pillar、可见度和 URL 内容差距分析 | 方法有参考价值，但需要拆分、重写和补治理；不可直接接入 |
| `yao-geo-skills` | 多 Skill 工具集，按知识资产、意图、页面、内容、监测和 GEOFlow 运营拆分 | 最适合作为当前六层 GEO 项目的能力来源，但必须用安全输入和文档化输出方式接入 |
| `yao-meta-skill` | Skill 工程、评测、治理、打包和迭代系统 | 不直接处理业务数据；适合 06C/07 把适配后的内部流程固化为 Skill |
| `GEOFlow` | 完整 GEO 内容工程和多站点分发平台 | 当前不部署；后续如要验证内容运营平台，应建立独立 PoC |

## 六层映射

| 六层 | 主要能力 | 推荐工具 | 接入方式 |
| --- | --- | --- | --- |
| 1. 品牌实体与事实治理 | 实体、别名、关系、事实卡、来源等级、禁用表达 | `yao-geo-brand-graph`、`yao-geo-knowledge-base-builder` | 只读安全公开知识库 JSON，输出 docs 下实体图谱和事实卡审计 |
| 2. 用户问题与搜索意图 | 30 题问题库、追问链路、查询重写、监测 Prompt | `yao-geo-intent-miner` | 读取审核后的问题库副本和公开 FAQ，输出意图矩阵 |
| 3. AI 可见度基线与诊断 | 基线说明、平台差异、采样口径、页面素材覆盖 | `yao-geo-page-audit`、`yao-geo-effect-monitor` | 06B 先做页面和监测设计，不运行平台采样 |
| 4. 内容知识资产 | 知识库、内容 brief、页面模块、事实卡、公开摘录 | `yao-geo-knowledge-base-builder`、`yao-geo-page-blueprint`、后续 `yao-geo-content-refiner` | 当前不生成文章；只输出内容资产结构和待审清单 |
| 5. 技术可发现与结构化 | 可抓取性、语义 HTML、Schema 候选、CMS 字段 | `yao-geo-page-audit`、`yao-geo-page-blueprint` | 只输出建议，不自动写 `app/` 或 `public/`，不生成上线 Schema |
| 6. 监测、复测与迭代 | 归因字段、月报、复测 Prompt、纠偏闭环、工具治理 | `yao-geo-tracking`、`yao-geo-effect-monitor`、后续 `yao-meta-skill` | 先建立指标口径和输出契约，再决定是否 PoC crawler 或 GEOFlow |

## 推荐安全架构

当前站点不是事实数据库。所有工具接入必须沿用现有治理链路：

```mermaid
flowchart LR
  C["外部 canonical<br/>只读主源"] --> R["人工审核"]
  R --> S["安全公开副本<br/>JSON/CSV/Markdown 摘录"]
  S --> T["GEO Skill 临时运行<br/>不调用 API 或仅经批准调用"]
  T --> D["docs/ 下报告和候选清单"]
  D --> H["人工审核"]
  H --> W["未来网站同步任务<br/>另行阶段执行"]
```

关键规则：

- Skill 不得直接读取 `internal-review` 作为外部 API 输入。
- Skill 不得把外部 canonical 工作簿传入 API、crawler、GEOFlow 或浏览器自动化。
- Skill 输出只落在 `docs/` 或临时运行目录。
- `app/`、`public/`、`AGENTS.md` 不由 06A 或 06B 自动修改。
- 所有 Schema、文章、页面改造、下载文件更新都必须进入后续人工审核阶段。

## 重叠关系

| 重叠区域 | 涉及工具 | 处理建议 |
| --- | --- | --- |
| 知识库和实体图谱 | `yao-geo-brand-graph`、`yao-geo-knowledge-base-builder` | Brand Graph 负责实体关系和消歧；Knowledge Base Builder 负责事实卡、FAQ、禁用表达和 prompt input pack |
| 页面诊断和页面蓝图 | `yao-geo-page-audit`、`yao-geo-page-blueprint` | Page Audit 先诊断现有公开路由；Page Blueprint 后生成未来改版蓝图 |
| 内容改造和文章生成 | `yao-geo-content-refiner`、`yao-geo-article-friendly`、`yao-geo-explainer-builder`、`yao-geo-ranking-article-builder` | 当前只保留 Content Refiner 的公开页面改造建议；文章生成类全部暂缓或拒绝 |
| 可见度和监测 | 原 `visibility_tester.py`、`yao-geo-effect-monitor`、三类 crawler | 旧可见度脚本重写；Effect Monitor 先做口径；crawler 只进独立复测 PoC |
| GEOFlow 运营和平台 | `GEOFlow`、`yao-geoflow-cli`、`yao-geoflow-design`、`yao-geoflow-template` | 当前不接入；只有独立 PoC 后才使用 CLI/design，legacy template 拒绝 |

## 推荐 06B 第一接入模块

推荐从 `yao-geo-page-audit` 开始，采用本项目安全模式：

- 输入：公开路由、本仓库治理文档、安全知识库 JSON、manifest。
- 输出：`docs/06b/page-audit/` 下的页面可抓取性、AI 可抽取性、内容证据、Schema 候选和修复清单。
- 禁止：不自动改页面、不生成 Schema、不跑 AI 平台采样、不读取 internal-review。

理由：它最贴近当前静态作品集的公开发布面，能在不触碰外部 canonical 和不生成内容的前提下，为后续 Brand Graph、Intent Miner、Tracking 和 Effect Monitor 提供页面级问题清单。
