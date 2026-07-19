# 07D1 首页 Schema 类型评估与隔离草稿报告

生成日期：2026-07-19

## 范围

本阶段只评估首页 `06B-PA-001`（首页无 JSON-LD），并生成三个隔离 JSON-LD 草稿。未注入页面，未修改 `app/` 或 `public/`。

## 首页事实

| item | observed value | source |
|---|---|---|
| canonical | https://evelay.github.io/yhl-geo-portfolio/ | `out/index.html` link rel=canonical |
| title | 公开研究首页 | `app/page.tsx` metadata and `out/index.html` |
| meta description | 元亨利红木家具GEO公开研究案例：225条AI回答、6项核心诊断、5个内容资产与13条公开FAQ。 | `app/page.tsx` metadata and `out/index.html` |
| H1 | 元亨利红木家具 GEO 诊断与可核验内容体系 | `app/page.tsx` and `out/index.html` |
| public summary | 本页呈现基于公开资料完成、未受元亨利委托且不代表品牌官方立场的独立 GEO 研究案例，围绕 AI 回答基线、品牌事实治理、内容体系和页面技术优化，诊断认知与证据缺口。 | homepage hero `.lede` |
| language | zh-CN | `app/layout.tsx` and rendered html lang |
| project identity | 本项目为基于公开资料完成的独立 GEO 研究与求职作品集，未受元亨利委托，不代表品牌官方立场；不声称已提升 AI 收录、引用、曝光、推荐或销售。 | global footer in `app/components.tsx` |
| existing JSON-LD | 0 script(s) | rendered homepage |
| site search | no | rendered homepage form/input scan |

主要模块：

- hero and project summary
- research design and baseline metrics
- direct answers
- six diagnostic findings
- content asset entries
- method and limits
- brand content proposal entries
- global research statement footer

## 方案比较

| option | schema types | status | evaluation |
|---|---|---|---|
| 07D1-A | WebSite | alternative | 字段最少、身份风险最低，可以解决 finding；但只描述站点，不显式描述当前首页这个页面，页面匹配度略弱。 |
| 07D1-B | WebSite + WebPage | recommended | 与首页作为站点入口和具体页面的双重事实最匹配；不需要 publisher、author、Organization、Brand、Person 或 SearchAction，维护成本仍低。 |
| 07D1-C | WebSite + CollectionPage | reject | 首页确实包含内容入口，但同时是诊断看板、方法说明和项目叙事；CollectionPage 会把页面过度建模为集合页。 |

## 推荐草稿

推荐选择 `07D1-B`：`WebSite + WebPage`。推荐 name 使用当前 H1，推荐 description 使用当前首页可见摘要原文，以保留非官方与独立研究边界。

本阶段不设置 `publisher`，不生成 `Organization`、`Brand`、`Person`，不生成 `SearchAction`。

## 验证结果

总体状态：`valid`

