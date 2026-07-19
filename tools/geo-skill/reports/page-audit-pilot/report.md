# 阶段 06B 页面审计模块试点报告

- 执行时间：2026-07-19T16:33:24+08:00
- 构建版本：17a24994cb351856e8b80d7cce5844585b462299
- 当前分支：refactor/portfolio-v2
- 构建方法：GitHub Pages equivalent: next build + scripts/prepare-github-pages.mjs with bundled Node
- Skill 来源：https://github.com/yaojingang/yao-geo-skills @ dc10716d97c40fed0a0a08e538a236b5e16b4822
- 审计边界：只读当前分支 `out/` 静态 HTML；不读取 internal-review；不调用外部 API；不修改页面。

## 审计页面
- `/`：首页，代表作品集整体叙事和项目身份。
- `/facts`：品牌事实页，代表品牌事实与证据表达。
- `/buying-guide`：购买指南页，代表决策型 GEO 内容。

## 每页摘要
### 首页 `/`
- title：公开研究首页
- description：元亨利红木家具GEO公开研究案例：225条AI回答、6项核心诊断、5个内容资产与13条公开FAQ。
- canonical：https://evelay.github.io/yhl-geo-portfolio/
- H1：让红木家具信息变得可回答、可核验
- 静态 main 正文长度：5358
- JSON-LD 类型：未发现
- 内链数量：30；外部来源链接数量：0
### 品牌事实页 `/facts`
- title：品牌事实与定位｜元亨利 GEO
- description：元亨利红木家具品牌事实、公开定位、品牌自述与待核验项的分层页面。
- canonical：https://evelay.github.io/yhl-geo-portfolio/
- H1：品牌事实与定位
- 静态 main 正文长度：916
- JSON-LD 类型：未发现
- 内链数量：17；外部来源链接数量：3
### 购买指南页 `/buying-guide`
- title：购买核验指南｜元亨利 GEO
- description：红木家具价格、门店、合同、证书、交付、售后和收藏表达的核验清单。
- canonical：https://evelay.github.io/yhl-geo-portfolio/
- H1：购买核验指南
- 静态 main 正文长度：826
- JSON-LD 类型：未发现
- 内链数量：17；外部来源链接数量：3

## 发现数量
- P0：0
- P1：2
- P2：6
- P3：2

## 维度数量
- 发现与抓取：2
- 页面元信息：0
- 语义结构：2
- 品牌事实与证据：0
- AI 可抽取性：3
- Schema：3
- 用户体验：0

