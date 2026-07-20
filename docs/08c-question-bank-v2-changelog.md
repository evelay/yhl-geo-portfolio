# 08C 问题库 v2 Release Candidate 变更日志

阶段：08C 创建版本化问题库 v2 Release Candidate
版本：v2-rc1
日期：2026-07-20

## 1. 创建目的

v2-rc1 用于在不修改当前 canonical v1 的前提下，记录 08B 已人工批准的 9 条候选问题，并为后续最终验证、人工批准、canonical 切换和 v2 核心测试集建立提供可审计基线。

## 2. v1 基线信息

- 当前 canonical 版本：v1
- 当前 canonical 文件：`redwood_geo/data/redwood_question_bank_30.csv`
- v1 记录数：30
- v1 question_id：q01 至 q30，连续且大小写一致
- v1 SHA-256：`ab0661732fffc3e0aa25adabadf5d3b9c58f00baa1c5bf045f5190ebcc596936`
- v2-rc1 不反向覆盖 v1

## 3. 新增 9 条问题

| v2 question_id | candidate_id | question | 加入原因 |
|---|---|---|---|
| q31 | CAND-INTENT-002 | 核验一件标注为元亨利的家具时，主材、辅材和证书信息应如何与合同、发票对应？ | 补齐单件证据链和购买核验任务，问题可独立复测，且可以只讨论合同、发票、证书和材质证明的对应关系。 |
| q32 | CAND-INTENT-003 | 购买后应保存哪些合同、证书、检测、交付和售后资料？ | post-decision 阶段覆盖偏薄，本题面向证据留存，不需要新增品牌事实。 |
| q33 | CAND-INTENT-005 | 如何判断官网自述、媒体报道和行业协会信息分别能证明什么？ | 来源层级和证明范围是稳定复测任务，可用方法论回答，不需要新增品牌事实。 |
| q34 | CAND-INTENT-008 | 商品宣传中的“白酸枝”“酸枝”等名称与红木国家标准名称不一致时，应以哪些文件和单件证据为准？ | 材料俗称、标准名称和产品凭证的关系是清晰缺口，可用权威标准与单件资料边界回答。 |
| q35 | CAND-INTENT-010 | 比较北京红木品牌时，如何用证据维度替代“哪个最好”？ | 补齐品牌比较框架缺口，明确避免排名化和“最好”判断，可稳定复测。 |
| q36 | CAND-INTENT-012 | 如何区分家具名称中的风格词、制作年代和收藏价值表述，避免把风格名称当成年代或价值证明？ | 风格词、年代和收藏价值的边界稳定且高风险，能补齐 q09、q22、q28 的交叉误判。 |
| q37 | CAND-INTENT-014 | 核验 AI 回答时，如果多个引用来自同一网页或二手转载，应如何复核原始来源和发布日期？ | 旧网页和二手转载的日期复核是稳定方法题，可减少 AI 把历史页面当当前事实的风险。 |
| q38 | CAND-INTENT-015 | 评价元亨利时，品牌整体信息与单件产品的材质、工艺和来源应如何区分？ | 品牌整体评价和单件产品评价混淆是高风险购买核验缺口，题目可独立理解并适合复测。 |
| q39 | CAND-INTENT-016 | 购买元亨利家具时，哪些材质、规格、证书、交付和售后承诺应写入书面合同，而不能只依赖宣传文案？ | 书面承诺边界是明确购买任务，与 q19/q26 相关但更聚焦合同化要求和宣传文案风险。 |

## 4. 排除的候选

| candidate_id | 08B 决定 | future_use | 排除原因 |
|---|---|---|---|
| CAND-INTENT-006 | merge-with-existing | merge-reference | 与 q08、q21、q22 的京作和风格边界高度重合，适合未来合并为变体或段落，不新增正式测试题。 |
| CAND-INTENT-007 | merge-with-existing | merge-reference | 与 q03 的材料主题和品牌经营事实边界同根，适合作为 q03 或材料页模块，不需要单独入库。 |
| CAND-INTENT-001 | hold-evidence | evidence-backlog | 问题有真实核验价值，但 07A2 已要求品牌、企业主体、官网和公开账号关系必须等待直接公开证据。 |
| CAND-INTENT-004 | hold-evidence | evidence-backlog | 动态信息涉及价格、门店、售后和查询日期，当前缺少可执行的日期复核规则和官方渠道证据。 |
| CAND-INTENT-009 | hold-evidence | evidence-backlog | 荣誉、排名和背书属于高风险强断言，当前缺少原始颁发主体、年份、证书或公开来源证据。 |
| CAND-INTENT-011 | hold-evidence | evidence-backlog | 07A2 已明确京作身份缺直接 evidence_id，不能通过问题入库暗示已有官方身份。 |
| CAND-INTENT-017 | page-follow-up-only | page-follow-up | q28 已覆盖收藏投资谨慎边界，本题更适合成为页面中的降级表达提示，不需要扩正式题。 |
| CAND-INTENT-018 | page-follow-up-only | page-follow-up | 这是内部数据治理和方法页说明，适合放入 08C 门禁或方法页面追问，不属于面向 AI 平台复测的市场问题。 |
| CAND-INTENT-013 | manual-review | multimodal-review | 问题价值高，但现有材料不足以确定它应进入正式复测题还是仅作为图片证据边界指南。 |

## 5. merge 候选处理

CAND-INTENT-006 和 CAND-INTENT-007 不进入 v2-rc1。它们保留为既有问题的合并参考，后续只能作为 q08/q21/q22 或 q03/q16 相关页面段落、追问变体或人工合并建议使用。

## 6. hold 候选处理

CAND-INTENT-001、CAND-INTENT-004、CAND-INTENT-009 和 CAND-INTENT-011 不进入 v2-rc1。它们进入证据补采 backlog，必须先补齐直接公开证据、来源年份和证明范围，再重新进入人工评审。

## 7. 页面追问处理

CAND-INTENT-017 和 CAND-INTENT-018 不进入 v2-rc1。它们只保留为页面追问或治理流程说明候选，不作为 AI 平台正式复测问题。

## 8. 图片场景处理

CAND-INTENT-013 继续暂缓。该问题涉及图片输入、单件对象识别、材质与真伪边界，08C 不创建图片测试题，不自动批准该候选，也不建立多模态测试集。

## 9. 总问题数量

- v1 原样保留：30
- 新增已批准候选：9
- v2-rc1 总量：39
- 排除候选：9
- 本轮人工核验后不修改：q32、q33、q35
- 本轮人工核验后 refined wording：q31、q34、q36、q37、q38、q39

## 10. 未切换 canonical 的原因

v2-rc1 只是版本化 release candidate。39 条最终文本、q31 至 q39 正式 ID、新增问题分类、风险标签、证据需求和页面映射仍需用户最终确认。确认前，网站不得读取 v2-rc1，平台不得使用 v2-rc1 复测。

## 11. 下一步验证

进入下一阶段前，需要人工最终确认：39 条问题文本、q31 至 q39 ID、分类、风险标签、证据需求、页面映射、是否切换 canonical，以及是否创建 v2 核心测试集。

## 12. 回滚方式

删除或忽略 `data/question-bank/redwood_question_bank_v2_rc1.csv`、`data/question-bank/question_bank_versions.json`、`data/question-bank/README.md` 和 08C 文档即可回到 v1-only 状态。外部 v1 canonical 未被修改，因此不需要从 v2 回写或恢复 v1。
