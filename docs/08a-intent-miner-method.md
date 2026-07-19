# 阶段 08A Intent Miner 方法说明

## 1. Skill 来源

- 来源仓库：`https://github.com/yaojingang/yao-geo-skills`
- 来源 Skill：`skills/yao-geo-intent-miner`
- 来源 commit：`eabfde0f0bdf53f84559bdfcba2595fcac1ad50f`
- 许可证：MIT License，本地裁剪副本保留版权和 LICENSE。

## 2. 当前项目适配

上游 Intent Miner 默认会输出较完整的问题库、追问、评分、资产和四格式报告。本阶段只采用其意图建模、追问链、证据需求和资产映射方法，降级为离线 CSV/Markdown/JSON 审计。

## 3. canonical 问题库

问题库唯一主源是 `redwood_question_bank_30.csv`。脚本只读该 CSV，保留 30 个原 question_id、原问题文本和原分类，不改写、不重排、不覆盖。

## 4. 输入边界

允许输入为 canonical 问题库、安全公开知识库 JSON、07A 实体/消歧记录、07A2 人工决定和公开路由职责。禁止读取 internal-review、archive、外部完整工作簿、原始 AI 回答、人工评分、未审核 FAQ、完整提示词、完整文章样稿和 PDF/DOCX。

## 5. 意图分类

每题只标一个主意图，限定在 brand-definition、fact-verification、material-understanding、craft-style-understanding、comparison、purchase-evaluation、risk-boundary、source-verification、recommendation、process-how-to。

## 6. 用户阶段

用户阶段限定为 awareness、consideration、decision、post-decision、research。阶段标注只表示内部决策链位置，不代表真实用户比例。

## 7. 追问链规则

追问必须自然、可独立理解、不带未经确认前提、不只是同义替换，并标明证据需求、目标页面和人工审核状态。所有追问初始状态均为 candidate。

## 8. 候选问题生成规则

候选问题只来自真实覆盖缺口，数量不超过 18 个，ID 使用 CAND-INTENT-001 起。候选不暗示官方身份、固定材料经营、升值收益、排行榜、价格、销量或市场份额。

## 9. 重复检查

重复检查分为完全重复、高度相似、同根意图、上下位问题和需人工合并。本阶段只给 retain、retain-as-variant、merge-candidate、rewrite-in-future-version、manual-review 建议，不删除 canonical。

## 10. 证据需求

证据需求限定为 brand-source、industry-standard、government-source、association-source、media-source、product-level-evidence、expert-source、multiple-source、no-brand-claim-required。证据类型计数不是证据充分性判断。

## 11. 页面映射

页面映射只使用当前公开路由和新页面候选。现有页面覆盖不为了提高覆盖率而强行标 fully-covered；需要证据的题保留 requires-evidence-first。

## 12. 人工审核节点

品牌主体关系、京作身份、材料与产品关系、荣誉/排名、价格/门店/售后、收藏投资和购买推荐均需要人工审核或证据优先。

## 13. 不修改 canonical 的原因

08A 是审计阶段。canonical 30 题已作为基线用于前序诊断，任何改题、重排或候选合入都会破坏前后可比性，因此只输出审计表和候选清单。

## 14. 后续 08B 门禁

进入 08B 前，需要人工确认候选题是否进入评审、哪些新页面候选可立项、哪些高风险证据需要补采，以及是否继续保持所有候选不写入 canonical。
