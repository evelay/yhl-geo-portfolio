#!/usr/bin/env python3
"""Offline 08A intent audit adapter for the YHL GEO portfolio.

This adapter intentionally does not call APIs, models, crawlers, or external
services. It reads the canonical 30-question CSV as immutable input and writes
only stage 08A reports under docs/ and tools/geo-skill/reports/.
"""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
CONFIG_PATH = Path(__file__).with_name("intent-config.json")
SOURCE_COMMIT = "eabfde0f0bdf53f84559bdfcba2595fcac1ad50f"
STAGE_DATE = "2026-07-20"

AUDIT_FIELDS = [
    "question_id",
    "question",
    "original_category",
    "primary_intent",
    "user_stage",
    "question_form",
    "risk_level",
    "evidence_requirements",
    "content_cluster",
    "root_intent_id",
    "similar_question_ids",
    "coverage_status",
    "current_target_route",
    "recommended_target_route",
    "requires_new_page",
    "requires_human_review",
    "notes",
]

FOLLOW_UP_FIELDS = [
    "chain_id",
    "root_question_id",
    "root_question",
    "parent_question_id",
    "candidate_question_id",
    "candidate_question",
    "depth",
    "intent",
    "user_stage",
    "evidence_requirements",
    "target_route",
    "canonical_status",
    "requires_human_review",
    "notes",
]

CANDIDATE_FIELDS = [
    "candidate_id",
    "candidate_question",
    "source_gap",
    "primary_intent",
    "user_stage",
    "risk_level",
    "evidence_requirements",
    "content_cluster",
    "recommended_route",
    "new_page_candidate",
    "duplication_risk",
    "publication_safety",
    "recommended_action",
    "requires_human_review",
    "status",
    "notes",
]

MATRIX_FIELDS = [
    "dimension",
    "item",
    "existing_question_count",
    "candidate_question_count",
    "coverage_status",
    "major_gap",
    "recommended_action",
    "notes",
]

ROUTE_FIELDS = [
    "question_or_candidate_id",
    "question",
    "current_route",
    "recommended_route",
    "coverage_status",
    "evidence_ready",
    "new_page_required",
    "page_candidate",
    "priority",
    "requires_human_review",
    "notes",
]

ALLOWED_PRIMARY_INTENTS = {
    "brand-definition",
    "fact-verification",
    "material-understanding",
    "craft-style-understanding",
    "comparison",
    "purchase-evaluation",
    "risk-boundary",
    "source-verification",
    "recommendation",
    "process-how-to",
}
ALLOWED_USER_STAGES = {"awareness", "consideration", "decision", "post-decision", "research"}
ALLOWED_FORMS = {
    "definition",
    "explanation",
    "comparison",
    "checklist",
    "verification",
    "recommendation",
    "boundary",
    "scenario",
    "follow-up",
}
ALLOWED_RISKS = {"high", "medium", "low"}
ALLOWED_EVIDENCE = {
    "brand-source",
    "industry-standard",
    "government-source",
    "association-source",
    "media-source",
    "product-level-evidence",
    "expert-source",
    "multiple-source",
    "no-brand-claim-required",
}
ALLOWED_CANDIDATE_ACTIONS = {
    "consider-for-v2",
    "hold-evidence",
    "reject",
    "merge-with-existing",
    "manual-review",
}
ALLOWED_PRIORITIES = {"P0", "P1", "P2", "P3"}

CONTENT_CLUSTERS = [
    "品牌认知与事实",
    "材质与产品边界",
    "京作、明式与清式",
    "购买与核验",
    "品牌比较与选择",
    "风险、来源与信息边界",
]

