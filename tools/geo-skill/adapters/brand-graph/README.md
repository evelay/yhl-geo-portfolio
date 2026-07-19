# 07A Brand Graph Adapter

本目录是 `yao-geo-brand-graph` 的元亨利作品集离线适配层。

## Scope

- 只读取 `public/downloads/yhl-geo-knowledge-base-public.json`。
- 不读取 `internal-review/`、外部工作簿、PDF/DOCX、完整文章样稿、完整提示词或历史归档。
- 不联网，不调用 API，不调用模型，不运行 crawler。
- 不修改输入 JSON。
- 只写入 `docs/` 和 `tools/geo-skill/reports/brand-graph-pilot/`。
- 不生成生产 JSON-LD、RDF、页面脚本或 `app/` / `public/` 修改。

## Run

```bash
python3 tools/geo-skill/adapters/brand-graph/build_brand_graph.py
```

## Outputs

- `docs/07a-entity-ledger.csv`
- `docs/07a-relation-ledger.csv`
- `docs/07a-disambiguation-table.csv`
- `docs/07a-schema-input-candidates.csv`
- `docs/07a-brand-graph-method.md`
- `tools/geo-skill/reports/brand-graph-pilot/report.md`
- `tools/geo-skill/reports/brand-graph-pilot/brand-graph.json`
- `tools/geo-skill/reports/brand-graph-pilot/brand-graph.mmd`
- `tools/geo-skill/reports/brand-graph-pilot/run-metadata.json`
- `tools/geo-skill/reports/brand-graph-pilot/evidence-gap-report.md`

All relations are candidates. The adapter never marks a relation as approved.
