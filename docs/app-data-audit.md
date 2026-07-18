# app/data.ts 只读审计

阶段：0.3 数据源主从关系审计  
文件：`/Users/lay/Documents/New project/outputs/yhl_geo_portfolio_delivery/website/app/data.ts`  
结论：本阶段未修改 `app/data.ts`。该文件当前是网站展示副本，不应作为原始事实、评分或交付物的唯一可信源。

## 1. 数据块清单

| 数据块 | 行号附近 | 类型 | 是否人工硬编码 | 候选来源 | 能否自动生成 | 主要风险 |
|---|---:|---|---|---|---|---|
| `updatedAt` | 1 | 网站版本日期 | 是 | 知识库 JSON `updatedAt`、策略工作簿更新时间、投递使用说明 | 可以 | 多个更新时间口径可能不一致 |
| base path / `downloadPath` | 3-27 | 下载链接工具 | 是，逻辑代码 | 网站部署配置 | 可以保留代码 | 非数据风险低 |
| `platformScores` | 30 | 首页平台均分 | 是 | 投递版数据工作簿 `Dashboard` / `Baseline150.total_score` | 可以 | 两位小数若手改会与工作簿漂移 |
| `naturalMentionByPlatform` | 38 | 非品牌词自然提及率 | 是 | 投递版数据工作簿 `Dashboard` / `UserIntent75` 非品牌词子样本 | 可以 | 子样本分母为 30，不可与 75 全量混用 |
| `categoryScoresV2` | 46 | 五类问题平均分 | 是 | 投递版数据工作簿 `CategoryMap` + `Baseline150` | 可以 | q01-q28 互斥分类若变化，图表需重算 |
| `riskAndMissingTags` | 54 | 高频风险/缺失标签 | 是 | 投递版数据工作簿 `RiskTags` / `MissingTags` | 可以 | 高风险；一条回答可多标签，不能按回答数解释 |
| `hallucinationByDataset` | 67 | 幻觉率对比 | 是 | 投递版数据工作簿 `Dashboard` | 可以 | Baseline 与 UserIntent 不能混为同一分母 |
| `sourceCoverageByPlatform` | 75 | 有效来源覆盖率 | 是 | 投递版数据工作簿 `effective_source_flag` / `Dashboard` | 可以 | 有效来源定义需固定，图片/CDN不计 |
| `completionAnswers` | 83 | 首页收口问答 | 是 | 投递使用说明、5 分钟讲稿、报告、工作簿指标 | 部分可以 | 文案是人工解释，需人工确认 |
| `sources` | 122 | 方法页信源子集 | 是 | 知识库工作簿 `信源主表`、公开 JSON `sources` | 可以 | 只列 B 类部分来源，不是完整 27 条信源 |
| `diagnoses` | 195 | 六项诊断卡 | 是 | 投递版工作簿 `EvidenceIndex`、报告、知识库事实边界 | 部分可以 | 诊断解释和行动建议包含人工判断 |
| `faq` | 276 | FAQ 展示数据 | 是 | 知识库 `内容FAQ映射`、公开 JSON `mappings.faq`、人工直接回答 | 部分可以 | 当前 FAQ 文案与 first_setup FAQ/schema 可能存在副本 |
| `factLevels` | 384 | 四级事实模型 | 是 | 知识库工作簿 `字段字典` / 公开 JSON `evidenceLevels` | 可以 | 与知识库事实等级口径需保持一致 |
| `contentStrategyAssets` | 391 | 内容资产/页面规划 | 是 | 90 天执行工作簿 `页面规格` / `内容总矩阵` | 可以 | 页面状态和覆盖题数会随执行计划变化 |
| `roadmap90` | 407 | 90 天路线 | 是 | 90 天执行工作簿 `90天排期`、14 页方案 | 可以 | 策略阶段变化后网站不会自动更新 |
| `strategyDownloads` | 413 | 策略下载链接 | 是 | `public/downloads` 文件清单 | 可以 | 下载副本与外部主文件需哈希校验 |
| `knowledgeDownloads` | 419 | 知识库下载链接 | 是 | `public/downloads` 文件清单 | 可以 | JSON/XLSX 有多份副本 |
| `promptSystemDownloads` | 424 | 提示词下载链接 | 是 | `public/downloads` 文件清单 | 可以 | Markdown 来源未确认 |
| `geoArticleDownloads` | 429 | 文章样稿下载链接 | 是 | `public/downloads` 文件清单 | 可以 | Markdown 与 TSX 文章正文可能漂移 |
| `nav` | 434 | 导航数据 | 是 | 网站路由结构 | 可以 | 低风险，但与 sitemap/页面存在性需一致 |

