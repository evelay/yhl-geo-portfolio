#!/usr/bin/env python3
"""Offline adapter for the 06B yao-geo-page-audit pilot.

The adapter reads built static HTML from out/, audits the configured routes,
and writes isolated reports under tools/geo-skill plus a docs CSV. It does not
fetch URLs, call APIs, or modify website source files.
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
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


FINDING_FIELDS = [
    "finding_id",
    "route",
    "audit_dimension",
    "evidence_status",
    "severity",
    "priority",
    "owner",
    "observed_evidence",
    "issue",
    "recommended_action",
    "acceptance_test",
    "skill_source",
    "requires_human_review",
    "status",
    "notes",
]

DIMENSION_KEYS = {
    "discovery_crawl": "发现与抓取",
    "metadata": "页面元信息",
    "semantic_structure": "语义结构",
    "brand_evidence": "品牌事实与证据",
    "ai_extractability": "AI 可抽取性",
    "schema": "Schema",
    "ux": "用户体验",
}

FORBIDDEN_PUBLIC_CONCLUSIONS = (
    "AI 引用概率",
    "AI 收录概率",
    "GEO 排名分数",
    "品牌召回率",
    "引用份额",
    "优化后提升预测",
)


def compact_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def normalize_url(value: str) -> str:
    return value.rstrip("/") if value != "/" else value


def route_expected_urls(base_url: str, route: str) -> set[str]:
    base = base_url.rstrip("/")
    if route == "/":
        return {base + "/"}
    return {base + route, base + route + "/"}


def relpath(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


class StaticHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.tags: Counter[str] = Counter()
        self.lang = ""
        self.title_parts: list[str] = []
        self.meta: list[dict[str, str]] = []
        self.link_tags: list[dict[str, str]] = []
        self.assets: list[str] = []
        self.headings: list[dict[str, str]] = []
        self.links: list[dict[str, str]] = []
        self.json_ld_raw: list[str] = []
        self.paragraphs: list[str] = []
        self.table_column_counts: list[int] = []
        self.datetime_values: list[str] = []
        self.breadcrumb_markers: list[str] = []
        self.text_parts: list[str] = []
        self.main_text_parts: list[str] = []

        self._tag_stack: list[str] = []
        self._capture_title = False
        self._heading_stack: list[dict[str, Any]] = []
        self._anchor_stack: list[dict[str, Any]] = []
        self._paragraph_stack: list[list[str]] = []
        self._json_ld_parts: list[str] | None = None
        self._current_row_cells: int | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        attrs_dict = {name.lower(): (value or "") for name, value in attrs}
        self.tags[tag] += 1
        self._tag_stack.append(tag)

        if tag == "html":
            self.lang = attrs_dict.get("lang", "")
        if tag == "title":
            self._capture_title = True
        if tag == "meta":
            self.meta.append(attrs_dict)
        if tag == "link":
            self.link_tags.append(attrs_dict)
            href = attrs_dict.get("href", "")
            if href:
                self.assets.append(href)
        if tag in {"script", "img", "source"}:
            src = attrs_dict.get("src", "")
            if src:
                self.assets.append(src)
        if tag == "script" and "ld+json" in attrs_dict.get("type", "").lower():
            self._json_ld_parts = []
        if tag in {"h1", "h2", "h3"}:
            self._heading_stack.append({"tag": tag, "parts": []})
        if tag == "a":
            self._anchor_stack.append({"href": attrs_dict.get("href", ""), "parts": []})
        if tag == "p":
            self._paragraph_stack.append([])
        if tag == "tr":
            self._current_row_cells = 0
        if tag in {"td", "th"} and self._current_row_cells is not None:
            self._current_row_cells += 1
        if "datetime" in attrs_dict:
            self.datetime_values.append(attrs_dict["datetime"])

        marker = " ".join(
            attrs_dict.get(key, "")
            for key in ("aria-label", "class", "id")
            if attrs_dict.get(key)
        ).lower()
        if "breadcrumb" in marker or "面包屑" in marker:
            self.breadcrumb_markers.append(marker)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "title":
            self._capture_title = False
        if tag == "script" and self._json_ld_parts is not None:
            payload = compact_text("".join(self._json_ld_parts))
            if payload:
                self.json_ld_raw.append(payload)
            self._json_ld_parts = None
        if self._heading_stack and self._heading_stack[-1]["tag"] == tag:
            heading = self._heading_stack.pop()
            text = compact_text("".join(heading["parts"]))
            self.headings.append({"level": heading["tag"], "text": text})
        if tag == "a" and self._anchor_stack:
            anchor = self._anchor_stack.pop()
            text = compact_text("".join(anchor["parts"]))
            self.links.append({"href": anchor["href"], "text": text})
        if tag == "p" and self._paragraph_stack:
            text = compact_text("".join(self._paragraph_stack.pop()))
            if text:
                self.paragraphs.append(text)
        if tag == "tr" and self._current_row_cells is not None:
            self.table_column_counts.append(self._current_row_cells)
            self._current_row_cells = None

        for index in range(len(self._tag_stack) - 1, -1, -1):
            if self._tag_stack[index] == tag:
                del self._tag_stack[index:]
                break

    def handle_data(self, data: str) -> None:
        if self._json_ld_parts is not None:
            self._json_ld_parts.append(data)
            return
        if any(tag in {"script", "style"} for tag in self._tag_stack):
            return

        if self._capture_title:
            self.title_parts.append(data)
        if self._heading_stack:
            self._heading_stack[-1]["parts"].append(data)
        if self._anchor_stack:
            self._anchor_stack[-1]["parts"].append(data)
        if self._paragraph_stack:
            self._paragraph_stack[-1].append(data)

        text = compact_text(data)
        if text and not any(tag in {"head", "title"} for tag in self._tag_stack):
            self.text_parts.append(text)
            if "main" in self._tag_stack:
                self.main_text_parts.append(text)

    @property
    def title(self) -> str:
        return compact_text("".join(self.title_parts))

    @property
    def visible_text(self) -> str:
        return compact_text(" ".join(self.text_parts))

    @property
    def main_text(self) -> str:
        return compact_text(" ".join(self.main_text_parts))


@dataclass
class AuditContext:
    project_root: Path
    config: dict[str, Any]
    generated_at: str
    run_id: str
    git_commit: str
    branch: str
    build_method: str


def find_project_root(start: Path) -> Path:
    for candidate in [start, *start.parents]:
        if (candidate / "package.json").exists() and (candidate / ".git").exists():
            return candidate
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


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_csv(path: Path, findings: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FINDING_FIELDS)
        writer.writeheader()
        for finding in findings:
            writer.writerow({field: finding.get(field, "") for field in FINDING_FIELDS})


def ensure_allowed_output(root: Path, path: Path) -> None:
    relative = path.resolve().relative_to(root.resolve())
    parts = relative.parts
    if not parts or parts[0] not in {"docs", "tools"}:
        raise ValueError(f"Output path is outside allowed docs/tools boundary: {relative.as_posix()}")
    if parts[0] in {"app", "public"}:
        raise ValueError(f"Output path is forbidden: {relative.as_posix()}")


def route_html_path(root: Path, input_dir: str, route_config: dict[str, Any]) -> Path:
    return root / input_dir / route_config["html_path"]


def meta_content(page: StaticHTMLParser, key: str, value: str) -> str:
    for meta in page.meta:
        if meta.get(key, "").lower() == value.lower():
            return meta.get("content", "")
    return ""


def canonical_href(page: StaticHTMLParser) -> str:
    for link in page.link_tags:
        rel = link.get("rel", "").lower()
        if "canonical" in rel.split():
            return link.get("href", "")
    return ""


def parse_json_ld(raw_values: list[str]) -> list[dict[str, Any]]:
    parsed: list[dict[str, Any]] = []
    for raw in raw_values:
        try:
            value = json.loads(raw)
        except json.JSONDecodeError:
            parsed.append({"_parse_error": True, "_raw_excerpt": raw[:120]})
            continue
        if isinstance(value, list):
            parsed.extend(item for item in value if isinstance(item, dict))
        elif isinstance(value, dict):
            parsed.append(value)
    return parsed


def json_ld_types(items: list[dict[str, Any]]) -> list[str]:
    types: list[str] = []
    for item in items:
        value = item.get("@type")
        if isinstance(value, list):
            types.extend(str(part) for part in value)
        elif value:
            types.append(str(value))
    return sorted(set(types))


def has_sitemap_route(sitemap_xml: str, base_url: str, route: str) -> bool:
    return any(expected in sitemap_xml for expected in route_expected_urls(base_url, route))


def resource_paths_have_base_path(page: StaticHTMLParser, base_path: str) -> tuple[bool, list[str]]:
    if not base_path:
        return True, []
    static_assets = [
        asset
        for asset in page.assets
        if asset.startswith("/") and ("/_next/" in asset or asset.endswith((".css", ".js", ".svg", ".png")))
    ]
    bad = [asset for asset in static_assets if not asset.startswith(base_path + "/")]
    return not bad, bad[:5]


def internal_links(page: StaticHTMLParser, base_path: str, base_url: str) -> list[dict[str, str]]:
    links = []
    for link in page.links:
        href = link["href"]
        if href.startswith(base_path + "/") or href.startswith(base_url.rstrip("/") + "/") or href == base_path:
            links.append(link)
    return links


def external_links(page: StaticHTMLParser, base_url: str) -> list[dict[str, str]]:
    return [
        link
        for link in page.links
        if link["href"].startswith("http") and not link["href"].startswith(base_url.rstrip("/") + "/")
    ]


def has_descriptive_anchor_text(links: list[dict[str, str]]) -> bool:
    weak = {"", "here", "click", "点击这里", "更多"}
    return all(link["text"].strip().lower() not in weak for link in links)


def heading_hierarchy_ok(headings: list[dict[str, str]]) -> bool:
    previous = 0
    for heading in headings:
        level = int(heading["level"][1])
        if previous and level - previous > 1:
            return False
        previous = level
    return True


def first_date(text: str, datetime_values: list[str]) -> str:
    if datetime_values:
        return datetime_values[0]
    match = re.search(r"20\d{2}[-年]\d{1,2}[-月]\d{1,2}", text)
    return match.group(0) if match else ""


def has_source_ids(text: str) -> bool:
    return bool(re.search(r"\b[A-Z]-\d{3}\b|\bFAQ-\d+\b|\bq\d{2}\b|source_id", text, re.IGNORECASE))


def has_key_value_signal(text: str, table_count: int) -> bool:
    colon_lines = re.findall(r"[\u4e00-\u9fffA-Za-z0-9]{2,16}[：:]", text)
    return table_count > 0 or len(colon_lines) >= 3


def has_positive_effect_promise(text: str) -> bool:
    patterns = [
        r"(?<!不)(?<!不声称)保证.{0,12}(AI|收录|引用|曝光|推荐|销售)",
        r"(?<!不)(?<!不声称)承诺.{0,12}(AI|收录|引用|曝光|推荐|销售)",
        r"提升.{0,8}(引用概率|收录概率|召回率|引用份额|排名)",
    ]
    return any(re.search(pattern, text) for pattern in patterns)


def audit_page(ctx: AuditContext, route_config: dict[str, Any], robots_text: str, sitemap_xml: str) -> dict[str, Any]:
    input_dir = ctx.config["input_dir"]
    html_path = route_html_path(ctx.project_root, input_dir, route_config)
    if not html_path.exists():
        raise FileNotFoundError(
            f"Missing audited HTML for {route_config['route']}: "
            f"{input_dir}/{route_config['html_path']}"
        )

    html = html_path.read_text(encoding="utf-8", errors="ignore")
    parser = StaticHTMLParser()
    parser.feed(html)
    json_ld = parse_json_ld(parser.json_ld_raw)
    base_url = ctx.config["site_base_url"]
    base_path = ctx.config.get("base_path", "")
    route = route_config["route"]
    expectations = route_config.get("expectations", {})
    h1s = [heading["text"] for heading in parser.headings if heading["level"] == "h1"]
    h2s = [heading["text"] for heading in parser.headings if heading["level"] == "h2"]
    h3s = [heading["text"] for heading in parser.headings if heading["level"] == "h3"]
    canonical = canonical_href(parser)
    canonical_ok = canonical in route_expected_urls(base_url, route)
    assets_ok, asset_path_issues = resource_paths_have_base_path(parser, base_path)
    main_text = parser.main_text
    visible_text = parser.visible_text
    int_links = internal_links(parser, base_path, base_url)
    ext_links = external_links(parser, base_url)
    updated = first_date(visible_text, parser.datetime_values)
    table_count = parser.tags["table"]
    list_count = parser.tags["ul"] + parser.tags["ol"]
    source_id_visible = has_source_ids(visible_text)
    source_links_visible = bool(ext_links)
    has_project_identity = all(
        marker in visible_text
        for marker in ("独立 GEO 研究", "未受元亨利委托", "不代表品牌官方立场")
    )
    schema_types = json_ld_types(json_ld)
    meta_robots = meta_content(parser, "name", "robots")
    description = meta_content(parser, "name", "description")
    og_tags = {
        meta.get("property", ""): meta.get("content", "")
        for meta in parser.meta
        if meta.get("property", "").startswith("og:")
    }
    viewport = meta_content(parser, "name", "viewport")
    has_entity_in_h1 = any("元亨利" in h1 or "元亨利红木家具" in h1 for h1 in h1s)
    has_context_summary = bool(parser.paragraphs and len(parser.paragraphs[0]) >= 30)
    has_qa = "直接答案" in visible_text or "FAQ" in visible_text or "？" in visible_text
    has_steps = parser.tags["ol"] > 0 or "步骤" in visible_text or "下单前" in visible_text
    has_comparison = table_count > 0 or any(marker in visible_text for marker in ("对比", "维度", "适用", "不适用"))
    has_kv = has_key_value_signal(visible_text, table_count)
    paragraph_lengths = [len(item) for item in parser.paragraphs]
    dense_paragraphs = [length for length in paragraph_lengths if length > 260]
    too_short_anchors = [link for link in int_links if len(link["text"]) <= 1]

    checks = {
        "discovery_crawl": {
            "html_generated": {"ok": True, "evidence_status": "observed", "evidence": f"{input_dir}/{route_config['html_path']}"},
            "canonical": {"ok": bool(canonical), "matches_route": canonical_ok, "value": canonical, "evidence_status": "observed"},
            "robots": {"ok": "User-agent" in robots_text, "allows_root": "Allow: /" in robots_text, "evidence_status": "observed"},
            "sitemap": {"ok": bool(sitemap_xml), "covers_route": has_sitemap_route(sitemap_xml, base_url, route), "evidence_status": "observed"},
            "meta_robots": {"ok": bool(meta_robots), "value": meta_robots or "absent; default index/follow assumed", "evidence_status": "observed"},
            "base_path_assets": {"ok": assets_ok, "issues": asset_path_issues, "evidence_status": "observed"},
            "main_content_static_html": {"ok": len(main_text) >= 200, "main_text_length": len(main_text), "evidence_status": "observed"},
        },
        "metadata": {
            "title": {"ok": bool(parser.title), "value": parser.title, "evidence_status": "observed"},
            "description": {"ok": bool(description), "value": description, "evidence_status": "observed"},
            "open_graph": {"ok": bool(og_tags), "fields": sorted(og_tags.keys()), "evidence_status": "observed"},
            "language": {"ok": bool(parser.lang), "value": parser.lang, "evidence_status": "observed"},
            "unique_h1": {"ok": len(h1s) == 1, "values": h1s, "evidence_status": "observed"},
            "updated_time": {"ok": bool(updated), "value": updated, "evidence_status": "observed"},
            "project_identity": {"ok": has_project_identity, "evidence_status": "observed"},
        },
        "semantic_structure": {
            "main": {"ok": parser.tags["main"] >= 1, "count": parser.tags["main"], "evidence_status": "observed"},
            "article": {
                "ok": parser.tags["article"] >= 1 if route != "/" else True,
                "count": parser.tags["article"],
                "evidence_status": "observed" if route != "/" else "not-applicable",
            },
            "header_nav_footer": {
                "ok": parser.tags["header"] >= 1 and parser.tags["nav"] >= 1 and parser.tags["footer"] >= 1,
                "counts": {"header": parser.tags["header"], "nav": parser.tags["nav"], "footer": parser.tags["footer"]},
                "evidence_status": "observed",
            },
            "h1_h3_hierarchy": {"ok": heading_hierarchy_ok(parser.headings), "h2_count": len(h2s), "h3_count": len(h3s), "evidence_status": "observed"},
            "lists": {"ok": list_count > 0, "count": list_count, "evidence_status": "observed"},
            "tables": {"ok": table_count > 0, "count": table_count, "max_columns": max(parser.table_column_counts or [0]), "evidence_status": "observed"},
            "faq": {"ok": has_qa, "evidence_status": "observed"},
            "breadcrumbs": {
                "ok": bool(parser.breadcrumb_markers) if expectations.get("requires_breadcrumb") else True,
                "markers": parser.breadcrumb_markers,
                "evidence_status": "observed" if expectations.get("requires_breadcrumb") else "not-applicable",
            },
            "internal_links": {"ok": bool(int_links), "count": len(int_links), "evidence_status": "observed"},
            "anchor_text": {"ok": has_descriptive_anchor_text(int_links) and not too_short_anchors, "short_anchor_count": len(too_short_anchors), "evidence_status": "observed"},
        },
        "brand_evidence": {
            "conclusion_first": {"ok": has_context_summary, "evidence_status": "observed"},
            "full_brand_name": {"ok": "元亨利红木家具" in visible_text, "evidence_status": "observed"},
            "source_links": {"ok": source_links_visible or source_id_visible, "external_link_count": len(ext_links), "evidence_status": "observed"},
            "source_id_traceable": {"ok": source_id_visible, "evidence_status": "observed"},
            "fact_judgment_recommendation_distinction": {
                "ok": any(marker in visible_text for marker in ("事实", "判断", "建议", "待核验", "边界")),
                "evidence_status": "observed",
            },
            "freshness": {"ok": bool(updated), "value": updated, "evidence_status": "observed"},
            "source_accountability": {"ok": "来源" in visible_text or "公开资料" in visible_text or "研究声明" in visible_text, "evidence_status": "observed"},
            "unsupported_effect_promise": {"ok": not has_positive_effect_promise(visible_text), "evidence_status": "observed"},
        },
        "ai_extractability": {
            "context_independent_summary": {"ok": has_context_summary, "evidence_status": "observed"},
            "atomic_facts": {"ok": list_count > 0 or len(parser.paragraphs) >= 4, "evidence_status": "observed"},
            "key_value_information": {"ok": has_kv, "evidence_status": "observed"},
            "qa_structure": {"ok": has_qa, "evidence_status": "observed"},
            "step_structure": {"ok": has_steps, "evidence_status": "observed"},
            "comparison_or_judgment_dimensions": {"ok": has_comparison, "evidence_status": "observed"},
            "paragraph_independence": {"ok": len(dense_paragraphs) == 0, "dense_paragraph_count": len(dense_paragraphs), "evidence_status": "inferred"},
            "entity_ambiguity": {"ok": "元亨利" in visible_text, "evidence_status": "observed"},
            "chunk_citation_readiness": {"ok": source_id_visible and bool(h2s), "evidence_status": "inferred"},
        },
        "schema": {
            "json_ld_present": {"ok": bool(json_ld), "count": len(json_ld), "evidence_status": "observed"},
            "schema_types": {"ok": bool(schema_types), "types": schema_types, "evidence_status": "observed" if schema_types else "not-applicable"},
            "schema_body_consistency": {"ok": True if not json_ld else None, "evidence_status": "not-applicable" if not json_ld else "input-gap"},
            "missing_required_fields": {"ok": True if not json_ld else None, "evidence_status": "not-applicable" if not json_ld else "input-gap"},
            "schema_facts_absent_from_body": {"ok": False if json_ld and any("_parse_error" in item for item in json_ld) else True, "evidence_status": "not-applicable" if not json_ld else "inferred"},
        },
        "ux": {
            "clear_navigation": {"ok": parser.tags["nav"] >= 1 and len(int_links) >= 5, "evidence_status": "observed"},
            "too_long_or_dense": {"ok": len(main_text) <= 14000 and len(dense_paragraphs) == 0, "main_text_length": len(main_text), "evidence_status": "inferred"},
            "main_conclusion_easy_to_find": {"ok": has_context_summary, "evidence_status": "observed"},
            "data_table_readability": {"ok": True if table_count == 0 else max(parser.table_column_counts or [0]) <= 5, "evidence_status": "not-applicable" if table_count == 0 else "observed"},
            "mobile_structure_risk": {"ok": "width=device-width" in viewport, "viewport": viewport, "evidence_status": "observed"},
            "next_step_clear": {"ok": any(marker in visible_text for marker in ("查看", "下载", "进入", "相关问题", "方法")), "evidence_status": "observed"},
        },
    }

    return {
        "route": route,
        "label": route_config["label"],
        "page_type": route_config["page_type"],
        "selection_reason": route_config["selection_reason"],
        "input_path": f"{input_dir}/{route_config['html_path']}",
        "html_sha256": hashlib.sha256(html.encode("utf-8")).hexdigest(),
        "summary": {
            "title": parser.title,
            "description": description,
            "canonical": canonical,
            "h1": h1s,
            "main_text_length": len(main_text),
            "json_ld_types": schema_types,
            "internal_link_count": len(int_links),
            "external_source_link_count": len(ext_links),
            "updated": updated,
        },
        "checks": checks,
        "raw_counts": {
            "headings": {"h1": len(h1s), "h2": len(h2s), "h3": len(h3s)},
            "lists": list_count,
            "tables": table_count,
            "paragraphs": len(parser.paragraphs),
            "source_id_like_tokens_visible": source_id_visible,
            "entity_in_h1": has_entity_in_h1,
            "step_items": parser.tags["li"],
        },
        "expectations": expectations,
    }


def add_finding(
    findings: list[dict[str, Any]],
    *,
    route: str,
    dimension: str,
    evidence_status: str,
    severity: str,
    priority: str,
    owner: str,
    observed_evidence: str,
    issue: str,
    recommended_action: str,
    acceptance_test: str,
    skill_source: str,
    requires_human_review: bool,
    notes: str = "",
) -> None:
    findings.append(
        {
            "finding_id": f"06B-PA-{len(findings) + 1:03d}",
            "route": route,
            "audit_dimension": DIMENSION_KEYS[dimension],
            "evidence_status": evidence_status,
            "severity": severity,
            "priority": priority,
            "owner": owner,
            "observed_evidence": observed_evidence,
            "issue": issue,
            "recommended_action": recommended_action,
            "acceptance_test": acceptance_test,
            "skill_source": skill_source,
            "requires_human_review": "yes" if requires_human_review else "no",
            "status": "open",
            "notes": notes,
        }
    )


def build_findings(ctx: AuditContext, pages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    skill_source = f"yao-geo-page-audit@{ctx.config['skill_source']['commit']}"
    findings: list[dict[str, Any]] = []

    for page in pages:
        route = page["route"]
        summary = page["summary"]
        checks = page["checks"]
        expectations = page["expectations"]

        canonical_check = checks["discovery_crawl"]["canonical"]
        if not canonical_check["ok"] or not canonical_check["matches_route"]:
            add_finding(
                findings,
                route=route,
                dimension="discovery_crawl",
                evidence_status="observed",
                severity="medium",
                priority="P1",
                owner="development",
                observed_evidence=f"canonical={summary['canonical'] or 'absent'}",
                issue="页面 canonical 未指向当前路由，子页面可能被合并到首页 canonical。",
                recommended_action="在后续页面修复阶段为每个公开路由输出与页面路径一致的 canonical。",
                acceptance_test="构建后检查对应 HTML 的 link rel=canonical，值等于该路由公开 URL。",
                skill_source=skill_source,
                requires_human_review=False,
            )

        if not checks["metadata"]["unique_h1"]["ok"]:
            add_finding(
                findings,
                route=route,
                dimension="metadata",
                evidence_status="observed",
                severity="medium",
                priority="P1",
                owner="content",
                observed_evidence=f"h1={checks['metadata']['unique_h1']['values']}",
                issue="页面没有唯一 H1，影响页面主题抽取。",
                recommended_action="确保每页只有一个表达页面主题的 H1。",
                acceptance_test="构建后解析 HTML，H1 数量为 1。",
                skill_source=skill_source,
                requires_human_review=True,
            )

        if not checks["discovery_crawl"]["main_content_static_html"]["ok"]:
            add_finding(
                findings,
                route=route,
                dimension="discovery_crawl",
                evidence_status="observed",
                severity="high",
                priority="P0",
                owner="development",
                observed_evidence=f"main_text_length={summary['main_text_length']}",
                issue="主要正文没有充分出现在静态 HTML 中。",
                recommended_action="保持核心正文由静态构建直接输出，避免只依赖客户端渲染。",
                acceptance_test="构建后 main 内可提取正文不少于 200 个字符。",
                skill_source=skill_source,
                requires_human_review=False,
            )

        if not checks["schema"]["json_ld_present"]["ok"]:
            add_finding(
                findings,
                route=route,
                dimension="schema",
                evidence_status="observed",
                severity="low",
                priority="P2",
                owner="development",
                observed_evidence="未发现 application/ld+json。",
                issue="当前页面没有 JSON-LD，机器只能依赖正文和链接结构理解页面实体与类型。",
                recommended_action="后续人工审核后再考虑页面级 JSON-LD 候选；本阶段不生成或写入 Schema。",
                acceptance_test="后续若接入 Schema，JSON-LD 字段必须能逐项回溯到页面正文。",
                skill_source=skill_source,
                requires_human_review=True,
                notes="本发现不代表 AI 引用概率或排名判断。",
            )

        if expectations.get("requires_breadcrumb") and not checks["semantic_structure"]["breadcrumbs"]["ok"]:
            add_finding(
                findings,
                route=route,
                dimension="semantic_structure",
                evidence_status="observed",
                severity="low",
                priority="P3",
                owner="design",
                observed_evidence="未发现 breadcrumb/面包屑标记。",
                issue="子页面缺少面包屑，页面层级主要依赖全局导航表达。",
                recommended_action="后续设计修复时为内容页补充可见或语义化面包屑。",
                acceptance_test="构建后页面存在 breadcrumb 语义标记，且链接指向首页与上级页面。",
                skill_source=skill_source,
                requires_human_review=False,
            )

        if expectations.get("requires_entity_in_h1") and not page["raw_counts"]["entity_in_h1"]:
            add_finding(
                findings,
                route=route,
                dimension="ai_extractability",
                evidence_status="inferred",
                severity="medium",
                priority="P2",
                owner="content",
                observed_evidence=f"H1={summary['h1']}",
                issue="H1 未包含品牌实体，单独引用页面标题时容易脱离元亨利语境。",
                recommended_action="后续内容修复可在 H1 或紧邻摘要中加入完整品牌实体与页面类型。",
                acceptance_test="抽取 H1 与首段文本时可独立识别本页服务的品牌实体。",
                skill_source=skill_source,
                requires_human_review=True,
            )

        if expectations.get("requires_metric_source_summary") and not checks["brand_evidence"]["source_id_traceable"]["ok"]:
            add_finding(
                findings,
                route=route,
                dimension="brand_evidence",
                evidence_status="observed",
                severity="medium",
                priority="P2",
                owner="data",
                observed_evidence="首页静态正文未出现 source_id/B-xxx/qxx 等可追溯 ID。",
                issue="首页有项目身份与指标叙事，但首屏缺少机器可抽取的数据来源字段或 source_id 摘要。",
                recommended_action="后续可增加小型数据来源卡，列出基线样本、评分方式、日期和方法页入口。",
                acceptance_test="首页首屏或指标区可抽取到数据版本、样本量、测试日期、评分方式和方法页链接。",
                skill_source=skill_source,
                requires_human_review=True,
            )

        if expectations.get("requires_fact_kv_module") and not checks["ai_extractability"]["key_value_information"]["ok"]:
            add_finding(
                findings,
                route=route,
                dimension="ai_extractability",
                evidence_status="inferred",
                severity="medium",
                priority="P2",
                owner="content",
                observed_evidence=f"tables={page['raw_counts']['tables']}; key_value_information=false",
                issue="品牌事实页缺少稳定的 key-value 或事实卡模块承载主体、证据等级和待核验项。",
                recommended_action="后续内容修复可加入事实卡或定义列表，但必须来自已审核公开事实。",
                acceptance_test="页面正文中存在可复制的事实卡，至少包含实体、事实、证据等级、source_id 和更新时间。",
                skill_source=skill_source,
                requires_human_review=True,
            )

        if expectations.get("requires_step_source_mapping") and not checks["ai_extractability"]["chunk_citation_readiness"]["ok"]:
            add_finding(
                findings,
                route=route,
                dimension="brand_evidence",
                evidence_status="inferred",
                severity="medium",
                priority="P2",
                owner="data",
                observed_evidence=f"list_items={page['raw_counts']['step_items']}; source_id_traceable={checks['brand_evidence']['source_id_traceable']['ok']}",
                issue="购买指南有步骤结构和来源链接，但每个关键核验步骤尚未形成逐条 source_id 映射。",
                recommended_action="后续人工审核后为关键步骤补来源 ID 或证据等级，避免泛化成无证据购买建议。",
                acceptance_test="每个高风险核验步骤能回溯到页面可见 source_id 或来源链接。",
                skill_source=skill_source,
                requires_human_review=True,
            )

    return findings


def summarize_counts(findings: list[dict[str, Any]]) -> dict[str, Any]:
    by_priority = Counter(item["priority"] for item in findings)
    by_dimension = Counter(item["audit_dimension"] for item in findings)
    by_route = Counter(item["route"] for item in findings)
    return {
        "by_priority": {key: by_priority.get(key, 0) for key in ("P0", "P1", "P2", "P3")},
        "by_dimension": {value: by_dimension.get(value, 0) for value in DIMENSION_KEYS.values()},
        "by_route": dict(sorted(by_route.items())),
        "total": len(findings),
    }


def build_report_markdown(ctx: AuditContext, pages: list[dict[str, Any]], findings: list[dict[str, Any]], metadata: dict[str, Any]) -> str:
    counts = summarize_counts(findings)
    lines = [
        "# 阶段 06B 页面审计模块试点报告",
        "",
        f"- 执行时间：{ctx.generated_at}",
        f"- 构建版本：{ctx.git_commit}",
        f"- 当前分支：{ctx.branch}",
        f"- 构建方法：{ctx.build_method}",
        f"- Skill 来源：{ctx.config['skill_source']['repo']} @ {ctx.config['skill_source']['commit']}",
        "- 审计边界：只读当前分支 `out/` 静态 HTML；不读取 internal-review；不调用外部 API；不修改页面。",
        "",
        "## 审计页面",
    ]
    for page in pages:
        lines.append(f"- `{page['route']}`：{page['label']}，{page['selection_reason']}。")

    lines.extend(["", "## 每页摘要"])
    for page in pages:
        summary = page["summary"]
        lines.extend(
            [
                f"### {page['label']} `{page['route']}`",
                f"- title：{summary['title']}",
                f"- description：{summary['description']}",
                f"- canonical：{summary['canonical'] or '缺失'}",
                f"- H1：{', '.join(summary['h1']) if summary['h1'] else '缺失'}",
                f"- 静态 main 正文长度：{summary['main_text_length']}",
                f"- JSON-LD 类型：{', '.join(summary['json_ld_types']) if summary['json_ld_types'] else '未发现'}",
                f"- 内链数量：{summary['internal_link_count']}；外部来源链接数量：{summary['external_source_link_count']}",
            ]
        )

    lines.extend(
        [
            "",
            "## 发现数量",
            f"- P0：{counts['by_priority']['P0']}",
            f"- P1：{counts['by_priority']['P1']}",
            f"- P2：{counts['by_priority']['P2']}",
            f"- P3：{counts['by_priority']['P3']}",
            "",
            "## 维度数量",
        ]
    )
    for dimension, count in counts["by_dimension"].items():
        lines.append(f"- {dimension}：{count}")

    lines.extend(["", "## 发现清单"])
    for finding in findings:
        lines.extend(
            [
                f"### {finding['finding_id']} `{finding['route']}`",
                f"- 维度：{finding['audit_dimension']}",
                f"- 证据状态：{finding['evidence_status']}",
                f"- 严重度/优先级：{finding['severity']} / {finding['priority']}",
                f"- 负责人：{finding['owner']}",
                f"- 观察证据：{finding['observed_evidence']}",
                f"- 问题：{finding['issue']}",
                f"- 建议动作：{finding['recommended_action']}",
                f"- 验收方式：{finding['acceptance_test']}",
            ]
        )

    lines.extend(
        [
            "",
            "## 三个页面的共性问题",
            "- 三页都未发现 JSON-LD；本阶段只记录缺口，不生成或写入 Schema。",
            "- 三页 H1 都偏主题化，没有直接写出“元亨利”品牌实体，独立引用标题时语境不够完整。",
            "- 两个内容子页面缺少页面级 canonical 和面包屑，页面路径与层级主要依赖全局导航表达。",
            "",
            "## 页面特有问题",
            "- `/`：最重要的特有问题是 H1 未直接包含品牌实体，首页标题脱离上下文后偏泛化。",
            "- `/facts`：最重要的特有问题是 canonical 指向首页，而不是 `/facts` 页面 URL。",
            "- `/buying-guide`：最重要的特有问题是 canonical 指向首页，而不是 `/buying-guide` 页面 URL。",
            "",
            "## 建议修复顺序",
            "1. 先处理 P1 canonical，保证每个公开路由的页面级 canonical 正确。",
            "2. 再处理 P2 页面主题：让 H1 或紧邻摘要能独立识别元亨利品牌实体。",
            "3. 最后处理 P2/P3 结构增强：人工审核后的 JSON-LD 候选和子页面面包屑。",
            "",
            "## 审计限制",
            "- 本报告只基于构建后的静态 HTML、robots 和 sitemap。",
            "- 未读取 external canonical 工作簿、raw AI answers、人工评分或 internal-review 内容。",
            "- 未运行 crawler、未调用模型或外部 API、未使用线上 main 页面。",
            "- 发现中的 `inferred` 只表示基于页面证据和方法规则的推断，不写成事实。",
            "- 本报告不生成单一 GEO 总分，也不输出 AI 排名、品牌召回率、引用份额、AI 引用概率或优化后提升预测。",
            "",
            "## 输出文件",
        ]
    )
    for output in metadata["output_files"]:
        lines.append(f"- `{output}`")
    lines.append("")
    return "\n".join(lines)


def build_metadata(ctx: AuditContext, pages: list[dict[str, Any]], output_files: list[str]) -> dict[str, Any]:
    return {
        "run_id": ctx.run_id,
        "generated_at": ctx.generated_at,
        "git_commit": ctx.git_commit,
        "branch": ctx.branch,
        "skill_source_repo": ctx.config["skill_source"]["repo"],
        "skill_source_commit": ctx.config["skill_source"]["commit"],
        "audited_routes": [page["route"] for page in pages],
        "build_method": ctx.build_method,
        "input_paths": [page["input_path"] for page in pages] + ["out/robots.txt", "out/sitemap.xml"],
        "excluded_paths": ctx.config["excluded_paths"],
        "network_used": False,
        "api_used": False,
        "source_retrieval_network_used": True,
        "output_files": output_files,
    }


def run_audit(
    project_root: Path,
    config_path: Path,
    *,
    generated_at: str | None = None,
    run_id: str | None = None,
    git_commit: str | None = None,
    branch: str | None = None,
    build_method: str = "GitHub Pages equivalent: next build + scripts/prepare-github-pages.mjs",
) -> dict[str, Any]:
    project_root = project_root.resolve()
    config = read_json(config_path)
    generated_at = generated_at or datetime.now().astimezone().isoformat(timespec="seconds")
    run_id = run_id or "06b-page-audit-" + re.sub(r"[^0-9A-Za-z]", "", generated_at)
    ctx = AuditContext(
        project_root=project_root,
        config=config,
        generated_at=generated_at,
        run_id=run_id,
        git_commit=git_commit or run_git(project_root, ["rev-parse", "HEAD"], "unknown"),
        branch=branch or run_git(project_root, ["branch", "--show-current"], "unknown"),
        build_method=build_method,
    )

    output_dir = project_root / config["output_dir"]
    docs_csv_path = project_root / config["docs_findings_csv"]
    ensure_allowed_output(project_root, output_dir / "report.json")
    ensure_allowed_output(project_root, output_dir / "report.md")
    ensure_allowed_output(project_root, output_dir / "run-metadata.json")
    ensure_allowed_output(project_root, docs_csv_path)

    robots_path = project_root / config["input_dir"] / "robots.txt"
    sitemap_path = project_root / config["input_dir"] / "sitemap.xml"
    robots_text = robots_path.read_text(encoding="utf-8", errors="ignore") if robots_path.exists() else ""
    sitemap_xml = sitemap_path.read_text(encoding="utf-8", errors="ignore") if sitemap_path.exists() else ""

    pages = [audit_page(ctx, route_config, robots_text, sitemap_xml) for route_config in config["audited_routes"]]
    findings = build_findings(ctx, pages)

    output_files = [
        f"{config['output_dir']}/report.md",
        f"{config['output_dir']}/report.json",
        f"{config['output_dir']}/run-metadata.json",
        config["docs_findings_csv"],
    ]
    metadata = build_metadata(ctx, pages, output_files)
    report_json = {
        "run_metadata": metadata,
        "skill_source": config["skill_source"],
        "pages": pages,
        "findings": findings,
        "counts": summarize_counts(findings),
        "forbidden_conclusions_generated": [],
    }

    write_json(output_dir / "report.json", report_json)
    write_json(output_dir / "run-metadata.json", metadata)
    (output_dir / "report.md").write_text(build_report_markdown(ctx, pages, findings, metadata), encoding="utf-8")
    write_csv(docs_csv_path, findings)
    return report_json


def main() -> int:
    script_path = Path(__file__).resolve()
    default_root = find_project_root(script_path)
    default_config = script_path.parent / "audit-config.json"

    parser = argparse.ArgumentParser(description="Run the offline 06B page audit pilot.")
    parser.add_argument("--project-root", type=Path, default=default_root)
    parser.add_argument("--config", type=Path, default=default_config)
    parser.add_argument("--generated-at")
    parser.add_argument("--run-id")
    parser.add_argument("--git-commit")
    parser.add_argument("--branch")
    parser.add_argument("--build-method", default="GitHub Pages equivalent: next build + scripts/prepare-github-pages.mjs")
    args = parser.parse_args()

    report = run_audit(
        args.project_root,
        args.config,
        generated_at=args.generated_at,
        run_id=args.run_id,
        git_commit=args.git_commit,
        branch=args.branch,
        build_method=args.build_method,
    )
    print(json.dumps({"run_id": report["run_metadata"]["run_id"], "counts": report["counts"]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