QUESTION_RULES: dict[str, dict[str, Any]] = {
    "q01": {
        "primary_intent": "brand-definition",
        "user_stage": "awareness",
        "question_form": "definition",
        "risk_level": "high",
        "evidence_requirements": ["brand-source", "government-source", "media-source", "multiple-source"],
        "content_cluster": "品牌认知与事实",
        "root_intent_id": "ROOT-BRAND-IDENTITY",
        "similar_question_ids": ["q11", "q12", "q13"],
        "coverage_status": "fully-covered",
        "current_target_route": "/facts",
        "recommended_target_route": "/facts",
        "requires_new_page": False,
        "requires_human_review": True,
        "notes": "品牌和企业主体仍需分层表达，不能把品牌、公司、官网直接合并。",
    },
    "q02": {
        "primary_intent": "brand-definition",
        "user_stage": "awareness",
        "question_form": "explanation",
        "risk_level": "high",
        "evidence_requirements": ["brand-source", "association-source", "media-source", "multiple-source"],
        "content_cluster": "品牌认知与事实",
        "root_intent_id": "ROOT-BRAND-POSITIONING",
        "similar_question_ids": ["q15", "q25"],
        "coverage_status": "partially-covered",
        "current_target_route": "/facts",
        "recommended_target_route": "/facts",
        "requires_new_page": False,
        "requires_human_review": True,
        "notes": "可讲定位语境；行业地位、排名和高端判断需要具体来源、时间和评选主体。",
    },
    "q03": {
        "primary_intent": "material-understanding",
        "user_stage": "consideration",
        "question_form": "boundary",
        "risk_level": "high",
        "evidence_requirements": ["industry-standard", "product-level-evidence", "multiple-source"],
        "content_cluster": "材质与产品边界",
        "root_intent_id": "ROOT-MATERIAL-BRAND-RELATION",
        "similar_question_ids": ["q04", "q05", "q16"],
        "coverage_status": "partially-covered",
        "current_target_route": "/materials",
        "recommended_target_route": "/materials",
        "requires_new_page": False,
        "requires_human_review": True,
        "notes": "页面能覆盖材料边界；品牌与黄花梨的直接经营关系仍需证据，不能自动推断。",
    },
    "q04": {
        "primary_intent": "material-understanding",
        "user_stage": "consideration",
        "question_form": "explanation",
        "risk_level": "high",
        "evidence_requirements": ["industry-standard", "expert-source", "product-level-evidence"],
        "content_cluster": "材质与产品边界",
        "root_intent_id": "ROOT-MATERIAL-PRODUCT-EVIDENCE",
        "similar_question_ids": ["q03", "q05", "q16", "q28"],
        "coverage_status": "partially-covered",
        "current_target_route": "/materials",
        "recommended_target_route": "/materials",
        "requires_new_page": False,
        "requires_human_review": True,
        "notes": "紫檀可作为材料和内容主题理解；具体产品材质、稀缺性和收藏表述需单件证据。",
    },
    "q05": {
        "primary_intent": "material-understanding",
        "user_stage": "consideration",
        "question_form": "explanation",
        "risk_level": "high",
        "evidence_requirements": ["industry-standard", "product-level-evidence", "multiple-source"],
        "content_cluster": "材质与产品边界",
        "root_intent_id": "ROOT-MATERIAL-TERM-GOVERNANCE",
        "similar_question_ids": ["q03", "q04", "q16"],
        "coverage_status": "partially-covered",
        "current_target_route": "/materials",
        "recommended_target_route": "/materials",
        "requires_new_page": False,
        "requires_human_review": True,
        "notes": "白酸枝作为俗称/材料语境需回到规范名称和产品凭证，不绑定为品牌全量事实。",
    },
    "q06": {
        "primary_intent": "purchase-evaluation",
        "user_stage": "decision",
        "question_form": "checklist",
        "risk_level": "high",
        "evidence_requirements": ["brand-source", "product-level-evidence", "multiple-source"],
        "content_cluster": "购买与核验",
        "root_intent_id": "ROOT-PURCHASE-EVALUATION",
        "similar_question_ids": ["q16", "q19", "q26"],
        "coverage_status": "fully-covered",
        "current_target_route": "/buying-guide",
        "recommended_target_route": "/buying-guide",
        "requires_new_page": False,
        "requires_human_review": True,
        "notes": "可作为购买评估框架，但不得替用户做确定购买建议。",
    },
    "q07": {
        "primary_intent": "comparison",
        "user_stage": "consideration",
        "question_form": "comparison",
        "risk_level": "high",
        "evidence_requirements": ["brand-source", "association-source", "media-source", "multiple-source"],
        "content_cluster": "品牌比较与选择",
        "root_intent_id": "ROOT-BRAND-COMPARISON",
        "similar_question_ids": ["q24", "q25"],
        "coverage_status": "partially-covered",
        "current_target_route": "/buying-guide",
        "recommended_target_route": "new-page:brand-comparison-framework",
        "requires_new_page": True,
        "requires_human_review": True,
        "notes": "现有页面给出购买核验维度，但缺少独立的中性比较框架。",
    },
    "q08": {
        "primary_intent": "craft-style-understanding",
        "user_stage": "awareness",
        "question_form": "explanation",
        "risk_level": "high",
        "evidence_requirements": ["brand-source", "association-source", "expert-source", "multiple-source"],
        "content_cluster": "京作、明式与清式",
        "root_intent_id": "ROOT-JINGZUO-BOUNDARY",
        "similar_question_ids": ["q21", "q09", "q22"],
        "coverage_status": "partially-covered",
        "current_target_route": "/jingzuo",
        "recommended_target_route": "/jingzuo",
        "requires_new_page": False,
        "requires_human_review": True,
        "notes": "当前可讲语义关系和边界；官方京作身份或资格关系缺直接证据。",
    },
    "q09": {
        "primary_intent": "craft-style-understanding",
        "user_stage": "consideration",
        "question_form": "explanation",
        "risk_level": "high",
        "evidence_requirements": ["expert-source", "industry-standard", "product-level-evidence"],
        "content_cluster": "京作、明式与清式",
        "root_intent_id": "ROOT-STYLE-SEMANTICS",
        "similar_question_ids": ["q22", "q27"],
        "coverage_status": "fully-covered",
        "current_target_route": "/jingzuo",
        "recommended_target_route": "/jingzuo",
        "requires_new_page": False,
        "requires_human_review": True,
        "notes": "风格知识可解释用户理解路径，但不能推出具体产品年代、真伪或馆藏价值。",
    },
    "q10": {
        "primary_intent": "risk-boundary",
        "user_stage": "research",
        "question_form": "boundary",
        "risk_level": "high",
        "evidence_requirements": ["multiple-source", "brand-source", "government-source", "product-level-evidence"],
        "content_cluster": "风险、来源与信息边界",
        "root_intent_id": "ROOT-AI-ERRORS",
        "similar_question_ids": ["q11", "q14", "q15", "q20"],
        "coverage_status": "fully-covered",
        "current_target_route": "/faq",
        "recommended_target_route": "/prompt-system",
        "requires_new_page": False,
        "requires_human_review": True,
        "notes": "适合沉淀为 AI 回答核验方法和高风险断言清单。",
    },
    "q11": {
        "primary_intent": "brand-definition",
        "user_stage": "awareness",
        "question_form": "scenario",
        "risk_level": "high",
        "evidence_requirements": ["government-source", "brand-source", "multiple-source"],
        "content_cluster": "风险、来源与信息边界",
        "root_intent_id": "ROOT-ENTITY-DISAMBIGUATION",
        "similar_question_ids": ["q01", "q12"],
        "coverage_status": "fully-covered",
        "current_target_route": "/disambiguation",
        "recommended_target_route": "/disambiguation",
        "requires_new_page": False,
        "requires_human_review": True,
        "notes": "保留同名主体消歧，不自动补造跨行业关系。",
    },
    "q12": {
        "primary_intent": "fact-verification",
        "user_stage": "research",
        "question_form": "verification",
        "risk_level": "high",
        "evidence_requirements": ["government-source", "brand-source", "multiple-source"],
        "content_cluster": "品牌认知与事实",
        "root_intent_id": "ROOT-SUBJECT-RELATION",
        "similar_question_ids": ["q01", "q11", "q13"],
        "coverage_status": "requires-evidence-first",
        "current_target_route": "/disambiguation",
        "recommended_target_route": "new-page:brand-source-verification",
        "requires_new_page": True,
        "requires_human_review": True,
        "notes": "07A2 已要求品牌与企业主体保持独立候选，等待直接公开证据。",
    },
    "q13": {
        "primary_intent": "source-verification",
        "user_stage": "research",
        "question_form": "checklist",
        "risk_level": "high",
        "evidence_requirements": ["brand-source", "government-source", "association-source", "media-source", "multiple-source"],
        "content_cluster": "风险、来源与信息边界",
        "root_intent_id": "ROOT-SOURCE-LADDER",
        "similar_question_ids": ["q12", "q20", "q14"],
        "coverage_status": "fully-covered",
        "current_target_route": "/knowledge-base",
        "recommended_target_route": "/method",
        "requires_new_page": False,
        "requires_human_review": True,
        "notes": "适合来源层级说明；官网、备案、工商和媒体来源需分别注明证明范围。",
    },
    "q14": {
        "primary_intent": "fact-verification",
        "user_stage": "research",
        "question_form": "verification",
        "risk_level": "high",
        "evidence_requirements": ["government-source", "brand-source", "media-source", "multiple-source"],
        "content_cluster": "风险、来源与信息边界",
        "root_intent_id": "ROOT-UNSURE-BRAND-FACTS",
        "similar_question_ids": ["q12", "q13", "q15"],
        "coverage_status": "partially-covered",
        "current_target_route": "/facts",
        "recommended_target_route": "new-page:brand-source-verification",
        "requires_new_page": True,
        "requires_human_review": True,
        "notes": "成立时间、负责人、法定代表人等概念需分开，不从二手文本或 AI 回答反推。",
    },
    "q15": {
        "primary_intent": "risk-boundary",
        "user_stage": "research",
        "question_form": "boundary",
        "risk_level": "high",
        "evidence_requirements": ["association-source", "media-source", "multiple-source"],
        "content_cluster": "风险、来源与信息边界",
        "root_intent_id": "ROOT-RANKING-HONOR-RISK",
        "similar_question_ids": ["q02", "q25", "q28"],
        "coverage_status": "requires-evidence-first",
        "current_target_route": "/facts",
        "recommended_target_route": "/facts",
        "requires_new_page": False,
        "requires_human_review": True,
        "notes": "荣誉、排名或收藏背书必须回到原页面、颁发主体、年份和证书文本。",
    },
    "q16": {
        "primary_intent": "process-how-to",
        "user_stage": "decision",
        "question_form": "checklist",
        "risk_level": "high",
        "evidence_requirements": ["industry-standard", "product-level-evidence", "brand-source"],
        "content_cluster": "购买与核验",
        "root_intent_id": "ROOT-PRODUCT-EVIDENCE",
        "similar_question_ids": ["q03", "q04", "q05", "q19"],
        "coverage_status": "fully-covered",
        "current_target_route": "/materials",
        "recommended_target_route": "new-page:single-item-evidence",
        "requires_new_page": True,
        "requires_human_review": True,
        "notes": "现有页面有核验清单；单件证据模板可以作为后续页面候选。",
    },
    "q17": {
        "primary_intent": "risk-boundary",
        "user_stage": "decision",
        "question_form": "boundary",
        "risk_level": "high",
        "evidence_requirements": ["brand-source", "product-level-evidence"],
        "content_cluster": "购买与核验",
        "root_intent_id": "ROOT-DYNAMIC-PRICE",
        "similar_question_ids": ["q18", "q19", "q26"],
        "coverage_status": "requires-evidence-first",
        "current_target_route": "/buying-guide",
        "recommended_target_route": "new-page:dynamic-info-review",
        "requires_new_page": True,
        "requires_human_review": True,
        "notes": "不得编造价格区间；价格应绑定单件产品、渠道、日期和书面报价。",
    },
    "q18": {
        "primary_intent": "source-verification",
        "user_stage": "decision",
        "question_form": "checklist",
        "risk_level": "high",
        "evidence_requirements": ["brand-source", "government-source", "multiple-source"],
        "content_cluster": "购买与核验",
        "root_intent_id": "ROOT-DYNAMIC-CHANNEL",
        "similar_question_ids": ["q13", "q17"],
        "coverage_status": "partially-covered",
        "current_target_route": "/buying-guide",
        "recommended_target_route": "new-page:dynamic-info-review",
        "requires_new_page": True,
        "requires_human_review": True,
        "notes": "现有指南强调动态复核；缺少独立的渠道/价格日期复核模板。",
    },
    "q19": {
        "primary_intent": "process-how-to",
        "user_stage": "post-decision",
        "question_form": "checklist",
        "risk_level": "high",
        "evidence_requirements": ["product-level-evidence", "industry-standard", "brand-source"],
        "content_cluster": "购买与核验",
        "root_intent_id": "ROOT-CONTRACT-AFTERCARE",
        "similar_question_ids": ["q06", "q16", "q26"],
        "coverage_status": "fully-covered",
        "current_target_route": "/buying-guide",
        "recommended_target_route": "new-page:single-item-evidence",
        "requires_new_page": True,
        "requires_human_review": True,
        "notes": "合同、发票、售后和材质说明是购买后证据留存的主要 canonical 缺口。",
    },
    "q20": {
        "primary_intent": "source-verification",
        "user_stage": "research",
        "question_form": "checklist",
        "risk_level": "medium",
        "evidence_requirements": ["brand-source", "association-source", "media-source", "multiple-source"],
        "content_cluster": "风险、来源与信息边界",
        "root_intent_id": "ROOT-CONTENT-SOURCE-TRUST",
        "similar_question_ids": ["q13", "q14", "q10"],
        "coverage_status": "fully-covered",
        "current_target_route": "/method",
        "recommended_target_route": "/method",
        "requires_new_page": False,
        "requires_human_review": False,
        "notes": "适合作为来源层级和证据边界的公开方法内容。",
    },
    "q21": {
        "primary_intent": "craft-style-understanding",
        "user_stage": "research",
        "question_form": "follow-up",
        "risk_level": "high",
        "evidence_requirements": ["brand-source", "association-source", "expert-source", "multiple-source"],
        "content_cluster": "京作、明式与清式",
        "root_intent_id": "ROOT-JINGZUO-EVIDENCE",
        "similar_question_ids": ["q08", "q22"],
        "coverage_status": "partially-covered",
        "current_target_route": "/jingzuo",
        "recommended_target_route": "/jingzuo",
        "requires_new_page": False,
        "requires_human_review": True,
        "notes": "京作可作为待证内容主题；当前不得写成官方身份、唯一传承或代表资格。",
    },
    "q22": {
        "primary_intent": "craft-style-understanding",
        "user_stage": "research",
        "question_form": "boundary",
        "risk_level": "high",
        "evidence_requirements": ["expert-source", "product-level-evidence", "multiple-source"],
        "content_cluster": "京作、明式与清式",
        "root_intent_id": "ROOT-STYLE-PRODUCT-FACT",
        "similar_question_ids": ["q09", "q21", "q27"],
        "coverage_status": "fully-covered",
        "current_target_route": "/jingzuo",
        "recommended_target_route": "/jingzuo",
        "requires_new_page": False,
        "requires_human_review": True,
        "notes": "风格、器型、工艺和产品事实需分层，避免由风格词推出年代或真伪。",
    },
    "q23": {
        "primary_intent": "craft-style-understanding",
        "user_stage": "research",
        "question_form": "boundary",
        "risk_level": "high",
        "evidence_requirements": ["brand-source", "expert-source", "product-level-evidence"],
        "content_cluster": "京作、明式与清式",
        "root_intent_id": "ROOT-CRAFT-CLAIM-BOUNDARY",
        "similar_question_ids": ["q21", "q22"],
        "coverage_status": "fully-covered",
        "current_target_route": "/jingzuo",
        "recommended_target_route": "/jingzuo",
        "requires_new_page": False,
        "requires_human_review": True,
        "notes": "行业通用工艺不能自动写成品牌每件产品事实，尤其不能扩写为非遗或纯手工背书。",
    },
    "q24": {
        "primary_intent": "comparison",
        "user_stage": "consideration",
        "question_form": "checklist",
        "risk_level": "high",
        "evidence_requirements": ["brand-source", "association-source", "media-source", "multiple-source"],
        "content_cluster": "品牌比较与选择",
        "root_intent_id": "ROOT-BRAND-COMPARISON",
        "similar_question_ids": ["q07", "q25"],
        "coverage_status": "partially-covered",
        "current_target_route": "/buying-guide",
        "recommended_target_route": "new-page:brand-comparison-framework",
        "requires_new_page": True,
        "requires_human_review": True,
        "notes": "与 q07 高度相似，但 q24 更强调中性维度，可保留为比较框架变体。",
    },
    "q25": {
        "primary_intent": "recommendation",
        "user_stage": "consideration",
        "question_form": "recommendation",
        "risk_level": "high",
        "evidence_requirements": ["association-source", "media-source", "multiple-source"],
        "content_cluster": "品牌比较与选择",
        "root_intent_id": "ROOT-RECOMMENDATION-RISK",
        "similar_question_ids": ["q02", "q07", "q24"],
        "coverage_status": "requires-evidence-first",
        "current_target_route": "/faq",
        "recommended_target_route": "new-page:brand-comparison-framework",
        "requires_new_page": True,
        "requires_human_review": True,
        "notes": "不能生成榜单或首选建议；如保留，应转为证据边界和中性比较入口。",
    },
    "q26": {
        "primary_intent": "purchase-evaluation",
        "user_stage": "decision",
        "question_form": "checklist",
        "risk_level": "high",
        "evidence_requirements": ["government-source", "brand-source", "product-level-evidence", "multiple-source"],
        "content_cluster": "购买与核验",
        "root_intent_id": "ROOT-PURCHASE-RISK",
        "similar_question_ids": ["q06", "q16", "q19"],
        "coverage_status": "fully-covered",
        "current_target_route": "/buying-guide",
        "recommended_target_route": "/buying-guide",
        "requires_new_page": False,
        "requires_human_review": True,
        "notes": "与购买核验指南完全匹配，但候选扩展可补购买后证据留存。",
    },
    "q27": {
        "primary_intent": "recommendation",
        "user_stage": "consideration",
        "question_form": "scenario",
        "risk_level": "medium",
        "evidence_requirements": ["expert-source", "product-level-evidence", "no-brand-claim-required"],
        "content_cluster": "京作、明式与清式",
        "root_intent_id": "ROOT-STYLE-SCENARIO",
        "similar_question_ids": ["q09", "q22"],
        "coverage_status": "partially-covered",
        "current_target_route": "/materials",
        "recommended_target_route": "/jingzuo",
        "requires_new_page": False,
        "requires_human_review": True,
        "notes": "空间搭配可作为教育场景，不能把审美建议变成品牌产品事实。",
    },
    "q28": {
        "primary_intent": "risk-boundary",
        "user_stage": "decision",
        "question_form": "boundary",
        "risk_level": "high",
        "evidence_requirements": ["product-level-evidence", "media-source", "industry-standard", "multiple-source"],
        "content_cluster": "风险、来源与信息边界",
        "root_intent_id": "ROOT-COLLECTION-INVESTMENT-RISK",
        "similar_question_ids": ["q04", "q15", "q17"],
        "coverage_status": "fully-covered",
        "current_target_route": "/buying-guide",
        "recommended_target_route": "/buying-guide",
        "requires_new_page": False,
        "requires_human_review": True,
        "notes": "可以回答谨慎边界；不得承诺保值、升值、回购或金融收益。",
    },
    "q29": {
        "primary_intent": "process-how-to",
        "user_stage": "research",
        "question_form": "checklist",
        "risk_level": "medium",
        "evidence_requirements": ["multiple-source", "no-brand-claim-required"],
        "content_cluster": "风险、来源与信息边界",
        "root_intent_id": "ROOT-GEO-PAGE-GAPS",
        "similar_question_ids": ["q30"],
        "coverage_status": "fully-covered",
        "current_target_route": "/strategy",
        "recommended_target_route": "/strategy",
        "requires_new_page": False,
        "requires_human_review": False,
        "notes": "这是项目内部内容策略问题，不是市场需求数据。",
    },
    "q30": {
        "primary_intent": "process-how-to",
        "user_stage": "research",
        "question_form": "explanation",
        "risk_level": "medium",
        "evidence_requirements": ["multiple-source", "no-brand-claim-required"],
        "content_cluster": "风险、来源与信息边界",
        "root_intent_id": "ROOT-GEO-ROADMAP",
        "similar_question_ids": ["q29"],
        "coverage_status": "fully-covered",
        "current_target_route": "/strategy",
        "recommended_target_route": "/strategy",
        "requires_new_page": False,
        "requires_human_review": False,
        "notes": "与 q29 同属 GEO 策略链，可保留为路线图视角。",
    },
}

