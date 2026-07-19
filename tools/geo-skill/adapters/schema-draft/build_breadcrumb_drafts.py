#!/usr/bin/env python3
"""Build isolated BreadcrumbList JSON-LD drafts for the 07B pilot."""

from __future__ import annotations

import argparse
import copy
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


CONFIG_PATH = Path(__file__).with_name("breadcrumb-config.json")
DEFAULT_REPORT_NAME = "breadcrumb-draft-report.md"
DEFAULT_VALIDATION_NAME = "breadcrumb-validation.json"
DEFAULT_METADATA_NAME = "run-metadata.json"

FORBIDDEN_SCHEMA_TYPES = {
    "AggregateRating",
    "Article",
    "Brand",
    "FAQPage",
    "Offer",
    "Organization",
    "Person",
    "Product",
    "Review",
}

FORBIDDEN_PROPERTIES = {
    "about",
    "aggregateRating",
    "author",
    "brand",
    "dateModified",
    "datePublished",
    "hasPart",
    "logo",
    "manufacturer",
    "material",
    "mentions",
    "offers",
    "publisher",
    "review",
    "seller",
}

ALLOWED_PROPERTIES = {"@context", "@type", "itemListElement", "position", "name", "item"}
FORBIDDEN_URL_PARTS = (
    "chatgpt.site",
    "localhost",
    "127.0.0.1",
    "/Users/",
    "/yhl-geo-portfolio/yhl-geo-portfolio/",
)


