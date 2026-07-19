# 阶段 07A 品牌实体图谱试点报告

## 输入范围

- 唯一品牌数据输入：`public/downloads/yhl-geo-knowledge-base-public.json`
- 输入 SHA-256：`379fbec902654f6daabd5cf5eb5ff856cd418f78e09ba5c772f6e69b8895c991`
- 公开快照版本：`1.1-public-filtered`
- publication scope：`public-filtered: reviewed public records with valid source_id only`
- 本次构建不读取 internal-review、外部工作簿、first_setup、yhl_geo_portfolio_final、旧版未过滤 JSON、完整文章样稿、完整提示词、PDF/DOCX、原始 AI 回答或人工评分工作簿。

## Skill 来源

- 来源仓库：`https://github.com/yaojingang/yao-geo-skills`
- 来源 Skill：`skills/yao-geo-brand-graph`
- 来源 commit：`dc10716d97c40fed0a0a08e538a236b5e16b4822`
- 原许可证：`MIT`
- 07A 仅接入实体消歧、关系证据和边界治理方法；未运行上游 URL 采样、Word/PDF/HTML 渲染、JSON-LD 或 RDF 输出。

## 实体数量和类型

- 实体总数：98
- BoundaryRule：9
- Brand：1
- ContentTopic：5
- CraftTradition：1
- FurnitureStyle：2
- Geography：1
- Material：4
- Organization：6
- ProductCategory：1
- PublicationAsset：6
- QuestionIntent：38
- Source：24

## 关系数量

- 关系总数：36
- public-safe：15
- review-required：21
- evidence-gap：19

## Public-Safe 候选关系

- `REL-07A-0001` `organization:beijing-yuanhengli-hardwood-furniture` -- `has_subject_verification_source` -> `source:s0-001` (source-confirmed, EV-006)
- `REL-07A-0006` `brand:yuanhengli` -- `has_self_description_source` -> `source:a-004` (source-confirmed, EV-002,EV-004)
- `REL-07A-0007` `brand:yuanhengli` -- `has_media_context_source` -> `source:b-011` (source-confirmed, EV-001)
- `REL-07A-0010` `material:redwood` -- `defined_by_standard` -> `source:b-001` (source-confirmed, EV-007)
- `REL-07A-0011` `material:redwood` -- `usage_expression_governed_by` -> `source:b-002` (source-confirmed, EV-007)
- `REL-07A-0013` `category:redwood-furniture` -- `purchase_should_preserve_vouchers` -> `boundary:single-item-evidence` (source-confirmed, EV-011,EV-012)
- `REL-07A-0014` `category:redwood-furniture` -- `contract_fields_should_be_written` -> `source:b-005` (source-confirmed, EV-009,EV-010)
- `REL-07A-0015` `organization:china-furniture-association` -- `information_entry_not_ranking` -> `boundary:no-ranking-claim` (source-confirmed, EV-002)
- `REL-07A-0026` `category:redwood-furniture` -- `item_material_conclusion_requires` -> `boundary:single-item-evidence` (source-confirmed, EV-007,EV-008)
- `REL-07A-0027` `category:redwood-furniture` -- `dynamic_info_requires_date` -> `boundary:dynamic-channel-review` (source-confirmed, EV-009,EV-010)
- `REL-07A-0028` `category:redwood-furniture` -- `must_not_promise_investment_return` -> `boundary:no-investment-return` (source-confirmed, EV-011,EV-012)
- `REL-07A-0029` `topic:zitan-understanding` -- `uses_material_boundary` -> `material:zitan` (snapshot-supported, EV-007)
- `REL-07A-0030` `topic:baisuanzhi-term` -- `uses_material_boundary` -> `material:suanzhi` (snapshot-supported, EV-003)
- `REL-07A-0031` `intent:q11` -- `governed_by_boundary` -> `boundary:no-brand-org-equivalence` (snapshot-supported, EV-006)
- `REL-07A-0032` `intent:q28` -- `governed_by_boundary` -> `boundary:no-investment-return` (snapshot-supported, EV-012)

## Review-Required 关系