## 发现清单
### 06B-PA-001 `/`
- 维度：Schema
- 证据状态：observed
- 严重度/优先级：low / P2
- 负责人：development
- 观察证据：未发现 application/ld+json。
- 问题：当前页面没有 JSON-LD，机器只能依赖正文和链接结构理解页面实体与类型。
- 建议动作：后续人工审核后再考虑页面级 JSON-LD 候选；本阶段不生成或写入 Schema。
- 验收方式：后续若接入 Schema，JSON-LD 字段必须能逐项回溯到页面正文。
### 06B-PA-002 `/`
- 维度：AI 可抽取性
- 证据状态：inferred
- 严重度/优先级：medium / P2
- 负责人：content
- 观察证据：H1=['让红木家具信息变得可回答、可核验']
- 问题：H1 未包含品牌实体，单独引用页面标题时容易脱离元亨利语境。
- 建议动作：后续内容修复可在 H1 或紧邻摘要中加入完整品牌实体与页面类型。
- 验收方式：抽取 H1 与首段文本时可独立识别本页服务的品牌实体。
### 06B-PA-003 `/facts`
- 维度：发现与抓取
- 证据状态：observed
- 严重度/优先级：medium / P1
- 负责人：development
- 观察证据：canonical=https://evelay.github.io/yhl-geo-portfolio/
- 问题：页面 canonical 未指向当前路由，子页面可能被合并到首页 canonical。
- 建议动作：在后续页面修复阶段为每个公开路由输出与页面路径一致的 canonical。
- 验收方式：构建后检查对应 HTML 的 link rel=canonical，值等于该路由公开 URL。
### 06B-PA-004 `/facts`
- 维度：Schema
- 证据状态：observed
- 严重度/优先级：low / P2
- 负责人：development
- 观察证据：未发现 application/ld+json。
- 问题：当前页面没有 JSON-LD，机器只能依赖正文和链接结构理解页面实体与类型。
- 建议动作：后续人工审核后再考虑页面级 JSON-LD 候选；本阶段不生成或写入 Schema。
- 验收方式：后续若接入 Schema，JSON-LD 字段必须能逐项回溯到页面正文。
### 06B-PA-005 `/facts`
- 维度：语义结构
- 证据状态：observed
- 严重度/优先级：low / P3
- 负责人：design
- 观察证据：未发现 breadcrumb/面包屑标记。
- 问题：子页面缺少面包屑，页面层级主要依赖全局导航表达。
- 建议动作：后续设计修复时为内容页补充可见或语义化面包屑。
- 验收方式：构建后页面存在 breadcrumb 语义标记，且链接指向首页与上级页面。
### 06B-PA-006 `/facts`
- 维度：AI 可抽取性
- 证据状态：inferred
- 严重度/优先级：medium / P2
- 负责人：content
- 观察证据：H1=['品牌事实与定位']
- 问题：H1 未包含品牌实体，单独引用页面标题时容易脱离元亨利语境。
- 建议动作：后续内容修复可在 H1 或紧邻摘要中加入完整品牌实体与页面类型。
- 验收方式：抽取 H1 与首段文本时可独立识别本页服务的品牌实体。
### 06B-PA-007 `/buying-guide`
- 维度：发现与抓取
- 证据状态：observed
- 严重度/优先级：medium / P1
- 负责人：development
- 观察证据：canonical=https://evelay.github.io/yhl-geo-portfolio/
- 问题：页面 canonical 未指向当前路由，子页面可能被合并到首页 canonical。
- 建议动作：在后续页面修复阶段为每个公开路由输出与页面路径一致的 canonical。
- 验收方式：构建后检查对应 HTML 的 link rel=canonical，值等于该路由公开 URL。
### 06B-PA-008 `/buying-guide`
- 维度：Schema
- 证据状态：observed
- 严重度/优先级：low / P2
- 负责人：development
- 观察证据：未发现 application/ld+json。
- 问题：当前页面没有 JSON-LD，机器只能依赖正文和链接结构理解页面实体与类型。
- 建议动作：后续人工审核后再考虑页面级 JSON-LD 候选；本阶段不生成或写入 Schema。
- 验收方式：后续若接入 Schema，JSON-LD 字段必须能逐项回溯到页面正文。
### 06B-PA-009 `/buying-guide`
- 维度：语义结构
- 证据状态：observed
- 严重度/优先级：low / P3
- 负责人：design
- 观察证据：未发现 breadcrumb/面包屑标记。
- 问题：子页面缺少面包屑，页面层级主要依赖全局导航表达。
- 建议动作：后续设计修复时为内容页补充可见或语义化面包屑。
- 验收方式：构建后页面存在 breadcrumb 语义标记，且链接指向首页与上级页面。
### 06B-PA-010 `/buying-guide`
- 维度：AI 可抽取性
- 证据状态：inferred
- 严重度/优先级：medium / P2
- 负责人：content
- 观察证据：H1=['购买核验指南']
- 问题：H1 未包含品牌实体，单独引用页面标题时容易脱离元亨利语境。
- 建议动作：后续内容修复可在 H1 或紧邻摘要中加入完整品牌实体与页面类型。
- 验收方式：抽取 H1 与首段文本时可独立识别本页服务的品牌实体。

## 三个页面的共性问题
- 三页都未发现 JSON-LD；本阶段只记录缺口，不生成或写入 Schema。
- 三页 H1 都偏主题化，没有直接写出“元亨利”品牌实体，独立引用标题时语境不够完整。
- 两个内容子页面缺少页面级 canonical 和面包屑，页面路径与层级主要依赖全局导航表达。

## 页面特有问题
- `/`：最重要的特有问题是 H1 未直接包含品牌实体，首页标题脱离上下文后偏泛化。
- `/facts`：最重要的特有问题是 canonical 指向首页，而不是 `/facts` 页面 URL。
- `/buying-guide`：最重要的特有问题是 canonical 指向首页，而不是 `/buying-guide` 页面 URL。

## 建议修复顺序
1. 先处理 P1 canonical，保证每个公开路由的页面级 canonical 正确。
2. 再处理 P2 页面主题：让 H1 或紧邻摘要能独立识别元亨利品牌实体。
3. 最后处理 P2/P3 结构增强：人工审核后的 JSON-LD 候选和子页面面包屑。

## 审计限制
- 本报告只基于构建后的静态 HTML、robots 和 sitemap。
- 未读取 external canonical 工作簿、raw AI answers、人工评分或 internal-review 内容。
- 未运行 crawler、未调用模型或外部 API、未使用线上 main 页面。
- 发现中的 `inferred` 只表示基于页面证据和方法规则的推断，不写成事实。
- 本报告不生成单一 GEO 总分，也不输出 AI 排名、品牌召回率、引用份额、AI 引用概率或优化后提升预测。

## 输出文件
- `tools/geo-skill/reports/page-audit-pilot/report.md`
- `tools/geo-skill/reports/page-audit-pilot/report.json`
- `tools/geo-skill/reports/page-audit-pilot/run-metadata.json`
- `docs/06b-page-audit-findings.csv`
