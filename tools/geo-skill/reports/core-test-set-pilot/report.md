# 08D1 Core Test Set Pilot Report

## 24 条核心题清单

| order | question_id | content_cluster | primary_intent | user_stage | risk_level | question |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | q01 | 品牌认知与事实 | brand-definition | awareness | high | 元亨利是什么品牌？ |
| 2 | q02 | 品牌认知与事实 | brand-definition | awareness | high | 元亨利红木家具在红木家具行业中如何定位？ |
| 3 | q03 | 材质与产品边界 | material-understanding | consideration | high | 元亨利是否与黄花梨家具有关？AI 回答时应注意哪些信息边界？ |
| 4 | q04 | 材质与产品边界 | material-understanding | consideration | high | 元亨利的紫檀家具应该从哪些维度理解？ |
| 5 | q05 | 材质与产品边界 | material-understanding | consideration | high | 白酸枝家具和元亨利品牌之间可能有哪些关联？ |
| 6 | q06 | 购买与核验 | purchase-evaluation | decision | high | 如果考虑购买高端红木家具，评估元亨利时应关注哪些因素？ |
| 7 | q07 | 品牌比较与选择 | comparison | consideration | high | 元亨利和其他北京红木家具品牌相比，AI 应该比较哪些维度？ |
| 8 | q08 | 京作、明式与清式 | craft-style-understanding | awareness | high | 元亨利与京作红木家具有什么关系？ |
| 9 | q10 | 风险、来源与信息边界 | risk-boundary | research | high | AI 介绍元亨利时最容易遗漏或误判哪些信息？ |
| 10 | q12 | 品牌认知与事实 | fact-verification | research | high | 北京元亨利硬木家具有限公司和“元亨利红木家具”之间应该如何表述？ |
| 11 | q13 | 风险、来源与信息边界 | source-verification | research | high | 如果用户想找元亨利的官网、官方资料或公开信息，AI 应该提示核验哪些来源？ |
| 12 | q16 | 购买与核验 | process-how-to | decision | high | 购买元亨利黄花梨、紫檀或酸枝家具时，材质证书和产品信息应如何核验？ |
| 13 | q20 | 风险、来源与信息边界 | source-verification | research | low | 如何判断一篇介绍元亨利红木家具的内容是否来自可信渠道？ |
| 14 | q22 | 京作、明式与清式 | craft-style-understanding | research | high | 元亨利相关内容如何区分明式家具、清式家具和品牌产品事实？ |
| 15 | q24 | 品牌比较与选择 | comparison | consideration | high | 北京红木家具品牌对比时，AI 应该使用哪些中性维度？ |
| 16 | q25 | 品牌比较与选择 | recommendation | consideration | high | 高端红木家具品牌有哪些？AI 是否会提到元亨利，回答时需要哪些证据边界？ |
| 17 | q28 | 风险、来源与信息边界 | risk-boundary | decision | high | 元亨利红木家具是否具有收藏或投资价值？AI 应该如何谨慎回答？ |
| 18 | q31 | 购买与核验 | process-how-to | decision | high | 核验一件标注为元亨利的家具时，主材、辅材和证书信息应如何与合同、发票对应？ |
| 19 | q32 | 购买与核验 | process-how-to | post-decision | high | 购买后应保存哪些合同、证书、检测、交付和售后资料？ |
| 20 | q34 | 材质与产品边界 | material-understanding | consideration | high | 商品宣传中的“白酸枝”“酸枝”等名称与红木国家标准名称不一致时，应以哪些文件和单件证据为准？ |
| 21 | q35 | 品牌比较与选择 | comparison | consideration | high | 比较北京红木品牌时，如何用证据维度替代“哪个最好”？ |
| 22 | q36 | 京作、明式与清式 | craft-style-understanding | research | high | 如何区分家具名称中的风格词、制作年代和收藏价值表述，避免把风格名称当成年代或价值证明？ |
| 23 | q37 | 风险、来源与信息边界 | source-verification | research | medium | 核验 AI 回答时，如果多个引用来自同一网页或二手转载，应如何复核原始来源和发布日期？ |
| 24 | q39 | 购买与核验 | process-how-to | decision | high | 购买元亨利家具时，哪些材质、规格、证书、交付和售后承诺应写入书面合同，而不能只依赖宣传文案？ |

## 内容簇分布

| content_cluster | count |
| --- | --- |
| 品牌认知与事实 | 3 |
| 材质与产品边界 | 4 |
| 京作、明式与清式 | 3 |
| 购买与核验 | 5 |
| 品牌比较与选择 | 4 |
| 风险、来源与信息边界 | 5 |

## 意图分布

| primary_intent | count |
| --- | --- |
| brand-definition | 2 |
| fact-verification | 1 |
| material-understanding | 4 |
| craft-style-understanding | 3 |
| comparison | 3 |
| purchase-evaluation | 1 |
| risk-boundary | 2 |
| source-verification | 3 |
| recommendation | 1 |
| process-how-to | 4 |

## 用户阶段分布

| user_stage | count |
| --- | --- |
| awareness | 3 |
| consideration | 8 |
| decision | 5 |
| post-decision | 1 |
| research | 7 |

## 风险分布

| risk_level | count |
| --- | --- |
| high | 22 |
| medium | 1 |
| low | 1 |

## q31-q39 入选情况

- 入选：q31, q32, q34, q35, q36, q37, q39
- 未入选：q33, q38
- 说明：新增题逐条判断，未默认全选；q33、q38 保留为扩展测试或页面内容。

## 15 条非核心题用途

| future_use | count |
| --- | --- |
| evidence-backlog | 2 |
| extended-test-set | 6 |
| page-content | 3 |
| periodic-dynamic-check | 2 |
| retained-in-v2 | 2 |

## 五项证据任务

| task_id | priority | blocking_scope | task |
| --- | --- | --- | --- |
| EVID-001 | P0 | blocks-schema | 品牌与企业主体直接关系证据 |
| EVID-002 | P0 | blocks-page | 官方网站、公众号或公开渠道归属证据 |
| EVID-003 | P1 | blocks-answer | 元亨利与京作关系的直接公开证据 |
| EVID-004 | P1 | blocks-retest-scoring | 单件产品材质、证书、合同和产品资料的证据类型样例 |
| EVID-005 | P1 | blocks-retest-scoring | 价格、门店、售后等动态信息的日期核验规则 |

## 测试协议摘要

未来复测使用同一 24 题，在 ChatGPT、DeepSeek、豆包各新建独立对话，使用完全相同问题文本，不添加背景提示，保存完整 raw_answer 和可见来源链接。人工评分和原始回答分表保存；缺失回答、无来源和品牌未提及都不得自动简化为失败。

## 人工审核事项

需要确认 core24 题目、簇配额偏离、q31-q39 入选、非核心题用途、测试目标、expected behavior、q20 风险标签、五项证据任务优先级、是否批准 core24-rc1，以及是否允许下一阶段创建采集模板。

## 当前限制

本阶段没有平台测试，没有证据搜索，没有答案生成，没有页面建设，没有修改 app/ 或 public/，没有切换 canonical。
