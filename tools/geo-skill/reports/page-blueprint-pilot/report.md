# 阶段 07C1 H1 与可见 Breadcrumb 页面蓝图报告

- 执行日期：2026-07-19
- 当前分支：`refactor/portfolio-v2`
- 项目 commit：`1e70b57d8cfdfef79aebc97249220f78080ecf77`
- Skill 来源：`https://github.com/yaojingang/yao-geo-skills` @ `eabfde0f0bdf53f84559bdfcba2595fcac1ad50f`
- Skill 路径：`skills/yao-geo-page-blueprint`
- 本地裁剪目录：`tools/geo-skill/upstream/yao-geo-page-blueprint/`
- 报告边界：只生成蓝图、方案和人工审核清单；不修改页面。

## 1. 前置状态

| 检查项 | 结果 |
| --- | --- |
| 工作目录与 Git 根目录 | 仓库根目录一致 |
| 当前分支 | `refactor/portfolio-v2` |
| upstream | `origin/refactor/portfolio-v2` |
| ahead/behind | `0/0` |
| 初始工作区 | clean |
| 是否切换 main | no |
| `AGENTS.md` | Git 根目录未发现 |

## 2. 输入与禁止项

已读取输入：

- 指定 `docs/` 治理、发布、canonical、breadcrumb schema 和页面审计文档。
- `tools/geo-skill/reports/page-audit-pilot-after-breadcrumb-schema/report.md`
- `tools/geo-skill/reports/page-audit-pilot-after-breadcrumb-schema/report.json`
- 三页源码、共享组件、website-copy 导航数据和相关样式。
- 三页构建后 HTML：`out/index.html`、`out/facts/index.html`、`out/buying-guide/index.html`。
- 上游 `yao-geo-page-blueprint` 的必要方法、接口、模板、eval、references、报告画像、脚本和许可证。

未使用输入：

- 未读取 `internal-review/` 文件内容。
- 未读取 `first_setup`、`final`、archive 或 outdated 文件。
- 未读取外部 canonical 工作簿、raw AI answers 或人工评分工作簿。
- 未调用外部 API 或模型。
- 未安装新依赖。

项目约束：

- 本项目是基于公开资料完成的独立 GEO 研究与求职作品集，不是元亨利官方委托。
- `app/data.ts` 是 website-copy，不是品牌事实主源。
- 不得虚构品牌事实、效果或实施结果。
- H1、breadcrumb 或摘要建议不得描述为 AI 排名、引用概率、收录概率或增长提升。

## 3. 当前页面只读记录

### `/`

| 项目 | 当前观察 |
| --- | --- |
| title | `公开研究首页` |
| meta description | `元亨利红木家具GEO公开研究案例：225条AI回答、6项核心诊断、5个内容资产与13条公开FAQ。` |
| H1 | `让红木家具信息变得可回答、可核验` |
| H1 下方摘要 | 现有 `.lede` 已说明独立研究、公开资料、未受委托、225 条 AI 回答、实体/来源/高客单风险与内容资产。 |
| 页面项目身份说明 | 页脚研究声明说明独立 GEO 研究与求职作品集，未受元亨利委托，不代表官方立场，不声称 AI 收录、引用、曝光、推荐或销售提升。 |
| canonical | `https://evelay.github.io/yhl-geo-portfolio/` |
| 可见导航 | 全站主导航，含研究首页、品牌事实、同名消歧、材质边界、京作/明清、购买核验、FAQ、优化方案、企业知识库、提示词体系、GEO文章样稿、方法与来源。 |
| 可见 breadcrumb | 未发现。首页不要求新增 breadcrumb。 |
| BreadcrumbList JSON-LD | 未发现。 |
| main/article/header 语义 | `main` 1 个，`header` 1 个，`footer` 1 个；首页卡片中存在多个 `article`。 |
| H1-H3 层级 | H1 1 个，H2 6 个，H3 25 个。 |
| 第一屏表达 | 页眉品牌为“元亨利 GEO / 公开研究案例”；H1 偏泛化，lede 才说明元亨利和独立研究身份。 |
| 用户下一步入口 | 查看六项诊断、品牌内容优化方案、企业知识库、提示词体系、GEO文章样稿、方法与来源；后续模块还有内容资产入口。 |

判断：当前首页 lede 已强约束项目身份，但 H1 脱离上下文后不能快速识别元亨利、GEO 项目和具体解决的问题。

### `/facts`

