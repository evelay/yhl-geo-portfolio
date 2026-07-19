#!/usr/bin/env python3
"""Offline adapter for the 07A yao-geo-brand-graph pilot.

The adapter reads the public-filtered knowledge base JSON, builds an isolated
candidate entity graph, and writes ledgers plus reports. It never fetches URLs,
calls APIs, invokes models, reads internal-review, or writes app/public output.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


ENTITY_FIELDS = [
    "entity_id",
    "canonical_name",
    "display_name",
    "entity_type",
    "aliases",
    "description",
    "evidence_ids",
    "evidence_status",
    "confidence",
    "publication_safety",
    "ambiguity_risk",
    "recommended_usage",
    "notes",
]

RELATION_FIELDS = [
    "relation_id",
    "subject_id",
    "predicate",
    "object_id",
    "evidence_ids",
    "evidence_status",
    "confidence",
    "publication_safety",
    "relation_interpretation",
    "prohibited_interpretation",
    "requires_human_review",
    "status",
    "notes",
]

DISAMBIGUATION_FIELDS = [
    "ambiguity_id",
    "mention",
    "possible_entity_a",
    "possible_entity_b",
    "ambiguity_type",
    "risk",
    "safe_interpretation",
    "unsafe_interpretation",
    "evidence_ids",
    "requires_human_decision",
    "status",
    "notes",
]

SCHEMA_CANDIDATE_FIELDS = [
    "candidate_id",
    "schema_target",
    "entity_or_relation_id",
    "evidence_ids",
    "confidence",
    "publication_safety",
    "eligible_for_07b",
    "block_reason",
    "requires_human_review",
    "notes",
]

ALLOWED_EVIDENCE_STATUS = {"source-confirmed", "snapshot-supported", "inferred", "evidence-gap"}
ALLOWED_CONFIDENCE = {"high", "medium", "low", "unknown"}
ALLOWED_PUBLICATION_SAFETY = {"public-safe", "review-required", "internal-only", "reject"}
ALLOWED_AMBIGUITY_RISK = {"high", "medium", "low"}
ALLOWED_ENTITY_TYPES = {
    "Brand",
    "Organization",
    "Material",
    "CraftTradition",
    "FurnitureStyle",
    "ProductCategory",
    "ContentTopic",
    "Geography",
    "Source",
    "QuestionIntent",
    "BoundaryRule",
    "PublicationAsset",
}
BLOCKED_STATUS_TERMS = {
    "L3",
    "pending",
    "prohibited",
    "internal-only",
    "level_three_review_required",
    "source_review_required",
    "unreviewed",
    "non_public",
    "missing_source_id",
    "blocked_publication_status",
    "restricted_internal_material",
}

FORBIDDEN_INTERPRETATION_TERMS = {
    "行业第一",
    "顶级",
    "领先",
    "排名",
    "国家级资质",
    "所有产品",
    "全部产品",
    "独家",
    "保值",
    "升值",
    "投资回报",
    "官方委托",
    "GEO 增长结果",
}


@dataclass(frozen=True)
class BuildContext:
    root: Path
    config_path: Path
    config: dict[str, Any]
    generated_at: str
    run_id: str
    branch: str
    commit: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        default="tools/geo-skill/adapters/brand-graph/graph-config.json",
        help="Adapter config path relative to project root.",
    )
    parser.add_argument("--generated-at", help="Override timestamp for deterministic tests.")
    parser.add_argument("--run-id", help="Override run id for deterministic tests.")
    parser.add_argument("--project-root", help="Project root override for tests.")
    return parser.parse_args()


def find_project_root(start: Path) -> Path:
    if (start / "package.json").exists() and (start / ".git").exists():
        return start.resolve()
    for candidate in [start, *start.parents]:
        if (candidate / "package.json").exists() and (candidate / ".git").exists():
            return candidate.resolve()
    raise RuntimeError("Could not locate project root with package.json and .git")


def run_git(root: Path, args: list[str], fallback: str) -> str:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=root,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
    except Exception:
        return fallback
    return result.stdout.strip() or fallback


def relpath(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: csv_value(row.get(field, "")) for field in fieldnames})


def csv_value(value: Any) -> str:
    if isinstance(value, list):
        return "|".join(str(item) for item in value)
    if value is True:
        return "yes"
    if value is False:
        return "no"
    if value is None:
        return ""
    return str(value)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def slug(value: str) -> str:
    mapping = {
        "元亨利红木家具": "yuanhengli",
        "北京元亨利硬木家具有限公司": "beijing-yuanhengli-hardwood-furniture",
        "bjyuanhengli.com": "bjyuanhengli-com",
        "红木": "redwood",
        "黄花梨": "huanghuali",
        "紫檀": "zitan",
        "酸枝": "suanzhi",
        "红木家具": "redwood-furniture",
        "明式家具": "ming-style-furniture",
        "清式家具": "qing-style-furniture",
        "中国家具协会": "china-furniture-association",
        "北京家具行业协会": "beijing-furniture-trade-association",
        "木材工业研究所": "wood-industry-research-institute",
        "人民网": "people-cn",
        "中国国家博物馆": "national-museum-of-china",
        "元亨利文化示范馆": "yuanhengli-culture-showroom",
        "贞穆堂": "zhenmutang",
        "北京": "beijing",
        "古典工艺": "classical-craft-terms",
        "京作": "jingzuo",
    }
    if value in mapping:
        return mapping[value]
    text = re.sub(r"[^a-z0-9]+", "-", value.lower())
    return re.sub(r"-+", "-", text).strip("-") or "item"


def source_entity_id(source_id: str) -> str:
    return "source:" + source_id.lower()


def require_safe_relative(path_text: str, root: Path, *, read_public_download: bool = False) -> Path:
    lowered = path_text.lower()
    blocked = ["internal-review", "first_setup", "yhl_geo_portfolio_final", "/archive/", "\\archive\\"]
    if any(fragment in lowered for fragment in blocked):
        raise ValueError(f"Blocked path fragment in {path_text}")
    if any(lowered.endswith(ext) for ext in [".xlsx", ".docx", ".pdf"]):
        raise ValueError(f"Blocked non-JSON input path {path_text}")
    path = (root / path_text).resolve()
    path.relative_to(root)
    if read_public_download:
        expected = (root / "public/downloads/yhl-geo-knowledge-base-public.json").resolve()
        if path != expected:
            raise ValueError("07A brand data input must be public/downloads/yhl-geo-knowledge-base-public.json")
    return path


def validate_public_snapshot(data: dict[str, Any]) -> dict[str, Any]:
    metadata = data.get("metadata", {})
    if data.get("version") != "1.1-public-filtered":
        raise ValueError("Input is not the public-filtered knowledge base snapshot")
    publication_scope = str(metadata.get("publication_scope", ""))
    if "public-filtered" not in publication_scope:
        raise ValueError("Input metadata lacks public-filtered publication scope")
    for key in ["publication_scope", "excluded_statuses", "record_count", "excluded_fact_count"]:
        if key not in metadata:
            raise ValueError(f"Input metadata lacks public review marker: {key}")

    found_blocked_terms: list[str] = []
    for container_name in ["facts", "sources"]:
        for item in data.get(container_name, []):
            status_text = " ".join(str(item.get(key, "")) for key in ["publication_status", "review_status", "status", "evidenceLevel"])
            if item.get("evidenceLevel") == "L3":
                found_blocked_terms.append(f"{container_name}:{item.get('id')}:L3")
            lowered = status_text.lower()
            for term in BLOCKED_STATUS_TERMS:
                if term.lower() in lowered and term not in {"L3"}:
                    found_blocked_terms.append(f"{container_name}:{item.get('id')}:{term}")
            if container_name == "sources" and item.get("usable") is not True:
                found_blocked_terms.append(f"sources:{item.get('id')}:not-usable")
    if found_blocked_terms:
        raise ValueError("Public input contains blocked records: " + ", ".join(found_blocked_terms))

    return {
        "version": data.get("version"),
        "publication_scope": publication_scope,
        "record_count": metadata.get("record_count"),
        "excluded_statuses": metadata.get("excluded_statuses", []),
        "fact_count": len(data.get("facts", [])),
        "source_count": len(data.get("sources", [])),
        "source_records_have_status": all("status" in item and item.get("usable") is True for item in data.get("sources", [])),
        "fact_records_have_evidence_level": all("evidenceLevel" in item for item in data.get("facts", [])),
    }


def evidence_for_facts(facts_by_id: dict[str, dict[str, Any]], fact_ids: list[str]) -> list[str]:
    values: list[str] = []
    for fact_id in fact_ids:
        values.extend(facts_by_id.get(fact_id, {}).get("evidenceIds", []))
    return sorted(dict.fromkeys(values))


def make_entity(
    entity_id: str,
    canonical_name: str,
    display_name: str,
    entity_type: str,
    aliases: list[str] | None,
    description: str,
    evidence_ids: list[str] | None,
    evidence_status: str,
    confidence: str,
    publication_safety: str,
    ambiguity_risk: str,
    recommended_usage: str,
    notes: str,
) -> dict[str, Any]:
    if entity_type not in ALLOWED_ENTITY_TYPES:
        raise ValueError(f"Unsupported entity type: {entity_type}")
    if evidence_status not in ALLOWED_EVIDENCE_STATUS:
        raise ValueError(f"Unsupported evidence status for {entity_id}: {evidence_status}")
    if confidence not in ALLOWED_CONFIDENCE:
        raise ValueError(f"Unsupported confidence for {entity_id}: {confidence}")
    if publication_safety not in ALLOWED_PUBLICATION_SAFETY:
        raise ValueError(f"Unsupported publication safety for {entity_id}: {publication_safety}")
    if ambiguity_risk not in ALLOWED_AMBIGUITY_RISK:
        raise ValueError(f"Unsupported ambiguity risk for {entity_id}: {ambiguity_risk}")
    return {
        "entity_id": entity_id,
        "canonical_name": canonical_name,
        "display_name": display_name,
        "entity_type": entity_type,
        "aliases": aliases or [],
        "description": description,
        "evidence_ids": evidence_ids or [],
        "evidence_status": evidence_status,
        "confidence": confidence,
        "publication_safety": publication_safety,
        "ambiguity_risk": ambiguity_risk,
        "recommended_usage": recommended_usage,
        "notes": notes,
    }


def make_relation(
    relation_id: str,
    subject_id: str,
    predicate: str,
    object_id: str,
    evidence_ids: list[str] | None,
    evidence_status: str,
    confidence: str,
    publication_safety: str,
    relation_interpretation: str,
    prohibited_interpretation: str,
    requires_human_review: bool,
    notes: str,
) -> dict[str, Any]:
    evidence_ids = evidence_ids or []
    if evidence_status not in ALLOWED_EVIDENCE_STATUS:
        raise ValueError(f"Unsupported evidence status for {relation_id}: {evidence_status}")
    if confidence not in ALLOWED_CONFIDENCE:
        raise ValueError(f"Unsupported confidence for {relation_id}: {confidence}")
    if publication_safety not in ALLOWED_PUBLICATION_SAFETY:
        raise ValueError(f"Unsupported publication safety for {relation_id}: {publication_safety}")
    if evidence_status == "source-confirmed" and not evidence_ids:
        raise ValueError(f"source-confirmed relation lacks evidence id: {relation_id}")
    if evidence_status == "inferred" and publication_safety == "public-safe":
        raise ValueError(f"inferred relation cannot be public-safe: {relation_id}")
    if evidence_status == "evidence-gap" and evidence_ids:
        raise ValueError(f"evidence-gap relation should not carry auto-filled evidence ids: {relation_id}")
    return {
        "relation_id": relation_id,
        "subject_id": subject_id,
        "predicate": predicate,
        "object_id": object_id,
        "evidence_ids": evidence_ids,
        "evidence_status": evidence_status,
        "confidence": confidence,
        "publication_safety": publication_safety,
        "relation_interpretation": relation_interpretation,
        "prohibited_interpretation": prohibited_interpretation,
        "requires_human_review": requires_human_review,
        "status": "candidate",
        "notes": notes,
    }


def build_entities(data: dict[str, Any]) -> list[dict[str, Any]]:
    facts_by_entity: dict[str, list[dict[str, Any]]] = {}
    for fact in data.get("facts", []):
        facts_by_entity.setdefault(fact.get("entityId", ""), []).append(fact)

    by_name = {item.get("name"): item for item in data.get("entities", [])}
    entities: list[dict[str, Any]] = []

    def fact_evidence_for_entity(original_id: str) -> list[str]:
        evidence: list[str] = []
        for fact in facts_by_entity.get(original_id, []):
            evidence.extend(fact.get("evidenceIds", []))
        return sorted(dict.fromkeys(evidence))

    brand = by_name["元亨利红木家具"]
    entities.append(
        make_entity(
            "brand:yuanhengli",
            brand["name"],
            "元亨利红木家具",
            "Brand",
            ["元亨利"],
            brand["description"],
            fact_evidence_for_entity(brand["id"]),
            "snapshot-supported",
            "medium",
            "review-required",
            "high",
            "仅作红木家具语境下的品牌识别对象；进入 Schema 前必须完成品牌/企业主体消歧。",
            brand.get("boundary", ""),
        )
    )

    org = by_name["北京元亨利硬木家具有限公司"]
    entities.append(
        make_entity(
            "organization:beijing-yuanhengli-hardwood-furniture",
            org["name"],
            org["name"],
            "Organization",
            [],
            org["description"],
            fact_evidence_for_entity(org["id"]),
            "source-confirmed",
            "high",
            "review-required",
            "high",
            "可作为企业主体候选；不得自动与品牌、网站或其他同名字号视为同一实体。",
            org.get("boundary", ""),
        )
    )

    website = by_name["bjyuanhengli.com"]
    entities.append(
        make_entity(
            "asset:bjyuanhengli-com",
            website["name"],
            "bjyuanhengli.com",
            "PublicationAsset",
            ["元亨利官网线索"],
            website["description"],
            fact_evidence_for_entity(website["id"]),
            "snapshot-supported",
            "medium",
            "review-required",
            "medium",
            "只作为官网/域名公开线索；备案、主体和页面状态需按日期复核。",
            website.get("boundary", ""),
        )
    )

    material_specs = [
        ("红木", "material:redwood", ["GB/T 18107-2017 语境"], "按国家标准解释红木术语，不证明任何单件材质。"),
        ("黄花梨", "material:huanghuali", ["花梨木相关俗称需回标准"], "材料概念和内容主题，不等同品牌定位或全部产品材质。"),
        ("紫檀", "material:zitan", ["紫檀木相关俗称需回标准"], "材料概念和内容主题，不替代单件证书、检测或合同。"),
        ("酸枝", "material:suanzhi", ["白酸枝", "白酸枝等俗称"], "材料概念及俗称治理对象，需回规范名称和书面资料。"),
    ]
    for name, entity_id, aliases, usage in material_specs:
        item = by_name[name]
        evidence_ids = fact_evidence_for_entity(item["id"])
        entities.append(
            make_entity(
                entity_id,
                name,
                name,
                "Material",
                aliases,
                item["description"],
                evidence_ids,
                "source-confirmed" if evidence_ids else "snapshot-supported",
                "high" if name == "红木" else "medium",
                "public-safe" if name == "红木" else "review-required",
                "medium",
                usage,
                item.get("boundary", ""),
            )
        )

    category = by_name["红木家具"]
    entities.append(
        make_entity(
            "category:redwood-furniture",
            category["name"],
            "红木家具",
            "ProductCategory",
            [],
            category["description"],
            fact_evidence_for_entity(category["id"]),
            "source-confirmed",
            "high",
            "public-safe",
            "low",
            "可作为产品类别和购买核验主题，不作为品牌全量产品或单件材质结论。",
            category.get("boundary", ""),
        )
    )

    craft_evidence = evidence_for_facts({fact["id"]: fact for fact in data["facts"]}, ["FACT-0012", "FACT-0013", "FACT-0014", "FACT-0015"])
    entities.append(
        make_entity(
            "craft:classical-process-terms",
            "古典工艺栏目术语",
            "古典工艺",
            "CraftTradition",
            ["刮磨", "打磨", "烫蜡", "包浆"],
            "官网工艺栏目中出现的工艺术语集合；本阶段不扩写为非遗、纯手工或每件产品工艺事实。",
            craft_evidence,
            "source-confirmed" if craft_evidence else "evidence-gap",
            "low",
            "review-required",
            "medium",
            "只可作为待审工艺内容主题。",
            "行业通用工艺和品牌一手自述需分开。",
        )
    )

    for name, entity_id in [("明式家具", "style:ming-style-furniture"), ("清式家具", "style:qing-style-furniture")]:
        item = by_name[name]
        evidence_ids = fact_evidence_for_entity(item["id"])
        entities.append(
            make_entity(
                entity_id,
                name,
                name,
                "FurnitureStyle",
                [name.replace("家具", "风格")],
                item["description"],
                evidence_ids,
                "source-confirmed" if evidence_ids else "evidence-gap",
                "medium",
                "review-required",
                "high",
                "只作为家具史与审美风格概念；不得推断具体年代、馆藏或文物年代。",
                item.get("boundary", ""),
            )
        )

    content_topics = [
        ("topic:huanghuali-relation", "黄花梨关系", ["元亨利与黄花梨是什么关系？"], "材料与内容主题关系，不能写成品牌定位或经营事实。"),
        ("topic:zitan-understanding", "紫檀家具理解", ["紫檀家具怎么理解？"], "材料、产品类别和单件证据边界主题。"),
        ("topic:baisuanzhi-term", "白酸枝关联", ["白酸枝等于某个固定树种吗？"], "俗称、规范名称和产品凭证一致性主题。"),
        ("topic:ming-qing-style", "明式/清式意义", ["明式、清式和品牌产品是什么关系？"], "风格教育主题，不证明具体产品年代。"),
        ("topic:jingzuo-unresolved", "京作关系待证", ["京作家具", "京作工艺"], "允许输入中未出现京作记录；仅记录待证消歧对象，不创建品牌官方身份事实。"),
    ]
    for entity_id, name, aliases, description in content_topics:
        evidence_status = "evidence-gap" if "jingzuo" in entity_id else "snapshot-supported"
        entities.append(
            make_entity(
                entity_id,
                name,
                name,
                "ContentTopic",
                aliases,
                description,
                [],
                evidence_status,
                "low" if evidence_status == "evidence-gap" else "medium",
                "review-required",
                "high" if "jingzuo" in entity_id else "medium",
                "只作为内容主题或待审意图，不作为经营范围、产品全量或官方身份事实。",
                "主题关系必须与材料、品牌事实和单件证据分层。",
            )
        )

    entities.append(
        make_entity(
            "geography:beijing",
            "北京",
            "北京",
            "Geography",
            ["北京市"],
            "公开来源名称和企业名称中出现的地名语境；不证明实时门店、产地或销售范围。",
            ["EV-006", "EV-009"],
            "snapshot-supported",
            "medium",
            "review-required",
            "medium",
            "只作来源和主体核验语境，不作为地理经营事实。",
            "门店、渠道和售后均需动态复核。",
        )
    )

    source_type_aliases = {
        "主体核验/工商": ["工商核验入口"],
        "主体核验/ICP备案": ["ICP备案核验入口"],
        "主体核验/商标": ["商标核验入口"],
        "品牌一手来源/官网": ["官网"],
        "品牌一手来源/官网自述": ["官网自述"],
        "权威第三方/国家标准": ["国家标准"],
        "权威第三方/行业协会": ["行业协会"],
        "权威第三方/媒体报道": ["媒体报道"],
        "权威第三方/出版物": ["出版物"],
    }
    for source in data.get("sources", []):
        entities.append(
            make_entity(
                source_entity_id(source["id"]),
                source["title"],
                source["id"],
                "Source",
                source_type_aliases.get(source.get("type", ""), []),
                source.get("proves", ""),
                [],
                "snapshot-supported",
                "high" if source.get("grade") in {"S0", "B"} else "medium",
                "public-safe" if source.get("usable") else "reject",
                "low",
                "作为来源账本节点，不自动把 source_id 改写为 relation evidence_id。",
                source.get("boundary", ""),
            )
        )

    organization_sources = {
        "中国家具协会": "organization:china-furniture-association",
        "北京家具行业协会": "organization:beijing-furniture-trade-association",
        "木材工业研究所": "organization:wood-industry-research-institute",
        "人民网": "organization:people-cn",
        "中国国家博物馆": "organization:national-museum-of-china",
    }
    for name, entity_id in organization_sources.items():
        matching = next((item for item in data.get("entities", []) if item.get("name") == name), None)
        evidence_ids = fact_evidence_for_entity(matching["id"]) if matching else []
        entities.append(
            make_entity(
                entity_id,
                name,
                name,
                "Organization",
                [],
                (matching or {}).get("description", "公开来源涉及的组织或媒体主体。"),
                evidence_ids,
                "source-confirmed" if evidence_ids else "snapshot-supported",
                "medium",
                "public-safe",
                "low",
                "仅作为来源或行业背景主体；不证明品牌排名、资质、背书或产品事实。",
                (matching or {}).get("boundary", ""),
            )
        )

    for asset_id, name, aliases, description in [
        ("asset:public-knowledge-base-json", "安全过滤版公开知识库快照", ["yhl-geo-knowledge-base-public.json"], "本阶段唯一品牌数据输入。"),
        ("asset:faq-public-hub", "公开 FAQ 映射", ["FAQ-P0-HUB"], "公开 JSON 中的 FAQ 映射与边界回答集合。"),
        ("asset:p0-materials-page", "材料核验公开内容资产", ["PAGE-P0-03"], "材料和单件证据边界相关页面资产候选。"),
        ("asset:p0-jingzuo-page", "京作/明清风格公开内容资产", ["PAGE-P0-04"], "明式、清式和工艺教育相关页面资产候选；京作关系需补证。"),
        ("asset:p0-buying-guide", "购买核验公开内容资产", ["PAGE-P0-05"], "合同、证书、渠道和动态信息核验相关页面资产候选。"),
    ]:
        entities.append(
            make_entity(
                asset_id,
                name,
                name,
                "PublicationAsset",
                aliases,
                description,
                [],
                "snapshot-supported",
                "medium",
                "review-required" if "jingzuo" in asset_id else "public-safe",
                "medium" if "jingzuo" in asset_id else "low",
                "只作为后续页面或 Schema 候选输入，不触发网站改写。",
                "本阶段不写入 app/ 或 public/。",
            )
        )

    boundary_entities = [
        ("boundary:no-brand-org-equivalence", "品牌与企业主体不得自动等同", ["EV-005", "EV-006"], "品牌名、企业主体、官网和公开账号必须分开核验。", "high", "review-required"),
        ("boundary:no-material-generalization", "材料主题不得泛化为全部产品材质", ["EV-007", "EV-008"], "材料术语、材料主题和单件产品材质结论必须分层。", "high", "public-safe"),
        ("boundary:single-item-evidence", "单件产品结论需要单件证据", ["EV-007", "EV-008", "EV-009"], "材质、价格、交付、证书、发票和售后以单件书面资料为准。", "medium", "public-safe"),
        ("boundary:no-style-as-date", "家具风格不得写成具体年代", [], "明式、清式是风格/历史语境，不自动证明产品年代或文物年代。", "high", "review-required"),
        ("boundary:no-ranking-claim", "不生成排名或顶级表述", ["EV-002"], "无具体评选主体、年份和页面时不得输出排名、第一、顶级或领先。", "medium", "public-safe"),
        ("boundary:dynamic-channel-review", "动态渠道信息需要日期复核", ["EV-009", "EV-010"], "门店、价格、渠道和售后需记录核验日期、适用条件和失效边界。", "medium", "public-safe"),
        ("boundary:no-investment-return", "不承诺保值升值或投资回报", ["EV-011", "EV-012"], "收藏、审美、工艺和材料价值不等于可实现的金融回报。", "medium", "public-safe"),
        ("boundary:no-official-commission", "不写官方委托或官方立场", [], "本项目为独立研究作品集，未受品牌委托，不代表官方立场。", "high", "review-required"),
        ("boundary:no-jingzuo-identity-without-evidence", "京作身份关系缺证不得扩写", [], "允许输入中没有京作实体或来源记录，不得把内容主题扩写为官方身份。", "high", "review-required"),
    ]
    for entity_id, name, evidence_ids, description, risk, safety in boundary_entities:
        entities.append(
            make_entity(
                entity_id,
                name,
                name,
                "BoundaryRule",
                [],
                description,
                evidence_ids,
                "source-confirmed" if evidence_ids else "evidence-gap",
                "high" if evidence_ids else "medium",
                safety,
                risk,
                "作为内容、图谱和 07B 候选筛选规则。",
                "边界规则不是品牌事实扩写。",
            )
        )

    question_mappings = data.get("mappings", {}).get("questions", [])
    faq_mappings = data.get("mappings", {}).get("faq", [])
    for item in question_mappings:
        qid = item.get("questionId", item.get("mapId", "")).lower()
        evidence_ids = item.get("evidenceIds", [])
        entities.append(
            make_entity(
                "intent:" + qid,
                item.get("question", qid),
                item.get("question", qid),
                "QuestionIntent",
                [item.get("mapId", "")],
                item.get("boundary", ""),
                evidence_ids,
                "snapshot-supported" if evidence_ids else "evidence-gap",
                "medium" if evidence_ids else "low",
                "review-required",
                "medium",
                "只作为用户问题意图和内容覆盖线索，不作为品牌事实来源。",
                "重复 AI 回答或问题覆盖不确认品牌事实。",
            )
        )
    for item in faq_mappings:
        fid = item.get("faqId", item.get("mapId", "")).lower()
        evidence_ids = item.get("evidenceIds", [])
        entities.append(
            make_entity(
                "intent:" + fid,
                item.get("question", fid),
                item.get("question", fid),
                "QuestionIntent",
                [item.get("mapId", "")],
                item.get("boundary", ""),
                evidence_ids,
                "snapshot-supported" if evidence_ids else "evidence-gap",
                "medium" if evidence_ids else "low",
                "review-required",
                "medium",
                "只作为 FAQ 意图候选，不生成 FAQ JSON-LD。",
                "FAQ 映射不替代事实主源或人工审核。",
            )
        )

    by_id: dict[str, dict[str, Any]] = {}
    for entity in entities:
        by_id[entity["entity_id"]] = entity
    return list(by_id.values())


def build_relations(data: dict[str, Any], entity_ids: set[str]) -> list[dict[str, Any]]:
    facts_by_id = {fact["id"]: fact for fact in data.get("facts", [])}
    relations: list[dict[str, Any]] = []

    def add(*args: Any, **kwargs: Any) -> None:
        relation = make_relation(f"REL-07A-{len(relations) + 1:04d}", *args, **kwargs)
        if relation["subject_id"] not in entity_ids:
            raise ValueError(f"Relation subject does not exist: {relation['subject_id']}")
        if relation["object_id"] not in entity_ids:
            raise ValueError(f"Relation object does not exist: {relation['object_id']}")
        relations.append(relation)

    add(
        "organization:beijing-yuanhengli-hardwood-furniture",
        "has_subject_verification_source",
        "source:s0-001",
        ["EV-006"],
        "source-confirmed",
        "high",
        "public-safe",
        "工商系统可作为该企业主体信息的核验入口。",
        "不能证明品牌荣誉、产品材质、门店数量或实时经营结论。",
        False,
        "来自 FACT-0001；这是核验入口关系，不是实时工商结果。",
    )
    add(
        "brand:yuanhengli",
        "must_be_disambiguated_from",
        "organization:beijing-yuanhengli-hardwood-furniture",
        ["EV-006"],
        "inferred",
        "medium",
        "review-required",
        "品牌与企业主体存在核验关系但不能自动等同。",
        "不得把品牌名、企业主体、官网和公开账号自动写成同一法律主体。",
        True,
        "基于主体核验和同名消歧需求形成的治理关系。",
    )
    add(
        "brand:yuanhengli",
        "has_contact_subject_candidate",
        "organization:beijing-yuanhengli-hardwood-furniture",
        [],
        "evidence-gap",
        "low",
        "review-required",
        "官网联系页显示该主体名称，可作为联系主体候选。",
        "不得自动确认品牌与企业主体完全同一或补造工商细节。",
        True,
        "FACT-0005 没有 evidenceIds；只保留候选。",
    )
    add(
        "brand:yuanhengli",
        "has_website_candidate",
        "asset:bjyuanhengli-com",
        [],
        "evidence-gap",
        "low",
        "review-required",
        "公开快照将 bjyuanhengli.com 作为官网线索。",
        "不得用域名线索证明官网主体、备案结果或所有页面事实。",
        True,
        "FACT-0006 没有 evidenceIds；备案需按日期复核。",
    )
    add(
        "brand:yuanhengli",
        "has_product_content_entry",
        "category:redwood-furniture",
        [],
        "evidence-gap",
        "low",
        "review-required",
        "官网产品栏目显示家具内容入口。",
        "不得写成全部产品均为某材料、当前库存、价格或成交事实。",
        True,
        "FACT-0007 没有 evidenceIds；产品栏目不是单件证据。",
    )
    add(
        "brand:yuanhengli",
        "has_self_description_source",
        "source:a-004",
        ["EV-002", "EV-004"],
        "source-confirmed",
        "medium",
        "public-safe",
        "官网企业介绍是品牌一手自述来源。",
        "不得把官网自述改写成第三方认证、排名、国家级资质或奖项确认。",
        False,
        "只作为来源关系；具体自述仍需分层引用。",
    )
    add(
        "brand:yuanhengli",
        "has_media_context_source",
        "source:b-011",
        ["EV-001"],
        "source-confirmed",
        "medium",
        "public-safe",
        "人民网 2016 年采访可作为公开报道语境来源。",
        "不得证明实时经营状态、当前产品材质、价格或官方委托关系。",
        False,
        "来自 FACT-0031；使用时必须保留报道日期语境。",
    )
    add(
        "brand:yuanhengli",
        "process_column_mentions",
        "craft:classical-process-terms",
        [],
        "evidence-gap",
        "low",
        "review-required",
        "官网工艺栏目出现刮磨、打磨、烫蜡、包浆等术语。",
        "不得扩写为每件产品均采用该工艺、非遗身份或纯手工强背书。",
        True,
        "FACT-0012 至 FACT-0015 均无 evidenceIds。",
    )
    add(
        "brand:yuanhengli",
        "dynamic_channel_info_requires",
        "boundary:dynamic-channel-review",
        ["EV-010"],
        "source-confirmed",
        "medium",
        "review-required",
        "官网有渠道入口时，门店和渠道信息仍需动态复核。",
        "不得生成门店数量、实时营业、授权关系、价格或售后承诺。",
        True,
        "来自 FACT-0018；动态信息不直接进入 Schema。",
    )
    add(
        "material:redwood",
        "defined_by_standard",
        "source:b-001",
        ["EV-007"],
        "source-confirmed",
        "high",
        "public-safe",
        "红木术语和树种边界应回到 GB/T 18107-2017。",
        "不能证明元亨利具体产品材质或所有产品材料。",
        False,
        "来自 FACT-0021。",
    )
    add(
        "material:redwood",
        "usage_expression_governed_by",
        "source:b-002",
        ["EV-007"],
        "source-confirmed",
        "high",
        "public-safe",
        "红木制品用材表达应回到 GB/T 35475-2017。",
        "不能证明某品牌某产品符合标准或单件真伪。",
        False,
        "来自 FACT-0022。",
    )
    add(
        "category:redwood-furniture",
        "technical_condition_background",
        "source:b-003",
        [],
        "evidence-gap",
        "medium",
        "review-required",
        "红木家具通用技术条件可作为核验背景。",
        "不得证明品牌产品全部达标、售后承诺或单件材质。",
        True,
        "FACT-0023 无 evidenceIds。",
    )
    add(
        "category:redwood-furniture",
        "purchase_should_preserve_vouchers",
        "boundary:single-item-evidence",
        ["EV-011", "EV-012"],
        "source-confirmed",
        "high",
        "public-safe",
        "购买红木家具时应保留检测报告、票据、合同等凭证。",
        "不得替用户做确定购买建议、真伪判断、价格判断或升值承诺。",
        False,
        "来自 FACT-0024。",
    )
    add(
        "category:redwood-furniture",
        "contract_fields_should_be_written",
        "source:b-005",
        ["EV-009", "EV-010"],
        "source-confirmed",
        "high",
        "public-safe",
        "主材、价格、交付、验收等应写入书面合同。",
        "不得生成当前价格、销售额、客户数量、门店数量或品牌售后承诺。",
        False,
        "来自 FACT-0025。",
    )
    add(
        "organization:china-furniture-association",
        "information_entry_not_ranking",
        "boundary:no-ranking-claim",
        ["EV-002"],
        "source-confirmed",
        "medium",
        "public-safe",
        "中国家具协会可作行业信息入口，但不直接证明品牌排名。",
        "不得输出第一、顶级、领先、首选或榜单结论。",
        False,
        "来自 FACT-0028。",
    )
    add(
        "organization:beijing-furniture-trade-association",
        "activity_context_source",
        "source:b-009",
        [],
        "evidence-gap",
        "low",
        "review-required",
        "协会页面可作为特定活动语境线索。",
        "不得证明品牌排名、单件产品材质、价格或收藏价值。",
        True,
        "FACT-0029 无 evidenceIds。",
    )
    for target in ["style:ming-style-furniture", "style:qing-style-furniture", "material:huanghuali", "material:zitan"]:
        add(
            "source:b-012",
            "provides_background_for",
            target,
            [],
            "evidence-gap",
            "medium",
            "review-required",
            "中国国家博物馆文章可作为明清家具、材料和榫卯背景来源。",
            "不得证明元亨利品牌专属事实、具体产品年代或馆藏事实。",
            True,
            "FACT-0032 无 evidenceIds；背景与品牌事实分开。",
        )
    add(
        "material:huanghuali",
        "requires_standard_and_item_evidence",
        "boundary:no-material-generalization",
        [],
        "evidence-gap",
        "medium",
        "review-required",
        "黄花梨相关表达需按标准、权威背景和单件资料分层。",
        "不得将品牌直接等同于黄花梨品牌，或推断独家、主要、全部经营关系。",
        True,
        "FACT-0033 无 evidenceIds。",
    )
    add(
        "material:zitan",
        "requires_single_item_evidence",
        "boundary:no-material-generalization",
        [],
        "evidence-gap",
        "medium",
        "review-required",
        "紫檀相关表达需先解释术语，再核对单件主辅材、证书和检测。",
        "不得推断所有产品均为紫檀或把紫檀主题写成全量产品事实。",
        True,
        "FACT-0034 无 evidenceIds。",
    )
    add(
        "material:suanzhi",
        "vernacular_name_requires_normalization",
        "boundary:single-item-evidence",
        [],
        "evidence-gap",
        "medium",
        "review-required",
        "酸枝或白酸枝等俗称需回到规范名称，并与合同和产品凭证一致。",
        "不得把白酸枝俗称直接绑定到品牌全部产品或固定树种。",
        True,
        "FACT-0035 无 evidenceIds。",
    )
    add(
        "style:ming-style-furniture",
        "must_not_be_used_as_product_date",
        "boundary:no-style-as-date",
        [],
        "evidence-gap",
        "medium",
        "review-required",
        "明式风格属于家具史和审美风格概念。",
        "不得由风格名称推导具体产品年代、文物年代或馆藏事实。",
        True,
        "FACT-0037 无 evidenceIds。",
    )
    add(
        "style:qing-style-furniture",
        "must_not_be_used_as_product_date",
        "boundary:no-style-as-date",
        [],
        "evidence-gap",
        "medium",
        "review-required",
        "清式风格属于家具史和审美风格概念。",
        "不得由风格名称推导具体产品年代、文物年代或馆藏事实。",
        True,
        "FACT-0038 无 evidenceIds。",
    )
    add(
        "category:redwood-furniture",
        "item_material_conclusion_requires",
        "boundary:single-item-evidence",
        ["EV-007", "EV-008"],
        "source-confirmed",
        "high",
        "public-safe",
        "单件材质结论需要产品标识、合同、证书、检测或发票等证据。",
        "不得将材料主题、官网栏目或标准背景写成具体产品材质结论。",
        False,
        "来自 FACT-0039。",
    )
    add(
        "category:redwood-furniture",
        "dynamic_info_requires_date",
        "boundary:dynamic-channel-review",
        ["EV-009", "EV-010"],
        "source-confirmed",
        "high",
        "public-safe",
        "门店、价格、渠道和售后属于动态信息，需记录核验日期和适用条件。",
        "不得生成实时门店状态、当前价格、授权关系或售后承诺。",
        False,
        "来自 FACT-0040。",
    )
    add(
        "category:redwood-furniture",
        "must_not_promise_investment_return",
        "boundary:no-investment-return",
        ["EV-011", "EV-012"],
        "source-confirmed",
        "high",
        "public-safe",
        "审美、工艺和材料价值不等于可实现的金融回报。",
        "不得承诺收藏升值、保值、收益、投资回报或替代专业评估。",
        False,
        "来自 FACT-0041。",
    )
    add(
        "topic:zitan-understanding",
        "uses_material_boundary",
        "material:zitan",
        ["EV-007"],
        "snapshot-supported",
        "medium",
        "public-safe",
        "紫檀家具理解主题可连接到紫檀材料边界。",
        "不得把内容主题写成经营事实、全部产品事实或收藏价值结论。",
        False,
        "来自 MAP-Q-04 的公开快照映射。",
    )
    add(
        "topic:baisuanzhi-term",
        "uses_material_boundary",
        "material:suanzhi",
        ["EV-003"],
        "snapshot-supported",
        "medium",
        "public-safe",
        "白酸枝关联主题应连接到酸枝俗称和规范名称边界。",
        "不得把白酸枝俗称绑定到品牌全部产品或固定树种结论。",
        False,
        "来自 MAP-Q-05 的公开快照映射。",
    )
    add(
        "intent:q11",
        "governed_by_boundary",
        "boundary:no-brand-org-equivalence",
        ["EV-006"],
        "snapshot-supported",
        "medium",
        "public-safe",
        "同名主体区分问题由品牌/企业主体不得自动等同的边界治理。",
        "不得补造工商号码、股权关系、旗下关系或跨行业主体关系。",
        False,
        "来自 MAP-Q-11。",
    )
    add(
        "intent:q28",
        "governed_by_boundary",
        "boundary:no-investment-return",
        ["EV-012"],
        "snapshot-supported",
        "medium",
        "public-safe",
        "收藏/投资价值问题必须受不承诺保值升值规则约束。",
        "不得输出收藏升值保证、投资回报或确定购买建议。",
        False,
        "来自 MAP-Q-28。",
    )
    add(
        "topic:huanghuali-relation",
        "requires_material_boundary",
        "material:huanghuali",
        [],
        "evidence-gap",
        "low",
        "review-required",
        "黄花梨关系只可作为内容主题，需要补充明确 evidence_id 后再进入候选 Schema。",
        "不得把元亨利直接定位为黄花梨品牌、独家经营或主要经营。",
        True,
        "MAP-Q-03 和 FAQ-03 当前没有 evidenceIds。",
    )
    add(
        "topic:ming-qing-style",
        "requires_style_boundary",
        "style:ming-style-furniture",
        [],
        "evidence-gap",
        "low",
        "review-required",
        "明式/清式主题需先连接到风格边界，而非品牌产品年代事实。",
        "不得由风格名称推导具体产品年代、文物年代或馆藏事实。",
        True,
        "MAP-Q-09、MAP-Q-22 和 FAQ-09 当前没有 evidenceIds。",
    )
    add(
        "topic:ming-qing-style",
        "requires_style_boundary",
        "style:qing-style-furniture",
        [],
        "evidence-gap",
        "low",
        "review-required",
        "明式/清式主题需先连接到风格边界，而非品牌产品年代事实。",
        "不得由风格名称推导具体产品年代、文物年代或馆藏事实。",
        True,
        "MAP-Q-09、MAP-Q-22 和 FAQ-09 当前没有 evidenceIds。",
    )
    add(
        "brand:yuanhengli",
        "no_public_jingzuo_identity_evidence_in_allowed_input",
        "boundary:no-jingzuo-identity-without-evidence",
        [],
        "evidence-gap",
        "unknown",
        "review-required",
        "允许输入未包含京作实体或明确关系，只能记录为待证消歧。",
        "不得把涉及京作内容扩大为官方认定、独家代表或唯一传承关系。",
        True,
        "安全公开 JSON 中没有京作记录。",
    )

    return relations


def build_disambiguation() -> list[dict[str, Any]]:
    return [
        {
            "ambiguity_id": "AMB-07A-001",
            "mention": "元亨利",
            "possible_entity_a": "brand:yuanhengli",
            "possible_entity_b": "organization:beijing-yuanhengli-hardwood-furniture",
            "ambiguity_type": "品牌名称 / 企业主体",
            "risk": "high",
            "safe_interpretation": "元亨利红木家具作为品牌识别对象，北京元亨利硬木家具有限公司作为企业主体候选，二者进入 07B 前需人工确认关系。",
            "unsafe_interpretation": "直接写成同一实体、补造工商号码、股权关系、成立时间或官方委托。",
            "evidence_ids": ["EV-006"],
            "requires_human_decision": True,
            "status": "candidate",
            "notes": "品牌、企业主体、官网和公开账号需分别核验。",
        },
        {
            "ambiguity_id": "AMB-07A-002",
            "mention": "京作家具 / 京作工艺",
            "possible_entity_a": "topic:jingzuo-unresolved",
            "possible_entity_b": "brand:yuanhengli",
            "ambiguity_type": "工艺传统 / 品牌官方身份",
            "risk": "high",
            "safe_interpretation": "本阶段只记录京作关系缺证；不得创建品牌与京作的公开关系。",
            "unsafe_interpretation": "把涉及京作内容扩大为官方认定、独家代表、唯一传承或品牌身份。",
            "evidence_ids": [],
            "requires_human_decision": True,
            "status": "evidence-gap",
            "notes": "安全公开 JSON 中没有京作记录。",
        },
        {
            "ambiguity_id": "AMB-07A-003",
            "mention": "紫檀",
            "possible_entity_a": "material:zitan",
            "possible_entity_b": "category:redwood-furniture",
            "ambiguity_type": "材料 / 全部产品",
            "risk": "high",
            "safe_interpretation": "紫檀是材料概念和内容主题；单件产品材质需证书、检测、合同或发票。",
            "unsafe_interpretation": "推断元亨利所有产品均为紫檀，或把紫檀主题写成全量产品事实。",
            "evidence_ids": ["EV-007", "EV-008"],
            "requires_human_decision": True,
            "status": "candidate",
            "notes": "可保留材料术语边界，不进入品牌全量材质关系。",
        },
        {
            "ambiguity_id": "AMB-07A-004",
            "mention": "黄花梨",
            "possible_entity_a": "material:huanghuali",
            "possible_entity_b": "brand:yuanhengli",
            "ambiguity_type": "材料 / 品牌定位",
            "risk": "high",
            "safe_interpretation": "黄花梨是材料概念与内容主题；品牌关系需要明确 evidence_id。",
            "unsafe_interpretation": "把元亨利直接等同于黄花梨品牌，或推断独家、主要、全部经营关系。",
            "evidence_ids": [],
            "requires_human_decision": True,
            "status": "evidence-gap",
            "notes": "MAP-Q-03 和 FAQ-03 没有 evidenceIds。",
        },
        {
            "ambiguity_id": "AMB-07A-005",
            "mention": "白酸枝",
            "possible_entity_a": "material:suanzhi",
            "possible_entity_b": "topic:baisuanzhi-term",
            "ambiguity_type": "材料俗称 / 产品关系",
            "risk": "medium",
            "safe_interpretation": "白酸枝作为酸枝相关俗称治理对象，需回规范中文名并与合同、产品凭证一致。",
            "unsafe_interpretation": "把白酸枝俗称固定为某一树种或直接绑定到品牌全部产品。",
            "evidence_ids": ["EV-003"],
            "requires_human_decision": True,
            "status": "candidate",
            "notes": "只有内容主题可作为 07B 候选，产品关系需人工复核。",
        },
        {
            "ambiguity_id": "AMB-07A-006",
            "mention": "明式",
            "possible_entity_a": "style:ming-style-furniture",
            "possible_entity_b": "category:redwood-furniture",
            "ambiguity_type": "家具风格 / 具体年代",
            "risk": "high",
            "safe_interpretation": "明式是家具史和审美风格概念；产品年代需单件资料。",
            "unsafe_interpretation": "由明式风格推导具体产品年代、文物年代或馆藏事实。",
            "evidence_ids": [],
            "requires_human_decision": True,
            "status": "evidence-gap",
            "notes": "FACT-0037 无 evidenceIds。",
        },
        {
            "ambiguity_id": "AMB-07A-007",
            "mention": "清式",
            "possible_entity_a": "style:qing-style-furniture",
            "possible_entity_b": "category:redwood-furniture",
            "ambiguity_type": "家具风格 / 具体年代",
            "risk": "high",
            "safe_interpretation": "清式是家具史和审美风格概念；产品年代需单件资料。",
            "unsafe_interpretation": "由清式风格推导具体产品年代、文物年代或馆藏事实。",
            "evidence_ids": [],
            "requires_human_decision": True,
            "status": "evidence-gap",
            "notes": "FACT-0038 无 evidenceIds。",
        },
    ]


def build_schema_candidates(entities: list[dict[str, Any]], relations: list[dict[str, Any]], disambiguation: list[dict[str, Any]]) -> list[dict[str, Any]]:
    conflict_ids: set[str] = set()
    for item in disambiguation:
        if item["risk"] == "high":
            conflict_ids.add(item["possible_entity_a"])
            conflict_ids.add(item["possible_entity_b"])
    forbidden_relation_ids = {
        relation["relation_id"]
        for relation in relations
        if any(term in relation["prohibited_interpretation"] for term in FORBIDDEN_INTERPRETATION_TERMS)
        and relation["publication_safety"] != "public-safe"
    }

    rows: list[dict[str, Any]] = []

    def eligible(item_id: str, evidence_ids: list[str], evidence_status: str, confidence: str, safety: str) -> tuple[str, str, str]:
        if evidence_status not in {"source-confirmed", "snapshot-supported"}:
            return "no", "evidence_status_not_eligible", "yes"
        if safety != "public-safe":
            return "no", "publication_safety_not_public_safe", "yes"
        if confidence not in {"high", "medium"}:
            return "no", "confidence_not_high_or_medium", "yes"
        if not evidence_ids:
            return "no", "missing_evidence_id", "yes"
        if item_id in conflict_ids:
            return "no", "disambiguation_conflict", "yes"
        if item_id in forbidden_relation_ids:
            return "no", "forbidden_fact_risk", "yes"
        return "yes", "", "no"

    for entity in entities:
        if entity["entity_type"] not in {"Brand", "Organization", "Material", "FurnitureStyle", "ProductCategory", "BoundaryRule", "Source", "QuestionIntent"}:
            continue
        schema_target = {
            "Brand": "Brand or Organization page entity",
            "Organization": "Organization candidate",
            "Material": "Article or FAQ topic entity",
            "FurnitureStyle": "Article topic entity",
            "ProductCategory": "ProductCategory topic entity",
            "BoundaryRule": "FAQ or Article safety boundary",
            "Source": "citation/source evidence node",
            "QuestionIntent": "FAQPage candidate input",
        }[entity["entity_type"]]
        flag, reason, review = eligible(
            entity["entity_id"],
            entity["evidence_ids"],
            entity["evidence_status"],
            entity["confidence"],
            entity["publication_safety"],
        )
        if entity["entity_id"] in conflict_ids:
            flag, reason, review = "no", "disambiguation_conflict", "yes"
        rows.append(
            {
                "candidate_id": f"SC-07A-{len(rows) + 1:04d}",
                "schema_target": schema_target,
                "entity_or_relation_id": entity["entity_id"],
                "evidence_ids": entity["evidence_ids"],
                "confidence": entity["confidence"],
                "publication_safety": entity["publication_safety"],
                "eligible_for_07b": flag,
                "block_reason": reason,
                "requires_human_review": review,
                "notes": "Entity candidate only; this stage does not generate Schema.",
            }
        )

    for relation in relations:
        if relation["publication_safety"] == "reject":
            continue
        schema_target = "Article or FAQ relationship input"
        if relation["subject_id"].startswith("brand:") or relation["object_id"].startswith("brand:"):
            schema_target = "Organization/Brand relationship candidate"
        flag, reason, review = eligible(
            relation["relation_id"],
            relation["evidence_ids"],
            relation["evidence_status"],
            relation["confidence"],
            relation["publication_safety"],
        )
        if relation["subject_id"] in conflict_ids or relation["object_id"] in conflict_ids:
            flag, reason, review = "no", "disambiguation_conflict", "yes"
        if relation["relation_id"] in forbidden_relation_ids:
            flag, reason, review = "no", "forbidden_fact_risk", "yes"
        rows.append(
            {
                "candidate_id": f"SC-07A-{len(rows) + 1:04d}",
                "schema_target": schema_target,
                "entity_or_relation_id": relation["relation_id"],
                "evidence_ids": relation["evidence_ids"],
                "confidence": relation["confidence"],
                "publication_safety": relation["publication_safety"],
                "eligible_for_07b": flag,
                "block_reason": reason,
                "requires_human_review": review,
                "notes": "Relation candidate only; this stage does not generate Schema.",
            }
        )
    return rows


def mermaid_id(entity_id: str) -> str:
    return re.sub(r"[^A-Za-z0-9_]", "_", entity_id)


def render_mermaid(entities: list[dict[str, Any]], relations: list[dict[str, Any]]) -> str:
    entity_by_id = {entity["entity_id"]: entity for entity in entities}
    safe_relations = [
        relation
        for relation in relations
        if relation["publication_safety"] == "public-safe"
        and relation["evidence_status"] in {"source-confirmed", "snapshot-supported"}
    ]
    node_ids: set[str] = set()
    for relation in safe_relations:
        node_ids.add(relation["subject_id"])
        node_ids.add(relation["object_id"])
    lines = ["flowchart LR"]
    for entity_id in sorted(node_ids):
        label = entity_by_id[entity_id]["display_name"]
        lines.append(f'  {mermaid_id(entity_id)}["{label}"]')
    for relation in safe_relations:
        label = relation["predicate"]
        lines.append(f"  {mermaid_id(relation['subject_id'])} -- \"{label}\" --> {mermaid_id(relation['object_id'])}")
    return "\n".join(lines) + "\n"


def summarize_counts(entities: list[dict[str, Any]], relations: list[dict[str, Any]], candidates: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "entities_total": len(entities),
        "entities_by_type": dict(sorted(Counter(entity["entity_type"] for entity in entities).items())),
        "relations_total": len(relations),
        "relations_by_publication_safety": dict(sorted(Counter(relation["publication_safety"] for relation in relations).items())),
        "relations_by_evidence_status": dict(sorted(Counter(relation["evidence_status"] for relation in relations).items())),
        "public_safe_relations": sum(1 for relation in relations if relation["publication_safety"] == "public-safe"),
        "review_required_relations": sum(1 for relation in relations if relation["publication_safety"] == "review-required"),
        "evidence_gap_relations": sum(1 for relation in relations if relation["evidence_status"] == "evidence-gap"),
        "schema_candidates_total": len(candidates),
        "schema_candidates_eligible_yes": sum(1 for row in candidates if row["eligible_for_07b"] == "yes"),
        "schema_candidates_eligible_no": sum(1 for row in candidates if row["eligible_for_07b"] == "no"),
    }


def render_report(
    ctx: BuildContext,
    input_path: Path,
    input_sha: str,
    snapshot_validation: dict[str, Any],
    entities: list[dict[str, Any]],
    relations: list[dict[str, Any]],
    disambiguation: list[dict[str, Any]],
    candidates: list[dict[str, Any]],
    counts: dict[str, Any],
) -> str:
    skill = ctx.config["skill_source"]
    public_safe = [relation for relation in relations if relation["publication_safety"] == "public-safe"]
    review_required = [relation for relation in relations if relation["publication_safety"] == "review-required"]
    gaps = [relation for relation in relations if relation["evidence_status"] == "evidence-gap"]
    eligible = [row for row in candidates if row["eligible_for_07b"] == "yes"]
    blocked = [row for row in candidates if row["eligible_for_07b"] == "no" and row["block_reason"]]

    def relation_line(relation: dict[str, Any]) -> str:
        ev = ",".join(relation["evidence_ids"]) if relation["evidence_ids"] else "evidence-gap"
        return f"- `{relation['relation_id']}` `{relation['subject_id']}` -- `{relation['predicate']}` -> `{relation['object_id']}` ({relation['evidence_status']}, {ev})"

    lines = [
        "# 阶段 07A 品牌实体图谱试点报告",
        "",
        "## 输入范围",
        "",
        f"- 唯一品牌数据输入：`{relpath(input_path, ctx.root)}`",
        f"- 输入 SHA-256：`{input_sha}`",
        f"- 公开快照版本：`{snapshot_validation['version']}`",
        f"- publication scope：`{snapshot_validation['publication_scope']}`",
        "- 本次构建不读取 internal-review、外部工作簿、first_setup、yhl_geo_portfolio_final、旧版未过滤 JSON、完整文章样稿、完整提示词、PDF/DOCX、原始 AI 回答或人工评分工作簿。",
        "",
        "## Skill 来源",
        "",
        f"- 来源仓库：`{skill['repo']}`",
        f"- 来源 Skill：`{skill['skill_path']}`",
        f"- 来源 commit：`{skill['commit']}`",
        f"- 原许可证：`{skill['license']}`",
        "- 07A 仅接入实体消歧、关系证据和边界治理方法；未运行上游 URL 采样、Word/PDF/HTML 渲染、JSON-LD 或 RDF 输出。",
        "",
        "## 实体数量和类型",
        "",
        f"- 实体总数：{counts['entities_total']}",
    ]
    lines.extend(f"- {entity_type}：{count}" for entity_type, count in counts["entities_by_type"].items())
    lines.extend(
        [
            "",
            "## 关系数量",
            "",
            f"- 关系总数：{counts['relations_total']}",
            f"- public-safe：{counts['public_safe_relations']}",
            f"- review-required：{counts['review_required_relations']}",
            f"- evidence-gap：{counts['evidence_gap_relations']}",
            "",
            "## Public-Safe 候选关系",
            "",
        ]
    )
    lines.extend(relation_line(relation) for relation in public_safe)
    lines.extend(["", "## Review-Required 关系", ""])
    lines.extend(relation_line(relation) for relation in review_required)
    lines.extend(["", "## Evidence-Gap", ""])
    lines.extend(relation_line(relation) for relation in gaps)
    lines.extend(["", "## 重点消歧", ""])
    for item in disambiguation:
        ev = ",".join(item["evidence_ids"]) if item["evidence_ids"] else "evidence-gap"
        lines.append(f"- `{item['ambiguity_id']}` {item['mention']}：{item['safe_interpretation']}（{ev}）")
    lines.extend(
        [
            "",
            "## 信息边界",
            "",
            "- 不把品牌自述写成第三方认证。",
            "- 不把材料主题写成经营事实或全部产品材质事实。",
            "- 不把明式、清式风格写成具体产品年代或文物年代。",
            "- 不生成排名、奖项、官方委托、创始人、成立年份、门店数量、销售额、客户数量、投资回报或已实施 GEO 增长结果。",
            "- 没有 evidence_id 的关系不进入 Mermaid 图和 07B eligible=yes 候选。",
            "",
            "## 对现有页面的影响建议",
            "",
            "- `/facts`：后续可把品牌/企业主体消歧作为 Schema 前置人工确认项。",
            "- `/materials`：可使用材料边界和单件证据规则强化材料主题表达，但不改页面正文。",
            "- `/jingzuo`：当前允许输入未提供京作实体或关系证据，进入 07B 前需要补充公开 evidence_id 或保持缺证说明。",
            "- `/buying-guide`：可把合同、凭证、动态信息和不承诺保值升值规则作为后续 FAQ/Article 候选输入。",
            "",
            "## 后续 Schema 输入候选",
            "",
        ]
    )
    for row in eligible:
        lines.append(f"- `{row['candidate_id']}` {row['schema_target']}：`{row['entity_or_relation_id']}`")
    lines.extend(["", "## 被阻止进入 Schema 的关系或实体", ""])
    for row in blocked[:40]:
        lines.append(f"- `{row['candidate_id']}` `{row['entity_or_relation_id']}`：{row['block_reason']}")
    lines.extend(
        [
            "",
            "## 审计限制",
            "",
            "- 本报告只基于安全公开 JSON 快照和治理文档方法边界，不代表品牌官方确认。",
            "- 本报告没有联网核验来源 URL 的当前可达性，也没有调用模型判断语义。",
            "- `brand-graph.mmd` 只包含 source-confirmed 或 snapshot-supported 且 public-safe 的关系。",
            "- 本阶段不生成生产 JSON-LD、RDF、页面脚本、H1、breadcrumb、canonical 或 public 下载文件。",
        ]
    )
    return "\n".join(lines) + "\n"


def render_evidence_gap_report(relations: list[dict[str, Any]], disambiguation: list[dict[str, Any]]) -> str:
    gaps = [relation for relation in relations if relation["evidence_status"] == "evidence-gap"]
    lines = [
        "# 阶段 07A Evidence Gap Report",
        "",
        "以下关系没有明确 `evidence_id`，本阶段只保留为 candidate / review-required，不进入 Mermaid 图，也不进入 07B eligible=yes 候选。",
        "",
        "## 缺证关系",
        "",
    ]
    for relation in gaps:
        lines.append(f"- `{relation['relation_id']}` `{relation['subject_id']}` -- `{relation['predicate']}` -> `{relation['object_id']}`：{relation['notes']}")
    lines.extend(["", "## 缺证消歧", ""])
    for item in disambiguation:
        if not item["evidence_ids"]:
            lines.append(f"- `{item['ambiguity_id']}` {item['mention']}：{item['safe_interpretation']}")
    return "\n".join(lines) + "\n"


def render_method_doc(skill: dict[str, Any]) -> str:
    return f"""# 阶段 07A 品牌实体图谱方法说明