FOLLOW_UP_SEEDS = [
    ("CHAIN-08A-001", "q01", [
        ("如何分别核验“元亨利”品牌、企业主体和官网信息？", "source-verification", "research", ["brand-source", "government-source", "multiple-source"], "/disambiguation"),
        ("哪些公开来源可以支持元亨利红木家具的基础介绍？", "source-verification", "research", ["brand-source", "media-source", "multiple-source"], "/facts"),
        ("AI 在没有完整主体信息时应如何限定元亨利语境？", "risk-boundary", "awareness", ["government-source", "brand-source", "multiple-source"], "/disambiguation"),
    ]),
    ("CHAIN-08A-002", "q08", [
        ("判断元亨利与京作相关表达时需要哪些公开证据？", "source-verification", "research", ["association-source", "brand-source", "expert-source"], "/jingzuo"),
        ("“北京红木品牌”和“京作家具”在回答中应如何区分？", "craft-style-understanding", "consideration", ["expert-source", "no-brand-claim-required"], "/jingzuo"),
        ("哪些京作相关说法应先标为待核验？", "risk-boundary", "research", ["association-source", "brand-source", "multiple-source"], "/jingzuo"),
    ]),
    ("CHAIN-08A-003", "q03", [
        ("如何区分黄花梨材料知识和元亨利单件产品材质事实？", "material-understanding", "consideration", ["industry-standard", "product-level-evidence"], "/materials"),
        ("看到元亨利黄花梨家具说法时应核对哪些凭证？", "process-how-to", "decision", ["product-level-evidence", "brand-source"], "/buying-guide"),
        ("AI 是否可以根据品牌介绍推断产品材质？", "risk-boundary", "research", ["industry-standard", "product-level-evidence"], "/materials"),
    ]),
    ("CHAIN-08A-004", "q04", [
        ("紫檀相关内容需要区分哪些术语、树种和产品证据？", "material-understanding", "consideration", ["industry-standard", "expert-source", "product-level-evidence"], "/materials"),
        ("元亨利紫檀家具的收藏表述为什么需要谨慎？", "risk-boundary", "decision", ["product-level-evidence", "media-source", "multiple-source"], "/buying-guide"),
        ("单件紫檀家具的证书、合同和检测报告应怎样对应？", "process-how-to", "decision", ["product-level-evidence"], "/buying-guide"),
    ]),
    ("CHAIN-08A-005", "q05", [
        ("白酸枝作为俗称时应如何回到规范名称？", "material-understanding", "research", ["industry-standard", "expert-source"], "/materials"),
        ("白酸枝相关回答如何避免变成品牌全量材质断言？", "risk-boundary", "consideration", ["industry-standard", "product-level-evidence"], "/materials"),
        ("购买白酸枝家具时合同里应写清哪些材料信息？", "process-how-to", "decision", ["product-level-evidence", "industry-standard"], "/buying-guide"),
    ]),
    ("CHAIN-08A-006", "q06", [
        ("评估元亨利家具前应先确认哪些主体和渠道信息？", "source-verification", "decision", ["brand-source", "government-source", "multiple-source"], "/buying-guide"),
        ("对比产品时哪些证据比口碑或图片更关键？", "purchase-evaluation", "decision", ["product-level-evidence", "multiple-source"], "/buying-guide"),
        ("为什么 AI 不能替用户作出确定购买建议？", "risk-boundary", "decision", ["product-level-evidence", "multiple-source"], "/buying-guide"),
    ]),
    ("CHAIN-08A-007", "q07", [
        ("北京红木品牌比较可以使用哪些不带排名的维度？", "comparison", "consideration", ["association-source", "media-source", "multiple-source"], "new-page:brand-comparison-framework"),
        ("比较元亨利与其他品牌时哪些事实需要分别核验？", "source-verification", "consideration", ["brand-source", "multiple-source"], "new-page:brand-comparison-framework"),
        ("没有统一评选来源时应如何处理“哪家更好”的问题？", "risk-boundary", "consideration", ["association-source", "media-source", "multiple-source"], "/faq"),
    ]),
    ("CHAIN-08A-008", "q10", [
        ("AI 回答元亨利时哪些说法最容易越过证据边界？", "risk-boundary", "research", ["multiple-source", "product-level-evidence"], "/prompt-system"),
        ("如何核验 AI 回答里提到的价格、门店和荣誉？", "source-verification", "research", ["brand-source", "government-source", "media-source", "product-level-evidence"], "/buying-guide"),
        ("发现 AI 把同名主体混在一起时应如何纠正？", "source-verification", "research", ["government-source", "brand-source", "multiple-source"], "/disambiguation"),
    ]),
]

