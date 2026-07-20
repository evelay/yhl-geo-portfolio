# 08A Intent Miner Adapter

本目录是 `yao-geo-intent-miner` 的元亨利作品集离线适配层。

## Scope

- 只读 canonical 问题库 `redwood_question_bank_30.csv`。
- 只读取安全公开知识库 JSON、07A 实体/消歧记录和 07A2 人工决定作为证据与边界参考。
- 不读取 `internal-review/`、archive、外部完整工作簿、原始 AI 回答、人工评分、未审核 FAQ、完整提示词、完整文章样稿或 PDF/DOCX。
- 不联网，不调用 API，不调用模型，不运行 crawler。
- 不修改 canonical，不生成正式答案，不生成文章，不创建页面。
- 只写入 `docs/` 与 `tools/geo-skill/reports/intent-miner-pilot/`。
- 不修改 `app/`、`public/`、`app/data.ts` 或网站页面。

## Run

```bash
python3 tools/geo-skill/adapters/intent-miner/audit_question_intents.py
python3 tools/geo-skill/adapters/intent-miner/build_core_test_set_rc1.py
```

## Outputs

- `docs/08a-question-intent-audit.csv`
- `docs/08a-follow-up-chains.csv`
- `docs/08a-candidate-questions.csv`
- `docs/08a-intent-coverage-matrix.csv`
- `docs/08a-question-route-map.csv`
- `docs/08a-intent-miner-method.md`
- `tools/geo-skill/reports/intent-miner-pilot/report.md`
- `tools/geo-skill/reports/intent-miner-pilot/report.json`
- `tools/geo-skill/reports/intent-miner-pilot/run-metadata.json`

All candidate questions remain `candidate`; none are written into canonical.

## 08D1 Core Test Set Outputs

- `data/question-bank/redwood_question_bank_v2_core24_rc1.csv`
- `docs/08d1-non-core-question-usage.csv`
- `docs/08d1-core-test-selection.csv`
- `docs/08d1-test-objective-matrix.csv`
- `docs/08d1-evidence-acquisition-backlog.csv`
- `docs/08d1-evidence-acquisition-plan.md`
- `docs/08d1-core-test-protocol.md`
- `docs/08d1-human-review.md`
- `docs/08d1-core-test-set-method.md`
- `tools/geo-skill/reports/core-test-set-pilot/report.md`
- `tools/geo-skill/reports/core-test-set-pilot/report.json`
- `tools/geo-skill/reports/core-test-set-pilot/run-metadata.json`

08D1 remains planning-only: no platform tests, no evidence search, no answers,
and no website runtime changes.

## Test

```bash
python3 tools/geo-skill/adapters/intent-miner/validate_core_test_set_rc1.py
python3 -m unittest discover tools/geo-skill/adapters/intent-miner/tests
```
