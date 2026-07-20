# 阶段 08B 候选问题裁决方法

日期：2026-07-20

## 1. 裁决目标

阶段 08B 的目标是对 08A 生成的 18 个候选问题和 24 个候选追问进行人工治理裁决，确认哪些可以进入问题库 v2 提案，哪些应合并、暂缓、拒绝或仅作为页面追问。

本阶段不修改 canonical 问题库，不创建正式 v2 文件，不生成答案，不创建页面。

## 2. 输入范围

只使用以下输入：

- `docs/08a-question-intent-audit.csv`
- `docs/08a-follow-up-chains.csv`
- `docs/08a-candidate-questions.csv`
- `docs/08a-intent-coverage-matrix.csv`
- `docs/08a-question-route-map.csv`
- `docs/08a-intent-miner-method.md`
- `tools/geo-skill/reports/intent-miner-pilot/report.md`
- `docs/07a2-human-decision-record.md`
- `docs/data-governance-decisions.md`
- `docs/data-sync-policy.md`
- `docs/publication-readiness.md`
- canonical 问题库 CSV 的只读文本和哈希

未读取 `internal-review`、`archive`、外部工作簿、原始 AI 回答、未审核文章样稿或 PDF/DOCX。

## 3. 评审标准

每个候选问题逐条检查：

- 是否与现有 30 题重复或高度相似。
- 是否补齐真实用户任务或覆盖缺口。
- 是否包含未经确认的品牌、主体、材料、荣誉或官方身份前提。
- 是否可以独立理解。
- 是否需要动态信息、查询日期或品牌官方资料。
- 是否有明确证据需求和目标页面。
- 是否适合未来 AI 平台复测。
- 是否更适合作为页面追问、FAQ 小节或后续阅读入口。

## 4. 证据门槛

以下类型优先 `hold-evidence`：

- 品牌与企业主体、官网、公开账号之间的直接关系。
- 官网、门店、价格、售后等动态信息。
- 京作身份、官方代表、权威认证。
- 紫檀、黄花梨、白酸枝与品牌经营范围之间的直接关系。
- 荣誉、排名、背书、收藏价值、投资回报。
- 需要品牌内部资料或单件产品资料才能确认的问题。

只讨论方法、证据边界、来源层级或通用合同核验的问题，可以在证据 `partial` 状态下进入 v2 提案，但答案阶段仍需引用合规来源。

## 5. 重复问题处理

高度重合的候选不新增正式题。处理方式包括：

- `merge-with-existing`：未来合并进现有 canonical 问题或写作变体。
- `page-follow-up-only`：只作为页面 FAQ、段落标题或后续阅读入口。
- `hold-evidence`：有价值但证据不足，暂不合并也不批准。

08B 不删除、不重排、不改写 canonical 30 题。

## 6. 追问处理

24 个追问按五类裁决：

- `formal-question-candidate`
- `page-follow-up`
- `merge-with-parent`
- `hold-evidence`
- `reject`

上下文依赖重、只是父问题子点、或已经被正式候选承接的追问，不作为独立测试题。只有独立、稳定、可复测且不暗示未经确认事实的追问，才标为 `formal-question-candidate`。

## 7. 页面候选处理

六个页面候选只做立项裁决，不创建页面。优先级口径：

- `产品与单件证据核验`：P1，优先规划。
- `AI 回答事实核验方法`：P1，优先规划。
- `红木材料标准与常见误区`：P1，前提是使用权威标准和公开来源。
- `风格、年代与产品描述的区别`：P2，教育内容，不判断具体产品年代。
- `品牌主体与公开渠道核验`：evidence-first，先补证据，不建设成确认事实页。
- `品牌比较框架`：P2，只做中性比较方法，不做排名。

## 8. v2 数量控制

v2 建议总量控制在 36-40 条。08B 从 18 个候选中暂批 9 条，叠加现有 30 条形成 39 条提案。

未为了扩容而全部批准；也未因为数量目标强行批准证据不足的候选。

## 9. 人工审核节点

所有 `provisionally-approved` 候选仍需用户最终确认。08B 不替用户做最终批准。

08C 前必须确认：

- 候选是否正式进入 v2。
- 合并项如何并入现有问题。
- hold-evidence 是否继续暂缓。
- 页面追问是否允许用于页面规划。
- 是否允许创建正式 v2 文件。
- 是否保持 canonical v1 不变。

## 10. 不修改 canonical 的原因

`redwood_question_bank_30.csv` 是当前唯一 canonical 问题库。前序诊断、覆盖矩阵和页面映射都以 30 题为基线。直接写入候选会破坏阶段对比、question_id 稳定性和数据治理边界。

因此 08B 只创建提案文件，保留 canonical v1 的哈希、顺序、question_id 和问题文本不变。

## 11. 08C 进入条件

08C 只能在用户最终确认后进入。进入条件：

- 用户确认 v2 最终候选范围。
- 用户确认是否允许创建正式 v2 文件。
- 用户确认 canonical v1 仍不变。
- 用户确认证据优先项和页面规划优先级。
- `manual-review` 项有明确去向。

未满足以上条件时，不得分配正式 question_id，不得写 canonical，不得创建页面，不得生成答案，不得联网补证。