| 项目 | 当前观察 |
| --- | --- |
| title | `品牌事实与定位｜元亨利 GEO` |
| meta description | `元亨利红木家具品牌事实、公开定位、品牌自述与待核验项的分层页面。` |
| H1 | `品牌事实与定位` |
| H1 下方摘要 | 现有 `.lede` 是直接答案，已说明“元亨利”在本案例中指红木家具语境中的品牌/企业主体，以及排名和强定位边界。 |
| 页面项目身份说明 | 页脚研究声明说明独立 GEO 研究与求职作品集，未受元亨利委托，不代表官方立场，不声称效果提升。 |
| canonical | `https://evelay.github.io/yhl-geo-portfolio/facts/` |
| 可见导航 | 全站主导航。 |
| 可见 breadcrumb | 未发现。 |
| BreadcrumbList JSON-LD | 已存在 1 个，层级为 `首页 -> 品牌事实与定位`。 |
| main/article/header 语义 | `main` 1 个，`article` 1 个，`header` 1 个，`footer` 1 个。 |
| H1-H3 层级 | H1 1 个，H2 5 个，H3 3 个。 |
| 第一屏表达 | `内容资产 01` + H1 + 直接答案框；H1 不含元亨利，lede 才补充品牌语境。 |
| 用户下一步入口 | 如何区分同名主体、官网一定是第三方证据吗、查看方法与来源、可核验来源。 |

判断：当前 H1 清楚但品牌语境不足。页面真实内容不仅是“定位”，还包含来源分层与信息边界。

### `/buying-guide`

| 项目 | 当前观察 |
| --- | --- |
| title | `购买核验指南｜元亨利 GEO` |
| meta description | `红木家具价格、门店、合同、证书、交付、售后和收藏表达的核验清单。` |
| H1 | `购买核验指南` |
| H1 下方摘要 | 现有 `.lede` 是直接答案，说明高客单红木家具不应依赖 AI 给出的价格、门店或保值升值判断，需核对型号、材质、合同、证书、交付、发票和售后主体。 |
| 页面项目身份说明 | 页脚研究声明说明独立 GEO 研究与求职作品集，未受元亨利委托，不代表官方立场，不声称效果提升。 |
| canonical | `https://evelay.github.io/yhl-geo-portfolio/buying-guide/` |
| 可见导航 | 全站主导航。 |
| 可见 breadcrumb | 未发现。 |
| BreadcrumbList JSON-LD | 已存在 1 个，层级为 `首页 -> 购买核验指南`。 |
| main/article/header 语义 | `main` 1 个，`article` 1 个，`header` 1 个，`footer` 1 个。 |
| H1-H3 层级 | H1 1 个，H2 5 个，H3 0 个。 |
| 第一屏表达 | `内容资产 05` + H1 + 直接答案框；H1 不含元亨利或红木家具，lede 才补充用户任务。 |
| 用户下一步入口 | 材质证据怎么分层、同名主体怎么确认、查看公开 FAQ、可核验来源。 |

判断：当前 H1 能表达任务但品牌和品类语境不足。页面需要继续保持核验指南，不应变成购买推荐或品牌背书。

## 4. 首页 H1 方案

| 候选 | 判断 |
| --- | --- |
| `元亨利品牌 GEO 诊断与内容体系设计` | 品牌和项目类型明确，较适合招聘方；“品牌”一词需由项目声明继续约束，避免被理解为官方项目。 |
| `元亨利 GEO 可见度诊断与品牌知识体系` | 项目类型明确，能解释诊断与知识体系；“可见度”应避免被误读为已带来增长。 |
| `元亨利品牌在 AI 搜索中的认知诊断与内容优化` | 普通用户易理解 AI 搜索语境；“内容优化”有中等风险，可能被误解为已完成优化实施。 |
| `元亨利红木家具 GEO 诊断与可核验内容体系` | 推荐。品牌、品类、GEO、诊断和内容体系均明确；与现有 lede、title、description 和项目声明一致，不暗示官方委托或效果提升。 |

首选：首页 H1 建议采用 `元亨利红木家具 GEO 诊断与可核验内容体系`。

同步建议：

- title 建议后续同步增强，不必改变 URL。
- description 可保留或轻微同步。
- 首页当前没有 BreadcrumbList，因此 H1 修改不触发 breadcrumb schema 同步。
- canonical 不变。

## 5. `/facts` H1 方案

