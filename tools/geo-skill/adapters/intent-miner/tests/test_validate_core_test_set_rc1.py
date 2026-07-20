from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "validate_core_test_set_rc1.py"
SPEC = importlib.util.spec_from_file_location("validate_core_test_set_rc1", MODULE_PATH)
validate_module = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(validate_module)


class CoreTestSetValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repo_root = validate_module.REPO_ROOT

    def validate(self) -> dict:
        return validate_module.validate(self.repo_root)

    def test_validation_passes(self) -> None:
        result = self.validate()
        self.assertTrue(result["ok"], result["errors"])

    def test_core_count_and_non_core_count(self) -> None:
        result = self.validate()
        self.assertEqual(24, result["counts"]["core"])
        self.assertEqual(15, result["counts"]["non_core"])

    def test_core_text_matches_v2(self) -> None:
        v2_by_id = {
            row["id"]: row
            for row in validate_module.read_csv(validate_module.V2_REL, self.repo_root)
        }
        core_rows = validate_module.read_csv(validate_module.CORE_REL, self.repo_root)
        for row in core_rows:
            self.assertEqual(v2_by_id[row["question_id"]]["question"], row["question"])

    def test_cluster_intent_stage_and_risk_coverage(self) -> None:
        result = self.validate()
        self.assertEqual(validate_module.CONTENT_CLUSTERS, set(result["distributions"]["content_cluster"]))
        self.assertEqual(validate_module.PRIMARY_INTENTS, set(result["distributions"]["primary_intent"]))
        self.assertEqual(validate_module.USER_STAGES, set(result["distributions"]["user_stage"]))
        self.assertTrue(validate_module.RISK_LEVELS.issubset(set(result["distributions"]["risk_level"])))
        self.assertGreaterEqual(result["distributions"]["risk_level"]["high"], 14)

    def test_new_questions_are_judged_not_all_selected(self) -> None:
        result = self.validate()
        self.assertEqual(7, result["counts"]["selected_added"])

    def test_non_core_future_use_values_are_allowed(self) -> None:
        rows = validate_module.read_csv(validate_module.NON_CORE_REL, self.repo_root)
        self.assertTrue(all(row["future_use"] in validate_module.FUTURE_USE_VALUES for row in rows))

    def test_evidence_tasks_exist_and_are_not_started(self) -> None:
        rows = validate_module.read_csv(validate_module.BACKLOG_REL, self.repo_root)
        task_ids = {row["evidence_task_id"] for row in rows}
        self.assertTrue(validate_module.EXPECTED_EVIDENCE_TASKS.issubset(task_ids))
        self.assertTrue(all(row["current_status"] == "not-started" for row in rows))

    def test_v1_and_v2_hashes_are_unchanged(self) -> None:
        result = self.validate()
        self.assertEqual(validate_module.CANONICAL_V1_SHA256, result["v1_sha256"])
        self.assertEqual(validate_module.V2_SHA256, result["v2_sha256"])

    def test_output_contains_no_absolute_paths_or_false_metrics(self) -> None:
        result = self.validate()
        rendered = json.dumps(result, ensure_ascii=False, sort_keys=True)
        self.assertNotIn("/Users/", rendered)
        for rel in validate_module.OUTPUT_RELS:
            text = validate_module.read_text(rel, self.repo_root)
            for term in validate_module.FORBIDDEN_PATH_TERMS:
                self.assertNotIn(term, text)
            for term in validate_module.FORBIDDEN_METRIC_TERMS:
                self.assertNotIn(term, text)

    def test_same_input_validation_result_is_stable(self) -> None:
        self.assertEqual(self.validate(), self.validate())


if __name__ == "__main__":
    unittest.main()
