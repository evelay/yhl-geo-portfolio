# 阶段 07D1 首页 Schema 类型评估方法

日期：2026-07-19

## 1. 首页 finding

本阶段只处理 `06B-PA-001`：首页 `/` 当前没有 `application/ld+json`。该 finding 在 `docs/06b-page-audit-findings.csv` 中必须继续保持 `open`，因为 07D1 只生成隔离草稿，不注入首页。

## 2. 为什么不能使用 Organization

阶段 07A2 已将 `Organization` 标记为 `defer`。当前公开证据不足以把元亨利品牌、企业主体、官网、公开账号和来源组织合并为可发布的结构化实体。为了补齐 Schema 而添加企业主体、法律关系、官网主体、成立时间、荣誉、行业地位或官方委托关系，都会扩大事实范围。

因此 07D1 不生成 `Organization`，也不通过 `publisher`、`owner`、`creator`、`author`、`copyrightHolder` 或 `accountablePerson` 间接生成组织或责任主体。

## 3. 为什么不把元亨利作为 publisher

本网站是独立 GEO 研究与求职作品集，不是元亨利官方网站，不是元亨利官方 GEO 项目，也不代表品牌官方立场。页面公开声明写明：项目基于公开资料完成，未受元亨利委托，不声称已提升 AI 收录、引用、曝光、推荐或销售。

把元亨利写成 `publisher` 会暗示品牌官方发布或承担页面责任，与当前项目身份冲突。当前也没有可安全表达的个人作者或发布组织，因此不设置 `publisher`。

## 4. 三种 Schema 方案

### 方案 A：WebSite only

只表达站点层级事实：`@context`、`@type`、`@id`、`url`、`name`、`description`、`inLanguage`。优点是字段最少、维护成本最低、官方身份风险最低；缺点是没有显式表达首页作为具体页面的事实。可作为备选。

### 方案 B：WebSite + WebPage

使用 `@graph`，包含 `WebSite` 与 `WebPage`，并通过 `WebPage.isPartOf` 指向 `WebSite`。该方案同时覆盖站点入口和当前首页页面，不依赖未确认主体，也不需要发布方、作者、组织、品牌、人物或搜索动作。推荐作为当前阶段后续人工审核的首选。

### 方案 C：WebSite + CollectionPage

使用 `@graph`，包含 `WebSite` 与 `CollectionPage`。首页确实包含五个内容资产入口、FAQ、知识库、提示词和文章样稿入口，但它同时承担研究设计、baseline 指标、六项诊断、方法边界和项目叙事。将首页建模为 `CollectionPage` 会放大“内容集合页”语义，当前拒绝。

## 5. 字段白名单

07D1 草稿只允许以下字段：

- `@context`
- `@graph`
- `@type`
- `@id`
- `url`
- `name`
- `description`
- `inLanguage`
- `isPartOf`

`name` 使用当前首页 H1：`元亨利红木家具 GEO 诊断与可核验内容体系`。

`description` 使用当前首页可见摘要原文：`本页呈现基于公开资料完成、未受元亨利委托且不代表品牌官方立场的独立 GEO 研究案例，围绕 AI 回答基线、品牌事实治理、内容体系和页面技术优化，诊断认知与证据缺口。`

## 6. 字段禁用清单

07D1 草稿不得包含：

- `publisher`
- `author`
- `creator`
- `copyrightHolder`
- `accountablePerson`
- `owner`
- `Organization`
- `Brand`
- `Person`
- `logo`
- `sameAs`
- `award`
- `review`
- `aggregateRating`
- `offers`
- `potentialAction`
- `SearchAction`

当前首页没有真实站内搜索功能，因此不得生成 `SearchAction`。

## 7. 页面事实来源

只读来源：

- `app/page.tsx`：首页 H1、摘要、页面模块和页面 metadata。
- `app/layout.tsx`：站点 canonical 推导、默认 metadata 和 `html lang="zh-CN"`。
- `app/components.tsx`：页眉导航、页脚研究声明。
- `app/data.ts`：与首页展示直接相关的导航、指标和内容资产入口。
- `out/index.html`：构建后 title、description、canonical、H1、摘要、语言和 JSON-LD 实际状态。
- `public/sitemap.xml`：首页公开 URL。
- `public/robots.txt`：sitemap 公开入口。
- `docs/06b-page-audit-findings.csv` 与 07A2、07B、07C 文档：治理边界、Schema 范围和当前 finding 状态。

仓库根目录未发现 `AGENTS.md`；本阶段未使用替代 agent 规则文件。

## 8. 人工审核节点

07D1 不替用户批准最终 Schema。进入 07D2 前，人工需要确认最终选用 `WebSite only`、`WebSite + WebPage` 或 `WebSite + CollectionPage`，并确认 name、description、publisher、实体禁用项、SearchAction、URL 和 canonical。

## 9. 后续注入条件

07D2 若要注入首页，至少需要重新确认：

- 当前分支仍为 `refactor/portfolio-v2`。
- upstream 仍为 `origin/refactor/portfolio-v2`，ahead/behind 仍为 `0/0`。
- 工作区干净。
- 首页 canonical、H1、公开摘要、语言和页面身份声明未变化。
- `06B-PA-001` 仍为 `open`。
- 人工审核已明确批准某一个草稿。
- 注入后 HTML 只有一个新的首页 JSON-LD，且不引入禁用字段或禁用类型。

## 10. 回滚方式

本阶段只新增 `docs/07d1-*` 和 `tools/geo-skill/` 下的隔离草稿、脚本、测试与报告。回滚可删除这些新增文件，或在提交后执行：

```bash
git revert <07D1-commit>
```

由于未修改 `app/` 或 `public/`，本阶段回滚不会移除任何生产页面注入。