| 候选 | 判断 |
| --- | --- |
| `品牌事实与定位` | 当前 H1，简洁但品牌实体不独立；只有结合 lede 或 title 才知道是元亨利。 |
| `元亨利品牌事实与定位` | 补足品牌实体，和现有 title、description 容易对齐；但对来源与信息边界的表达不够充分。 |
| `元亨利品牌事实、来源与信息边界` | 推荐。最贴近页面真实内容：事实分层、品牌自述、公开来源、待核验项和边界；不会把待确认事实写成确认事实。 |

首选：`/facts` H1 建议采用 `元亨利品牌事实、来源与信息边界`。

同步建议：

- title 建议同步，否则 title 仍强调“定位”而 H1 强调“来源与信息边界”。
- description 建议同步，说明“品牌事实、来源层级、品牌自述与待核验边界”。
- BreadcrumbList name 可继续使用简短页面名 `品牌事实与定位`，也可同步为完整 H1；需人工确认。
- canonical、URL 和 sitemap 不变。

## 6. `/buying-guide` H1 方案

| 候选 | 判断 |
| --- | --- |
| `购买核验指南` | 当前 H1，任务清楚但品牌和品类语境不足。 |
| `元亨利红木家具购买核验指南` | 推荐。直接说明品牌、品类和用户任务；“核验指南”保持中性，不构成购买推荐或品牌背书。 |
| `评估元亨利红木家具时应核验什么` | 任务语义最强，背书风险低；但更像问题句，作为页面 H1 和 breadcrumb name 较长。 |

首选：`/buying-guide` H1 建议采用 `元亨利红木家具购买核验指南`。

同步建议：

- title 建议同步。
- description 可保留或轻微同步，加入“元亨利红木家具”语境，但不得写成购买推荐。
- BreadcrumbList name 可继续使用简短页面名 `购买核验指南`，也可同步为完整 H1；需人工确认。
- canonical、URL 和 sitemap 不变。

## 7. 可见 Breadcrumb 蓝图

### 方案 A：简短导航名

- `/facts`：`首页 -> 品牌事实与定位`
- `/buying-guide`：`首页 -> 购买核验指南`

评估：

- 用户可读性：高，和当前导航、既有 JSON-LD name 接近。
- 导航简洁性：高。
- 与 H1 一致性：若 H1 改为完整品牌表达，则为“短页面名”而非完全一致；可解释。
- 与 BreadcrumbList JSON-LD 一致性：可保持现有 name 不变。
- 移动端长度：低风险。
- 品牌词重复：低风险。
- 是否需要修改 JSON-LD name：不强制。

### 方案 B：与新 H1 完全一致

示例：

- `/facts`：`首页 -> 元亨利品牌事实、来源与信息边界`
- `/buying-guide`：`首页 -> 元亨利红木家具购买核验指南`

评估：

- 用户可读性：中等，含品牌和任务但更长。
- 导航简洁性：中等到低。
- 与 H1 一致性：高。
- 与 BreadcrumbList JSON-LD 一致性：需要同步 JSON-LD name 才能完全一致。
- 移动端长度：中到高风险，尤其 `/facts` 推荐 H1 较长。
- 品牌词重复：中等，页眉和 H1 都已有品牌词。
- 是否需要修改 JSON-LD name：需要。

推荐：采用方案 A。理由是两个内页已有全站页眉品牌标识，后续 H1 也会补品牌语境，breadcrumb 更适合作为低强调的短路径。若人工要求完全一致，再采用方案 B 并同步 JSON-LD name。

## 8. 可见 Breadcrumb 组件设计建议

本阶段不写正式组件代码。后续实施可设计共享组件，例如 `VisibleBreadcrumb`，但需先由人工批准。

建议放置：

- 内页主内容上方。
- H1 之前。
- 更推荐位于项目免责声明或页面身份提示之后；当前两个内页没有独立的顶部免责声明，页脚有研究声明，因此可放在 `article-hero` 内 eyebrow 与 H1 之间，保持低强调。

HTML 语义建议：

```html
<nav aria-label="面包屑导航">
  <ol>
    <li><a href="/">首页</a></li>
    <li aria-current="page">当前页面</li>
  </ol>
</nav>
```

无障碍要求：

- 使用 `nav`。
- 使用清晰的 `aria-label`。
- 使用 `ol` 和 `li`。
- 当前页使用 `aria-current="page"`。
- 首页链接文字清晰，不只用图标。

GitHub Pages basePath 处理：