## 2. 导航数据

`nav` 包含 12 个站内入口，直接驱动页眉导航。候选来源是网站路由本身，而不是外部业务数据。当前不建议把它纳入品牌事实或指标主链。

## 3. 首页指标

首页图表和重点数字主要来自以下数组：

- `platformScores`
- `naturalMentionByPlatform`
- `categoryScoresV2`
- `riskAndMissingTags`
- `hallucinationByDataset`
- `sourceCoverageByPlatform`
- `completionAnswers`

这些都应该从投递版数据工作簿重算或导出。`completionAnswers` 是人工总结口径，虽然数字来自工作簿，但“最好平台”“最大问题”等解释需要人工确认。

## 4. 平台诊断数据

`diagnoses` 包含 D1-D6，每条有 `data`、`cases`、`cause`、`impact`、`source`、`action`。候选来源是：

- 投递版数据工作簿 `EvidenceIndex` 的 EV-001 到 EV-012。
- 投递版工作簿 `Baseline150` / `UserIntent75` 的原始回答摘录、评分和风险标签。
- 报告 Markdown 中的诊断解释。
- 知识库工作簿中的事实边界和来源等级。

其中 `cases` 涉及原始回答摘录编号，必须保持与 EvidenceIndex 一致。

## 5. FAQ

`faq` 包含 15 条展示 FAQ，每条有：

- `id`
- `question`
- `directAnswer`
- `detail`
- `boundary`
- `sourceIds`
- `related`

候选来源是知识库工作簿 `内容FAQ映射` 和公开 JSON `mappings.faq`，但当前 `directAnswer` 和 `detail` 更像网站人工文案。`first_setup/faq_pairs.json` 也是一个潜在副本，需人工确认是否已淘汰。

## 6. 信源

`sources` 只包含 10 条 B 类或权威/行业来源：B-001 到 B-005、B-008 到 B-012。它不是完整信源库。完整信源候选主源为知识库工作簿 `信源主表`，公开 JSON 中也有完整 `sources` 数组。

风险：

- 网站方法页会让读者看到部分来源，容易误以为是完整 27 条。
- 若完整信源表状态更新，`app/data.ts` 中的 `sources` 不会自动同步。

## 7. 下载链接

下载链接分为四组：

- `strategyDownloads`
- `knowledgeDownloads`
- `promptSystemDownloads`
- `geoArticleDownloads`

其中 5 个下载件已确认是外部文件的逐字节副本：知识库 XLSX、公开 JSON、90 天执行 XLSX、14 页方案 PDF、14 页方案 DOCX。3 个 Markdown 下载件尚未确认主文件：提示词体系、文章矩阵、完整文章样稿。

## 8. 文章或页面信息

`contentStrategyAssets` 是页面/内容资产计划，候选来源是 90 天执行工作簿；`nav` 是当前网站路由结构；`app/geo-articles/page.tsx` 和 `app/prompt-system/page.tsx` 另有大块页面级硬编码数据，不在 `app/data.ts` 内，但与 `public/downloads` Markdown 交付物有内容重合。

## 9. 人工硬编码内容

本次审计将 `app/data.ts` 归为 12 类硬编码网站展示数据：

1. 更新时间和部署路径。
2. 首页图表指标。
3. 首页收口问答。
4. 信源子集。
5. 六项诊断卡。
6. FAQ。
7. 事实等级。
8. 内容资产计划。
9. 90 天路线图。
10. 下载链接。
11. 导航。
12. 页面状态、标签和展示文案。

## 10. 可以由数据文件自动生成的内容

建议后续可自动生成：

- 平台均分、类别均分、来源覆盖、幻觉率、风险/缺失标签计数。
- 信源子集和完整信源列表。
- 事实等级。
- 内容资产覆盖题数、证据等级、页面状态。
- 下载链接清单和哈希。
- 公开知识库统计数。

仍需人工审核但可结构化输出：

- FAQ 直接回答。
- 诊断卡解释。
- 首页收口问答。
- 文章样稿和提示词模块。

## 11. 涉及品牌事实或效果承诺的内容

涉及品牌事实：

- `sources`
- `diagnoses`
- `faq`
- `factLevels`
- `contentStrategyAssets`
- `roadmap90`
- `completionAnswers`

涉及效果或研究边界：

- `completionAnswers` 中“最好平台”“最大 GEO 问题”等。
- 首页/方法页依赖的 Baseline150、UserIntent75、来源覆盖、幻觉率等指标。
- `roadmap90` 和策略下载描述中的执行计划。

当前文件没有直接声称真实曝光、销售或 AI 推荐提升，但相关边界仍应继续从工作簿/报告同步，避免后续文案漂移。
