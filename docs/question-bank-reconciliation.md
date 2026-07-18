# 元亨利 GEO 作品集｜问题库核对报告

阶段：0.3B 确认并锁定唯一可信数据源
日期：2026-07-19
核对方式：只读读取 CSV 与投递版工作簿 `CategoryMap`，比较 `question_id`、问题文本、分类和数量。

## 1. 文件路径

- CSV 文件：`/Users/lay/Documents/New project/redwood_geo/data/redwood_question_bank_30.csv`
- 工作簿文件：`/Users/lay/Documents/New project/outputs/yhl_geo_portfolio_delivery/元亨利GEO_投递版数据与分析.xlsx`
- 工作簿 Sheet：`CategoryMap`

## 2. 数量核对

| 来源 | 问题数量 |
|---|---:|
| CSV `redwood_question_bank_30.csv` | 30 |
| 工作簿 `CategoryMap` | 30 |

两边均为 30 条问题记录，不含表头或说明行。

## 3. question_id 一致情况

- CSV ID 范围：`q01` 到 `q30`
- 工作簿 ID 范围：`q01` 到 `q30`
- CSV 独有 ID：无
- 工作簿独有 ID：无
- 结论：`question_id` 完全一致。

## 4. 问题文本一致情况

- 完全一致记录：30
- 冲突记录：0
- 结论：问题文本完全一致。

## 5. 分类一致情况

分类字段不是逐字相同：

- CSV 使用原始细分类，例如“材质-黄花梨”“主体核验”“购买避坑”。
- `CategoryMap` 使用作品集展示分组 `portfolio_category_v2`，例如“材质类”“品牌认知类”“购买决策类”“GEO策略题”。

这属于分类粒度差异。按本阶段判断规则，只要 `question_id` 与问题文本完全一致，即可确认 CSV 为问题库 canonical，`CategoryMap` 作为 working / duplicate。

| question_id | CSV 分类 | CategoryMap 分类 |
|---|---|---|
| q01 | 品牌认知 | 品牌认知类 |
| q02 | 品牌认知 | 品牌认知类 |
| q03 | 材质-黄花梨 | 材质类 |
| q04 | 材质-紫檀 | 材质类 |
| q05 | 材质-白酸枝 | 材质类 |
| q06 | 购买决策 | 购买决策类 |
| q07 | 品牌对比 | 购买决策类 |
| q08 | 行业认知 | 京作与风格类 |
| q09 | 行业认知 | 京作与风格类 |
| q10 | AI误判风险 | 风险边界类 |
| q11 | 同名歧义 | 品牌认知类 |
| q12 | 主体核验 | 品牌认知类 |
| q13 | 主体核验 | 品牌认知类 |
| q14 | 可靠性验证 | 风险边界类 |
| q15 | 可靠性验证 | 风险边界类 |
| q16 | 购买决策 | 材质类 |
| q17 | 购买决策 | 购买决策类 |
| q18 | 购买决策 | 购买决策类 |
| q19 | 购买决策 | 购买决策类 |
| q20 | 来源可信 | 风险边界类 |
| q21 | 京作与工艺 | 京作与风格类 |
| q22 | 风格语义 | 京作与风格类 |
| q23 | 工艺语义 | 京作与风格类 |
| q24 | 品牌对比 | 购买决策类 |
| q25 | 推荐场景 | 购买决策类 |
| q26 | 购买避坑 | 购买决策类 |
| q27 | 空间搭配 | 京作与风格类 |
| q28 | 收藏投资 | 风险边界类 |
| q29 | 内容策略 | GEO策略题 |
| q30 | 内容策略 | GEO策略题 |

## 6. CSV 独有记录

无。

## 7. 工作簿独有记录

无。

## 8. 冲突记录

- `question_id` 冲突：无
- 问题文本冲突：无
- 数量冲突：无
- 分类逐字差异：30 条，见上表；该差异为分类粒度差异，不阻断 CSV canonical 决定。

## 9. 是否满足确定 CSV 为主源的条件

满足。

依据：

- `question_id` 完全一致。
- 问题文本完全一致。
- 两边均为 30 条。
- 不存在一方独有问题。

正式结论：

- `/Users/lay/Documents/New project/redwood_geo/data/redwood_question_bank_30.csv` 标记为问题库 canonical。
- 投递版数据与分析工作簿中的 `CategoryMap` 标记为 working / duplicate。