class PageSignalParser(HTMLParser):
    """Collect the few rendered HTML signals needed for this isolated pilot."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.canonical: str | None = None
        self._in_title = False
        self._h1_depth = 0
        self._title_parts: list[str] = []
        self._h1_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {key.lower(): value or "" for key, value in attrs}
        if tag.lower() == "title":
            self._in_title = True
        if tag.lower() == "h1" and self._h1_depth == 0:
            self._h1_depth = 1
        elif self._h1_depth > 0:
            self._h1_depth += 1
        if tag.lower() == "link":
            rel = {part.strip().lower() for part in attr.get("rel", "").split()}
            if "canonical" in rel and attr.get("href"):
                self.canonical = attr["href"]

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "title":
            self._in_title = False
        if self._h1_depth > 0:
            self._h1_depth -= 1

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self._title_parts.append(data)
        if self._h1_depth > 0:
            self._h1_parts.append(data)

    @property
    def title(self) -> str:
        return collapse_text("".join(self._title_parts))

    @property
    def h1(self) -> str:
        return collapse_text("".join(self._h1_parts))


def collapse_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def load_config(path: Path = CONFIG_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"


def extract_page_signals(repo_root: Path, relative_path: str) -> dict[str, str | None]:
    path = repo_root / relative_path
    parser = PageSignalParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return {"title": parser.title, "h1": parser.h1, "canonical": parser.canonical}


def build_drafts(config: dict[str, Any]) -> dict[str, dict[str, Any]]:
    root = config["root"]
    drafts: dict[str, dict[str, Any]] = {}
    for page in config["pages"]:
        drafts[page["draft_file"]] = {
            "@context": config["schema_context"],
            "@type": config["schema_type"],
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": 1,
                    "name": root["name"],
                    "item": root["canonical_url"],
                },
                {
                    "@type": "ListItem",
                    "position": 2,
                    "name": page["page_name"],
                    "item": page["canonical_url"],
                },
            ],
        }
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


def status_for(ok: bool) -> str:
    return "pass" if ok else "fail"


def add_check(checks: list[dict[str, str]], check_id: str, ok: bool, detail: str) -> None:
    checks.append({"id": check_id, "status": status_for(ok), "detail": detail})


def has_duplicate_base_path(url: str) -> bool:
    return "/yhl-geo-portfolio/yhl-geo-portfolio/" in url


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


def validate(
    config: dict[str, Any],
    drafts: dict[str, dict[str, Any]],
    repo_root: Path,
    output_dir: Path,
) -> tuple[dict[str, Any], dict[str, dict[str, str | None]]]:
    checks: list[dict[str, str]] = []
    page_signals: dict[str, dict[str, str | None]] = {}

    expected_files = [page["draft_file"] for page in config["pages"]]
    add_check(
        checks,
        "expected_two_drafts",
        sorted(drafts) == sorted(expected_files) and len(drafts) == 2,
        "exactly /facts and /buying-guide draft files are planned",
    )

    root_signals = extract_page_signals(repo_root, config["root"]["html_path"])
    page_signals[config["root"]["route"]] = root_signals
    add_check(
        checks,
        "homepage_canonical_matches_html",
        root_signals["canonical"] == config["root"]["canonical_url"],
        "homepage canonical matches rendered HTML and config",
    )

    stable_a = {name: dump_json(data) for name, data in build_drafts(copy.deepcopy(config)).items()}
    stable_b = {name: dump_json(data) for name, data in build_drafts(copy.deepcopy(config)).items()}
    add_check(
        checks,
        "stable_jsonld_generation",
        stable_a == stable_b,
        "same config produces byte-stable JSON-LD draft content",
    )

    planned_files = expected_files + [DEFAULT_REPORT_NAME, DEFAULT_VALIDATION_NAME, DEFAULT_METADATA_NAME]
    add_check(
        checks,
        "no_app_or_public_write_targets",
        targets_avoid_app_public(repo_root, output_targets(repo_root, output_dir, planned_files)),
        "planned outputs do not target app/ or public/",
    )

    for page in config["pages"]:
        draft = drafts[page["draft_file"]]
        signals = extract_page_signals(repo_root, page["html_path"])
        page_signals[page["route"]] = signals
        elements = draft.get("itemListElement")
        values = walk_values(draft)
        keys = collect_keys(draft)
        type_values = [value for value in values if isinstance(value, str)]
        string_values = [value for value in values if isinstance(value, str)]
        item_urls = [
            element.get("item")
            for element in elements
            if isinstance(element, dict) and isinstance(element.get("item"), str)
        ] if isinstance(elements, list) else []

        add_check(
            checks,
            f"{page['route']}_jsonld_context",
            draft.get("@context") == "https://schema.org",
            f"{page['draft_file']} uses https://schema.org",
        )
        add_check(
            checks,
            f"{page['route']}_jsonld_type",
            draft.get("@type") == "BreadcrumbList",
            f"{page['draft_file']} uses BreadcrumbList only",
        )
        add_check(
            checks,
            f"{page['route']}_item_list_array",
            isinstance(elements, list),
            "itemListElement is an array",
        )
        add_check(
            checks,
            f"{page['route']}_positions_continuous",
            isinstance(elements, list)
            and [item.get("position") for item in elements if isinstance(item, dict)] == [1, 2],
            "positions are 1 and 2",
        )
        add_check(
            checks,
            f"{page['route']}_homepage_position_1",
            isinstance(elements, list)
            and elements[0].get("name") == config["root"]["name"]
            and elements[0].get("item") == config["root"]["canonical_url"],
            "homepage is position 1",
        )
        add_check(
            checks,
            f"{page['route']}_target_position_2",
            isinstance(elements, list)
            and elements[1].get("name") == page["page_name"]
            and elements[1].get("item") == page["canonical_url"],
            "target page is position 2",
        )
        add_check(
            checks,
            f"{page['route']}_canonical_matches_html",
            signals["canonical"] == page["canonical_url"],
            "draft target URL matches rendered canonical",
        )
        add_check(
            checks,
            f"{page['route']}_h1_matches_current_page",
            signals["h1"] == page.get("h1", page["page_name"]),
            "rendered H1 matches current page config",
        )
        add_check(
            checks,
            f"{page['route']}_no_extra_levels",
            isinstance(elements, list) and len(elements) == 2,
            "breadcrumb contains only homepage and target page",
        )
        add_check(
            checks,
            f"{page['route']}_list_items_complete",
            isinstance(elements, list)
            and all(
                isinstance(item, dict)
                and item.get("@type") == "ListItem"
                and isinstance(item.get("name"), str)
                and isinstance(item.get("item"), str)
                for item in elements
            ),
            "each ListItem has @type, name and item",
        )
        add_check(
            checks,
            f"{page['route']}_no_duplicate_base_path",
            not any(has_duplicate_base_path(url) for url in item_urls),
            "no duplicated /yhl-geo-portfolio/ basePath",
        )
        add_check(
            checks,
            f"{page['route']}_no_forbidden_url_parts",
            not any(part in value for value in string_values for part in FORBIDDEN_URL_PARTS),
            "no chatgpt.site, localhost, 127.0.0.1, local absolute path markers or duplicated basePath",
        )
        add_check(
            checks,
            f"{page['route']}_no_forbidden_schema_types",
            not any(value in FORBIDDEN_SCHEMA_TYPES for value in type_values),
            "no Organization, Brand, Person, Article, FAQPage, Product, Offer, Review or AggregateRating",
        )
        add_check(
            checks,
            f"{page['route']}_no_forbidden_properties",
            not any(key in FORBIDDEN_PROPERTIES for key in keys)
            and all(key in ALLOWED_PROPERTIES for key in keys),
            "only BreadcrumbList/ListItem properties are present",
        )

    all_passed = all(check["status"] == "pass" for check in checks)
    validation = {
        "stage": config["stage"],
        "validation_status": "valid" if all_passed else "invalid",
        "draft_count": len(drafts),
        "checks": checks,
        "drafts": [
            {
                "draft_id": page["draft_id"],
                "route": page["route"],
                "draft_file": page["draft_file"],
                "status": "valid" if all_passed else "manual-review",
            }
            for page in config["pages"]
        ],
    }
    return validation, page_signals


def build_report(
    config: dict[str, Any],
    validation: dict[str, Any],
    page_signals: dict[str, dict[str, str | None]],
) -> str:
    lines = [
        "# 07B BreadcrumbList 隔离草稿报告",
        "",
        f"生成日期：{config['generated_date']}",
        "",
        "## 范围",
        "",
        "本阶段只为 `/facts` 和 `/buying-guide` 生成 `BreadcrumbList` JSON-LD 隔离草稿。首页只作为 position 1 的根节点，不为首页生成独立草稿。",
        "",
        "草稿只写入 `tools/geo-skill/reports/schema-draft-pilot/`，未注入页面，未修改 `app/` 或 `public/`。",
        "",
        "## breadcrumb-ready 为 0 的说明",
        "",
        "`docs/07a2-schema-candidate-classification.csv` 中 14 个实体图谱候选均不具备 breadcrumb-ready 输入属性，`allowed_in_07b` 均为 `no`。这些候选属于品牌实体、事实、FAQ、Article、QuestionIntent、BoundaryRule 或治理规则候选，不是页面层级候选。",
        "",
        "`BreadcrumbList` 的输入不是品牌关系或实体事实，而是已确认的真实页面层级、页面 H1 或可见标题、导航文字和 canonical URL。因此 breadcrumb-ready 为 0 不阻止本阶段生成两个页面级 breadcrumb 草稿，也不得为了增加数量去改写原候选分类。",
        "",
        "## 页面观察",
        "",
        "| route | rendered title | rendered H1 | canonical | nav label | visible breadcrumb |",
        "|---|---|---|---|---|---|",
    ]
    root = config["root"]
    root_signals = page_signals[root["route"]]
    lines.append(
        f"| `/` | {root_signals['title']} | {root_signals['h1']} | {root_signals['canonical']} | 研究首页 | none observed |"
    )
    for page in config["pages"]:
        signals = page_signals[page["route"]]
        lines.append(
            f"| `{page['route']}` | {signals['title']} | {signals['h1']} | {signals['canonical']} | {page['nav_label']} | none observed |"
        )
    lines.extend(
        [
            "",
            "## 草稿",
            "",
            "| route | draft file | hierarchy | page name basis |",
            "|---|---|---|---|",
        ]
    )
    for page in config["pages"]:
        lines.append(
            f"| `{page['route']}` | `{page['draft_file']}` | {' > '.join(page['hierarchy'])} | approved short breadcrumb name; current H1 tracked separately |"
        )
    lines.extend(
        [
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
            "## 禁止项确认",
            "",
            "- 未生成 Organization、Brand、Person、Article、FAQPage、Product、Offer、Review 或 AggregateRating Schema。",
            "- 未包含 author、publisher、logo、datePublished、dateModified、brand、material、offers、review 或 aggregateRating 等字段。",
            "- 未写入品牌实体关系、材料关系、京作关系、产品声明或内部治理规则。",
            "- 未读取 `internal-review/` 或 `archive/`。",
            "- 未调用 API、模型或安装新依赖。",
            "- 未修改 `app/` 或 `public/`，未进行页面注入。",
            "",
            "## 后续人工审核",
            "",
            "进入 07B2 注入前，需人工确认两页的页面名称、canonical、导航短标签与 breadcrumb 层级可接受，并确认仍不需要新增中间层级。",
            "",
        ]
    )
    return "\n".join(lines)


def build_metadata(config: dict[str, Any], validation: dict[str, Any]) -> dict[str, Any]:
    return {
        "stage": config["stage"],
        "stage_name": config["stage_name"],
        "generated_date": config["generated_date"],
        "script": "tools/geo-skill/adapters/schema-draft/build_breadcrumb_drafts.py",
        "config": "tools/geo-skill/adapters/schema-draft/breadcrumb-config.json",
        "python_standard_library_only": True,
        "network_access": "not-used",
        "api_calls": "none",
        "model_calls": "none",
        "internal_review_read": "no",
        "archive_read": "no",
        "page_injection": "no",
        "app_public_write": "no",
        "build_command": "not run in 07B; out/ was used as the current read-only build artifact after timestamp and clean-status checks",
        "source_documents": config["source_documents"],
        "outputs": [
            page["draft_file"] for page in config["pages"]
        ] + [DEFAULT_REPORT_NAME, DEFAULT_VALIDATION_NAME, DEFAULT_METADATA_NAME],
        "validation_status": validation["validation_status"],
    }


def build_output_files(
    config: dict[str, Any],
    repo_root: Path,
    output_dir: Path,
) -> dict[str, str]:
    drafts = build_drafts(config)
    validation, page_signals = validate(config, drafts, repo_root, output_dir)
    files = {name: dump_json(data) for name, data in drafts.items()}
    files[DEFAULT_VALIDATION_NAME] = dump_json(validation)
    files[DEFAULT_REPORT_NAME] = build_report(config, validation, page_signals)
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