| check | status | detail |
|---|---|---|
| `expected_three_drafts` | `pass` | exactly WebSite, WebSite+WebPage and WebSite+CollectionPage drafts are planned |
| `homepage_canonical_matches_html` | `pass` | homepage canonical matches rendered HTML and config |
| `homepage_title_matches_html` | `pass` | homepage title matches rendered HTML and config |
| `homepage_meta_description_matches_html` | `pass` | homepage meta description matches rendered HTML and config |
| `homepage_h1_matches_html` | `pass` | homepage has exactly one H1 and it matches config |
| `homepage_summary_matches_html` | `pass` | homepage public summary matches proposed Schema description |
| `homepage_language_matches_html` | `pass` | homepage html lang is zh-CN |
| `homepage_has_no_jsonld_now` | `pass` | current homepage still has no JSON-LD before any future injection |
| `homepage_has_no_site_search` | `pass` | no verified homepage site search or SearchAction input |
| `homepage_identity_statement_present` | `pass` | rendered homepage includes independent research and non-official statement |
| `homepage_html_has_no_forbidden_markers` | `pass` | rendered homepage has no local path, old domain or duplicate basePath marker |
| `stable_jsonld_generation` | `pass` | same config produces byte-stable JSON-LD draft content |
| `no_app_or_public_write_targets` | `pass` | planned outputs do not target app/ or public/ |
| `finding_06b_pa_001_still_open` | `pass` | 06B-PA-001 remains open because this stage does not inject homepage JSON-LD |
| `07D1-A_json_parseable` | `pass` | website-only.jsonld round-trips as JSON |
| `07D1-A_context` | `pass` | @context is https://schema.org |
| `07D1-A_schema_types` | `pass` | @type sequence is ['WebSite'] |
| `07D1-A_ids_are_public` | `pass` | @id values use public GitHub Pages URL |
| `07D1-A_url_matches_canonical` | `pass` | all url values match homepage canonical |
| `07D1-A_name_matches_h1` | `pass` | all name values match current homepage H1 |
| `07D1-A_description_matches_public_summary` | `pass` | description equals the rendered public homepage summary |
| `07D1-A_language` | `pass` | inLanguage is zh-CN |
| `07D1-A_no_local_or_old_urls` | `pass` | no local user-home, loopback, old-domain or duplicated basePath markers |
| `07D1-A_no_duplicate_base_path` | `pass` | no duplicated /yhl-geo-portfolio/ basePath |
| `07D1-A_no_forbidden_schema_types` | `pass` | no Organization, Brand, Person or SearchAction types |
| `07D1-A_no_forbidden_properties` | `pass` | only whitelisted properties are present |
| `07D1-A_no_search_action` | `pass` | SearchAction is absent because no verified site search exists |
| `07D1-A_no_false_effect_or_official_claim` | `pass` | no official-site, official-project, commissioned, growth or effect claims |
| `07D1-B_json_parseable` | `pass` | website-webpage-graph.jsonld round-trips as JSON |
| `07D1-B_context` | `pass` | @context is https://schema.org |
| `07D1-B_schema_types` | `pass` | @type sequence is ['WebSite', 'WebPage'] |
| `07D1-B_ids_are_public` | `pass` | @id values use public GitHub Pages URL |
| `07D1-B_url_matches_canonical` | `pass` | all url values match homepage canonical |
| `07D1-B_name_matches_h1` | `pass` | all name values match current homepage H1 |
| `07D1-B_description_matches_public_summary` | `pass` | description equals the rendered public homepage summary |
| `07D1-B_language` | `pass` | inLanguage is zh-CN |
| `07D1-B_no_local_or_old_urls` | `pass` | no local user-home, loopback, old-domain or duplicated basePath markers |
| `07D1-B_no_duplicate_base_path` | `pass` | no duplicated /yhl-geo-portfolio/ basePath |
| `07D1-B_no_forbidden_schema_types` | `pass` | no Organization, Brand, Person or SearchAction types |
| `07D1-B_no_forbidden_properties` | `pass` | only whitelisted properties are present |
| `07D1-B_no_search_action` | `pass` | SearchAction is absent because no verified site search exists |
| `07D1-B_no_false_effect_or_official_claim` | `pass` | no official-site, official-project, commissioned, growth or effect claims |
| `07D1-B_page_is_part_of_website` | `pass` | page node points to WebSite with isPartOf |
| `07D1-C_json_parseable` | `pass` | website-collectionpage-graph.jsonld round-trips as JSON |
| `07D1-C_context` | `pass` | @context is https://schema.org |
| `07D1-C_schema_types` | `pass` | @type sequence is ['WebSite', 'CollectionPage'] |
| `07D1-C_ids_are_public` | `pass` | @id values use public GitHub Pages URL |
| `07D1-C_url_matches_canonical` | `pass` | all url values match homepage canonical |
| `07D1-C_name_matches_h1` | `pass` | all name values match current homepage H1 |
| `07D1-C_description_matches_public_summary` | `pass` | description equals the rendered public homepage summary |
| `07D1-C_language` | `pass` | inLanguage is zh-CN |
| `07D1-C_no_local_or_old_urls` | `pass` | no local user-home, loopback, old-domain or duplicated basePath markers |
| `07D1-C_no_duplicate_base_path` | `pass` | no duplicated /yhl-geo-portfolio/ basePath |
| `07D1-C_no_forbidden_schema_types` | `pass` | no Organization, Brand, Person or SearchAction types |
| `07D1-C_no_forbidden_properties` | `pass` | only whitelisted properties are present |
| `07D1-C_no_search_action` | `pass` | SearchAction is absent because no verified site search exists |
| `07D1-C_no_false_effect_or_official_claim` | `pass` | no official-site, official-project, commissioned, growth or effect claims |
| `07D1-C_page_is_part_of_website` | `pass` | page node points to WebSite with isPartOf |

## 后续人工审核

进入 07D2 注入前，需要人工确认最终 Schema 类型、name、description、是否继续不设置 publisher / Organization / Brand / Person / SearchAction，以及是否允许下一阶段写入首页。