- `REL-07A-0002` `brand:yuanhengli` -- `must_be_disambiguated_from` -> `organization:beijing-yuanhengli-hardwood-furniture` (inferred, EV-006)
- `REL-07A-0003` `brand:yuanhengli` -- `has_contact_subject_candidate` -> `organization:beijing-yuanhengli-hardwood-furniture` (evidence-gap, evidence-gap)
- `REL-07A-0004` `brand:yuanhengli` -- `has_website_candidate` -> `asset:bjyuanhengli-com` (evidence-gap, evidence-gap)
- `REL-07A-0005` `brand:yuanhengli` -- `has_product_content_entry` -> `category:redwood-furniture` (evidence-gap, evidence-gap)
- `REL-07A-0008` `brand:yuanhengli` -- `process_column_mentions` -> `craft:classical-process-terms` (evidence-gap, evidence-gap)
- `REL-07A-0009` `brand:yuanhengli` -- `dynamic_channel_info_requires` -> `boundary:dynamic-channel-review` (source-confirmed, EV-010)
- `REL-07A-0012` `category:redwood-furniture` -- `technical_condition_background` -> `source:b-003` (evidence-gap, evidence-gap)
- `REL-07A-0016` `organization:beijing-furniture-trade-association` -- `activity_context_source` -> `source:b-009` (evidence-gap, evidence-gap)
- `REL-07A-0017` `source:b-012` -- `provides_background_for` -> `style:ming-style-furniture` (evidence-gap, evidence-gap)
- `REL-07A-0018` `source:b-012` -- `provides_background_for` -> `style:qing-style-furniture` (evidence-gap, evidence-gap)
- `REL-07A-0019` `source:b-012` -- `provides_background_for` -> `material:huanghuali` (evidence-gap, evidence-gap)
- `REL-07A-0020` `source:b-012` -- `provides_background_for` -> `material:zitan` (evidence-gap, evidence-gap)
- `REL-07A-0021` `material:huanghuali` -- `requires_standard_and_item_evidence` -> `boundary:no-material-generalization` (evidence-gap, evidence-gap)
- `REL-07A-0022` `material:zitan` -- `requires_single_item_evidence` -> `boundary:no-material-generalization` (evidence-gap, evidence-gap)
- `REL-07A-0023` `material:suanzhi` -- `vernacular_name_requires_normalization` -> `boundary:single-item-evidence` (evidence-gap, evidence-gap)
- `REL-07A-0024` `style:ming-style-furniture` -- `must_not_be_used_as_product_date` -> `boundary:no-style-as-date` (evidence-gap, evidence-gap)
- `REL-07A-0025` `style:qing-style-furniture` -- `must_not_be_used_as_product_date` -> `boundary:no-style-as-date` (evidence-gap, evidence-gap)
- `REL-07A-0033` `topic:huanghuali-relation` -- `requires_material_boundary` -> `material:huanghuali` (evidence-gap, evidence-gap)
- `REL-07A-0034` `topic:ming-qing-style` -- `requires_style_boundary` -> `style:ming-style-furniture` (evidence-gap, evidence-gap)
- `REL-07A-0035` `topic:ming-qing-style` -- `requires_style_boundary` -> `style:qing-style-furniture` (evidence-gap, evidence-gap)
- `REL-07A-0036` `brand:yuanhengli` -- `no_public_jingzuo_identity_evidence_in_allowed_input` -> `boundary:no-jingzuo-identity-without-evidence` (evidence-gap, evidence-gap)

## Evidence-Gap