- 必须兼容 `/yhl-geo-portfolio`。
- 优先复用 Next `Link` 与项目已有路径辅助逻辑。
- 不硬编码错误根路径，不手写重复 `/yhl-geo-portfolio/yhl-geo-portfolio`。
- 构建后检查链接是否输出为 `/yhl-geo-portfolio/`。

样式要求：

- 使用现有网站视觉语言：暖底、teal/cinnabar 低强调边界、紧凑文字。
- 不增加复杂卡片。
- 不进行全站视觉重构。
- 移动端允许换行。
- 文本不得挤出容器或遮挡 H1。

## 9. 页面摘要蓝图

| route | 是否需要 | 推荐摘要草稿 | 解决的问题 | 是否重组现有信息 | 人工审核 |
| --- | --- | --- | --- | --- | --- |
| `/` | yes | `本页汇总基于公开资料的元亨利红木家具 GEO 基线诊断、风险边界和内容资产设计，说明研究范围、数据口径与后续核验入口。` | H1 改具体后，摘要承接独立研究、数据口径和页面用途。 | yes | yes |
| `/facts` | yes | `本页用于说明元亨利红木家具相关品牌事实的来源层级、可写边界与待核验事项，避免把品牌自述、行业印象或排名推断写成确认事实。` | 补足来源和信息边界，避免只读 H1 时误以为页面确认所有事实。 | yes | yes |
| `/buying-guide` | yes | `本页把元亨利红木家具购买前后的核验动作整理为清单，聚焦合同、材质、证书、交付、售后和动态信息复核，不提供购买推荐或投资判断。` | 强化核验任务和非背书边界。 | yes | yes |

说明：三段摘要均只重组当前页面已有信息，不新增品牌事实或效果结果。

## 10. Schema 同步影响分析

通用结论：

- H1 修改不应自动改变 URL。
- canonical 不应因为文案变化而改变。
- sitemap 不应因为文案变化而改变。
- title 和 description 可按人工确认后的 H1 进行一致性同步。
- 用户可见 breadcrumb 和 JSON-LD name 可以使用简短页面名，也可以完整匹配 H1，但必须保持不冲突。
- 采用方案 A 时，两页现有 BreadcrumbList name 可保持不变。
- 采用方案 B 时，两页现有 BreadcrumbList name 需要同步更新。
- 后续实施后必须重新运行页面审计和 Schema 注入测试。

| route | H1 影响 BreadcrumbList name | 影响 canonical | 影响 title | 影响 description | 影响 URL | 影响 sitemap | 需重跑页面审计 | 需重跑 Schema 测试 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `/` | no，首页当前无 BreadcrumbList | no | yes，建议同步 | optional | no | no | yes | no，除非新增 Schema |
| `/facts` | optional，取决于短名或完整 H1 方案 | no | yes，建议同步 | yes，建议同步 | no | no | yes | yes，若 JSON-LD name 改动或新增可见 breadcrumb |
| `/buying-guide` | optional，取决于短名或完整 H1 方案 | no | yes，建议同步 | optional | no | no | yes | yes，若 JSON-LD name 改动或新增可见 breadcrumb |

## 11. 本阶段不实施事项

本阶段未修改：

- `app/`
- `public/`
- 页面正文
- H1
- title 或 description
- 可见 breadcrumb
- 现有 BreadcrumbList JSON-LD
- canonical
- sitemap
- robots
- 视觉样式
- 其他 Schema

本阶段未生成：

- GEO 总分
- AI 引用概率
- 收录概率
- 排名分数
- H1 优化提升预测
- Word、PDF 或正式 HTML 页面

## 12. 进入 07C2 前人工确认

进入实施前，请人工确认：

1. 首页最终 H1。
2. `/facts` 最终 H1。
3. `/buying-guide` 最终 H1。
4. 是否添加三页摘要。
5. 可见 breadcrumb 使用简短名称还是完整 H1。
6. 是否允许同步更新现有 BreadcrumbList name。
7. 是否保持 URL 和 canonical 不变。
8. 是否只在两个内页增加可见 breadcrumb。
9. 是否进入 07C2 实施。

## 13. 输出文件

- `docs/07c1-page-blueprint-method.md`
- `docs/07c1-h1-options.csv`
- `docs/07c1-breadcrumb-options.csv`
- `docs/07c1-human-review.md`
- `tools/geo-skill/reports/page-blueprint-pilot/report.md`
- `tools/geo-skill/reports/page-blueprint-pilot/report.json`
- `tools/geo-skill/reports/page-blueprint-pilot/run-metadata.json`
