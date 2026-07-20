#!/usr/bin/env python3
"""Validate the 08D1 v2 core24 planning artifacts offline."""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
CANONICAL_V1_REL = "../../../redwood_geo/data/redwood_question_bank_30.csv"
CANONICAL_V1_SHA256 = "ab0661732fffc3e0aa25adabadf5d3b9c58f00baa1c5bf045f5190ebcc596936"
V2_REL = "data/question-bank/redwood_question_bank_v2_rc1.csv"
V2_SHA256 = "de9726f7b1fe8bf0b9e77358e2a8e6b6ab422c754a03a4e171d249104581b538"
CORE_REL = "data/question-bank/redwood_question_bank_v2_core24_rc1.csv"
VERSIONS_REL = "data/question-bank/question_bank_versions.json"
NON_CORE_REL = "docs/08d1-non-core-question-usage.csv"
SELECTION_REL = "docs/08d1-core-test-selection.csv"
MATRIX_REL = "docs/08d1-test-objective-matrix.csv"
BACKLOG_REL = "docs/08d1-evidence-acquisition-backlog.csv"
REPORT_DIR_REL = "tools/geo-skill/reports/core-test-set-pilot"
PROPOSAL_REL = "docs/08b-question-bank-v2-proposal.csv"
CANDIDATES_REL = "docs/08a-candidate-questions.csv"

