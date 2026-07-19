# 阶段 07B BreadcrumbList Schema 隔离草稿方法

日期：2026-07-19

## 1. 为什么 BreadcrumbList 先于 Organization

`BreadcrumbList` 只表达页面层级和 canonical URL，不声明品牌主体、企业主体、人物、材料、产品、价格、评价或背书关系。阶段 07A2 已将 `Organization` 标记为 defer，因为品牌、企业主体、官网和公开账号之间仍缺少可直接写入 Schema 的公开证据链。

因此 07B 先做 `BreadcrumbList`，可以降低 Schema 试点风险：它验证的是页面结构，不放大实体事实，也不提前合并 `brand:yuanhengli` 与 `organization:beijing-yuanhengli-hardwood-furniture`。

## 2. breadcrumb-ready 为 0 仍可生成 breadcrumb 的原因

`docs/07a2-schema-candidate-classification.csv` 中 14 个实体图谱候选的 `allowed_in_07b` 均为 `no`，即本阶段记录的 breadcrumb-ready 数量为 0。这 14 项属于品牌实体、事实、FAQ、Article、QuestionIntent、BoundaryRule 或治理规则候选，不是页面层级候选。

`BreadcrumbList` 的输入不是这些品牌关系，也不是材料、京作、产品或 FAQ 事实。它的输入来自已经确认的真实页面层级、页面 H1 或可见标题、导航文字和页面 canonical URL。

因此，breadcrumb-ready 为 0 不妨碍本阶段为真实页面创建 breadcrumb 草稿；也不得为了让 breadcrumb-ready 数量大于 0 而修改原候选分类。

## 3. BreadcrumbList 的真实输入来源

本阶段只读以下页面和构建产物：

- `app/page.tsx`
- `app/facts/page.tsx`
- `app/buying-guide/page.tsx`
- `app/components.tsx`
- `app/data.ts`
- `app/layout.tsx`
- `out/index.html`
- `out/facts/index.html`
- `out/buying-guide/index.html`

页面名称优先采用目标页真实 H1；若 H1 与 metadata title 不一致，需在报告中说明并进入人工审核。本阶段两页 H1 与 metadata title 一致。

## 4. 页面范围

07B 只生成两个草稿：

- `/facts`
- `/buying-guide`

首页 `/` 只作为 breadcrumb 根节点，不为首页自身生成独立 `BreadcrumbList` 草稿。

本阶段确认的层级为：

- `/facts`：首页 > 品牌事实与定位
- `/buying-guide`：首页 > 购买核验指南

当前真实路由中未发现“知识中心”等中间层级，因此不得添加不存在的中间层级。

## 5. URL 口径

所有 breadcrumb item URL 必须与当前 canonical 完全一致，并统一保留结尾斜杠：

- 首页：`https://evelay.github.io/yhl-geo-portfolio/`
- `/facts`：`https://evelay.github.io/yhl-geo-portfolio/facts/`
- `/buying-guide`：`https://evelay.github.io/yhl-geo-portfolio/buying-guide/`

不得出现 `chatgpt.site`、`localhost`、本地绝对路径，或重复 `/yhl-geo-portfolio/yhl-geo-portfolio/`。

## 6. 页面名称取值规则

根节点使用简短名称“首页”，用于表达 breadcrumb 的起点。首页真实公开名称在页面中表现为 metadata title“公开研究首页”、导航标签“研究首页”以及页眉品牌标识“元亨利 GEO / 公开研究案例”。

目标页使用真实 H1：

- `/facts` 使用“品牌事实与定位”，不是导航短标签“品牌事实”。
- `/buying-guide` 使用“购买核验指南”，不是导航短标签“购买核验”。

示例中较短的“品牌事实”或“购买指南”不覆盖真实页面 H1。

## 7. 输出隔离规则

草稿和报告只写入：

- `tools/geo-skill/adapters/schema-draft/`
- `tools/geo-skill/reports/schema-draft-pilot/`
- `docs/07b-*`

不得写入 `app/` 或 `public/`，不得注入页面，不得修改 sitemap、robots、canonical、H1、正文或可见 breadcrumb UI。

## 8. 人工审核节点

进入 07B2 页面注入前，人工需要确认：

- 两个目标页是否仍为试点范围。
- 目标页名称是否采用当前 H1。
- 根节点“首页”是否可接受。
- 是否确认没有“知识中心”等真实中间层级。
- canonical 是否仍与页面一致。
- 导航短标签与 breadcrumb 显示名称不同是否可接受。
- 是否允许下一阶段把已批准草稿注入页面。

本阶段不替用户做最终批准。

## 9. 后续注入条件

只有在人工审核通过后，下一阶段才可考虑页面注入。注入前还需重新确认：

- 当前分支、upstream、ahead/behind 和工作区状态。
- 两页 H1、metadata title、canonical 和路由未变化。
- JSON-LD 仍只包含 `BreadcrumbList` 与 `ListItem`。
- app 注入位置不会产生重复 JSON-LD。
- 构建后 HTML 可解析且 canonical 与 item URL 一致。

## 10. 回滚方法

本阶段若需回滚，可删除本阶段新增的 `docs/07b-*` 文件、`tools/geo-skill/adapters/schema-draft/` 和 `tools/geo-skill/reports/schema-draft-pilot/`，或直接 revert 本阶段 commit。由于没有修改 `app/`、`public/` 或页面 HTML 注入逻辑，回滚不会影响线上页面。

## 11. 当前暂缓的 Schema 类型

本阶段暂缓或禁止生成以下 Schema：

- Organization
- Brand
- Person
- Article
- FAQPage
- Product
- Offer
- Review
- AggregateRating

这些类型需要后续证据补采、页面审核和人工裁决，不得在 07B 中顺带生成。

