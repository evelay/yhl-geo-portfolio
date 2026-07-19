# GEO Skill Isolated Tooling

本目录用于隔离接入外部 GEO Skill 方法。当前包含阶段 06B 的
`yao-geo-page-audit` 页面审计试点，以及阶段 07A 的
`yao-geo-brand-graph` 品牌实体图谱试点。

## 边界

- 只保留本项目适配所需的上游契约、参考方法和许可证。
- 不把外部 Skill 注册为全局 Codex Skill。
- 不写入 `.codex/skills` 或 `.agents/skills`。
- 不读取 `internal-review/`、外部 canonical 工作簿、raw AI answers 或人工评分。
- 不修改 `app/`、`public/`、页面正文、Schema、robots、sitemap 或 canonical。
- 审计输出只写入 `tools/geo-skill/reports/` 和 `docs/`。

## 目录

- `upstream/yao-geo-page-audit/`：裁剪后的上游 Skill 契约、参考方法和 MIT LICENSE。
- `upstream/yao-geo-brand-graph/`：裁剪后的上游 Skill 契约、参考方法、相关脚本和 MIT LICENSE。
- `adapters/page-audit/`：本项目离线适配脚本、配置和测试。
- `adapters/brand-graph/`：本项目品牌实体图谱离线适配脚本、配置和测试。
- `reports/page-audit-pilot/`：阶段 06B 三页试点审计报告。
- `reports/brand-graph-pilot/`：阶段 07A 品牌实体图谱试点报告。

## 当前试点

审计范围固定为：

- `/`
- `/facts`
- `/buying-guide`

运行方式：

```bash
python3 tools/geo-skill/adapters/page-audit/run_local_page_audit.py
```

脚本默认读取 `out/` 中的静态 HTML，生成 Markdown、JSON、run metadata 和 findings CSV。

阶段 07A 运行方式：

```bash
python3 tools/geo-skill/adapters/brand-graph/build_brand_graph.py
```

脚本默认只读取 `public/downloads/yhl-geo-knowledge-base-public.json`，生成实体账本、关系账本、消歧表、Schema 候选输入清单、Mermaid 公开子图和 evidence-gap 报告。