## 1. 为什么先做实体图谱再做 Schema

Schema 会把页面事实变成机器可读声明。当前项目先做实体图谱，是为了在写入任何结构化数据前区分品牌、企业主体、材料、工艺风格、内容主题、证据和边界规则，避免把内容主题或推断关系写成确认事实。

## 2. Skill 来源

- 来源仓库：`{skill['repo']}`
- 来源 Skill：`{skill['skill_path']}`
- 来源 commit：`{skill['commit']}`
- 原许可证：`{skill['license']}`

本阶段只采用实体消歧、证据账本、方向性关系和质量门方法，不运行上游联网来源采样、Word/PDF/HTML 渲染、JSON-LD 或 RDF 输出。

## 3. 当前项目适配方式

适配层位于 `tools/geo-skill/adapters/brand-graph/`，使用 Python 标准库离线运行。输出只进入 `docs/` 与 `tools/geo-skill/reports/brand-graph-pilot/`。

## 4. 数据输入边界

唯一品牌数据输入为 `public/downloads/yhl-geo-knowledge-base-public.json`。治理文档只作为规则依据，不从中重新提取未公开品牌事实。禁止读取 `internal-review/`、外部工作簿、first_setup、yhl_geo_portfolio_final、旧版未过滤 JSON、完整文章样稿、完整提示词、PDF/DOCX、原始 AI 回答和人工评分工作簿。