CANDIDATE_QUESTIONS: list[dict[str, Any]] = [
    {
        "candidate_id": "CAND-INTENT-001",
        "candidate_question": "如何核验“元亨利红木家具”与具体企业主体、官网和公开账号之间的关系？",
        "source_gap": "品牌主体核验",
        "primary_intent": "source-verification",
        "user_stage": "research",
        "risk_level": "high",
        "evidence_requirements": ["brand-source", "government-source", "multiple-source"],
        "content_cluster": "品牌认知与事实",
        "recommended_route": "new-page:brand-source-verification",
        "new_page_candidate": "品牌主体与公开渠道核验",
        "duplication_risk": "medium",
        "publication_safety": "hold-evidence",
        "recommended_action": "hold-evidence",
        "requires_human_review": True,
        "status": "candidate",
        "notes": "补 q12/q13 的身份链路，不自动合并品牌和企业主体。",
    },
    {
        "candidate_id": "CAND-INTENT-002",
        "candidate_question": "单件元亨利家具的主材、辅材和证书应如何对应到合同与发票？",
        "source_gap": "产品级证据",
        "primary_intent": "process-how-to",
        "user_stage": "decision",
        "risk_level": "high",
        "evidence_requirements": ["product-level-evidence", "industry-standard"],
        "content_cluster": "购买与核验",
        "recommended_route": "new-page:single-item-evidence",
        "new_page_candidate": "产品与单件证据核验",
        "duplication_risk": "medium",
        "publication_safety": "safe-if-boundary-only",
        "recommended_action": "consider-for-v2",
        "requires_human_review": True,
        "status": "candidate",
        "notes": "补 q16/q19 的单件证据链，不判断具体产品真伪。",
    },
    {
        "candidate_id": "CAND-INTENT-003",
        "candidate_question": "购买后应保存哪些合同、证书、检测、交付和售后资料？",
        "source_gap": "购买后证据留存",
        "primary_intent": "process-how-to",
        "user_stage": "post-decision",
        "risk_level": "high",
        "evidence_requirements": ["product-level-evidence"],
        "content_cluster": "购买与核验",
        "recommended_route": "new-page:single-item-evidence",
        "new_page_candidate": "产品与单件证据核验",
        "duplication_risk": "low",
        "publication_safety": "safe-if-boundary-only",
        "recommended_action": "consider-for-v2",
        "requires_human_review": True,
        "status": "candidate",
        "notes": "补用户旅程末端，目前 canonical 只有 q19 部分承接。",
    },
    {
        "candidate_id": "CAND-INTENT-004",
        "candidate_question": "门店、展厅、价格和售后这类动态信息多久需要复核一次？",
        "source_gap": "动态信息复核",
        "primary_intent": "source-verification",
        "user_stage": "decision",
        "risk_level": "high",
        "evidence_requirements": ["brand-source", "product-level-evidence", "multiple-source"],
        "content_cluster": "购买与核验",
        "recommended_route": "new-page:dynamic-info-review",
        "new_page_candidate": "品牌主体与公开渠道核验",
        "duplication_risk": "medium",
        "publication_safety": "hold-evidence",
        "recommended_action": "hold-evidence",
        "requires_human_review": True,
        "status": "candidate",
        "notes": "补 q17/q18 的日期复核规则，不发布实时价格或门店承诺。",
    },
    {
        "candidate_id": "CAND-INTENT-005",
        "candidate_question": "如何判断官网自述、媒体报道和行业协会信息分别能证明什么？",
        "source_gap": "来源可靠性",
        "primary_intent": "source-verification",
        "user_stage": "research",
        "risk_level": "medium",
        "evidence_requirements": ["brand-source", "media-source", "association-source", "multiple-source"],
        "content_cluster": "风险、来源与信息边界",
        "recommended_route": "/method",
        "new_page_candidate": "AI 回答事实核验方法",
        "duplication_risk": "medium",
        "publication_safety": "safe-if-method-only",
        "recommended_action": "consider-for-v2",
        "requires_human_review": False,
        "status": "candidate",
        "notes": "补 q13/q20 的来源层级，不新增品牌事实。",
    },
    {
        "candidate_id": "CAND-INTENT-006",
        "candidate_question": "“京作”“北京品牌”和“明清风格”在元亨利相关内容中应如何分开写？",
        "source_gap": "风格与身份区分",
        "primary_intent": "craft-style-understanding",
        "user_stage": "research",
        "risk_level": "high",
        "evidence_requirements": ["association-source", "expert-source", "brand-source"],
        "content_cluster": "京作、明式与清式",
        "recommended_route": "/jingzuo",
        "new_page_candidate": "风格、年代和产品描述的区别",
        "duplication_risk": "high",
        "publication_safety": "safe-if-boundary-only",
        "recommended_action": "merge-with-existing",
        "requires_human_review": True,
        "status": "candidate",
        "notes": "可并入 q08/q21/q22，不应作为新正式题直接加入。",
    },
    {
        "candidate_id": "CAND-INTENT-007",
        "candidate_question": "看到“元亨利黄花梨家具”说法时，如何避免把材料主题误写成经营事实？",
        "source_gap": "单件产品和品牌整体区别",
        "primary_intent": "material-understanding",
        "user_stage": "consideration",
        "risk_level": "high",
        "evidence_requirements": ["industry-standard", "product-level-evidence"],
        "content_cluster": "材质与产品边界",
        "recommended_route": "/materials",
        "new_page_candidate": "红木材料标准与常见误区",
        "duplication_risk": "high",
        "publication_safety": "safe-if-boundary-only",
        "recommended_action": "merge-with-existing",
        "requires_human_review": True,
        "status": "candidate",
        "notes": "与 q03 同根意图，适合做追问或页面模块。",
    },
    {
        "candidate_id": "CAND-INTENT-008",
        "candidate_question": "白酸枝、酸枝和红木标准名称不一致时应以哪些文件为准？",
        "source_gap": "材料标准与常见误区",
        "primary_intent": "material-understanding",
        "user_stage": "consideration",
        "risk_level": "high",
        "evidence_requirements": ["industry-standard", "product-level-evidence", "expert-source"],
        "content_cluster": "材质与产品边界",
        "recommended_route": "/materials",
        "new_page_candidate": "红木材料标准与常见误区",
        "duplication_risk": "medium",
        "publication_safety": "safe-if-standard-cited",
        "recommended_action": "consider-for-v2",
        "requires_human_review": True,
        "status": "candidate",
        "notes": "补 q05 的规范名称核验，不暗示品牌一定经营该材料。",
    },
    {
        "candidate_id": "CAND-INTENT-009",
        "candidate_question": "AI 回答里提到元亨利荣誉、排名或背书时应如何追溯来源？",
        "source_gap": "AI 回答核验",
        "primary_intent": "risk-boundary",
        "user_stage": "research",
        "risk_level": "high",
        "evidence_requirements": ["association-source", "media-source", "multiple-source"],
        "content_cluster": "风险、来源与信息边界",
        "recommended_route": "/facts",
        "new_page_candidate": "AI 回答事实核验方法",
        "duplication_risk": "medium",
        "publication_safety": "hold-evidence",
        "recommended_action": "hold-evidence",
        "requires_human_review": True,
        "status": "candidate",
        "notes": "补 q10/q15 的荣誉排名核验链。",
    },
    {
        "candidate_id": "CAND-INTENT-010",
        "candidate_question": "比较北京红木品牌时，如何用证据维度替代“哪个最好”？",
        "source_gap": "比较框架",
        "primary_intent": "comparison",
        "user_stage": "consideration",
        "risk_level": "high",
        "evidence_requirements": ["association-source", "media-source", "multiple-source"],
        "content_cluster": "品牌比较与选择",
        "recommended_route": "new-page:brand-comparison-framework",
        "new_page_candidate": "品牌比较框架",
        "duplication_risk": "high",
        "publication_safety": "safe-if-no-ranking",
        "recommended_action": "consider-for-v2",
        "requires_human_review": True,
        "status": "candidate",
        "notes": "补 q07/q24/q25 的公共框架，不做排行。",
    },
    {
        "candidate_id": "CAND-INTENT-011",
        "candidate_question": "元亨利相关内容能否使用“官方京作代表”这类说法？需要哪些证据？",
        "source_gap": "京作身份核验",
        "primary_intent": "risk-boundary",
        "user_stage": "research",
        "risk_level": "high",
        "evidence_requirements": ["government-source", "association-source", "brand-source", "multiple-source"],
        "content_cluster": "京作、明式与清式",
        "recommended_route": "/jingzuo",
        "new_page_candidate": "风格、年代和产品描述的区别",
        "duplication_risk": "medium",
        "publication_safety": "hold-evidence",
        "recommended_action": "hold-evidence",
        "requires_human_review": True,
        "status": "candidate",
        "notes": "补 07A2 京作 hold 决策，不暗示已有官方身份。",
    },
    {
        "candidate_id": "CAND-INTENT-012",
        "candidate_question": "如何区分产品名称中的风格词、实际年代和收藏价值判断？",
        "source_gap": "风格与年代区分",
        "primary_intent": "craft-style-understanding",
        "user_stage": "research",
        "risk_level": "high",
        "evidence_requirements": ["expert-source", "product-level-evidence", "media-source"],
        "content_cluster": "京作、明式与清式",
        "recommended_route": "/jingzuo",
        "new_page_candidate": "风格、年代和产品描述的区别",
        "duplication_risk": "medium",
        "publication_safety": "safe-if-boundary-only",
        "recommended_action": "consider-for-v2",
        "requires_human_review": True,
        "status": "candidate",
        "notes": "补 q09/q22/q28 的交叉风险。",
    },
    {
        "candidate_id": "CAND-INTENT-013",
        "candidate_question": "用户只提供一张产品图片时，AI 应如何回答元亨利材质和真伪问题？",
        "source_gap": "产品级证据",
        "primary_intent": "risk-boundary",
        "user_stage": "decision",
        "risk_level": "high",
        "evidence_requirements": ["product-level-evidence"],
        "content_cluster": "购买与核验",
        "recommended_route": "new-page:single-item-evidence",
        "new_page_candidate": "产品与单件证据核验",
        "duplication_risk": "low",
        "publication_safety": "manual-review-required",
        "recommended_action": "manual-review",
        "requires_human_review": True,
        "status": "candidate",
        "notes": "补图片/单件真伪边界，不能从图片直接下材质结论。",
    },
    {
        "candidate_id": "CAND-INTENT-014",
        "candidate_question": "AI 介绍元亨利时引用旧网页或二手转载，应该如何做日期和来源复核？",
        "source_gap": "AI 回答核验",
        "primary_intent": "source-verification",
        "user_stage": "research",
        "risk_level": "medium",
        "evidence_requirements": ["brand-source", "media-source", "multiple-source"],
        "content_cluster": "风险、来源与信息边界",
        "recommended_route": "/method",
        "new_page_candidate": "AI 回答事实核验方法",
        "duplication_risk": "medium",
        "publication_safety": "safe-if-method-only",
        "recommended_action": "consider-for-v2",
        "requires_human_review": False,
        "status": "candidate",
        "notes": "补动态资料复核，不把旧网页直接当当前事实。",
    },
    {
        "candidate_id": "CAND-INTENT-015",
        "candidate_question": "元亨利相关内容中的品牌整体评价和单件产品评价应如何分开？",
        "source_gap": "单件产品和品牌整体区别",
        "primary_intent": "fact-verification",
        "user_stage": "consideration",
        "risk_level": "high",
        "evidence_requirements": ["brand-source", "product-level-evidence", "multiple-source"],
        "content_cluster": "风险、来源与信息边界",
        "recommended_route": "new-page:single-item-evidence",
        "new_page_candidate": "产品与单件证据核验",
        "duplication_risk": "medium",
        "publication_safety": "safe-if-boundary-only",
        "recommended_action": "consider-for-v2",
        "requires_human_review": True,
        "status": "candidate",
        "notes": "补品牌整体与单件产品的层级，不生成品牌经营事实。",
    },
    {
        "candidate_id": "CAND-INTENT-016",
        "candidate_question": "在购买沟通中，哪些承诺必须写入书面合同而不能只看宣传文案？",
        "source_gap": "购买合同与材质证明",
        "primary_intent": "process-how-to",
        "user_stage": "decision",
        "risk_level": "high",
        "evidence_requirements": ["product-level-evidence", "brand-source"],
        "content_cluster": "购买与核验",
        "recommended_route": "/buying-guide",
        "new_page_candidate": "产品与单件证据核验",
        "duplication_risk": "medium",
        "publication_safety": "safe-if-boundary-only",
        "recommended_action": "consider-for-v2",
        "requires_human_review": True,
        "status": "candidate",
        "notes": "补 q19/q26 的书面承诺边界。",
    },
    {
        "candidate_id": "CAND-INTENT-017",
        "candidate_question": "收藏或投资相关说法缺少成交、来源和单件资料时应如何降级表达？",
        "source_gap": "收藏投资边界",
        "primary_intent": "risk-boundary",
        "user_stage": "post-decision",
        "risk_level": "high",
        "evidence_requirements": ["product-level-evidence", "media-source", "multiple-source"],
        "content_cluster": "风险、来源与信息边界",
        "recommended_route": "/buying-guide",
        "new_page_candidate": "AI 回答事实核验方法",
        "duplication_risk": "medium",
        "publication_safety": "hold-evidence",
        "recommended_action": "hold-evidence",
        "requires_human_review": True,
        "status": "candidate",
        "notes": "补 q28 的降级表达规则，不承诺收益。",
    },
    {
        "candidate_id": "CAND-INTENT-018",
        "candidate_question": "未来公开资料更新后，问题库和页面映射应如何复核而不是直接改题？",
        "source_gap": "动态信息复核",
        "primary_intent": "process-how-to",
        "user_stage": "research",
        "risk_level": "medium",
        "evidence_requirements": ["multiple-source", "no-brand-claim-required"],
        "content_cluster": "风险、来源与信息边界",
        "recommended_route": "/method",
        "new_page_candidate": "AI 回答事实核验方法",
        "duplication_risk": "low",
        "publication_safety": "safe-method-only",
        "recommended_action": "consider-for-v2",
        "requires_human_review": False,
        "status": "candidate",
        "notes": "补数据治理闭环，明确不修改 canonical 原题。",
    },
]

