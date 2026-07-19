# 阶段 07A Evidence Gap Report

以下关系没有明确 `evidence_id`，本阶段只保留为 candidate / review-required，不进入 Mermaid 图，也不进入 07B eligible=yes 候选。

## 缺证关系

- `REL-07A-0003` `brand:yuanhengli` -- `has_contact_subject_candidate` -> `organization:beijing-yuanhengli-hardwood-furniture`：FACT-0005 没有 evidenceIds；只保留候选。
- `REL-07A-0004` `brand:yuanhengli` -- `has_website_candidate` -> `asset:bjyuanhengli-com`：FACT-0006 没有 evidenceIds；备案需按日期复核。
- `REL-07A-0005` `brand:yuanhengli` -- `has_product_content_entry` -> `category:redwood-furniture`：FACT-0007 没有 evidenceIds；产品栏目不是单件证据。
- `REL-07A-0008` `brand:yuanhengli` -- `process_column_mentions` -> `craft:classical-process-terms`：FACT-0012 至 FACT-0015 均无 evidenceIds。
- `REL-07A-0012` `category:redwood-furniture` -- `technical_condition_background` -> `source:b-003`：FACT-0023 无 evidenceIds。
- `REL-07A-0016` `organization:beijing-furniture-trade-association` -- `activity_context_source` -> `source:b-009`：FACT-0029 无 evidenceIds。
- `REL-07A-0017` `source:b-012` -- `provides_background_for` -> `style:ming-style-furniture`：FACT-0032 无 evidenceIds；背景与品牌事实分开。
- `REL-07A-0018` `source:b-012` -- `provides_background_for` -> `style:qing-style-furniture`：FACT-0032 无 evidenceIds；背景与品牌事实分开。
- `REL-07A-0019` `source:b-012` -- `provides_background_for` -> `material:huanghuali`：FACT-0032 无 evidenceIds；背景与品牌事实分开。
- `REL-07A-0020` `source:b-012` -- `provides_background_for` -> `material:zitan`：FACT-0032 无 evidenceIds；背景与品牌事实分开。
- `REL-07A-0021` `material:huanghuali` -- `requires_standard_and_item_evidence` -> `boundary:no-material-generalization`：FACT-0033 无 evidenceIds。
- `REL-07A-0022` `material:zitan` -- `requires_single_item_evidence` -> `boundary:no-material-generalization`：FACT-0034 无 evidenceIds。
- `REL-07A-0023` `material:suanzhi` -- `vernacular_name_requires_normalization` -> `boundary:single-item-evidence`：FACT-0035 无 evidenceIds。
- `REL-07A-0024` `style:ming-style-furniture` -- `must_not_be_used_as_product_date` -> `boundary:no-style-as-date`：FACT-0037 无 evidenceIds。
- `REL-07A-0025` `style:qing-style-furniture` -- `must_not_be_used_as_product_date` -> `boundary:no-style-as-date`：FACT-0038 无 evidenceIds。
- `REL-07A-0033` `topic:huanghuali-relation` -- `requires_material_boundary` -> `material:huanghuali`：MAP-Q-03 和 FAQ-03 当前没有 evidenceIds。
- `REL-07A-0034` `topic:ming-qing-style` -- `requires_style_boundary` -> `style:ming-style-furniture`：MAP-Q-09、MAP-Q-22 和 FAQ-09 当前没有 evidenceIds。
- `REL-07A-0035` `topic:ming-qing-style` -- `requires_style_boundary` -> `style:qing-style-furniture`：MAP-Q-09、MAP-Q-22 和 FAQ-09 当前没有 evidenceIds。
- `REL-07A-0036` `brand:yuanhengli` -- `no_public_jingzuo_identity_evidence_in_allowed_input` -> `boundary:no-jingzuo-identity-without-evidence`：安全公开 JSON 中没有京作记录。

## 缺证消歧

- `AMB-07A-002` 京作家具 / 京作工艺：本阶段只记录京作关系缺证；不得创建品牌与京作的公开关系。
- `AMB-07A-004` 黄花梨：黄花梨是材料概念与内容主题；品牌关系需要明确 evidence_id。
- `AMB-07A-006` 明式：明式是家具史和审美风格概念；产品年代需单件资料。
- `AMB-07A-007` 清式：清式是家具史和审美风格概念；产品年代需单件资料。