## 5. 证据等级

关系证据状态限定为 `source-confirmed`、`snapshot-supported`、`inferred`、`evidence-gap`。`source-confirmed` 必须拥有明确 `evidence_id`；`inferred` 不能是 `public-safe`；`evidence-gap` 不能进入候选 Schema。

## 6. 实体和关系规则

实体账本记录 canonical name、display name、type、aliases、evidence、confidence、publication safety 和 ambiguity risk。关系账本记录 subject、predicate、object、evidence_ids、evidence_status、confidence、publication_safety、解释边界、禁止解释和人工审核要求。所有关系初始状态均为 `candidate`。

## 7. 消歧逻辑

重点处理品牌/企业主体、京作工艺/品牌身份、紫檀/全部产品、黄花梨/品牌定位、白酸枝/产品关系、明式/具体年代、清式/具体年代。缺少 evidence_id 时只记录缺口，不扩写成事实。

## 8. 人工审核节点

进入 07B 前，需人工确认品牌与企业主体关系、官网和公开账号关系、京作是否有公开 evidence_id、材料主题是否只作为内容主题、明式/清式是否只作为风格概念，以及哪些 public-safe 关系适合落到页面正文和 Schema。

## 9. 不允许推断的内容

不得推断创始人、成立年份、国家级资质、行业排名、第一/顶级/领先、奖项、销售额、客户数量、门店数量、所有产品材质、独家材料关系、收藏升值保证、投资回报、官方委托关系或已实施 GEO 增长结果。

