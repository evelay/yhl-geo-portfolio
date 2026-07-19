# 阶段 07A2 实体关系人工裁决记录

日期：2026-07-19

## 1. 决策目的

本记录承接阶段 07A 的品牌实体图谱结果，用人工治理决定确认哪些实体、关系和候选可以进入后续 Schema 草稿范围，哪些只能作为内容治理、页面素材、研究议题或待核验证据关系。

阶段 07A2 不生成 JSON-LD，不修改网站页面，不修改安全知识库，不读取 internal-review，也不把证据等级自动等同为 Schema 可发布资格。

## 2. 品牌与企业主体决定

`brand:yuanhengli` 和 `organization:beijing-yuanhengli-hardwood-furniture` 必须保持为两个独立候选实体。

当前不得将“元亨利品牌”和任何企业 `Organization` 自动合并为同一个 canonical entity。两个实体均标记为 `hold-identity-evidence`，不得进入 `Organization` Schema，也不得进入 `Brand` Schema。

重新开放条件是补采到公开、可追溯、可写入 evidence ledger 的 `evidence_id`，且该证据可以直接支持品牌名称、法律主体、官网或公开账号之间的具体关系。

## 3. 京作关系决定

`topic:jingzuo-unresolved` 和 `REL-07A-0036` 只可作为内容主题关系、待核验工艺关联和页面研究议题。

当前不得表达为官方京作代表、唯一传承、独家关系或已获权威认证的身份关系。没有直接 `evidence_id` 的京作关系标记为 `hold-evidence`，不得进入生产 Schema。

## 4. 材料关系决定

红木、紫檀、黄花梨、酸枝和白酸枝相关表达只允许作为 `Material` 实体、`ContentTopic` 或页面中的教育和研究主题。

不得推断全部产品使用该材料、主要产品必然使用该材料、品牌等同材料品类、独家经营关系、收藏价值或投资回报。材料关系不得进入 `Organization` Schema 的产品、服务、offer 或商业承诺字段。

## 5. 明式和清式决定

明式、清式只作为 `FurnitureStyle`、`ContentTopic` 和用户教育概念。

不得表达为具体家具生产年代、文物年代、产品真实性证明或品牌官方身份。与年代、馆藏或产品真伪有关的关系一律排除在生产 Schema 外。

## 6. BoundaryRule 决定

`BoundaryRule` 是内部事实治理和内容审核规则。

所有 BoundaryRule 均处理为 `content-governance-only`，不进入生产 Schema。它们可用于内容审核、Prompt 限制、页面免责声明和后续人工审查清单。

## 7. QuestionIntent 决定

`QuestionIntent` 用于问题库、内容映射、AI 测试和 FAQ 规划。

QuestionIntent 不得作为品牌实体 Schema 中的事实或关系。所有 QuestionIntent 均处理为 `research-only`，不进入生产 Schema。

## 8. FAQ 进入 Schema 的条件

FAQ 候选只有同时满足以下条件时，才可以进入后续 FAQ Schema 映射：

- 问题和答案已经在公开页面真实显示。
- publication decision 为 `publish`。
- `source_id` 有效。
- 不含 pending、L3、prohibited 或 internal-only 内容。
- 问题和答案与页面正文一致。

本阶段只做 eligibility 分类，不生成 FAQ JSON-LD。

## 9. Article 进入 Schema 的条件

Article 候选只有同时满足以下条件时，才可以进入后续 Article Schema：

- 页面已经公开。
- 页面正文通过发布审核。
- headline 与页面 H1 一致。
- `datePublished` 或 `dateModified` 可确认。
- 作者或责任主体可安全表达。
- 页面引用与来源可追溯。

本阶段只做 eligibility 分类，不生成 Article JSON-LD。

## 10. BreadcrumbList 进入条件

`BreadcrumbList` 可以作为 07B 的第一实施目标，因为它只反映真实导航层级，不表达品牌、企业、材料、工艺、作者或产品事实。

允许进入 07B 的试点路由为：

- `/`
- `/facts`
- `/buying-guide`

07B 只能在隔离目录创建草稿并验证与真实页面导航一致，不得自动注入页面。

## 11. Organization 暂缓原因

`Organization` Schema 当前状态为 `defer`。

暂缓原因是品牌、企业主体、官网、公开账号和来源组织之间仍需直接公开证据确认。不得为了完成 Schema 类型数量而编造企业主体、法律关系、官网主体、成立时间、荣誉、行业地位或官方委托关系。

## 12. Person 当前拒绝原因

`Person` Schema 当前状态为 `reject-for-current-stage`。

当前输入没有足够安全的作者身份、专家资质、人物关系、职务或外部背书证据。不得为了补充结构化数据而编造作者、专家、创始人、负责人或人物关系。

## 13. 需要补采的 evidence

后续若要重新评估 Schema 范围，需要补采以下公开 evidence：

- 品牌与企业主体关系的直接公开证据。
- 官网域名、备案主体、品牌主体和联系主体之间的可追溯证据。
- 京作家具或京作工艺与品牌之间的直接公开关系证据。
- 材料术语与具体页面正文、标准来源和单件证据边界的一致性证据。
- 明式、清式作为风格概念的公开来源证据，不得用于产品年代结论。
- FAQ 问答在公开页面真实展示且通过发布审核的页面证据。
- Article 页面 H1、headline、发布时间、修改时间、责任主体和引用来源证据。

## 14. 未来重新开放决定的条件

只有在补采证据进入证据账本、页面正文通过发布审核、人工确认不会扩大为禁止事实后，才可以重新开放被 hold、defer 或 reject-for-current-stage 的 Schema 决定。

重新开放不得自动批准。每个实体和关系必须重新执行人工裁决，并记录新的 `evidence_id`、页面依赖、Schema 类型、发布边界和回滚条件。
