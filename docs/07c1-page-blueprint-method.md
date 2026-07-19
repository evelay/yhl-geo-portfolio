# 阶段 07C1 H1 与可见 Breadcrumb 页面蓝图方法

日期：2026-07-19
分支：`refactor/portfolio-v2`

## 1. Skill 来源

本阶段参考 `yao-geo-skills` 仓库中的 `skills/yao-geo-page-blueprint`。

- 来源仓库：`https://github.com/yaojingang/yao-geo-skills`
- 来源 commit：`eabfde0f0bdf53f84559bdfcba2595fcac1ad50f`
- 原许可证：MIT
- 本地裁剪目录：`tools/geo-skill/upstream/yao-geo-page-blueprint/`

Git 根目录未发现 `AGENTS.md`。本阶段以现有治理文档、页面源码和构建后 HTML 为项目依据。

## 2. 当前项目适配方式

原 Skill 面向完整 GEO 页面蓝图，通常包含 query fan-out、实体关系、证据区、HTML 结构、Schema、CMS 字段、无障碍和四格式报告。本阶段只裁剪其中与页面结构直接相关的方法：

- 首屏 H1 必须能独立说明页面对象与页面用途。
- H1 下方摘要应补足页面上下文，但不得新增品牌事实。
- breadcrumb 只表达真实页面层级，不伪造不存在的中间层级。
- Schema 候选或同步建议必须来自页面正文、已存在 JSON-LD 和 canonical，不写正文没有的事实。
- 页面结构建议必须能由人工审核后再实施。

本阶段不使用原 Skill 的 Word、PDF、HTML 报告生成流程，也不运行上游渲染脚本。

## 3. 页面范围

只处理以下三个页面：

- `/`
- `/facts`
- `/buying-guide`

其中可见 breadcrumb 蓝图只覆盖两个内页：

- `/facts`
- `/buying-guide`

首页只作为内页 breadcrumb 的根节点，不为首页设计自身 breadcrumb。

## 4. 输入边界

允许输入：

- `docs/` 中已列出的治理、发布、canonical、breadcrumb schema 和页面审计文档。
- `tools/geo-skill/reports/page-audit-pilot-after-breadcrumb-schema/report.md`
- `tools/geo-skill/reports/page-audit-pilot-after-breadcrumb-schema/report.json`
- `app/page.tsx`
- `app/facts/page.tsx`
- `app/buying-guide/page.tsx`
- `app/components.tsx`
- `app/data.ts` 中与三页导航、标题和内容有关的 website-copy 信息。
- `app/globals.css` 中与 header、hero、article、标题和未来 breadcrumb 样式相关的信息。
- `out/index.html`
- `out/facts/index.html`
- `out/buying-guide/index.html`

禁止输入：

- `internal-review/` 文件内容。
- `first_setup/`。
- `final/`。
- archive 或 outdated 文件。
- 外部 canonical 工作簿、raw AI answers 或人工评分工作簿。
- 未经审核的品牌事实、效果数据或实施结果。

`app/data.ts` 在本项目中是 website-copy，只用于观察当前公开导航、页面名称和页面文案承接关系，不作为品牌事实主源。

## 5. 不进行的工作

本阶段不修改：

- `app/`
- `public/`
- 页面正文
- H1
- title 或 description
- 可见 breadcrumb
- 现有 `BreadcrumbList` JSON-LD
- canonical
- sitemap
- robots
- 视觉样式
- 其他 Schema

本阶段不生成：

- GEO 总分
- AI 引用概率
- 收录概率
- 排名分数
- H1 优化提升预测
- Word、PDF 或正式 HTML 页面

## 6. H1 判断标准

每个 H1 候选按以下标准判断：

- 是否明确品牌或页面服务对象。
- 是否明确页面类型或项目类型。
- 是否准确反映已完成工作，避免把蓝图、诊断或作品集写成官方实施。
- 是否暗示官方委托、官方项目或品牌背书。
- 是否暗示已经取得优化增长、收录增长、引用率提升或商业结果。
- 是否适合招聘方快速理解作品集价值。
- 是否容易被普通用户理解。
- 是否与现有 title、description、项目声明和页面正文一致。

H1 可以补足“元亨利”“红木家具”“GEO 诊断”“内容体系”“购买核验”等上下文，但不能新增品牌荣誉、排名、效果或未核验事实。

## 7. Breadcrumb 判断标准

可见 breadcrumb 只表达真实页面层级。当前没有真实存在的“知识中心”等中间路由，因此层级保持两级：

- `/facts`：首页 -> 品牌事实与定位
- `/buying-guide`：首页 -> 购买核验指南

判断标准：

- 用户可读性。
- 导航简洁性。
- 与 H1 的一致性或可解释差异。
- 与现有 `BreadcrumbList` JSON-LD 的一致性。
- 移动端长度与换行风险。
- 是否重复品牌词导致视觉负担。
- 是否需要同步修改现有 JSON-LD `name` 字段。

推荐优先使用简短导航名，并让用户可见 breadcrumb 与现有 `BreadcrumbList` name 保持一致；若人工选择完整 H1 方案，则应同步更新 JSON-LD name，避免可见和机器字段冲突。

## 8. 页面摘要判断标准

H1 后摘要应控制在 40-90 字，作用是让页面上下文独立，不承担新增事实或效果承诺。

摘要只允许重组当前页面已有信息：

- 页面用途。
- 研究边界。
- 数据或事实口径。
- 用户下一步。
- 需要核验的事项。

摘要不得新增品牌事实、荣誉、排名、官方背书、AI 引用概率、收录概率、效果增长或购买推荐。

## 9. Schema 同步规则

H1 或 breadcrumb 文案变化不应自动改变 URL、canonical 或 sitemap。

同步规则：

- H1 修改不影响页面 URL。
- 文案变化不影响 canonical。
- 文案变化通常不影响 sitemap，除非 URL 变化；本阶段不建议 URL 变化。
- title 和 meta description 可以为一致性进行文案同步，但必须人工审核。
- `BreadcrumbList` name 可以与 H1 完全一致，也可以采用可解释的简短页面名。
- 选择后，用户可见 breadcrumb 与 JSON-LD 不得表达互相矛盾的页面名称。
- 如果 JSON-LD name 变更，后续实施阶段必须重新运行页面审计与 Schema 注入测试。

## 10. 人工审核节点

进入 07C2 之前，人工必须确认：

- 首页最终 H1。
- `/facts` 最终 H1。
- `/buying-guide` 最终 H1。
- 三页是否添加或调整 H1 下方摘要。
- 可见 breadcrumb 使用简短名称还是完整 H1。
- 是否允许同步更新现有 `BreadcrumbList` name。
- URL 和 canonical 是否保持不变。
- 是否只在两个内页增加可见 breadcrumb。
- 是否进入 07C2 实施。

## 11. 后续实施门禁

07C2 实施前必须重新确认：

- 分支仍为 `refactor/portfolio-v2`。
- upstream 仍为 `origin/refactor/portfolio-v2`。
- ahead/behind 为 `0/0`。
- 工作区干净。
- 目标页面 H1、title、description、canonical 和现有 JSON-LD 未在其他提交中改变。
- 仍不读取 `internal-review/`、`first_setup/`、`final/` 或 archive。
- 只实施经人工确认的 H1、摘要和两个内页可见 breadcrumb。
- 实施后重新运行构建、页面审计和 Schema/BreadcrumbList 回归测试。
