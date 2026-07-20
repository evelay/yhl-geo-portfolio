#!/usr/bin/env python3
"""Validate the 08C question bank v2 release candidate offline.

The validator is intentionally read-only. It checks the external v1 canonical
hash, the versioned v2 RC file, mapping/exclusion records, and local 08C docs.
It does not call APIs, crawlers, models, or write to the external canonical.
"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
CANONICAL_V1_REL = "../../../redwood_geo/data/redwood_question_bank_30.csv"
CANONICAL_V1_SHA256 = "ab0661732fffc3e0aa25adabadf5d3b9c58f00baa1c5bf045f5190ebcc596936"
V2_REL = "data/question-bank/redwood_question_bank_v2_rc1.csv"
VERSIONS_REL = "data/question-bank/question_bank_versions.json"
MAPPING_REL = "docs/08c-question-id-mapping.csv"
EXCLUDED_REL = "docs/08c-excluded-candidates.csv"
CANDIDATES_REL = "docs/08a-candidate-questions.csv"

APPROVED_CANDIDATES = [
    "CAND-INTENT-002",
    "CAND-INTENT-003",
    "CAND-INTENT-005",
    "CAND-INTENT-008",
    "CAND-INTENT-010",
    "CAND-INTENT-012",
    "CAND-INTENT-014",
    "CAND-INTENT-015",
    "CAND-INTENT-016",
]
EXCLUDED_CANDIDATES = [
    "CAND-INTENT-001",
    "CAND-INTENT-004",
    "CAND-INTENT-006",
    "CAND-INTENT-007",
    "CAND-INTENT-009",
    "CAND-INTENT-011",
    "CAND-INTENT-013",
    "CAND-INTENT-017",
    "CAND-INTENT-018",
]
FORBIDDEN_PATH_TERMS = ["/Users/", "file://", "~/" ]
FORBIDDEN_METRIC_TERMS = [
    "搜索趋势",
    "搜索量",
    "用户数量",
    "市场需求比例",
    "AI 引用概率",
    "AI引用概率",
    "排名分数",
    "品牌声量",
    "转化率预测",
]
OUTPUT_RELS = [
    V2_REL,
    VERSIONS_REL,
    "data/question-bank/README.md",
    MAPPING_REL,
    EXCLUDED_REL,
    "docs/08c-question-bank-v2-changelog.md",
    "docs/08c-question-bank-v2-validation.md",
    "docs/08c-v2-release-approval.md",
]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def canonical_v1_path(repo_root: Path) -> Path:
    return (repo_root / CANONICAL_V1_REL).resolve()


def check(condition: bool, name: str, errors: list[str], details: str = "") -> None:
    if not condition:
        errors.append(f"{name}: {details}" if details else name)


def validate(repo_root: Path = REPO_ROOT) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []

    v1_path = canonical_v1_path(repo_root)
    v2_path = repo_root / V2_REL
    versions_path = repo_root / VERSIONS_REL
    mapping_path = repo_root / MAPPING_REL
    excluded_path = repo_root / EXCLUDED_REL
    candidates_path = repo_root / CANDIDATES_REL

    v1_sha = sha256_file(v1_path)
    check(v1_sha == CANONICAL_V1_SHA256, "v1_hash_matches_expected", errors, v1_sha)

    v1_rows = read_csv(v1_path)
    v2_rows = read_csv(v2_path)
    mapping_rows = read_csv(mapping_path)
    excluded_rows = read_csv(excluded_path)
    candidates = {row["candidate_id"]: row for row in read_csv(candidates_path)}

    expected_v1_ids = [f"q{index:02d}" for index in range(1, 31)]
    expected_new_ids = [f"q{index:02d}" for index in range(31, 40)]

    check(len(v1_rows) == 30, "v1_count_is_30", errors, str(len(v1_rows)))
    check([row["id"] for row in v1_rows] == expected_v1_ids, "v1_ids_are_q01_to_q30", errors)
    check(len(v2_rows) == 39, "v2_count_is_39", errors, str(len(v2_rows)))
    check(len(mapping_rows) == 39, "mapping_count_is_39", errors, str(len(mapping_rows)))
    check(len(excluded_rows) == 9, "excluded_count_is_9", errors, str(len(excluded_rows)))

    carried_v2 = v2_rows[:30]
    added_v2 = v2_rows[30:]
    check([row["id"] for row in carried_v2] == expected_v1_ids, "first_30_ids_match_v1", errors)
    check([row["question"] for row in carried_v2] == [row["question"] for row in v1_rows], "first_30_questions_match_v1", errors)
    for field in ["id", "category", "intent_level", "target_gap", "question", "expected_focus"]:
        check([row[field] for row in carried_v2] == [row[field] for row in v1_rows], f"first_30_{field}_preserved", errors)

    check([row["id"] for row in added_v2] == expected_new_ids, "new_ids_are_q31_to_q39", errors)
    check([row["source_candidate_id"] for row in added_v2] == APPROVED_CANDIDATES, "approved_candidates_match_added_rows", errors)
    check(len({row["id"] for row in v2_rows}) == len(v2_rows), "question_ids_are_unique", errors)
    check(all(row["id"].strip() for row in v2_rows), "no_empty_question_id", errors)
    check(all(row["question"].strip() for row in v2_rows), "no_empty_question_text", errors)
    check(len({row["question"] for row in v2_rows}) == len(v2_rows), "no_duplicate_question_text", errors)
    check(all(row["primary_intent"].strip() for row in added_v2), "added_rows_have_primary_intent", errors)
    check(all(row["risk_level"].strip() for row in added_v2), "added_rows_have_risk_level", errors)
    high_risk_missing = [row["id"] for row in added_v2 if row["risk_level"] == "high" and not row["evidence_requirements"].strip()]
    check(not high_risk_missing, "high_risk_added_rows_have_evidence", errors, ",".join(high_risk_missing))
    check(all(row["version"] == "v1" for row in carried_v2), "carried_rows_version_v1", errors)
    check(all(row["record_status"] == "canonical-carried-forward" for row in carried_v2), "carried_rows_status", errors)
    check(all(row["added_in_version"] == "v1" for row in carried_v2), "carried_rows_added_in_v1", errors)
    check(all(row["version"] == "v2-rc1" for row in added_v2), "added_rows_version_v2_rc1", errors)
    check(all(row["record_status"] == "approved-candidate" for row in added_v2), "added_rows_status", errors)
    check(all(row["added_in_version"] == "v2-rc1" for row in added_v2), "added_rows_added_in_v2_rc1", errors)
    check(all(row["approval_reference"] == "08B" for row in added_v2), "added_rows_approval_reference_08b", errors)

    excluded_ids = {row["candidate_id"] for row in excluded_rows}
    check(excluded_ids == set(EXCLUDED_CANDIDATES), "excluded_candidates_match_expected", errors, ",".join(sorted(excluded_ids)))
    added_source_ids = {row["source_candidate_id"] for row in added_v2}
    check(not added_source_ids.intersection(EXCLUDED_CANDIDATES), "excluded_candidate_ids_not_in_v2", errors)
    v2_questions = {row["question"] for row in v2_rows}
    mixed_questions = sorted(
        candidate_id for candidate_id in EXCLUDED_CANDIDATES
        if candidates[candidate_id]["candidate_question"] in v2_questions
    )
    check(not mixed_questions, "excluded_candidate_questions_not_in_v2", errors, ",".join(mixed_questions))

    mapping_source_types = {row["source_type"] for row in mapping_rows}
    check(mapping_source_types <= {"carried-from-v1", "approved-from-08b"}, "mapping_source_types_allowed", errors, ",".join(sorted(mapping_source_types)))
    check([row["v2_question_id"] for row in mapping_rows] == [row["id"] for row in v2_rows], "mapping_ids_match_v2_order", errors)
    check([row["candidate_id"] for row in mapping_rows[30:]] == APPROVED_CANDIDATES, "mapping_approved_candidates_match", errors)

    versions = json.loads(read_text(versions_path))
    check(versions.get("current_canonical_version") == "v1", "manifest_current_canonical_v1", errors)
    check(versions.get("release_candidate_version") == "v2-rc1", "manifest_release_candidate_v2_rc1", errors)
    check(versions.get("release_candidate_record_count") == 39, "manifest_v2_count_39", errors)
    check(versions.get("carried_forward_count") == 30, "manifest_carried_count_30", errors)
    check(versions.get("added_count") == 9, "manifest_added_count_9", errors)
    check(versions.get("excluded_candidate_count") == 9, "manifest_excluded_count_9", errors)
    check(versions.get("canonical_switch_status") == "not-switched", "manifest_not_switched", errors)
    check(versions.get("current_canonical_sha256") == CANONICAL_V1_SHA256, "manifest_v1_hash", errors)

    for rel in OUTPUT_RELS:
        path = repo_root / rel
        text = read_text(path)
        for term in FORBIDDEN_PATH_TERMS:
            if term in text:
                errors.append(f"forbidden_absolute_path_in_output: {rel}")
                break
        for term in FORBIDDEN_METRIC_TERMS:
            if term in text:
                errors.append(f"forbidden_metric_term_in_output: {rel}:{term}")

    return {
        "ok": not errors,
        "counts": {
            "v1": len(v1_rows),
            "v2": len(v2_rows),
            "carried_forward": len(carried_v2),
            "added": len(added_v2),
            "excluded": len(excluded_rows),
        },
        "files": {
            "canonical_v1": "redwood_geo/data/redwood_question_bank_30.csv",
            "v2_release_candidate": V2_REL,
            "versions": VERSIONS_REL,
            "mapping": MAPPING_REL,
            "excluded": EXCLUDED_REL,
        },
        "approved_candidates": APPROVED_CANDIDATES,
        "excluded_candidates": EXCLUDED_CANDIDATES,
        "v1_sha256": v1_sha,
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    result = validate()
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
