# 阶段 08B 候选问题人工裁决报告

日期：2026-07-20

本报告记录 08B 对 08A 候选问题、候选追问和页面候选的人工治理决定。08B 未修改 canonical 问题库，未创建正式 v2 文件，未创建页面，未生成答案，未联网搜索证据。

## 1. 候选问题裁决分布

18 个候选问题全部完成裁决。

| human_decision | 数量 |
| --- | ---: |
| approve-for-v2 | 9 |
| merge-with-existing | 2 |
| hold-evidence | 4 |
| page-follow-up-only | 2 |
| reject | 0 |
| manual-review | 1 |

## 2. 候选追问裁决分布

24 个候选追问全部完成裁决。

| decision | 数量 |
| --- | ---: |
| formal-question-candidate | 3 |
| page-follow-up | 10 |
| merge-with-parent | 6 |
| hold-evidence | 5 |
| reject | 0 |

## 3. Provisionally Approved 候选

| 临时 ID | 候选 ID | 问题 |
| --- | --- | --- |
| V2-CAND-001 | CAND-INTENT-002 | 单件元亨利家具的主材、辅材和证书应如何对应到合同与发票？ |
| V2-CAND-002 | CAND-INTENT-003 | 购买后应保存哪些合同、证书、检测、交付和售后资料？ |
| V2-CAND-003 | CAND-INTENT-005 | 如何判断官网自述、媒体报道和行业协会信息分别能证明什么？ |
| V2-CAND-004 | CAND-INTENT-008 | 白酸枝、酸枝和红木标准名称不一致时应以哪些文件为准？ |
| V2-CAND-005 | CAND-INTENT-010 | 比较北京红木品牌时，如何用证据维度替代“哪个最好”？ |
| V2-CAND-006 | CAND-INTENT-012 | 如何区分产品名称中的风格词、实际年代和收藏价值判断？ |
| V2-CAND-007 | CAND-INTENT-014 | AI 介绍元亨利时引用旧网页或二手转载，应该如何做日期和来源复核？ |
| V2-CAND-008 | CAND-INTENT-015 | 元亨利相关内容中的品牌整体评价和单件产品评价应如何分开？ |
| V2-CAND-009 | CAND-INTENT-016 | 在购买沟通中，哪些承诺必须写入书面合同而不能只看宣传文案？ |

## 4. Hold Evidence

| 候选 ID | 原因 |
| --- | --- |
| CAND-INTENT-001 | 品牌、企业主体、官网和公开账号关系缺直接公开证据。 |
| CAND-INTENT-004 | 动态价格、门店、展厅和售后信息缺日期复核规则。 |
| CAND-INTENT-009 | 荣誉、排名或背书缺原始颁发主体、年份和公开来源。 |
| CAND-INTENT-011 | “官方京作代表”缺直接 evidence_id。 |

## 5. Merge

| 候选 ID | 合并方向 |
| --- | --- |
| CAND-INTENT-006 | 并入 q08 / q21 / q22 的京作和风格边界。 |
| CAND-INTENT-007 | 并入 q03 / q16 的材料主题和单件证据边界。 |

## 6. Page Follow-Up

| 候选 ID | 页面方向 |
| --- | --- |
| CAND-INTENT-017 | 作为 /buying-guide 或 AI 回答事实核验方法中的收藏投资降级表达提示。 |
| CAND-INTENT-018 | 作为 /method 中的问题库与页面映射复核流程说明。 |

## 7. Reject / Manual Review

`reject` 为 0 条。

| 候选 ID | 状态 | 原因 |
| --- | --- | --- |
| CAND-INTENT-013 | manual-review | 图片单独判断材质和真伪的场景需要单独证据边界规则。 |

## 8. v2 提案总量

v2 提案总数：39 条。

- canonical-existing：30 条，保留原 question_id、原顺序和原问题文本。
- candidate-addition：9 条，仅使用 `V2-CAND-001` 至 `V2-CAND-009` 临时 ID。

本报告不创建正式 v2 canonical 文件，不分配正式 question_id。

## 9. 页面候选优先级

| 页面候选 | 决策 | 优先级 | 阶段 |
| --- | --- | --- | --- |
| 产品与单件证据核验 | approve-for-planning | P1 | next-content-pilot |
| AI 回答事实核验方法 | approve-for-planning | P1 | next-content-pilot |
| 红木材料标准与常见误区 | approve-for-planning | P1 | next-content-pilot |
| 风格、年代与产品描述的区别 | approve-for-planning | P2 | later-content-cluster |
| 品牌主体与公开渠道核验 | evidence-first | P1 | research-first |
| 品牌比较框架 | approve-for-planning | P2 | later-content-cluster |

## 10. 证据补采优先级

不超过五项：

1. 品牌与企业主体的直接关系证据。
2. 官方网站、公众号或公开渠道的归属证据。
3. 京作关系的直接公开证据。
4. 单件产品材质与产品资料的证据类型样例。
5. 动态价格、门店、售后信息的日期核验规则。

## 11. 最终需人工确认事项

- 哪些 `provisionally-approved` 候选正式进入 v2。
- 哪些候选与现有问题合并。
- 哪些继续 `hold-evidence`。
- 哪些只作为页面追问。
- `manual-review` 的图片场景如何处理。
- v2 最终目标数量是否为 39 条或调整到 36-40 范围内其他数量。
- 哪些页面进入下一阶段规划。
- 哪些证据优先补采。
- 是否允许 08C 创建正式 v2 文件。
- 是否继续保持 canonical v1 不变。

## 12. 限制确认

- 未修改 canonical 问题库。
- 未修改 `app/` 或 `public/`。
- 未读取 `internal-review`。
- 未读取 `archive`。
- 未调用 API、外部模型或 crawler。
- 未创建页面、答案、FAQ 正文或文章。
