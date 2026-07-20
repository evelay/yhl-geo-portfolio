# 08C 问题库 v2 Release Candidate 验证报告

阶段：08C
版本：v2-rc1
日期：2026-07-20

## 验证结果

| 检查项 | 结果 | 说明 |
|---|---|---|
| v2 总数恰好 39 | pass | v2-rc1 CSV 记录数为 39。 |
| 前 30 条与 v1 question_id 完全一致 | pass | q01 至 q30 顺序一致。 |
| 前 30 条问题文本完全一致 | pass | 逐行比对通过。 |
| v1 顺序保持不变 | pass | v2 前 30 行沿用 v1 顺序。 |
| 新增 9 条与批准名单完全一致 | pass | CAND-INTENT-002, CAND-INTENT-003, CAND-INTENT-005, CAND-INTENT-008, CAND-INTENT-010, CAND-INTENT-012, CAND-INTENT-014, CAND-INTENT-015, CAND-INTENT-016 |
| 新 question_id 唯一 | pass | q31 至 q39 未重复。 |
| 不存在重复问题文本 | pass | 39 条问题文本唯一。 |
| 不存在空 question_id | pass | 所有 id 非空。 |
| 不存在空问题文本 | pass | 所有 question 非空。 |
| 9 条新增问题都有 primary_intent | pass | 新增行均来自 08A 候选元数据。 |
| 9 条新增问题都有 risk_level | pass | 新增行均包含 risk_level。 |
| 高风险问题都有 evidence_requirements | pass | 高风险新增行均包含 evidence_requirements。 |
| hold、page-follow-up、manual-review 候选未混入 v2 | pass | 排除候选只出现在 docs/08c-excluded-candidates.csv。 |
| v1 文件哈希未改变 | pass | ab0661732fffc3e0aa25adabadf5d3b9c58f00baa1c5bf045f5190ebcc596936 |
| v2 文件不含绝对本地路径 | pass | v2 CSV 未记录本地绝对路径。 |
| v2 文件不含虚构流量或效果类指标 | pass | v2 CSV 仅含问题与治理字段。 |

## 关键计数

- v1 canonical：30 条
- v2-rc1：39 条
- 原样保留：30 条
- 新增 approved candidates：9 条
- 排除 candidates：9 条

## 边界确认

- v2-rc1 未切换为 canonical。
- 网站未读取 v2-rc1。
- 本阶段未创建答案、页面、复测表或核心测试集。
- 外部 v1 canonical 哈希保持为 `ab0661732fffc3e0aa25adabadf5d3b9c58f00baa1c5bf045f5190ebcc596936`。

## 离线测试

- `python3 tools/geo-skill/adapters/intent-miner/validate_question_bank_v2.py`：pass
- `python3 -m unittest discover tools/geo-skill/adapters/intent-miner/tests`：20 tests passed