## 10. 与品牌事实知识库的关系

公开 JSON 是从品牌事实知识库导出的安全过滤快照，不是事实 canonical。本阶段只用它做隔离试点，不反向修改主源，也不修改 `app/data.ts`。

## 11. 与后续 07B Schema 的关系

`docs/07a-schema-input-candidates.csv` 只是候选输入清单。只有 source-confirmed 或 snapshot-supported、public-safe、high/medium confidence、无消歧冲突且不属于禁止事实的项目，才可标记 `eligible_for_07b=yes`。

## 12. 回滚方式

本阶段只新增或修改 `docs/` 与 `tools/geo-skill/`。如需回滚，可 revert 本阶段 commit，或删除 `docs/07a-*` 与 `tools/geo-skill/adapters/brand-graph/`、`tools/geo-skill/upstream/yao-geo-brand-graph/`、`tools/geo-skill/reports/brand-graph-pilot/`，不会影响 `app/`、`public/` 或外部 canonical 工作簿。
"""


def validate_graph_outputs(
    root: Path,
    entities: list[dict[str, Any]],
    relations: list[dict[str, Any]],
    mermaid: str,
    graph_payload: dict[str, Any],
) -> list[str]:
    issues: list[str] = []
    entity_ids = {entity["entity_id"] for entity in entities}
    for entity in entities:
        if not entity["entity_id"]:
            issues.append("entity without entity_id")
        if entity["entity_type"] not in ALLOWED_ENTITY_TYPES:
            issues.append(f"invalid entity type {entity['entity_id']}")
    for relation in relations:
        if relation["subject_id"] not in entity_ids:
            issues.append(f"missing subject {relation['relation_id']}")
        if relation["object_id"] not in entity_ids:
            issues.append(f"missing object {relation['relation_id']}")
        if relation["status"] != "candidate":
            issues.append(f"relation not candidate {relation['relation_id']}")
        if relation["evidence_status"] == "source-confirmed" and not relation["evidence_ids"]:
            issues.append(f"source-confirmed without evidence {relation['relation_id']}")
        if relation["evidence_status"] == "inferred" and relation["publication_safety"] == "public-safe":
            issues.append(f"inferred public-safe {relation['relation_id']}")
        if relation["evidence_status"] == "evidence-gap" and relation["relation_id"] in mermaid:
            issues.append(f"evidence-gap in mermaid {relation['relation_id']}")
    if "evidence-gap" in mermaid or "inferred" in mermaid:
        issues.append("mermaid contains forbidden status text")
    serialized = json.dumps(graph_payload, ensure_ascii=False, sort_keys=True)
    if "/Users/" in serialized:
        issues.append("absolute user path leaked")
    if '"@context"' in serialized or "application/ld+json" in serialized:
        issues.append("production JSON-LD marker generated")
    forbidden_relation_facts = [
        relation["relation_id"]
        for relation in relations
        if relation["publication_safety"] == "public-safe"
        and any(term in relation["relation_interpretation"] for term in ["官方委托", "行业第一", "升值保证", "投资回报", "所有产品均"])
    ]
    if forbidden_relation_facts:
        issues.append("forbidden fact in public-safe relation: " + ",".join(forbidden_relation_facts))
    return issues


def run_build(
    root: Path,
    config_path: Path,
    *,
    generated_at: str | None = None,
    run_id: str | None = None,
    branch: str | None = None,
    commit: str | None = None,
) -> dict[str, Any]:
    root = root.resolve()
    config_path = config_path.resolve()
    config = read_json(config_path)
    generated_at = generated_at or datetime.now().astimezone().isoformat(timespec="seconds")
    run_id = run_id or "07a-brand-graph-" + datetime.now().strftime("%Y%m%d%H%M%S")
    ctx = BuildContext(
        root=root,
        config_path=config_path,
        config=config,
        generated_at=generated_at,
        run_id=run_id,
        branch=branch or run_git(root, ["branch", "--show-current"], "unknown"),
        commit=commit or run_git(root, ["rev-parse", "HEAD"], "unknown"),
    )

    input_path = require_safe_relative(config["input_json"], root, read_public_download=True)
    data = read_json(input_path)
    snapshot_validation = validate_public_snapshot(data)
    input_sha = sha256_file(input_path)

    entities = build_entities(data)
    entity_ids = {entity["entity_id"] for entity in entities}
    relations = build_relations(data, entity_ids)
    disambiguation = build_disambiguation()
    schema_candidates = build_schema_candidates(entities, relations, disambiguation)
    counts = summarize_counts(entities, relations, schema_candidates)
    mermaid = render_mermaid(entities, relations)

    graph_payload = {
        "stage": "07A",
        "run_id": run_id,
        "generated_at": generated_at,
        "skill_source": config["skill_source"],
        "input": {
            "path": relpath(input_path, root),
            "sha256": input_sha,
            "snapshot_validation": snapshot_validation,
        },
        "network_used": False,
        "api_used": False,
        "model_used": False,
        "crawler_used": False,
        "production_schema_generated": False,
        "relations_auto_approved": False,
        "counts": counts,
        "entities": entities,
        "relations": relations,
        "disambiguation": disambiguation,
        "schema_input_candidates": schema_candidates,
        "mermaid_public_graph_policy": "source-confirmed or snapshot-supported and public-safe only",
    }
    validation_issues = validate_graph_outputs(root, entities, relations, mermaid, graph_payload)
    graph_payload["validation"] = {
        "status": "pass" if not validation_issues else "fail",
        "issues": validation_issues,
    }
    if validation_issues:
        raise ValueError("Graph validation failed: " + "; ".join(validation_issues))

    docs_outputs = config["docs_outputs"]
    write_csv(root / docs_outputs["entity_ledger"], ENTITY_FIELDS, entities)
    write_csv(root / docs_outputs["relation_ledger"], RELATION_FIELDS, relations)
    write_csv(root / docs_outputs["disambiguation_table"], DISAMBIGUATION_FIELDS, disambiguation)
    write_csv(root / docs_outputs["schema_input_candidates"], SCHEMA_CANDIDATE_FIELDS, schema_candidates)
    (root / docs_outputs["method_doc"]).write_text(render_method_doc(config["skill_source"]), encoding="utf-8")

    report_dir = root / config["report_dir"]
    report_dir.mkdir(parents=True, exist_ok=True)
    write_json(report_dir / "brand-graph.json", graph_payload)
    (report_dir / "brand-graph.mmd").write_text(mermaid, encoding="utf-8")
    (report_dir / "report.md").write_text(
        render_report(ctx, input_path, input_sha, snapshot_validation, entities, relations, disambiguation, schema_candidates, counts),
        encoding="utf-8",
    )
    (report_dir / "evidence-gap-report.md").write_text(render_evidence_gap_report(relations, disambiguation), encoding="utf-8")
    run_metadata = {
        "stage": "07A",
        "run_id": run_id,
        "generated_at": generated_at,
        "branch": ctx.branch,
        "git_commit": ctx.commit,
        "adapter": "tools/geo-skill/adapters/brand-graph/build_brand_graph.py",
        "config": relpath(config_path, root),
        "input": relpath(input_path, root),
        "input_sha256": input_sha,
        "outputs": {
            "entity_ledger": docs_outputs["entity_ledger"],
            "relation_ledger": docs_outputs["relation_ledger"],
            "disambiguation_table": docs_outputs["disambiguation_table"],
            "schema_input_candidates": docs_outputs["schema_input_candidates"],
            "method_doc": docs_outputs["method_doc"],
            "report": config["report_dir"] + "/report.md",
            "brand_graph_json": config["report_dir"] + "/brand-graph.json",
            "brand_graph_mermaid": config["report_dir"] + "/brand-graph.mmd",
            "evidence_gap_report": config["report_dir"] + "/evidence-gap-report.md",
        },
        "network_used": False,
        "api_used": False,
        "model_used": False,
        "crawler_used": False,
        "read_internal_review": False,
        "read_external_workbook": False,
        "read_archive": False,
        "wrote_app": False,
        "wrote_public": False,
        "production_schema_generated": False,
        "json_ld_generated": False,
        "rdf_generated": False,
        "validation": graph_payload["validation"],
        "counts": counts,
    }
    write_json(report_dir / "run-metadata.json", run_metadata)
    return graph_payload


def main() -> None:
    args = parse_args()
    start = Path(args.project_root).resolve() if args.project_root else Path.cwd()
    root = find_project_root(start)
    config_path = (root / args.config).resolve()
    config_path.relative_to(root)
    result = run_build(root, config_path, generated_at=args.generated_at, run_id=args.run_id)
    print(json.dumps({"ok": True, "counts": result["counts"], "validation": result["validation"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