- `REL-07A-0003` `brand:yuanhengli` -- `has_contact_subject_candidate` -> `organization:beijing-yuanhengli-hardwood-furniture` (evidence-gap, evidence-gap)
- `REL-07A-0004` `brand:yuanhengli` -- `has_website_candidate` -> `asset:bjyuanhengli-com` (evidence-gap, evidence-gap)
- `REL-07A-0005` `brand:yuanhengli` -- `has_product_content_entry` -> `category:redwood-furniture` (evidence-gap, evidence-gap)
- `REL-07A-0008` `brand:yuanhengli` -- `process_column_mentions` -> `craft:classical-process-terms` (evidence-gap, evidence-gap)
- `REL-07A-0012` `category:redwood-furniture` -- `technical_condition_background` -> `source:b-003` (evidence-gap, evidence-gap)
- `REL-07A-0016` `organization:beijing-furniture-trade-association` -- `activity_context_source` -> `source:b-009` (evidence-gap, evidence-gap)
- `REL-07A-0017` `source:b-012` -- `provides_background_for` -> `style:ming-style-furniture` (evidence-gap, evidence-gap)
- `REL-07A-0018` `source:b-012` -- `provides_background_for` -> `style:qing-style-furniture` (evidence-gap, evidence-gap)
- `REL-07A-0019` `source:b-012` -- `provides_background_for` -> `material:huanghuali` (evidence-gap, evidence-gap)
- `REL-07A-0020` `source:b-012` -- `provides_background_for` -> `material:zitan` (evidence-gap, evidence-gap)
- `REL-07A-0021` `material:huanghuali` -- `requires_standard_and_item_evidence` -> `boundary:no-material-generalization` (evidence-gap, evidence-gap)
- `REL-07A-0022` `material:zitan` -- `requires_single_item_evidence` -> `boundary:no-material-generalization` (evidence-gap, evidence-gap)
- `REL-07A-0023` `material:suanzhi` -- `vernacular_name_requires_normalization` -> `boundary:single-item-evidence` (evidence-gap, evidence-gap)
- `REL-07A-0024` `style:ming-style-furniture` -- `must_not_be_used_as_product_date` -> `boundary:no-style-as-date` (evidence-gap, evidence-gap)
- `REL-07A-0025` `style:qing-style-furniture` -- `must_not_be_used_as_product_date` -> `boundary:no-style-as-date` (evidence-gap, evidence-gap)
- `REL-07A-0033` `topic:huanghuali-relation` -- `requires_material_boundary` -> `material:huanghuali` (evidence-gap, evidence-gap)
- `REL-07A-0034` `topic:ming-qing-style` -- `requires_style_boundary` -> `style:ming-style-furniture` (evidence-gap, evidence-gap)
- `REL-07A-0035` `topic:ming-qing-style` -- `requires_style_boundary` -> `style:qing-style-furniture` (evidence-gap, evidence-gap)
- `REL-07A-0036` `brand:yuanhengli` -- `no_public_jingzuo_identity_evidence_in_allowed_input` -> `boundary:no-jingzuo-identity-without-evidence` (evidence-gap, evidence-gap)

## 重点消歧

- `AMB-07A-001` 元亨利：元亨利红木家具作为品牌识别对象，北京元亨利硬木家具有限公司作为企业主体候选，二者进入 07B 前需人工确认关系。（EV-006）
- `AMB-07A-002` 京作家具 / 京作工艺：本阶段只记录京作关系缺证；不得创建品牌与京作的公开关系。（evidence-gap）
- `AMB-07A-003` 紫檀：紫檀是材料概念和内容主题；单件产品材质需证书、检测、合同或发票。（EV-007,EV-008）
- `AMB-07A-004` 黄花梨：黄花梨是材料概念与内容主题；品牌关系需要明确 evidence_id。（evidence-gap）
- `AMB-07A-005` 白酸枝：白酸枝作为酸枝相关俗称治理对象，需回规范中文名并与合同、产品凭证一致。（EV-003）
- `AMB-07A-006` 明式：明式是家具史和审美风格概念；产品年代需单件资料。（evidence-gap）
- `AMB-07A-007` 清式：清式是家具史和审美风格概念；产品年代需单件资料。（evidence-gap）

## 信息边界

- 不把品牌自述写成第三方认证。
- 不把材料主题写成经营事实或全部产品材质事实。
- 不把明式、清式风格写成具体产品年代或文物年代。
- 不生成排名、奖项、官方委托、创始人、成立年份、门店数量、销售额、客户数量、投资回报或已实施 GEO 增长结果。
- 没有 evidence_id 的关系不进入 Mermaid 图和 07B eligible=yes 候选。

## 对现有页面的影响建议

- `/facts`：后续可把品牌/企业主体消歧作为 Schema 前置人工确认项。
- `/materials`：可使用材料边界和单件证据规则强化材料主题表达，但不改页面正文。
- `/jingzuo`：当前允许输入未提供京作实体或关系证据，进入 07B 前需要补充公开 evidence_id 或保持缺证说明。
- `/buying-guide`：可把合同、凭证、动态信息和不承诺保值升值规则作为后续 FAQ/Article 候选输入。

## 后续 Schema 输入候选