CONTENT_CLUSTERS = {
    "品牌认知与事实",
    "材质与产品边界",
    "京作、明式与清式",
    "购买与核验",
    "品牌比较与选择",
    "风险、来源与信息边界",
}
PRIMARY_INTENTS = {
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
USER_STAGES = {"awareness", "consideration", "decision", "post-decision", "research"}
RISK_LEVELS = {"high", "medium", "low"}
FUTURE_USE_VALUES = {
    "extended-test-set",
    "page-content",
    "evidence-backlog",
    "periodic-dynamic-check",
    "multimodal-future",
    "retained-in-v2",
}
PRIORITY_VALUES = {"P0", "P1", "P2", "P3"}
BLOCKING_SCOPE_VALUES = {
    "blocks-schema",
    "blocks-page",
    "blocks-answer",
    "blocks-retest-scoring",
    "does-not-block",
}
FLAG_VALUES = {"yes", "no", "conditional"}
EXPECTED_EVIDENCE_TASKS = {"EVID-001", "EVID-002", "EVID-003", "EVID-004", "EVID-005"}
FORBIDDEN_PATH_TERMS = ["/Users/", "file://", "~/"]
FORBIDDEN_METRIC_TERMS = [
    "搜索量",
    "搜索趋势",
    "GEO 总分",
    "GEO总分",
    "引用概率",
    "排名分数",
    "效果预测",
]
OUTPUT_RELS = [
    CORE_REL,
    VERSIONS_REL,
    NON_CORE_REL,
    SELECTION_REL,
    MATRIX_REL,
    BACKLOG_REL,
    "docs/08d1-evidence-acquisition-plan.md",
    "docs/08d1-core-test-protocol.md",
    "docs/08d1-human-review.md",
    "docs/08d1-core-test-set-method.md",
    f"{REPORT_DIR_REL}/report.md",
    f"{REPORT_DIR_REL}/report.json",
    f"{REPORT_DIR_REL}/run-metadata.json",
]


def canonical_v1_path(repo_root: Path = REPO_ROOT) -> Path:
    return (repo_root / CANONICAL_V1_REL).resolve()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_csv(rel: str, repo_root: Path = REPO_ROOT) -> list[dict[str, str]]:
    with (repo_root / rel).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(rel: str, repo_root: Path = REPO_ROOT) -> dict[str, Any]:
    return json.loads((repo_root / rel).read_text(encoding="utf-8"))


def read_text(rel: str, repo_root: Path = REPO_ROOT) -> str:
    return (repo_root / rel).read_text(encoding="utf-8")


def check(condition: bool, name: str, errors: list[str], details: str = "") -> None:
    if not condition:
        errors.append(f"{name}: {details}" if details else name)


def validate(repo_root: Path = REPO_ROOT) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []

    v1_path = canonical_v1_path(repo_root)
    v1_sha = sha256_file(v1_path)
    v2_path = repo_root / V2_REL
    v2_sha = sha256_file(v2_path)

    v2_rows = read_csv(V2_REL, repo_root)
    core_rows = read_csv(CORE_REL, repo_root)
    non_core_rows = read_csv(NON_CORE_REL, repo_root)
    selection_rows = read_csv(SELECTION_REL, repo_root)
    matrix_rows = read_csv(MATRIX_REL, repo_root)
    backlog_rows = read_csv(BACKLOG_REL, repo_root)
    proposal_rows = read_csv(PROPOSAL_REL, repo_root)
    candidate_rows = read_csv(CANDIDATES_REL, repo_root)
    versions = read_json(VERSIONS_REL, repo_root)

    v2_by_id = {row["id"]: row for row in v2_rows}
    proposal_by_id: dict[str, dict[str, str]] = {}
    for row in proposal_rows:
        qid = row["current_question_id"] or f"q{int(row['proposed_order']):02d}"
        proposal_by_id[qid] = row
    candidate_013 = next(row for row in candidate_rows if row["candidate_id"] == "CAND-INTENT-013")

    core_ids = [row["question_id"] for row in core_rows]
    non_core_ids = [row["question_id"] for row in non_core_rows]
    selected_ids_from_selection = [row["question_id"] for row in selection_rows if row["selected"] == "yes"]
    not_selected_ids_from_selection = [row["question_id"] for row in selection_rows if row["selected"] == "no"]

    check(v1_sha == CANONICAL_V1_SHA256, "v1_hash_unchanged", errors, v1_sha)
    check(v2_sha == V2_SHA256, "v2_hash_unchanged", errors, v2_sha)
    check(len(v2_rows) == 39, "v2_count_is_39", errors, str(len(v2_rows)))
    check(len(core_rows) == 24, "core_count_is_24", errors, str(len(core_rows)))
    check(len(non_core_rows) == 15, "non_core_count_is_15", errors, str(len(non_core_rows)))
    check(len(selection_rows) == 39, "selection_count_is_39", errors, str(len(selection_rows)))
    check(set(core_ids).issubset(v2_by_id), "all_core_ids_exist_in_v2", errors)
    check([row["question"] for row in core_rows] == [v2_by_id[row["question_id"]]["question"] for row in core_rows], "core_questions_match_v2_exactly", errors)
    check(len(core_ids) == len(set(core_ids)), "no_duplicate_core_question_id", errors)
    check(len({row["question"] for row in core_rows}) == len(core_rows), "no_duplicate_core_question_text", errors)
    check([int(row["core_order"]) for row in core_rows] == list(range(1, 25)), "core_order_is_1_to_24", errors)
    check(set(core_ids).isdisjoint(non_core_ids), "core_and_non_core_disjoint", errors)
    check(set(core_ids + non_core_ids) == set(v2_by_id), "core_plus_non_core_cover_all_v2", errors)
    check(selected_ids_from_selection == core_ids, "selection_yes_matches_core_order", errors)
    check(set(not_selected_ids_from_selection) == set(non_core_ids), "selection_no_matches_non_core", errors)
    check(all(row["selected"] in {"yes", "no"} for row in selection_rows), "selection_values_allowed", errors)
    check(all(row["review_status"] == "pending-human-review" for row in core_rows), "core_review_status_pending", errors)
    check(all(row["source_version"] == "v2-rc1" for row in core_rows), "core_source_version_v2_rc1", errors)
    check(all(row["question_id"] in v2_by_id for row in matrix_rows), "matrix_ids_exist_in_v2", errors)
    check([row["question_id"] for row in matrix_rows] == core_ids, "matrix_matches_core_order", errors)

    cluster_counts = Counter(row["content_cluster"] for row in core_rows)
    intent_counts = Counter(row["primary_intent"] for row in core_rows)
    stage_counts = Counter(row["user_stage"] for row in core_rows)
    risk_counts = Counter(row["risk_level"] for row in core_rows)
    check(set(cluster_counts) == CONTENT_CLUSTERS, "all_six_clusters_covered", errors, str(dict(cluster_counts)))
    check(min(cluster_counts.values()) >= 3, "each_cluster_at_least_3", errors, str(dict(cluster_counts)))
    check(set(intent_counts) == PRIMARY_INTENTS, "all_ten_intents_covered", errors, str(dict(intent_counts)))
    check(set(stage_counts) == USER_STAGES, "all_user_stages_covered", errors, str(dict(stage_counts)))
    check(stage_counts["awareness"] >= 2, "awareness_at_least_2", errors, str(stage_counts["awareness"]))
    check(stage_counts["consideration"] >= 5, "consideration_at_least_5", errors, str(stage_counts["consideration"]))
    check(stage_counts["decision"] >= 5, "decision_at_least_5", errors, str(stage_counts["decision"]))
    check(stage_counts["post-decision"] >= 1, "post_decision_at_least_1", errors, str(stage_counts["post-decision"]))
    check(stage_counts["research"] >= 5, "research_at_least_5", errors, str(stage_counts["research"]))
    check(RISK_LEVELS.issubset(set(risk_counts)), "high_medium_low_covered", errors, str(dict(risk_counts)))
    check(risk_counts["high"] >= 14, "high_risk_at_least_14", errors, str(risk_counts["high"]))
    if risk_counts["medium"] < 6:
        warnings.append(f"medium_risk_below_recommended: {risk_counts['medium']}")
    if risk_counts["low"] < 1:
        warnings.append(f"low_risk_below_recommended: {risk_counts['low']}")

    check(candidate_013["candidate_question"] not in {row["question"] for row in core_rows}, "cand_intent_013_not_in_core", errors)
    selected_new = [qid for qid in core_ids if int(qid[1:]) >= 31]
    check(0 < len(selected_new) < 9, "new_questions_not_all_selected", errors, str(selected_new))
    check(all(row["future_use"] in FUTURE_USE_VALUES for row in non_core_rows), "non_core_future_use_allowed", errors)
    check(not any(row["future_use"] == "delete" for row in non_core_rows), "non_core_not_deleted", errors)

    matrix_flag_fields = [
        "brand_mention_relevant",
        "positioning_accuracy_relevant",
        "factual_accuracy_relevant",
        "source_traceability_relevant",
        "boundary_control_relevant",
        "recommendation_position_relevant",
        "response_stability_relevant",
    ]
    for field in matrix_flag_fields:
        bad_values = sorted({row[field] for row in matrix_rows} - FLAG_VALUES)
        check(not bad_values, f"matrix_{field}_values_allowed", errors, ",".join(bad_values))

    task_ids = {row["evidence_task_id"] for row in backlog_rows}
    check(EXPECTED_EVIDENCE_TASKS.issubset(task_ids), "five_evidence_tasks_exist", errors, str(task_ids))
    check(all(row["priority"] in PRIORITY_VALUES for row in backlog_rows), "evidence_priority_allowed", errors)
    check(all(row["blocking_scope"] in BLOCKING_SCOPE_VALUES for row in backlog_rows), "evidence_blocking_scope_allowed", errors)
    check(all(row["current_status"] == "not-started" for row in backlog_rows), "evidence_status_not_started", errors)
    check(all(row["requires_human_approval"] == "yes" for row in backlog_rows), "evidence_requires_human_approval", errors)

    check(versions.get("current_canonical_version") == "v1", "manifest_current_canonical_v1", errors)
    check(versions.get("canonical_switch_status") == "not-switched", "manifest_not_switched", errors)
    check(versions.get("release_candidate_version") == "v2-rc1", "manifest_release_candidate_v2_rc1", errors)
    check(versions.get("release_candidate_review_status") == "approved", "manifest_release_candidate_approved", errors)
    check(versions.get("website_consuming_v2") is False, "manifest_website_not_consuming_v2", errors)
    check(versions.get("platform_retest_using_v2") is False, "manifest_platform_not_using_v2", errors)
    check(versions.get("core_test_candidate_version") == "v2-core24-rc1", "manifest_core_candidate_version", errors)
    check(versions.get("core_test_candidate_file") == CORE_REL, "manifest_core_candidate_file", errors)
    check(versions.get("core_test_candidate_count") == 24, "manifest_core_candidate_count", errors)
    check(versions.get("core_test_review_status") == "pending", "manifest_core_review_pending", errors)
    check(versions.get("platform_retest_status") == "not-started", "manifest_platform_retest_not_started", errors)

    for rel in OUTPUT_RELS:
        text = read_text(rel, repo_root)
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
            "v2": len(v2_rows),
            "core": len(core_rows),
            "non_core": len(non_core_rows),
            "selected_added": len(selected_new),
        },
        "distributions": {
            "content_cluster": dict(cluster_counts),
            "primary_intent": dict(intent_counts),
            "user_stage": dict(stage_counts),
            "risk_level": dict(risk_counts),
        },
        "files": {
            "core": CORE_REL,
            "non_core": NON_CORE_REL,
            "selection": SELECTION_REL,
            "matrix": MATRIX_REL,
            "evidence_backlog": BACKLOG_REL,
            "report_dir": REPORT_DIR_REL,
        },
        "v1_sha256": v1_sha,
        "v2_sha256": v2_sha,
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    result = validate()
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
