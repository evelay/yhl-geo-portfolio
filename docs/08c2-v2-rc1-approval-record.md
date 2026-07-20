# 08C2 v2-rc1 Approval Record

阶段：08C2
日期：2026-07-20

## 批准对象

- approved object: `data/question-bank/redwood_question_bank_v2_rc1.csv`
- approved version: v2-rc1
- approved record count: 39
- carried from v1: 30
- additions: 9

## 人工检查范围

用户已完成人工检查，并确认：

1. q01-q30 保持 v1 原文不变。
2. q31-q39 的问题文本通过。
3. q31-q39 的 question_id 通过。
4. 候选 ID 映射通过。
5. 分类、风险等级和证据需求通过。
6. v2 总问题数为 39。
7. 未批准候选没有进入 v2。
8. CAND-INTENT-013 继续留在 multimodal-review。
9. 当前只批准 release candidate，不切换 canonical。

## q31-q39 最终确认

- q31-q39 的 question_id 连续且唯一。
- q31-q39 的 source_candidate_id 与批准候选映射一致。
- q31-q39 的问题文本、分类、风险等级和证据需求按人工检查结果批准为 v2-rc1。
- 本阶段未修改任何问题文本、question_id 或 source_candidate_id。

## v1 哈希

- canonical v1 SHA-256: `ab0661732fffc3e0aa25adabadf5d3b9c58f00baa1c5bf045f5190ebcc596936`
- canonical v1 status: unchanged

## 未进入 v2 的候选

以下候选未进入 v2-rc1：

- CAND-INTENT-001
- CAND-INTENT-004
- CAND-INTENT-006
- CAND-INTENT-007
- CAND-INTENT-009
- CAND-INTENT-011
- CAND-INTENT-013
- CAND-INTENT-017
- CAND-INTENT-018

## 图片问题暂缓原因

CAND-INTENT-013 仍保留为 multimodal-review。该候选涉及用户仅提供产品图片时的材质和真伪判断边界，必须先建立图片来源、对象明确性、多模态证据规则和人工风险边界；当前不得仅凭图片进入正式 v2 复测题。

## 当前边界

- canonical switched: no
- website consuming v2: no
- platform retest using v2: no
- core test set created: no
- platform retest sheet created: no
- answers generated: no
- content pages created: no

## 下一阶段进入条件

进入 08D 前必须保持当前批准记录、版本清单和 v2-rc1 验证通过，并由用户明确授权下一阶段范围。08D 才可以在不切换 canonical 的前提下准备后续测试或复测相关资产；若需切换 canonical，必须另行取得明确批准。

## 回滚方式

如需撤回本次批准，回滚本阶段提交即可：恢复 `docs/08c-v2-release-approval.md` 的 human review status，移除 `question_bank_versions.json` 中 release candidate approval 相关字段，并删除本批准记录。由于本阶段未修改 canonical v1、v2 CSV、网站代码或 public 资源，无需从 v2 回写或恢复问题文本。