- `SC-07A-0003` Article or FAQ topic entity：`material:redwood`
- `SC-07A-0034` Organization candidate：`organization:china-furniture-association`
- `SC-07A-0037` Organization candidate：`organization:people-cn`
- `SC-07A-0040` FAQ or Article safety boundary：`boundary:no-material-generalization`
- `SC-07A-0041` FAQ or Article safety boundary：`boundary:single-item-evidence`
- `SC-07A-0043` FAQ or Article safety boundary：`boundary:no-ranking-claim`
- `SC-07A-0044` FAQ or Article safety boundary：`boundary:dynamic-channel-review`
- `SC-07A-0045` FAQ or Article safety boundary：`boundary:no-investment-return`
- `SC-07A-0095` Article or FAQ relationship input：`REL-07A-0010`
- `SC-07A-0096` Article or FAQ relationship input：`REL-07A-0011`
- `SC-07A-0100` Article or FAQ relationship input：`REL-07A-0015`
- `SC-07A-0115` Article or FAQ relationship input：`REL-07A-0030`
- `SC-07A-0116` Article or FAQ relationship input：`REL-07A-0031`
- `SC-07A-0117` Article or FAQ relationship input：`REL-07A-0032`

## 被阻止进入 Schema 的关系或实体

- `SC-07A-0001` `brand:yuanhengli`：disambiguation_conflict
- `SC-07A-0002` `organization:beijing-yuanhengli-hardwood-furniture`：disambiguation_conflict
- `SC-07A-0004` `material:huanghuali`：disambiguation_conflict
- `SC-07A-0005` `material:zitan`：disambiguation_conflict
- `SC-07A-0006` `material:suanzhi`：publication_safety_not_public_safe
- `SC-07A-0007` `category:redwood-furniture`：disambiguation_conflict
- `SC-07A-0008` `style:ming-style-furniture`：disambiguation_conflict
- `SC-07A-0009` `style:qing-style-furniture`：disambiguation_conflict
- `SC-07A-0010` `source:s0-001`：missing_evidence_id
- `SC-07A-0011` `source:s0-002`：missing_evidence_id
- `SC-07A-0012` `source:s0-003`：missing_evidence_id
- `SC-07A-0013` `source:s0-004`：missing_evidence_id
- `SC-07A-0014` `source:a-001`：missing_evidence_id
- `SC-07A-0015` `source:a-002`：missing_evidence_id
- `SC-07A-0016` `source:a-003`：missing_evidence_id
- `SC-07A-0017` `source:a-004`：missing_evidence_id
- `SC-07A-0018` `source:a-005`：missing_evidence_id
- `SC-07A-0019` `source:a-006`：missing_evidence_id
- `SC-07A-0020` `source:a-007`：missing_evidence_id
- `SC-07A-0021` `source:a-008`：missing_evidence_id
- `SC-07A-0022` `source:a-009`：missing_evidence_id
- `SC-07A-0023` `source:a-010`：missing_evidence_id
- `SC-07A-0024` `source:b-001`：missing_evidence_id
- `SC-07A-0025` `source:b-002`：missing_evidence_id
- `SC-07A-0026` `source:b-003`：missing_evidence_id
- `SC-07A-0027` `source:b-004`：missing_evidence_id
- `SC-07A-0028` `source:b-005`：missing_evidence_id
- `SC-07A-0029` `source:b-008`：missing_evidence_id
- `SC-07A-0030` `source:b-009`：missing_evidence_id
- `SC-07A-0031` `source:b-010`：missing_evidence_id
- `SC-07A-0032` `source:b-011`：missing_evidence_id
- `SC-07A-0033` `source:b-012`：missing_evidence_id
- `SC-07A-0035` `organization:beijing-furniture-trade-association`：missing_evidence_id
- `SC-07A-0036` `organization:wood-industry-research-institute`：missing_evidence_id
- `SC-07A-0038` `organization:national-museum-of-china`：missing_evidence_id
- `SC-07A-0039` `boundary:no-brand-org-equivalence`：publication_safety_not_public_safe
- `SC-07A-0042` `boundary:no-style-as-date`：evidence_status_not_eligible
- `SC-07A-0046` `boundary:no-official-commission`：evidence_status_not_eligible
- `SC-07A-0047` `boundary:no-jingzuo-identity-without-evidence`：evidence_status_not_eligible
- `SC-07A-0048` `intent:q01`：publication_safety_not_public_safe

## 审计限制

- 本报告只基于安全公开 JSON 快照和治理文档方法边界，不代表品牌官方确认。
- 本报告没有联网核验来源 URL 的当前可达性，也没有调用模型判断语义。
- `brand-graph.mmd` 只包含 source-confirmed 或 snapshot-supported 且 public-safe 的关系。
- 本阶段不生成生产 JSON-LD、RDF、页面脚本、H1、breadcrumb、canonical 或 public 下载文件。
