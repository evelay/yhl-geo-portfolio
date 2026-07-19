# 阶段 08A 问题意图与追问链审计报告

本报告是元亨利 GEO 作品集的内部问题库审计，不是市场规模、平台热度、排名或效果预测数据。所有候选问题均为 `candidate`，不自动进入 canonical。

## 30 个问题概览

- canonical 问题数量：30
- 高风险问题数量：26
- 完全重复：0
- 相似/同根意图组：6
- 候选问题数量：18

### 意图分布

| 项目 | 数量 |
| --- | ---: |
| brand-definition | 3 |
| comparison | 2 |
| craft-style-understanding | 5 |
| fact-verification | 2 |
| material-understanding | 3 |
| process-how-to | 4 |
| purchase-evaluation | 2 |
| recommendation | 2 |
| risk-boundary | 4 |
| source-verification | 3 |

### 用户阶段分布

| 项目 | 数量 |
| --- | ---: |
| awareness | 4 |
| consideration | 8 |
| decision | 6 |
| post-decision | 1 |
| research | 11 |

### 六类内容簇分布

| 项目 | 数量 |
| --- | ---: |
| 京作、明式与清式 | 6 |
| 品牌比较与选择 | 3 |
| 品牌认知与事实 | 3 |
| 材质与产品边界 | 3 |
| 购买与核验 | 6 |
| 风险、来源与信息边界 | 9 |

### 页面覆盖状态

| 项目 | 数量 |
| --- | ---: |
| fully-covered | 15 |
| partially-covered | 11 |
| requires-evidence-first | 4 |

## 高风险问题

高风险问题包括品牌/企业主体、京作身份、材质关系、排名、收藏投资、产品级证据、官方身份和购买推荐相关问题。

q01, q02, q03, q04, q05, q06, q07, q08, q09, q10, q11, q12, q13, q14, q15, q16, q17, q18, q19, q21, q22, q23, q24, q25, q26, q28

## 重复和相似问题

- SIM-08A-001：q07|q24；同一根意图的不同问法；建议 `retain-as-variant`。均指向中性比较维度；q07带品牌对象，q24更通用。
- SIM-08A-002：q08|q21；上下位问题；建议 `retain-as-variant`。q08问关系语义，q21强调可核验证据和表达边界。
- SIM-08A-003：q03|q04|q05|q16；同一根意图的不同材料分支；建议 `retain-as-variant`。不能合并为单题，否则会丢失黄花梨、紫檀、白酸枝和证书链路差异。
- SIM-08A-004：q12|q13|q14|q20；来源核验链；建议 `retain-as-variant`。主体、官网来源、不确定人物事实和内容可信度是同一核验链的不同节点。
- SIM-08A-005：q06|q16|q19|q26；购买任务链；建议 `retain-as-variant`。覆盖评估、单件材质、合同售后和避坑，不建议删除。
- SIM-08A-006：q29|q30；上下位问题；建议 `retain-as-variant`。q29是页面缺口，q30是策略优先级。

## 追问链

- CHAIN-08A-001：根问题 q01，候选追问 3 条，目标入口 /disambiguation 等。
- CHAIN-08A-002：根问题 q08，候选追问 3 条，目标入口 /jingzuo 等。
- CHAIN-08A-003：根问题 q03，候选追问 3 条，目标入口 /materials 等。
- CHAIN-08A-004：根问题 q04，候选追问 3 条，目标入口 /materials 等。
- CHAIN-08A-005：根问题 q05，候选追问 3 条，目标入口 /materials 等。
- CHAIN-08A-006：根问题 q06，候选追问 3 条，目标入口 /buying-guide 等。
- CHAIN-08A-007：根问题 q07，候选追问 3 条，目标入口 new-page:brand-comparison-framework 等。
- CHAIN-08A-008：根问题 q10，候选追问 3 条，目标入口 /prompt-system 等。

## 候选问题

