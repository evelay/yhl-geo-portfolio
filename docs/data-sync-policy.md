# 元亨利 GEO 作品集｜数据同步策略

阶段：0.3B 确认并锁定唯一可信数据源
日期：2026-07-19

## 1. 同步原则

1. 原始回答不能在网站中修改。
2. 人工评分只能在主工作簿中修改。
3. 派生指标必须从主工作簿重新计算。
4. 品牌事实必须在知识库工作簿中确认。
5. 公开 JSON 必须由知识库主源导出。
6. `app/data.ts` 只能作为网站展示副本。
7. 网站数据不得反向覆盖主工作簿。
8. 下载文件必须标注来源版本。
9. 早期归档不得参与当前计算。
10. 数据更新后必须完成验证流程，确认网站副本、下载副本和派生文件没有漂移。

## 2. 标准同步流程

主源修改
→ 人工审核
→ 导出公开快照
→ 重新计算派生指标
→ 更新网站副本
→ 构建验证
→ 提交版本

## 3. 主源更新规则

- 原始回答、人工评分、风险标签、缺失标签、证据备注和核心指标，以 `/Users/lay/Documents/New project/outputs/yhl_geo_portfolio_delivery/元亨利GEO_投递版数据与分析.xlsx` 为准。
- 问题库以 `/Users/lay/Documents/New project/redwood_geo/data/redwood_question_bank_30.csv` 为准；投递版工作簿 `CategoryMap` 是 working / duplicate。
- 品牌事实、信源、FAQ 映射以 `/Users/lay/Documents/New project/outputs/yhl_geo_portfolio_delivery/knowledge_base/元亨利GEO品牌事实知识库.xlsx` 为准。
- 提示词体系和 GEO 文章样稿以对应 Markdown 文件为准。
- 90 天策略计划以 `/Users/lay/Documents/New project/outputs/yhl_geo_portfolio_delivery/strategy/元亨利红木家具GEO_90天内容执行工作簿.xlsx` 为准。

## 4. 网站副本更新规则

- `app/data.ts` 的指标、FAQ、信源、诊断、路线图和下载链接，必须来自已确认主源或已审核派生快照。
- TSX 页面属于 website-copy 或 presentation，不得作为核心事实、评分、指标或策略计划的主源。
- 构建后的 HTML 属于 derived，不得用于反向覆盖 Markdown、工作簿、CSV 或 JSON 主源。
- `public/downloads` 中的文件只能作为下载交付副本；除已确认的 Markdown canonical 外，不得直接在下载目录修事实。

## 5. 下载副本规则

下载文件发布前必须记录：

- 来源 canonical 路径。
- 来源文件版本日期。
- 导出或复制时间。
- 文件哈希。
- 是否为 derived、delivery 或 Markdown canonical。

如果下载副本与 canonical 哈希或内容不一致，必须重新导出或重新复制，不得在下载副本中局部修补。

## 6. 验证流程

数据更新后至少完成以下检查：

1. 外部 canonical 路径仍真实存在。
2. 问题库 `question_id` 和问题文本与工作簿 working copy 一致。
3. 工作簿派生指标重新计算完成。
4. 公开知识库 JSON 由知识库工作簿重新导出。
5. `app/data.ts` 和 TSX 页面只接收已审核展示副本。
6. `public/downloads` 文件标注并校验来源版本。
7. 早期归档目录未被纳入计算或网站同步。
8. 构建验证通过。
9. `git diff` 只包含预期文件。
10. 提交信息记录数据版本或治理原因。

## 7. 冲突处理

- 主工作簿与网站副本冲突时，以主工作簿为准。
- 知识库工作簿与公开 JSON 冲突时，以知识库工作簿为准。
- Markdown canonical 与 TSX 页面冲突时，以 Markdown 为准。
- CSV 问题库与 `CategoryMap` 的 `question_id` 或问题文本冲突时，标记 `decision-pending` 并等待人工确认。
- 归档目录与当前 delivery 体系冲突时，归档目录不得参与裁决。