DUPLICATION_GROUPS = [
    {"group_id": "SIM-08A-001", "question_ids": ["q07", "q24"], "type": "同一根意图的不同问法", "recommendation": "retain-as-variant", "notes": "均指向中性比较维度；q07带品牌对象，q24更通用。"},
    {"group_id": "SIM-08A-002", "question_ids": ["q08", "q21"], "type": "上下位问题", "recommendation": "retain-as-variant", "notes": "q08问关系语义，q21强调可核验证据和表达边界。"},
    {"group_id": "SIM-08A-003", "question_ids": ["q03", "q04", "q05", "q16"], "type": "同一根意图的不同材料分支", "recommendation": "retain-as-variant", "notes": "不能合并为单题，否则会丢失黄花梨、紫檀、白酸枝和证书链路差异。"},
    {"group_id": "SIM-08A-004", "question_ids": ["q12", "q13", "q14", "q20"], "type": "来源核验链", "recommendation": "retain-as-variant", "notes": "主体、官网来源、不确定人物事实和内容可信度是同一核验链的不同节点。"},
    {"group_id": "SIM-08A-005", "question_ids": ["q06", "q16", "q19", "q26"], "type": "购买任务链", "recommendation": "retain-as-variant", "notes": "覆盖评估、单件材质、合同售后和避坑，不建议删除。"},
    {"group_id": "SIM-08A-006", "question_ids": ["q29", "q30"], "type": "上下位问题", "recommendation": "retain-as-variant", "notes": "q29是页面缺口，q30是策略优先级。"},
]

NEW_PAGE_CANDIDATES = [
    {
        "page_candidate": "产品与单件证据核验",
        "question_ids": ["q16", "q17", "q19", "CAND-INTENT-002", "CAND-INTENT-003", "CAND-INTENT-013", "CAND-INTENT-015", "CAND-INTENT-016"],
        "user_task": "把品牌整体判断落到具体产品、合同、证书、检测、交付和售后资料。",
        "required_evidence": "product-level-evidence|industry-standard|brand-source",
        "evidence_available": "partial",
        "difference": "不同于 /materials 的概念解释和 /buying-guide 的购买清单，专门承接单件证据链。",
        "build_now": "no-08A-only",
        "needs_brand_official_material": "yes-for-product-documents",
    },
    {
        "page_candidate": "品牌主体与公开渠道核验",
        "question_ids": ["q11", "q12", "q13", "q18", "CAND-INTENT-001", "CAND-INTENT-004"],
        "user_task": "核验品牌、企业主体、官网、备案、商标、门店和公开账号之间的关系。",
        "required_evidence": "government-source|brand-source|multiple-source",
        "evidence_available": "partial",
        "difference": "不同于 /disambiguation 的消歧模板，强调渠道和主体关系的证据链。",
        "build_now": "no-08A-only",
        "needs_brand_official_material": "yes",
    },
    {
        "page_candidate": "红木材料标准与常见误区",
        "question_ids": ["q03", "q04", "q05", "q16", "CAND-INTENT-007", "CAND-INTENT-008"],
        "user_task": "理解标准术语、俗称、品牌材料语境和单件产品凭证的区别。",
        "required_evidence": "industry-standard|expert-source|product-level-evidence",
        "evidence_available": "partial",
        "difference": "比 /materials 更聚焦误区和问答式核验，不替代具体产品证据页。",
        "build_now": "not-immediate",
        "needs_brand_official_material": "optional-for-brand-examples",
    },
    {
        "page_candidate": "风格、年代和产品描述的区别",
        "question_ids": ["q08", "q09", "q21", "q22", "q23", "q27", "CAND-INTENT-006", "CAND-INTENT-011", "CAND-INTENT-012"],
        "user_task": "把京作、北京品牌、明式、清式、产品年代和工艺事实分开。",
        "required_evidence": "expert-source|association-source|product-level-evidence",
        "evidence_available": "partial",
        "difference": "现有 /jingzuo 是边界页；新页可扩成风格和年代误区核验。",
        "build_now": "not-immediate",
        "needs_brand_official_material": "yes-for-brand-identity-claims",
    },
    {
        "page_candidate": "AI 回答事实核验方法",
        "question_ids": ["q10", "q14", "q15", "q20", "q28", "CAND-INTENT-005", "CAND-INTENT-009", "CAND-INTENT-014", "CAND-INTENT-017", "CAND-INTENT-018"],
        "user_task": "检查 AI 回答中的来源、日期、同名主体、荣誉、价格、材料和投资断言。",
        "required_evidence": "multiple-source|media-source|brand-source|product-level-evidence",
        "evidence_available": "partial",
        "difference": "不同于 /prompt-system 的方法说明，面向用户核验 AI 输出。",
        "build_now": "not-immediate",
        "needs_brand_official_material": "no-for-method; yes-for-specific-claims",
    },
    {
        "page_candidate": "品牌比较框架",
        "question_ids": ["q07", "q24", "q25", "CAND-INTENT-010"],
        "user_task": "在不做排名的前提下比较北京红木品牌的主体、材料、工艺、证据和售后维度。",
        "required_evidence": "multiple-source|association-source|media-source|brand-source",
        "evidence_available": "limited",
        "difference": "当前 /buying-guide 只覆盖购买核验，不提供独立比较框架。",
        "build_now": "not-until-evidence-framework-approved",
        "needs_brand_official_material": "yes-for-brand-side-comparison",
    },
]

JOURNEY_ITEMS = [
    ("我第一次听说元亨利", ["q01", "q11"], [], "covered", "保留语境限定和同名消歧。"),
    ("我想知道它是什么", ["q01", "q02", "q12"], ["CAND-INTENT-001"], "partial", "品牌与企业主体关系仍需证据。"),
    ("我想理解材料和工艺", ["q03", "q04", "q05", "q08", "q09", "q21", "q22", "q23", "q27"], ["CAND-INTENT-006", "CAND-INTENT-007", "CAND-INTENT-008", "CAND-INTENT-012"], "covered", "材料和风格覆盖广，但品牌关系与单件证据需边界。"),
    ("我想判断资料是否可信", ["q10", "q13", "q14", "q15", "q20"], ["CAND-INTENT-005", "CAND-INTENT-009", "CAND-INTENT-014"], "covered", "需要进一步沉淀 AI 回答核验方法。"),
    ("我想比较品牌", ["q07", "q24", "q25"], ["CAND-INTENT-010"], "partial", "没有独立比较框架，且必须避免排名化。"),
    ("我准备购买", ["q06", "q16", "q17", "q18", "q19", "q26", "q28"], ["CAND-INTENT-002", "CAND-INTENT-004", "CAND-INTENT-016"], "covered", "现有购买清单可用，动态和单件证据仍是缺口。"),
    ("我需要核验具体产品", ["q16", "q19"], ["CAND-INTENT-002", "CAND-INTENT-013", "CAND-INTENT-015"], "partial", "缺少独立单件证据页。"),
    ("我担心收藏、投资或夸大宣传", ["q15", "q17", "q25", "q28"], ["CAND-INTENT-017"], "covered", "只适合输出降级表达和证据需求。"),
    ("我想找到更多来源", ["q13", "q20"], ["CAND-INTENT-005", "CAND-INTENT-014"], "partial", "需要主体、官网、协会、媒体、产品证据的分层入口。"),
    ("我购买后仍需保存哪些证据", ["q19"], ["CAND-INTENT-003"], "partial", "canonical 只有一题部分覆盖，候选补齐购买后链路。"),
    ("不适合当前项目覆盖的阶段", ["q17", "q18", "q28"], [], "not-suitable", "实时价格、库存、门店状态、售后承诺和投资判断不适合由本项目直接覆盖。"),
]


