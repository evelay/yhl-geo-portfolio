# 07B BreadcrumbList 隔离草稿报告

生成日期：2026-07-19

## 范围

本阶段只为 `/facts` 和 `/buying-guide` 生成 `BreadcrumbList` JSON-LD 隔离草稿。首页只作为 position 1 的根节点，不为首页生成独立草稿。

草稿只写入 `tools/geo-skill/reports/schema-draft-pilot/`，未注入页面，未修改 `app/` 或 `public/`。

## breadcrumb-ready 为 0 的说明

`docs/07a2-schema-candidate-classification.csv` 中 14 个实体图谱候选均不具备 breadcrumb-ready 输入属性，`allowed_in_07b` 均为 `no`。这些候选属于品牌实体、事实、FAQ、Article、QuestionIntent、BoundaryRule 或治理规则候选，不是页面层级候选。

`BreadcrumbList` 的输入不是品牌关系或实体事实，而是已确认的真实页面层级、页面 H1 或可见标题、导航文字和 canonical URL。因此 breadcrumb-ready 为 0 不阻止本阶段生成两个页面级 breadcrumb 草稿，也不得为了增加数量去改写原候选分类。

## 页面观察

| route | rendered title | rendered H1 | canonical | nav label | visible breadcrumb |
|---|---|---|---|---|---|
| `/` | 公开研究首页 | 让红木家具信息变得可回答、可核验 | https://evelay.github.io/yhl-geo-portfolio/ | 研究首页 | none observed |
| `/facts` | 品牌事实与定位｜元亨利 GEO | 品牌事实与定位 | https://evelay.github.io/yhl-geo-portfolio/facts/ | 品牌事实 | none observed |
| `/buying-guide` | 购买核验指南｜元亨利 GEO | 购买核验指南 | https://evelay.github.io/yhl-geo-portfolio/buying-guide/ | 购买核验 | none observed |

## 草稿

| route | draft file | hierarchy | page name basis |
|---|---|---|---|
| `/facts` | `facts-breadcrumb.jsonld` | 首页 > 品牌事实与定位 | rendered H1 and metadata title |
| `/buying-guide` | `buying-guide-breadcrumb.jsonld` | 首页 > 购买核验指南 | rendered H1 and metadata title |

## 验证结果

总体状态：`valid`

| check | status | detail |
|---|---|---|
| `expected_two_drafts` | `pass` | exactly /facts and /buying-guide draft files are planned |
| `homepage_canonical_matches_html` | `pass` | homepage canonical matches rendered HTML and config |
| `stable_jsonld_generation` | `pass` | same config produces byte-stable JSON-LD draft content |
| `no_app_or_public_write_targets` | `pass` | planned outputs do not target app/ or public/ |
| `/facts_jsonld_context` | `pass` | facts-breadcrumb.jsonld uses https://schema.org |
| `/facts_jsonld_type` | `pass` | facts-breadcrumb.jsonld uses BreadcrumbList only |
| `/facts_item_list_array` | `pass` | itemListElement is an array |
| `/facts_positions_continuous` | `pass` | positions are 1 and 2 |
| `/facts_homepage_position_1` | `pass` | homepage is position 1 |
| `/facts_target_position_2` | `pass` | target page is position 2 |
| `/facts_canonical_matches_html` | `pass` | draft target URL matches rendered canonical |
| `/facts_page_name_matches_h1` | `pass` | draft page name matches rendered H1 |
| `/facts_no_extra_levels` | `pass` | breadcrumb contains only homepage and target page |
| `/facts_list_items_complete` | `pass` | each ListItem has @type, name and item |
| `/facts_no_duplicate_base_path` | `pass` | no duplicated /yhl-geo-portfolio/ basePath |
| `/facts_no_forbidden_url_parts` | `pass` | no chatgpt.site, localhost, 127.0.0.1, local absolute path markers or duplicated basePath |
| `/facts_no_forbidden_schema_types` | `pass` | no Organization, Brand, Person, Article, FAQPage, Product, Offer, Review or AggregateRating |
| `/facts_no_forbidden_properties` | `pass` | only BreadcrumbList/ListItem properties are present |
| `/buying-guide_jsonld_context` | `pass` | buying-guide-breadcrumb.jsonld uses https://schema.org |
| `/buying-guide_jsonld_type` | `pass` | buying-guide-breadcrumb.jsonld uses BreadcrumbList only |
| `/buying-guide_item_list_array` | `pass` | itemListElement is an array |
| `/buying-guide_positions_continuous` | `pass` | positions are 1 and 2 |
| `/buying-guide_homepage_position_1` | `pass` | homepage is position 1 |
| `/buying-guide_target_position_2` | `pass` | target page is position 2 |
| `/buying-guide_canonical_matches_html` | `pass` | draft target URL matches rendered canonical |
| `/buying-guide_page_name_matches_h1` | `pass` | draft page name matches rendered H1 |
| `/buying-guide_no_extra_levels` | `pass` | breadcrumb contains only homepage and target page |
| `/buying-guide_list_items_complete` | `pass` | each ListItem has @type, name and item |
| `/buying-guide_no_duplicate_base_path` | `pass` | no duplicated /yhl-geo-portfolio/ basePath |
| `/buying-guide_no_forbidden_url_parts` | `pass` | no chatgpt.site, localhost, 127.0.0.1, local absolute path markers or duplicated basePath |
| `/buying-guide_no_forbidden_schema_types` | `pass` | no Organization, Brand, Person, Article, FAQPage, Product, Offer, Review or AggregateRating |
| `/buying-guide_no_forbidden_properties` | `pass` | only BreadcrumbList/ListItem properties are present |

## 禁止项确认

- 未生成 Organization、Brand、Person、Article、FAQPage、Product、Offer、Review 或 AggregateRating Schema。
- 未包含 author、publisher、logo、datePublished、dateModified、brand、material、offers、review 或 aggregateRating 等字段。
- 未写入品牌实体关系、材料关系、京作关系、产品声明或内部治理规则。
- 未读取 `internal-review/` 或 `archive/`。
- 未调用 API、模型或安装新依赖。
- 未修改 `app/` 或 `public/`，未进行页面注入。

## 后续人工审核

进入 07B2 注入前，需人工确认两页的页面名称、canonical、导航短标签与 breadcrumb 层级可接受，并确认仍不需要新增中间层级。
