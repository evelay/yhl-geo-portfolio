# 阶段 07B BreadcrumbList 人工审核清单

日期：2026-07-19

本清单记录技术观察与 07B2 注入前人工决定。

## 07B2 人工决定

审核状态：`approved-for-injection`

- `/facts` breadcrumb 名称使用：`品牌事实与定位`
- `/buying-guide` breadcrumb 名称使用：`购买核验指南`
- 根节点使用：`首页`
- `/facts` 层级：`首页 > 品牌事实与定位`
- `/buying-guide` 层级：`首页 > 购买核验指南`
- 当前网站没有真实存在的“知识中心”中间路由，因此不得增加该层级。
- 只允许注入这两个 `BreadcrumbList`。
- 不允许生成或注入首页 `BreadcrumbList`。
- 不允许生成其他 Schema。

## /facts

- 页面路由：`/facts`
- 页面真实标题：`品牌事实与定位`
- canonical：`https://evelay.github.io/yhl-geo-portfolio/facts/`
- breadcrumb 层级：`首页 > 品牌事实与定位`
- 草稿文件：`tools/geo-skill/reports/schema-draft-pilot/facts-breadcrumb.jsonld`
- 是否与页面导航一致：部分一致。主导航短标签为“品牌事实”，页面 H1 为“品牌事实与定位”。
- 是否与可见 breadcrumb 一致：不可比较。当前页面未发现可见 breadcrumb UI。
- 是否存在中间层级缺失：未发现。当前路由和导航未显示“知识中心”等中间层级。
- 是否允许下一阶段注入：`approved-for-injection`
- 人工确认项：确认是否使用 H1“品牌事实与定位”作为 Schema name；确认根节点“首页”是否可接受；确认无需增加中间层级；确认注入前仍不生成其他 Schema 类型。

## /buying-guide

- 页面路由：`/buying-guide`
- 页面真实标题：`购买核验指南`
- canonical：`https://evelay.github.io/yhl-geo-portfolio/buying-guide/`
- breadcrumb 层级：`首页 > 购买核验指南`
- 草稿文件：`tools/geo-skill/reports/schema-draft-pilot/buying-guide-breadcrumb.jsonld`
- 是否与页面导航一致：部分一致。主导航短标签为“购买核验”，页面 H1 为“购买核验指南”。
- 是否与可见 breadcrumb 一致：不可比较。当前页面未发现可见 breadcrumb UI。
- 是否存在中间层级缺失：未发现。当前路由和导航未显示“知识中心”等中间层级。
- 是否允许下一阶段注入：`approved-for-injection`
- 人工确认项：确认是否使用 H1“购买核验指南”作为 Schema name；确认根节点“首页”是否可接受；确认无需增加中间层级；确认注入前仍不生成其他 Schema 类型。