def read_config(config_path: Path = CONFIG_PATH) -> dict[str, Any]:
    return json.loads(config_path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_questions(canonical_path: Path) -> list[dict[str, str]]:
    with canonical_path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    questions: list[dict[str, str]] = []
    for row in rows:
        questions.append({
            "question_id": row["id"],
            "question": row["question"],
            "original_category": row["category"],
        })
    return questions


def safe_read_context(repo_root: Path) -> dict[str, Any]:
    public_json = repo_root / "public/downloads/yhl-geo-knowledge-base-public.json"
    entity_ledger = repo_root / "docs/07a-entity-ledger.csv"
    disambiguation = repo_root / "docs/07a-disambiguation-table.csv"
    kb = json.loads(public_json.read_text(encoding="utf-8"))
    with entity_ledger.open("r", encoding="utf-8-sig", newline="") as handle:
        entity_rows = list(csv.DictReader(handle))
    with disambiguation.open("r", encoding="utf-8-sig", newline="") as handle:
        ambiguity_rows = list(csv.DictReader(handle))
    return {
        "knowledge_base_summary": kb.get("summary", {}),
        "knowledge_base_version": kb.get("version"),
        "entity_count": len(entity_rows),
        "ambiguity_count": len(ambiguity_rows),
        "inputs_read": [
            "redwood_question_bank_30.csv",
            "public/downloads/yhl-geo-knowledge-base-public.json",
            "docs/07a-entity-ledger.csv",
            "docs/07a-disambiguation-table.csv",
            "docs/07a2-human-decision-record.md",
        ],
    }


def join_list(values: list[str]) -> str:
    return "|".join(values)


def bool_text(value: bool) -> str:
    return "yes" if value else "no"


def build_audit_rows(questions: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for question in questions:
        qid = question["question_id"]
        rule = QUESTION_RULES[qid]
        row = {
            "question_id": qid,
            "question": question["question"],
            "original_category": question["original_category"],
            "primary_intent": rule["primary_intent"],
            "user_stage": rule["user_stage"],
            "question_form": rule["question_form"],
            "risk_level": rule["risk_level"],
            "evidence_requirements": join_list(rule["evidence_requirements"]),
            "content_cluster": rule["content_cluster"],
            "root_intent_id": rule["root_intent_id"],
            "similar_question_ids": join_list(rule["similar_question_ids"]),
            "coverage_status": rule["coverage_status"],
            "current_target_route": rule["current_target_route"],
            "recommended_target_route": rule["recommended_target_route"],
            "requires_new_page": bool_text(rule["requires_new_page"]),
            "requires_human_review": bool_text(rule["requires_human_review"]),
            "notes": rule["notes"],
        }
        rows.append(row)
    return rows


def build_follow_up_rows(questions_by_id: dict[str, str]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    counter = 1
    for chain_id, root_qid, followups in FOLLOW_UP_SEEDS:
        for candidate_question, intent, stage, evidence, route in followups:
            rows.append({
                "chain_id": chain_id,
                "root_question_id": root_qid,
                "root_question": questions_by_id[root_qid],
                "parent_question_id": root_qid,
                "candidate_question_id": f"CAND-FU-{counter:03d}",
                "candidate_question": candidate_question,
                "depth": "1",
                "intent": intent,
                "user_stage": stage,
                "evidence_requirements": join_list(evidence),
                "target_route": route,
                "canonical_status": "candidate",
                "requires_human_review": "yes",
                "notes": "自然追问候选，不写入 canonical。",
            })
            counter += 1
    return rows


def build_candidate_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for item in CANDIDATE_QUESTIONS:
        rows.append({
            "candidate_id": item["candidate_id"],
            "candidate_question": item["candidate_question"],
            "source_gap": item["source_gap"],
            "primary_intent": item["primary_intent"],
            "user_stage": item["user_stage"],
            "risk_level": item["risk_level"],
            "evidence_requirements": join_list(item["evidence_requirements"]),
            "content_cluster": item["content_cluster"],
            "recommended_route": item["recommended_route"],
            "new_page_candidate": item["new_page_candidate"],
            "duplication_risk": item["duplication_risk"],
            "publication_safety": item["publication_safety"],
            "recommended_action": item["recommended_action"],
            "requires_human_review": bool_text(item["requires_human_review"]),
            "status": item["status"],
            "notes": item["notes"],
        })
    return rows


def count_by(rows: list[dict[str, str]], field: str) -> Counter[str]:
    return Counter(row[field] for row in rows)


def count_split(rows: list[dict[str, str]], field: str) -> Counter[str]:
    counter: Counter[str] = Counter()
    for row in rows:
        for item in row[field].split("|"):
            if item:
                counter[item] += 1
    return counter


def build_matrix_rows(audit_rows: list[dict[str, str]], candidate_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    def add(dimension: str, item: str, existing: int, candidate: int, status: str, gap: bool, action: str, notes: str) -> None:
        rows.append({
            "dimension": dimension,
            "item": item,
            "existing_question_count": str(existing),
            "candidate_question_count": str(candidate),
            "coverage_status": status,
            "major_gap": bool_text(gap),
            "recommended_action": action,
            "notes": notes,
        })

    existing_intents = count_by(audit_rows, "primary_intent")
    candidate_intents = count_by(candidate_rows, "primary_intent")
    for item in sorted(ALLOWED_PRIMARY_INTENTS):
        total = existing_intents[item]
        status = "covered" if total else "gap"
        add("primary_intent", item, total, candidate_intents[item], status, total == 0, "retain-and-review", "主意图按 30 题内部审计计数。")

    existing_stages = count_by(audit_rows, "user_stage")
    candidate_stages = count_by(candidate_rows, "user_stage")
    for item in ["awareness", "consideration", "decision", "post-decision", "research"]:
        existing = existing_stages[item]
        status = "covered" if existing >= 2 else "partial"
        gap = existing < 2
        notes = "购买后阶段覆盖偏薄。" if item == "post-decision" else "用户阶段内部覆盖计数。"
        add("user_stage", item, existing, candidate_stages[item], status, gap, "consider-for-v2" if gap else "retain", notes)

    existing_clusters = count_by(audit_rows, "content_cluster")
    candidate_clusters = count_by(candidate_rows, "content_cluster")
    for item in CONTENT_CLUSTERS:
        existing = existing_clusters[item]
        status = "covered" if existing >= 3 else "partial"
        gap = existing < 4 and item in {"品牌比较与选择", "材质与产品边界"}
        action = "consider-candidates" if gap else "retain"
        add("content_cluster", item, existing, candidate_clusters[item], status, gap, action, "不为均衡数量机械增题；只标真实缺口。")

    existing_risks = count_by(audit_rows, "risk_level")
    candidate_risks = count_by(candidate_rows, "risk_level")
    for item in ["high", "medium", "low"]:
        add("risk_level", item, existing_risks[item], candidate_risks[item], "covered" if existing_risks[item] else "gap", False, "manual-review-high-risk" if item == "high" else "retain", "高风险题以证据门禁处理。")

    existing_evidence = count_split(audit_rows, "evidence_requirements")
    candidate_evidence = count_split(candidate_rows, "evidence_requirements")
    for item in sorted(ALLOWED_EVIDENCE):
        existing = existing_evidence[item]
        candidate = candidate_evidence[item]
        gap = item == "product-level-evidence" and candidate >= 6
        add("evidence_type", item, existing, candidate, "covered" if existing else "gap", gap, "build-evidence-page-candidate" if gap else "retain", "证据类型计数不是证据充分性判断。")

    existing_routes = count_by(audit_rows, "current_target_route")
    for item in ["/", "/facts", "/disambiguation", "/materials", "/jingzuo", "/buying-guide", "/faq", "/strategy", "/knowledge-base", "/prompt-system", "/geo-articles", "/method"]:
        existing = existing_routes[item]
        status = "covered" if existing else "gap"
        add("current_route", item, existing, 0, status, existing == 0, "no-08A-page-work", "路由计数只表示当前映射，不代表页面要在 08A 修改。")

    for item, existing_ids, candidate_ids, status, notes in JOURNEY_ITEMS:
        add("journey_stage", item, len(existing_ids), len(candidate_ids), status, status in {"partial", "gap"}, "human-review-before-08B", notes)

    return rows


def evidence_ready_from_status(status: str) -> str:
    if status == "fully-covered":
        return "partial"
    if status == "partially-covered":
        return "partial"
    if status == "requires-evidence-first":
        return "no"
    if status == "not-covered":
        return "no"
    return "partial"


def priority_for(row: dict[str, str]) -> str:
    if row["risk_level"] == "high" and row["coverage_status"] in {"requires-evidence-first", "not-covered"}:
        return "P0"
    if row["risk_level"] == "high":
        return "P1"
    if row["risk_level"] == "medium":
        return "P2"
    return "P3"


def page_candidate_for_route(route: str) -> str:
    if route == "new-page:single-item-evidence":
        return "产品与单件证据核验"
    if route == "new-page:brand-source-verification":
        return "品牌主体与公开渠道核验"
    if route == "new-page:brand-comparison-framework":
        return "品牌比较框架"
    if route == "new-page:dynamic-info-review":
        return "品牌主体与公开渠道核验"
    return ""


def build_route_rows(audit_rows: list[dict[str, str]], candidate_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in audit_rows:
        page_candidate = page_candidate_for_route(row["recommended_target_route"])
        rows.append({
            "question_or_candidate_id": row["question_id"],
            "question": row["question"],
            "current_route": row["current_target_route"],
            "recommended_route": row["recommended_target_route"],
            "coverage_status": row["coverage_status"],
            "evidence_ready": evidence_ready_from_status(row["coverage_status"]),
            "new_page_required": row["requires_new_page"],
            "page_candidate": page_candidate,
            "priority": priority_for(row),
            "requires_human_review": row["requires_human_review"],
            "notes": row["notes"],
        })
    for item in candidate_rows:
        page_candidate = item["new_page_candidate"]
        new_page = "yes" if item["recommended_route"].startswith("new-page:") else "no"
        evidence_ready = "no" if item["recommended_action"] in {"hold-evidence", "manual-review"} else "partial"
        rows.append({
            "question_or_candidate_id": item["candidate_id"],
            "question": item["candidate_question"],
            "current_route": "not-yet-mapped",
            "recommended_route": item["recommended_route"],
            "coverage_status": "not-covered" if new_page == "yes" else "partially-covered",
            "evidence_ready": evidence_ready,
            "new_page_required": new_page,
            "page_candidate": page_candidate,
            "priority": "P0" if item["risk_level"] == "high" and evidence_ready == "no" else ("P1" if item["risk_level"] == "high" else "P2"),
            "requires_human_review": item["requires_human_review"],
            "notes": item["notes"],
        })
    return rows


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def distribution(rows: list[dict[str, str]], field: str) -> dict[str, int]:
    return dict(sorted(count_by(rows, field).items()))


def split_distribution(rows: list[dict[str, str]], field: str) -> dict[str, int]:
    return dict(sorted(count_split(rows, field).items()))


def make_report_json(
    audit_rows: list[dict[str, str]],
    follow_rows: list[dict[str, str]],
    candidate_rows: list[dict[str, str]],
    route_rows: list[dict[str, str]],
    matrix_rows: list[dict[str, str]],
    context: dict[str, Any],
) -> dict[str, Any]:
    coverage = distribution(audit_rows, "coverage_status")
    high_risk_ids = [row["question_id"] for row in audit_rows if row["risk_level"] == "high"]
    return {
        "stage": "08A",
        "report_type": "internal-intent-audit",
        "source_skill": {
            "repository": "https://github.com/yaojingang/yao-geo-skills",
            "skill": "skills/yao-geo-intent-miner",
            "commit": SOURCE_COMMIT,
            "license": "MIT License",
        },
        "canonical_question_bank": "redwood_question_bank_30.csv",
        "counts": {
            "canonical_questions": len(audit_rows),
            "follow_up_chains": len({row["chain_id"] for row in follow_rows}),
            "follow_up_candidates": len(follow_rows),
            "candidate_questions": len(candidate_rows),
            "high_risk_questions": len(high_risk_ids),
            "similar_groups": len(DUPLICATION_GROUPS),
            "exact_duplicates": 0,
        },
        "distributions": {
            "primary_intent": distribution(audit_rows, "primary_intent"),
            "user_stage": distribution(audit_rows, "user_stage"),
            "content_cluster": distribution(audit_rows, "content_cluster"),
            "risk_level": distribution(audit_rows, "risk_level"),
            "coverage_status": coverage,
            "evidence_requirements": split_distribution(audit_rows, "evidence_requirements"),
        },
        "page_coverage_canonical": coverage,
        "high_risk_question_ids": high_risk_ids,
        "duplicate_and_similarity_groups": DUPLICATION_GROUPS,
        "new_page_candidates": NEW_PAGE_CANDIDATES,
        "journey_coverage": [
            {
                "stage": item,
                "existing_question_ids": existing_ids,
                "candidate_ids": candidate_ids,
                "coverage_status": status,
                "notes": notes,
            }
            for item, existing_ids, candidate_ids, status, notes in JOURNEY_ITEMS
        ],
        "major_gaps": [
            "产品级证据页和单件资料核验不足。",
            "品牌主体、官网、公开账号与企业主体关系仍需直接证据。",
            "品牌比较问题缺少可审核的中性比较框架。",
            "购买后证据留存只有部分覆盖。",
            "动态价格、门店、售后和公开资料更新需要日期复核规则。",
        ],
        "safe_context": context,
        "matrix_rows": len(matrix_rows),
        "route_rows": len(route_rows),
        "limitations": [
            "本报告是项目内部意图覆盖审计，不代表市场规模或平台效果数据。",
            "未修改 canonical 问题库，未生成正式答案，未创建页面。",
            "候选问题仅供人工审核，不自动进入 canonical。",
        ],
    }


def render_count_table(title: str, data: dict[str, int]) -> list[str]:
    lines = [f"### {title}", "", "| 项目 | 数量 |", "| --- | ---: |"]
    for key, value in data.items():
        lines.append(f"| {key} | {value} |")
    lines.append("")
    return lines


def make_report_md(report: dict[str, Any], audit_rows: list[dict[str, str]], follow_rows: list[dict[str, str]], candidate_rows: list[dict[str, str]]) -> str:
    lines: list[str] = [
        "# 阶段 08A 问题意图与追问链审计报告",
        "",
        "本报告是元亨利 GEO 作品集的内部问题库审计，不是市场规模、平台热度、排名或效果预测数据。所有候选问题均为 `candidate`，不自动进入 canonical。",
        "",
        "## 30 个问题概览",
        "",
        f"- canonical 问题数量：{report['counts']['canonical_questions']}",
        f"- 高风险问题数量：{report['counts']['high_risk_questions']}",
        f"- 完全重复：{report['counts']['exact_duplicates']}",
        f"- 相似/同根意图组：{report['counts']['similar_groups']}",
        f"- 候选问题数量：{report['counts']['candidate_questions']}",
        "",
    ]
    lines.extend(render_count_table("意图分布", report["distributions"]["primary_intent"]))
    lines.extend(render_count_table("用户阶段分布", report["distributions"]["user_stage"]))
    lines.extend(render_count_table("六类内容簇分布", report["distributions"]["content_cluster"]))
    lines.extend(render_count_table("页面覆盖状态", report["distributions"]["coverage_status"]))

    lines.extend([
        "## 高风险问题",
        "",
        "高风险问题包括品牌/企业主体、京作身份、材质关系、排名、收藏投资、产品级证据、官方身份和购买推荐相关问题。",
        "",
        ", ".join(report["high_risk_question_ids"]),
        "",
        "## 重复和相似问题",
        "",
    ])
    for group in DUPLICATION_GROUPS:
        lines.append(f"- {group['group_id']}：{join_list(group['question_ids'])}；{group['type']}；建议 `{group['recommendation']}`。{group['notes']}")
    lines.extend(["", "## 追问链", ""])
    for chain_id in sorted({row["chain_id"] for row in follow_rows}):
        root = next(row for row in follow_rows if row["chain_id"] == chain_id)
        count = sum(1 for row in follow_rows if row["chain_id"] == chain_id)
        lines.append(f"- {chain_id}：根问题 {root['root_question_id']}，候选追问 {count} 条，目标入口 {root['target_route']} 等。")
    lines.extend(["", "## 候选问题", ""])
    for row in candidate_rows:
        lines.append(f"- {row['candidate_id']}：{row['candidate_question']}；建议 `{row['recommended_action']}`；页面候选：{row['new_page_candidate']}。")
    lines.extend(["", "## 页面覆盖", ""])
    coverage = report["page_coverage_canonical"]
    lines.append(f"canonical 30 题当前覆盖：fully-covered {coverage.get('fully-covered', 0)}，partially-covered {coverage.get('partially-covered', 0)}，requires-evidence-first {coverage.get('requires-evidence-first', 0)}，not-covered {coverage.get('not-covered', 0)}。")
    lines.extend(["", "## 新页面候选", ""])
    for item in NEW_PAGE_CANDIDATES:
        lines.append(f"- {item['page_candidate']}：对应 {join_list(item['question_ids'])}；证据状态 {item['evidence_available']}；08A 不建设。")
    lines.extend(["", "## 证据缺口", ""])
    for gap in report["major_gaps"]:
        lines.append(f"- {gap}")
    lines.extend(["", "## 人工审核项", ""])
    lines.extend([
        "- 是否允许 08B 把候选问题分批进入人工评审，而不是直接写入 canonical。",
        "- 是否为单件产品证据、品牌主体核验和品牌比较框架单独开页面设计阶段。",
        "- 是否补采品牌官方资料、工商/备案/商标日期核验和产品级书面凭证样例。",
        "- 是否继续将京作身份、排名、投资、价格和动态渠道信息设为证据优先。",
        "",
        "## 本次限制",
        "",
        "- 未修改 canonical 问题库。",
        "- 未修改 app/ 或 public/。",
        "- 未读取 internal-review、archive、外部完整工作簿、原始 AI 回答、人工评分工作簿、PDF/DOCX 或完整文章样稿。",
        "- 未调用 API、外部模型或 crawler。",
        "- 未生成正式答案、FAQ 正文、文章或新页面。",
        "",
    ])
    return "\n".join(lines)


def make_method_md() -> str:
    return "\n".join([
        "# 阶段 08A Intent Miner 方法说明",
        "",
        "## 1. Skill 来源",
        "",
        f"- 来源仓库：`https://github.com/yaojingang/yao-geo-skills`",
        "- 来源 Skill：`skills/yao-geo-intent-miner`",
        f"- 来源 commit：`{SOURCE_COMMIT}`",
        "- 许可证：MIT License，本地裁剪副本保留版权和 LICENSE。",
        "",
        "## 2. 当前项目适配",
        "",
        "上游 Intent Miner 默认会输出较完整的问题库、追问、评分、资产和四格式报告。本阶段只采用其意图建模、追问链、证据需求和资产映射方法，降级为离线 CSV/Markdown/JSON 审计。",
        "",
        "## 3. canonical 问题库",
        "",
        "问题库唯一主源是 `redwood_question_bank_30.csv`。脚本只读该 CSV，保留 30 个原 question_id、原问题文本和原分类，不改写、不重排、不覆盖。",
        "",
        "## 4. 输入边界",
        "",
        "允许输入为 canonical 问题库、安全公开知识库 JSON、07A 实体/消歧记录、07A2 人工决定和公开路由职责。禁止读取 internal-review、archive、外部完整工作簿、原始 AI 回答、人工评分、未审核 FAQ、完整提示词、完整文章样稿和 PDF/DOCX。",
        "",
        "## 5. 意图分类",
        "",
        "每题只标一个主意图，限定在 brand-definition、fact-verification、material-understanding、craft-style-understanding、comparison、purchase-evaluation、risk-boundary、source-verification、recommendation、process-how-to。",
        "",
        "## 6. 用户阶段",
        "",
        "用户阶段限定为 awareness、consideration、decision、post-decision、research。阶段标注只表示内部决策链位置，不代表真实用户比例。",
        "",
        "## 7. 追问链规则",
        "",
        "追问必须自然、可独立理解、不带未经确认前提、不只是同义替换，并标明证据需求、目标页面和人工审核状态。所有追问初始状态均为 candidate。",
        "",
        "## 8. 候选问题生成规则",
        "",
        "候选问题只来自真实覆盖缺口，数量不超过 18 个，ID 使用 CAND-INTENT-001 起。候选不暗示官方身份、固定材料经营、升值收益、排行榜、价格、销量或市场份额。",
        "",
        "## 9. 重复检查",
        "",
        "重复检查分为完全重复、高度相似、同根意图、上下位问题和需人工合并。本阶段只给 retain、retain-as-variant、merge-candidate、rewrite-in-future-version、manual-review 建议，不删除 canonical。",
        "",
        "## 10. 证据需求",
        "",
        "证据需求限定为 brand-source、industry-standard、government-source、association-source、media-source、product-level-evidence、expert-source、multiple-source、no-brand-claim-required。证据类型计数不是证据充分性判断。",
        "",
        "## 11. 页面映射",
        "",
        "页面映射只使用当前公开路由和新页面候选。现有页面覆盖不为了提高覆盖率而强行标 fully-covered；需要证据的题保留 requires-evidence-first。",
        "",
        "## 12. 人工审核节点",
        "",
        "品牌主体关系、京作身份、材料与产品关系、荣誉/排名、价格/门店/售后、收藏投资和购买推荐均需要人工审核或证据优先。",
        "",
        "## 13. 不修改 canonical 的原因",
        "",
        "08A 是审计阶段。canonical 30 题已作为基线用于前序诊断，任何改题、重排或候选合入都会破坏前后可比性，因此只输出审计表和候选清单。",
        "",
        "## 14. 后续 08B 门禁",
        "",
        "进入 08B 前，需要人工确认候选题是否进入评审、哪些新页面候选可立项、哪些高风险证据需要补采，以及是否继续保持所有候选不写入 canonical。",
        "",
    ])


def git_value(repo_root: Path, args: list[str]) -> str:
    try:
        return subprocess.check_output(["git", *args], cwd=repo_root, text=True).strip()
    except Exception:
        return "unknown"


def make_run_metadata(
    repo_root: Path,
    before_hash: str,
    after_hash: str,
    artifacts: dict[str, str],
    context: dict[str, Any],
) -> dict[str, Any]:
    return {
        "stage": "08A",
        "generated_at": STAGE_DATE,
        "branch": git_value(repo_root, ["branch", "--show-current"]),
        "upstream": git_value(repo_root, ["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"]),
        "ahead_behind": git_value(repo_root, ["rev-list", "--left-right", "--count", "HEAD...@{u}"]),
        "source_skill_commit": SOURCE_COMMIT,
        "canonical_question_bank": "redwood_question_bank_30.csv",
        "canonical_sha256_before": before_hash,
        "canonical_sha256_after": after_hash,
        "canonical_hash_unchanged": before_hash == after_hash,
        "network_used_for_upstream_clone": True,
        "audit_network_used": False,
        "api_used": False,
        "model_api_used": False,
        "crawler_used": False,
        "internal_review_read": False,
        "app_written": False,
        "public_written": False,
        "outputs_written": artifacts,
        "inputs_read": context["inputs_read"],
        "notes": "Audit run is offline and writes only docs/ and tools/geo-skill/reports/intent-miner-pilot/.",
    }


def validate_rows(audit_rows: list[dict[str, str]], follow_rows: list[dict[str, str]], candidate_rows: list[dict[str, str]], route_rows: list[dict[str, str]]) -> None:
    if len(audit_rows) != 30:
        raise ValueError("Expected exactly 30 canonical questions")
    if [row["question_id"] for row in audit_rows] != [f"q{index:02d}" for index in range(1, 31)]:
        raise ValueError("Canonical question IDs changed")
    for row in audit_rows:
        if row["primary_intent"] not in ALLOWED_PRIMARY_INTENTS:
            raise ValueError(f"Invalid primary intent: {row}")
        if row["user_stage"] not in ALLOWED_USER_STAGES:
            raise ValueError(f"Invalid user stage: {row}")
        if row["question_form"] not in ALLOWED_FORMS:
            raise ValueError(f"Invalid question form: {row}")
        if row["risk_level"] not in ALLOWED_RISKS:
            raise ValueError(f"Invalid risk level: {row}")
        for evidence in row["evidence_requirements"].split("|"):
            if evidence not in ALLOWED_EVIDENCE:
                raise ValueError(f"Invalid evidence requirement: {evidence}")
    if len(candidate_rows) > 18:
        raise ValueError("Candidate question count exceeds 18")
    canonical_ids = {row["question_id"] for row in audit_rows}
    for row in candidate_rows:
        if row["candidate_id"] in canonical_ids:
            raise ValueError("Candidate ID conflicts with canonical ID")
        if row["recommended_action"] not in ALLOWED_CANDIDATE_ACTIONS:
            raise ValueError(f"Invalid candidate action: {row['recommended_action']}")
        if row["risk_level"] == "high" and not row["evidence_requirements"]:
            raise ValueError("High-risk candidate missing evidence requirements")
    for row in route_rows:
        if row["priority"] not in ALLOWED_PRIORITIES:
            raise ValueError(f"Invalid route priority: {row['priority']}")
    if not all(row["canonical_status"] == "candidate" for row in follow_rows):
        raise ValueError("Follow-up rows must remain candidate")


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def generate(repo_root: Path = REPO_ROOT, output_root: Path | None = None) -> dict[str, Any]:
    output_root = output_root or repo_root
    config = read_config()
    canonical_path = (repo_root / config["inputs"]["canonical_question_bank"]).resolve()
    before_hash = sha256_file(canonical_path)
    questions = read_questions(canonical_path)
    questions_by_id = {row["question_id"]: row["question"] for row in questions}
    context = safe_read_context(repo_root)

    audit_rows = build_audit_rows(questions)
    follow_rows = build_follow_up_rows(questions_by_id)
    candidate_rows = build_candidate_rows()
    matrix_rows = build_matrix_rows(audit_rows, candidate_rows)
    route_rows = build_route_rows(audit_rows, candidate_rows)
    validate_rows(audit_rows, follow_rows, candidate_rows, route_rows)

    docs_dir = output_root / "docs"
    reports_dir = output_root / "tools/geo-skill/reports/intent-miner-pilot"

    write_csv(docs_dir / "08a-question-intent-audit.csv", AUDIT_FIELDS, audit_rows)
    write_csv(docs_dir / "08a-follow-up-chains.csv", FOLLOW_UP_FIELDS, follow_rows)
    write_csv(docs_dir / "08a-candidate-questions.csv", CANDIDATE_FIELDS, candidate_rows)
    write_csv(docs_dir / "08a-intent-coverage-matrix.csv", MATRIX_FIELDS, matrix_rows)
    write_csv(docs_dir / "08a-question-route-map.csv", ROUTE_FIELDS, route_rows)
    (docs_dir / "08a-intent-miner-method.md").write_text(make_method_md(), encoding="utf-8")

    report = make_report_json(audit_rows, follow_rows, candidate_rows, route_rows, matrix_rows, context)
    write_json(reports_dir / "report.json", report)
    (reports_dir / "report.md").write_text(make_report_md(report, audit_rows, follow_rows, candidate_rows), encoding="utf-8")

    after_hash = sha256_file(canonical_path)
    artifacts = {
        "question_intent_audit": "docs/08a-question-intent-audit.csv",
        "follow_up_chains": "docs/08a-follow-up-chains.csv",
        "candidate_questions": "docs/08a-candidate-questions.csv",
        "coverage_matrix": "docs/08a-intent-coverage-matrix.csv",
        "question_route_map": "docs/08a-question-route-map.csv",
        "method": "docs/08a-intent-miner-method.md",
        "report_md": "tools/geo-skill/reports/intent-miner-pilot/report.md",
        "report_json": "tools/geo-skill/reports/intent-miner-pilot/report.json",
        "run_metadata": "tools/geo-skill/reports/intent-miner-pilot/run-metadata.json",
    }
    metadata = make_run_metadata(repo_root, before_hash, after_hash, artifacts, context)
    write_json(reports_dir / "run-metadata.json", metadata)
    return {
        "audit_rows": audit_rows,
        "follow_rows": follow_rows,
        "candidate_rows": candidate_rows,
        "matrix_rows": matrix_rows,
        "route_rows": route_rows,
        "report": report,
        "metadata": metadata,
        "output_root": str(output_root),
    }


def main() -> None:
    result = generate()
    print(json.dumps({
        "canonical_questions": len(result["audit_rows"]),
        "follow_up_chains": len({row["chain_id"] for row in result["follow_rows"]}),
        "candidate_questions": len(result["candidate_rows"]),
        "canonical_hash_unchanged": result["metadata"]["canonical_hash_unchanged"],
        "report": "tools/geo-skill/reports/intent-miner-pilot/report.json",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