- CAND-INTENT-001：如何核验“元亨利红木家具”与具体企业主体、官网和公开账号之间的关系？；建议 `hold-evidence`；页面候选：品牌主体与公开渠道核验。
- CAND-INTENT-002：单件元亨利家具的主材、辅材和证书应如何对应到合同与发票？；建议 `consider-for-v2`；页面候选：产品与单件证据核验。
- CAND-INTENT-003：购买后应保存哪些合同、证书、检测、交付和售后资料？；建议 `consider-for-v2`；页面候选：产品与单件证据核验。
- CAND-INTENT-004：门店、展厅、价格和售后这类动态信息多久需要复核一次？；建议 `hold-evidence`；页面候选：品牌主体与公开渠道核验。
- CAND-INTENT-005：如何判断官网自述、媒体报道和行业协会信息分别能证明什么？；建议 `consider-for-v2`；页面候选：AI 回答事实核验方法。
- CAND-INTENT-006：“京作”“北京品牌”和“明清风格”在元亨利相关内容中应如何分开写？；建议 `merge-with-existing`；页面候选：风格、年代和产品描述的区别。
- CAND-INTENT-007：看到“元亨利黄花梨家具”说法时，如何避免把材料主题误写成经营事实？；建议 `merge-with-existing`；页面候选：红木材料标准与常见误区。
- CAND-INTENT-008：白酸枝、酸枝和红木标准名称不一致时应以哪些文件为准？；建议 `consider-for-v2`；页面候选：红木材料标准与常见误区。
- CAND-INTENT-009：AI 回答里提到元亨利荣誉、排名或背书时应如何追溯来源？；建议 `hold-evidence`；页面候选：AI 回答事实核验方法。
- CAND-INTENT-010：比较北京红木品牌时，如何用证据维度替代“哪个最好”？；建议 `consider-for-v2`；页面候选：品牌比较框架。
- CAND-INTENT-011：元亨利相关内容能否使用“官方京作代表”这类说法？需要哪些证据？；建议 `hold-evidence`；页面候选：风格、年代和产品描述的区别。
- CAND-INTENT-012：如何区分产品名称中的风格词、实际年代和收藏价值判断？；建议 `consider-for-v2`；页面候选：风格、年代和产品描述的区别。
- CAND-INTENT-013：用户只提供一张产品图片时，AI 应如何回答元亨利材质和真伪问题？；建议 `manual-review`；页面候选：产品与单件证据核验。
- CAND-INTENT-014：AI 介绍元亨利时引用旧网页或二手转载，应该如何做日期和来源复核？；建议 `consider-for-v2`；页面候选：AI 回答事实核验方法。
- CAND-INTENT-015：元亨利相关内容中的品牌整体评价和单件产品评价应如何分开？；建议 `consider-for-v2`；页面候选：产品与单件证据核验。
- CAND-INTENT-016：在购买沟通中，哪些承诺必须写入书面合同而不能只看宣传文案？；建议 `consider-for-v2`；页面候选：产品与单件证据核验。
- CAND-INTENT-017：收藏或投资相关说法缺少成交、来源和单件资料时应如何降级表达？；建议 `hold-evidence`；页面候选：AI 回答事实核验方法。
- CAND-INTENT-018：未来公开资料更新后，问题库和页面映射应如何复核而不是直接改题？；建议 `consider-for-v2`；页面候选：AI 回答事实核验方法。

## 页面覆盖

canonical 30 题当前覆盖：fully-covered 15，partially-covered 11，requires-evidence-first 4，not-covered 0。

## 新页面候选

- 产品与单件证据核验：对应 q16|q17|q19|CAND-INTENT-002|CAND-INTENT-003|CAND-INTENT-013|CAND-INTENT-015|CAND-INTENT-016；证据状态 partial；08A 不建设。
- 品牌主体与公开渠道核验：对应 q11|q12|q13|q18|CAND-INTENT-001|CAND-INTENT-004；证据状态 partial；08A 不建设。
- 红木材料标准与常见误区：对应 q03|q04|q05|q16|CAND-INTENT-007|CAND-INTENT-008；证据状态 partial；08A 不建设。
- 风格、年代和产品描述的区别：对应 q08|q09|q21|q22|q23|q27|CAND-INTENT-006|CAND-INTENT-011|CAND-INTENT-012；证据状态 partial；08A 不建设。
- AI 回答事实核验方法：对应 q10|q14|q15|q20|q28|CAND-INTENT-005|CAND-INTENT-009|CAND-INTENT-014|CAND-INTENT-017|CAND-INTENT-018；证据状态 partial；08A 不建设。
- 品牌比较框架：对应 q07|q24|q25|CAND-INTENT-010；证据状态 limited；08A 不建设。

## 证据缺口

- 产品级证据页和单件资料核验不足。
- 品牌主体、官网、公开账号与企业主体关系仍需直接证据。
- 品牌比较问题缺少可审核的中性比较框架。
- 购买后证据留存只有部分覆盖。
- 动态价格、门店、售后和公开资料更新需要日期复核规则。

## 人工审核项

- 是否允许 08B 把候选问题分批进入人工评审，而不是直接写入 canonical。
- 是否为单件产品证据、品牌主体核验和品牌比较框架单独开页面设计阶段。
- 是否补采品牌官方资料、工商/备案/商标日期核验和产品级书面凭证样例。
- 是否继续将京作身份、排名、投资、价格和动态渠道信息设为证据优先。

## 本次限制

- 未修改 canonical 问题库。
- 未修改 app/ 或 public/。
- 未读取 internal-review、archive、外部完整工作簿、原始 AI 回答、人工评分工作簿、PDF/DOCX 或完整文章样稿。
- 未调用 API、外部模型或 crawler。
- 未生成正式答案、FAQ 正文、文章或新页面。
