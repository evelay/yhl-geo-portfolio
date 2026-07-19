#!/usr/bin/env python3
"""Build isolated homepage Schema JSON-LD drafts for the 07D1 pilot."""

from __future__ import annotations

import argparse
import copy
import csv
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


CONFIG_PATH = Path(__file__).with_name("home-schema-config.json")
DEFAULT_COMPARISON_NAME = "comparison-report.md"
DEFAULT_VALIDATION_NAME = "validation.json"
DEFAULT_METADATA_NAME = "run-metadata.json"

ALLOWED_PROPERTIES = {
    "@context",
    "@graph",
    "@id",
    "@type",
    "description",
    "inLanguage",
    "isPartOf",
    "name",
    "url",
}

PUBLIC_URL_PREFIX = "https://evelay.github.io/yhl-geo-portfolio/"
FORBIDDEN_URL_PARTS = (
    "/Users/",
    "localhost",
    "127.0.0.1",
    "chatgpt.site",
    "/yhl-geo-portfolio/yhl-geo-portfolio/",
)


class HomepageSignalParser(HTMLParser):
    """Collect only the rendered homepage signals needed for 07D1."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.lang: str | None = None
        self.canonical: str | None = None
        self.meta_description: str | None = None
        self.h1_values: list[str] = []
        self.json_ld_raw: list[str] = []
        self.has_search_form = False
        self.has_search_input = False
        self._in_title = False
        self._title_parts: list[str] = []
        self._capture_h1 = False
        self._h1_parts: list[str] = []
        self._capture_lede = False
        self._lede_parts: list[str] = []
        self._capture_json_ld = False
        self._json_ld_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = {name.lower(): value or "" for name, value in attrs}
        tag_name = tag.lower()

        if tag_name == "html":
            self.lang = attrs_dict.get("lang") or None
        elif tag_name == "title":
            self._in_title = True
        elif tag_name == "meta" and attrs_dict.get("name", "").lower() == "description":
            self.meta_description = attrs_dict.get("content") or None
        elif tag_name == "link":
            rel = {part.strip().lower() for part in attrs_dict.get("rel", "").split()}
            if "canonical" in rel and attrs_dict.get("href"):
                self.canonical = attrs_dict["href"]
        elif tag_name == "h1":
            self._capture_h1 = True
            self._h1_parts = []
        elif tag_name == "p" and "lede" in attrs_dict.get("class", "").split():
            self._capture_lede = True
            self._lede_parts = []
        elif tag_name == "script" and "ld+json" in attrs_dict.get("type", "").lower():
            self._capture_json_ld = True
            self._json_ld_parts = []
        elif tag_name == "form":
            role = attrs_dict.get("role", "").lower()
            action = attrs_dict.get("action", "").lower()
            aria_label = attrs_dict.get("aria-label", "")
            if role == "search" or "search" in action or "搜索" in aria_label:
                self.has_search_form = True
        elif tag_name == "input":
            input_type = attrs_dict.get("type", "").lower()
            name = attrs_dict.get("name", "").lower()
            aria_label = attrs_dict.get("aria-label", "")
            if input_type == "search" or name in {"q", "query", "search"} or "搜索" in aria_label:
                self.has_search_input = True

    def handle_endtag(self, tag: str) -> None:
        tag_name = tag.lower()
        if tag_name == "title":
            self._in_title = False
        elif tag_name == "h1" and self._capture_h1:
            self.h1_values.append(collapse_text("".join(self._h1_parts)))
            self._capture_h1 = False
        elif tag_name == "p" and self._capture_lede:
            self._capture_lede = False
        elif tag_name == "script" and self._capture_json_ld:
            self.json_ld_raw.append("".join(self._json_ld_parts).strip())
            self._capture_json_ld = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self._title_parts.append(data)
        if self._capture_h1:
            self._h1_parts.append(data)
        if self._capture_lede:
            self._lede_parts.append(data)
        if self._capture_json_ld:
            self._json_ld_parts.append(data)

    @property
    def title(self) -> str:
        return collapse_text("".join(self._title_parts))

    @property
    def lede(self) -> str:
        return collapse_text("".join(self._lede_parts))

    @property
    def has_site_search(self) -> bool:
        return self.has_search_form or self.has_search_input


def collapse_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def load_config(path: Path = CONFIG_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"


def parse_homepage(repo_root: Path, config: dict[str, Any]) -> dict[str, Any]:
    home = config["homepage"]
    html = (repo_root / home["html_path"]).read_text(encoding="utf-8")
    parser = HomepageSignalParser()
    parser.feed(html)
    json_ld = []
    parse_errors = []
    for raw in parser.json_ld_raw:
        try:
            json_ld.append(json.loads(raw))
        except json.JSONDecodeError as exc:
            parse_errors.append(str(exc))
    return {
        "lang": parser.lang,
        "title": parser.title,
        "meta_description": parser.meta_description,
        "canonical": parser.canonical,
        "h1_values": parser.h1_values,
        "lede": parser.lede,
        "json_ld_count": len(parser.json_ld_raw),
        "json_ld_parse_errors": parse_errors,
        "json_ld_types": schema_types(json_ld),
        "has_site_search": parser.has_site_search,
        "html_contains_search_action": "SearchAction" in html,
        "identity_statement_present": home["identity_statement"] in html,
        "forbidden_html_markers_present": [
            marker for marker in FORBIDDEN_URL_PARTS if marker in html
        ],
    }


def website_node(home: dict[str, Any]) -> dict[str, Any]:
    return {
        "@type": "WebSite",
        "@id": f"{home['canonical_url']}#website",
        "url": home["canonical_url"],
        "name": home["h1"],
        "description": home["schema_description"],
        "inLanguage": home["in_language"],
    }


def page_node(home: dict[str, Any], schema_type: str, fragment: str) -> dict[str, Any]:
    return {
        "@type": schema_type,
        "@id": f"{home['canonical_url']}#{fragment}",
        "url": home["canonical_url"],
        "name": home["h1"],
        "description": home["schema_description"],
        "inLanguage": home["in_language"],
        "isPartOf": {
            "@id": f"{home['canonical_url']}#website",
        },
    }


def build_drafts(config: dict[str, Any]) -> dict[str, dict[str, Any]]:
    home = config["homepage"]
    site = website_node(home)
    drafts: dict[str, dict[str, Any]] = {}
    for option in config["options"]:
        schema_types = option["schema_types"]
        if schema_types == ["WebSite"]:
            draft = {"@context": config["schema_context"], **site}
        elif schema_types == ["WebSite", "WebPage"]:
            draft = {
                "@context": config["schema_context"],
                "@graph": [
                    site,
                    page_node(home, "WebPage", "webpage"),
                ],
            }
        elif schema_types == ["WebSite", "CollectionPage"]:
            draft = {
                "@context": config["schema_context"],
                "@graph": [
                    site,
                    page_node(home, "CollectionPage", "collectionpage"),
                ],
            }
        else:
            raise ValueError(f"unsupported option schema_types: {schema_types}")
        drafts[option["draft_file"]] = draft
    return drafts


def walk_values(value: Any) -> list[Any]:
    if isinstance(value, dict):
        values: list[Any] = []
        for child in value.values():
            values.extend(walk_values(child))
        return values
    if isinstance(value, list):
        values = []
        for child in value:
            values.extend(walk_values(child))
        return values
    return [value]


def collect_keys(value: Any) -> list[str]:
    if isinstance(value, dict):
        keys = list(value.keys())
        for child in value.values():
            keys.extend(collect_keys(child))
        return keys
    if isinstance(value, list):
        keys: list[str] = []
        for child in value:
            keys.extend(collect_keys(child))
        return keys
    return []


def collect_nodes(draft: dict[str, Any]) -> list[dict[str, Any]]:
    if "@graph" in draft:
        return [node for node in draft.get("@graph", []) if isinstance(node, dict)]
    return [draft]


def schema_types(items: list[Any]) -> list[str]:
    values: list[str] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        value = item.get("@type")
        if isinstance(value, list):
            values.extend(str(child) for child in value)
        elif value:
            values.append(str(value))
    return values


def draft_schema_types(draft: dict[str, Any]) -> list[str]:
    values: list[str] = []

    def collect(value: Any) -> None:
        if isinstance(value, dict):
            type_value = value.get("@type")
            if isinstance(type_value, list):
                values.extend(str(child) for child in type_value)
            elif type_value:
                values.append(str(type_value))
            for child in value.values():
                collect(child)
        elif isinstance(value, list):
            for child in value:
                collect(child)

    collect(draft)
    return values


def output_targets(repo_root: Path, output_dir: Path, files: list[str]) -> list[Path]:
    base = output_dir if output_dir.is_absolute() else repo_root / output_dir
    return [base / file_name for file_name in files]


def targets_avoid_app_public(repo_root: Path, targets: list[Path]) -> bool:
    root = repo_root.resolve()
    for target in targets:
        resolved = target.resolve()
        try:
            relative = resolved.relative_to(root)
        except ValueError:
            continue
        if relative.parts and relative.parts[0] in {"app", "public"}:
            return False
    return True


def finding_status(repo_root: Path, finding_id: str) -> str | None:
    path = repo_root / "docs/06b-page-audit-findings.csv"
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row.get("finding_id") == finding_id:
                return row.get("status")
    return None


def status_for(ok: bool) -> str:
    return "pass" if ok else "fail"


def add_check(checks: list[dict[str, str]], check_id: str, ok: bool, detail: str) -> None:
    checks.append({"id": check_id, "status": status_for(ok), "detail": detail})


def has_duplicate_base_path(value: str) -> bool:
    return "/yhl-geo-portfolio/yhl-geo-portfolio/" in value


def has_public_id(value: str) -> bool:
    return value.startswith(PUBLIC_URL_PREFIX)


def validate_draft(
    draft: dict[str, Any],
    option: dict[str, Any],
    config: dict[str, Any],
    homepage_signals: dict[str, Any],
) -> list[dict[str, str]]:
    checks: list[dict[str, str]] = []
    home = config["homepage"]
    nodes = collect_nodes(draft)
    string_values = [value for value in walk_values(draft) if isinstance(value, str)]
    keys = collect_keys(draft)
    types = draft_schema_types(draft)
    id_values = [node.get("@id") for node in nodes if isinstance(node.get("@id"), str)]
    url_values = [node.get("url") for node in nodes if isinstance(node.get("url"), str)]
    name_values = [node.get("name") for node in nodes if isinstance(node.get("name"), str)]
    description_values = [
        node.get("description") for node in nodes if isinstance(node.get("description"), str)
    ]
    language_values = [
        node.get("inLanguage") for node in nodes if isinstance(node.get("inLanguage"), str)
    ]

    round_tripped = json.loads(dump_json(draft))
    add_check(
        checks,
        f"{option['option_id']}_json_parseable",
        round_tripped == draft,
        f"{option['draft_file']} round-trips as JSON",
    )
    add_check(
        checks,
        f"{option['option_id']}_context",
        draft.get("@context") == config["schema_context"],
        "@context is https://schema.org",
    )
    add_check(
        checks,
        f"{option['option_id']}_schema_types",
        types == option["schema_types"],
        f"@type sequence is {option['schema_types']}",
    )
    add_check(
        checks,
        f"{option['option_id']}_ids_are_public",
        bool(id_values) and all(has_public_id(value) for value in id_values),
        "@id values use public GitHub Pages URL",
    )
    add_check(
        checks,
        f"{option['option_id']}_url_matches_canonical",
        bool(url_values) and all(value == home["canonical_url"] for value in url_values),
        "all url values match homepage canonical",
    )
    add_check(
        checks,
        f"{option['option_id']}_name_matches_h1",
        bool(name_values) and all(value == home["h1"] for value in name_values),
        "all name values match current homepage H1",
    )
    add_check(
        checks,
        f"{option['option_id']}_description_matches_public_summary",
        bool(description_values)
        and all(value == home["schema_description"] for value in description_values)
        and homepage_signals["lede"] == home["schema_description"],
        "description equals the rendered public homepage summary",
    )
    add_check(
        checks,
        f"{option['option_id']}_language",
        bool(language_values) and all(value == home["in_language"] for value in language_values),
        "inLanguage is zh-CN",
    )
    add_check(
        checks,
        f"{option['option_id']}_no_local_or_old_urls",
        not any(marker in value for value in string_values for marker in FORBIDDEN_URL_PARTS),
        "no local user-home, loopback, old-domain or duplicated basePath markers",
    )
    add_check(
        checks,
        f"{option['option_id']}_no_duplicate_base_path",
        not any(has_duplicate_base_path(value) for value in string_values),
        "no duplicated /yhl-geo-portfolio/ basePath",
    )
    add_check(
        checks,
        f"{option['option_id']}_no_forbidden_schema_types",
        not any(value in config["forbidden_schema_types"] for value in types),
        "no Organization, Brand, Person or SearchAction types",
    )
    add_check(
        checks,
        f"{option['option_id']}_no_forbidden_properties",
        not any(key in config["forbidden_properties"] for key in keys)
        and all(key in ALLOWED_PROPERTIES for key in keys),
        "only whitelisted properties are present",
    )
    add_check(
        checks,
        f"{option['option_id']}_no_search_action",
        "SearchAction" not in types and "potentialAction" not in keys,
        "SearchAction is absent because no verified site search exists",
    )
    add_check(
        checks,
        f"{option['option_id']}_no_false_effect_or_official_claim",
        not any(fragment in value for value in string_values for fragment in config["forbidden_text_fragments"]),
        "no official-site, official-project, commissioned, growth or effect claims",
    )
    if "WebPage" in option["schema_types"] or "CollectionPage" in option["schema_types"]:
        page_nodes = [node for node in nodes if node.get("@type") in {"WebPage", "CollectionPage"}]
        add_check(
            checks,
            f"{option['option_id']}_page_is_part_of_website",
            len(page_nodes) == 1
            and page_nodes[0].get("isPartOf") == {"@id": f"{home['canonical_url']}#website"},
            "page node points to WebSite with isPartOf",
        )
    return checks


def validate(
    config: dict[str, Any],
    drafts: dict[str, dict[str, Any]],
    repo_root: Path,
    output_dir: Path,
) -> tuple[dict[str, Any], dict[str, Any]]:
    checks: list[dict[str, str]] = []
    home = config["homepage"]
    homepage_signals = parse_homepage(repo_root, config)

    expected_files = [option["draft_file"] for option in config["options"]]
    planned_files = expected_files + [
        DEFAULT_COMPARISON_NAME,
        DEFAULT_VALIDATION_NAME,
        DEFAULT_METADATA_NAME,
    ]

    add_check(
        checks,
        "expected_three_drafts",
        sorted(drafts) == sorted(expected_files) and len(drafts) == 3,
        "exactly WebSite, WebSite+WebPage and WebSite+CollectionPage drafts are planned",
    )
    add_check(
        checks,
        "homepage_canonical_matches_html",
        homepage_signals["canonical"] == home["canonical_url"],
        "homepage canonical matches rendered HTML and config",
    )
    add_check(
        checks,
        "homepage_title_matches_html",
        homepage_signals["title"] == home["title"],
        "homepage title matches rendered HTML and config",
    )
    add_check(
        checks,
        "homepage_meta_description_matches_html",
        homepage_signals["meta_description"] == home["metadata_description"],
        "homepage meta description matches rendered HTML and config",
    )
    add_check(
        checks,
        "homepage_h1_matches_html",
        homepage_signals["h1_values"] == [home["h1"]],
        "homepage has exactly one H1 and it matches config",
    )
    add_check(
        checks,
        "homepage_summary_matches_html",
        homepage_signals["lede"] == home["schema_description"],
        "homepage public summary matches proposed Schema description",
    )
    add_check(
        checks,
        "homepage_language_matches_html",
        homepage_signals["lang"] == home["in_language"],
        "homepage html lang is zh-CN",
    )
    add_check(
        checks,
        "homepage_has_no_jsonld_now",
        homepage_signals["json_ld_count"] == 0,
        "current homepage still has no JSON-LD before any future injection",
    )
    add_check(
        checks,
        "homepage_has_no_site_search",
        homepage_signals["has_site_search"] is False
        and homepage_signals["html_contains_search_action"] is False
        and home["has_site_search"] is False,
        "no verified homepage site search or SearchAction input",
    )
    add_check(
        checks,
        "homepage_identity_statement_present",
        homepage_signals["identity_statement_present"] is True,
        "rendered homepage includes independent research and non-official statement",
    )
    add_check(
        checks,
        "homepage_html_has_no_forbidden_markers",
        homepage_signals["forbidden_html_markers_present"] == [],
        "rendered homepage has no local path, old domain or duplicate basePath marker",
    )
    add_check(
        checks,
        "stable_jsonld_generation",
        {name: dump_json(data) for name, data in build_drafts(copy.deepcopy(config)).items()}
        == {name: dump_json(data) for name, data in build_drafts(copy.deepcopy(config)).items()},
        "same config produces byte-stable JSON-LD draft content",
    )
    add_check(
        checks,
        "no_app_or_public_write_targets",
        targets_avoid_app_public(repo_root, output_targets(repo_root, output_dir, planned_files)),
        "planned outputs do not target app/ or public/",
    )
    add_check(
        checks,
        "finding_06b_pa_001_still_open",
        finding_status(repo_root, "06B-PA-001") == "open",
        "06B-PA-001 remains open because this stage does not inject homepage JSON-LD",
    )

    per_option: dict[str, list[dict[str, str]]] = {}
    for option in config["options"]:
        option_checks = validate_draft(
            drafts[option["draft_file"]],
            option,
            config,
            homepage_signals,
        )
        per_option[option["option_id"]] = option_checks
        checks.extend(option_checks)

    all_passed = all(check["status"] == "pass" for check in checks)
    validation = {
        "stage": config["stage"],
        "validation_status": "valid" if all_passed else "invalid",
        "draft_count": len(drafts),
        "homepage_facts": {
            "canonical": homepage_signals["canonical"],
            "title": homepage_signals["title"],
            "meta_description": homepage_signals["meta_description"],
            "h1": homepage_signals["h1_values"][0] if homepage_signals["h1_values"] else None,
            "summary": homepage_signals["lede"],
            "language": homepage_signals["lang"],
            "json_ld_count": homepage_signals["json_ld_count"],
            "has_site_search": homepage_signals["has_site_search"],
        },
        "drafts": [
            {
                "option_id": option["option_id"],
                "schema_types": option["schema_types"],
                "draft_file": option["draft_file"],
                "recommended_status": option["recommended_status"],
                "status": "valid"
                if all(check["status"] == "pass" for check in per_option[option["option_id"]])
                else "manual-review",
            }
            for option in config["options"]
        ],
        "checks": checks,
    }
    return validation, homepage_signals


def build_report(
    config: dict[str, Any],
    validation: dict[str, Any],
    homepage_signals: dict[str, Any],
) -> str:
    home = config["homepage"]
    lines = [
        "# 07D1 首页 Schema 类型评估与隔离草稿报告",
        "",
        f"生成日期：{config['generated_date']}",
        "",
        "## 范围",
        "",
        "本阶段只评估首页 `06B-PA-001`（首页无 JSON-LD），并生成三个隔离 JSON-LD 草稿。未注入页面，未修改 `app/` 或 `public/`。",
        "",
        "## 首页事实",
        "",
        "| item | observed value | source |",
        "|---|---|---|",
        f"| canonical | {homepage_signals['canonical']} | `{home['html_path']}` link rel=canonical |",
        f"| title | {homepage_signals['title']} | `{home['source_file']}` metadata and `{home['html_path']}` |",
        f"| meta description | {homepage_signals['meta_description']} | `{home['source_file']}` metadata and `{home['html_path']}` |",
        f"| H1 | {homepage_signals['h1_values'][0] if homepage_signals['h1_values'] else ''} | `{home['source_file']}` and `{home['html_path']}` |",
        f"| public summary | {homepage_signals['lede']} | homepage hero `.lede` |",
        f"| language | {homepage_signals['lang']} | `app/layout.tsx` and rendered html lang |",
        f"| project identity | {home['identity_statement']} | global footer in `app/components.tsx` |",
        f"| existing JSON-LD | {homepage_signals['json_ld_count']} script(s) | rendered homepage |",
        f"| site search | {'yes' if homepage_signals['has_site_search'] else 'no'} | rendered homepage form/input scan |",
        "",
        "主要模块：",
        "",
    ]
    for module in home["modules"]:
        lines.append(f"- {module}")
    lines.extend(
        [
            "",
            "## 方案比较",
            "",
            "| option | schema types | status | evaluation |",
            "|---|---|---|---|",
            "| 07D1-A | WebSite | alternative | 字段最少、身份风险最低，可以解决 finding；但只描述站点，不显式描述当前首页这个页面，页面匹配度略弱。 |",
            "| 07D1-B | WebSite + WebPage | recommended | 与首页作为站点入口和具体页面的双重事实最匹配；不需要 publisher、author、Organization、Brand、Person 或 SearchAction，维护成本仍低。 |",
            "| 07D1-C | WebSite + CollectionPage | reject | 首页确实包含内容入口，但同时是诊断看板、方法说明和项目叙事；CollectionPage 会把页面过度建模为集合页。 |",
            "",
            "## 推荐草稿",
            "",
            "推荐选择 `07D1-B`：`WebSite + WebPage`。推荐 name 使用当前 H1，推荐 description 使用当前首页可见摘要原文，以保留非官方与独立研究边界。",
            "",
            "本阶段不设置 `publisher`，不生成 `Organization`、`Brand`、`Person`，不生成 `SearchAction`。",
            "",
            "## 验证结果",
            "",
            f"总体状态：`{validation['validation_status']}`",
            "",
            "| check | status | detail |",
            "|---|---|---|",
        ]
    )
    for check in validation["checks"]:
        lines.append(f"| `{check['id']}` | `{check['status']}` | {check['detail']} |")
    lines.extend(
        [
            "",
            "## 后续人工审核",
            "",
            "进入 07D2 注入前，需要人工确认最终 Schema 类型、name、description、是否继续不设置 publisher / Organization / Brand / Person / SearchAction，以及是否允许下一阶段写入首页。",
            "",
        ]
    )
    return "\n".join(lines)


def build_metadata(config: dict[str, Any], validation: dict[str, Any]) -> dict[str, Any]:
    return {
        "stage": config["stage"],
        "stage_name": config["stage_name"],
        "generated_date": config["generated_date"],
        "script": "tools/geo-skill/adapters/schema-draft/build_home_schema_drafts.py",
        "config": "tools/geo-skill/adapters/schema-draft/home-schema-config.json",
        "python_standard_library_only": True,
        "network_access": "not-used",
        "api_calls": "none",
        "model_calls": "none",
        "new_dependencies": "none",
        "page_injection": "no",
        "app_public_write": "no",
        "internal_review_file_content_read": "no",
        "archive_file_content_read": "no",
        "source_documents": config["source_documents"],
        "outputs": [
            option["draft_file"] for option in config["options"]
        ] + [
            DEFAULT_COMPARISON_NAME,
            DEFAULT_VALIDATION_NAME,
            DEFAULT_METADATA_NAME,
        ],
        "validation_status": validation["validation_status"],
    }


def build_output_files(
    config: dict[str, Any],
    repo_root: Path,
    output_dir: Path,
) -> dict[str, str]:
    drafts = build_drafts(config)
    validation, homepage_signals = validate(config, drafts, repo_root, output_dir)
    files = {name: dump_json(data) for name, data in drafts.items()}
    files[DEFAULT_COMPARISON_NAME] = build_report(config, validation, homepage_signals)
    files[DEFAULT_VALIDATION_NAME] = dump_json(validation)
    files[DEFAULT_METADATA_NAME] = dump_json(build_metadata(config, validation))
    return files


def write_output_files(files: dict[str, str], repo_root: Path, output_dir: Path) -> None:
    base = output_dir if output_dir.is_absolute() else repo_root / output_dir
    base.mkdir(parents=True, exist_ok=True)
    for file_name, content in files.items():
        (base / file_name).write_text(content, encoding="utf-8")


def build_outputs(
    config: dict[str, Any],
    repo_root: Path,
    output_dir: Path | None = None,
) -> dict[str, str]:
    selected_output_dir = output_dir or Path(config["allowed_output_dir"])
    files = build_output_files(config, repo_root, selected_output_dir)
    write_output_files(files, repo_root, selected_output_dir)
    return files


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default=str(CONFIG_PATH))
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output-dir", default=None)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    config = load_config(Path(args.config))
    output_dir = Path(args.output_dir) if args.output_dir else Path(config["allowed_output_dir"])
    files = build_outputs(config, repo_root, output_dir)
    validation = json.loads(files[DEFAULT_VALIDATION_NAME])
    return 0 if validation["validation_status"] == "valid" else 1


if __name__ == "__main__":
    raise SystemExit(main())
