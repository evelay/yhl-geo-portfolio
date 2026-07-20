from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "validate_question_bank_v2.py"
SPEC = importlib.util.spec_from_file_location("validate_question_bank_v2", MODULE_PATH)
validate_module = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(validate_module)


class QuestionBankV2ValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repo_root = validate_module.REPO_ROOT
        self.v1_path = validate_module.canonical_v1_path(self.repo_root)

    def validate(self) -> dict:
        return validate_module.validate(self.repo_root)

    def test_validation_passes(self) -> None:
        result = self.validate()
        self.assertTrue(result["ok"], result["errors"])

    def test_v1_hash_matches_expected(self) -> None:
        self.assertEqual(validate_module.CANONICAL_V1_SHA256, validate_module.sha256_file(self.v1_path))

    def test_v2_has_39_rows_and_preserves_v1_30(self) -> None:
        v1_rows = validate_module.read_csv(self.v1_path)
        v2_rows = validate_module.read_csv(self.repo_root / validate_module.V2_REL)
        self.assertEqual(39, len(v2_rows))
        self.assertEqual([row["id"] for row in v1_rows], [row["id"] for row in v2_rows[:30]])
        self.assertEqual([row["question"] for row in v1_rows], [row["question"] for row in v2_rows[:30]])
        for field in ["id", "category", "intent_level", "target_gap", "question", "expected_focus"]:
            self.assertEqual([row[field] for row in v1_rows], [row[field] for row in v2_rows[:30]])

    def test_added_candidates_and_ids_are_exact(self) -> None:
        v2_rows = validate_module.read_csv(self.repo_root / validate_module.V2_REL)
        self.assertEqual([f"q{index:02d}" for index in range(31, 40)], [row["id"] for row in v2_rows[30:]])
        self.assertEqual(validate_module.APPROVED_CANDIDATES, [row["source_candidate_id"] for row in v2_rows[30:]])

    def test_ids_and_question_text_are_clean(self) -> None:
        v2_rows = validate_module.read_csv(self.repo_root / validate_module.V2_REL)
        self.assertEqual(len(v2_rows), len({row["id"] for row in v2_rows}))
        self.assertEqual(len(v2_rows), len({row["question"] for row in v2_rows}))
        self.assertTrue(all(row["id"].strip() for row in v2_rows))
        self.assertTrue(all(row["question"].strip() for row in v2_rows))

    def test_added_high_risk_questions_have_evidence_requirements(self) -> None:
        v2_rows = validate_module.read_csv(self.repo_root / validate_module.V2_REL)
        for row in v2_rows[30:]:
            self.assertTrue(row["primary_intent"])
            self.assertTrue(row["risk_level"])
            if row["risk_level"] == "high":
                self.assertTrue(row["evidence_requirements"])

    def test_unapproved_candidates_are_not_in_v2(self) -> None:
        v2_rows = validate_module.read_csv(self.repo_root / validate_module.V2_REL)
        candidate_rows = {
            row["candidate_id"]: row
            for row in validate_module.read_csv(self.repo_root / validate_module.CANDIDATES_REL)
        }
        source_ids = {row["source_candidate_id"] for row in v2_rows[30:]}
        self.assertFalse(source_ids.intersection(validate_module.EXCLUDED_CANDIDATES))
        v2_questions = {row["question"] for row in v2_rows}
        for candidate_id in validate_module.EXCLUDED_CANDIDATES:
            self.assertNotIn(candidate_rows[candidate_id]["candidate_question"], v2_questions)

    def test_validator_does_not_write_external_canonical(self) -> None:
        before = validate_module.sha256_file(self.v1_path)
        self.validate()
        after = validate_module.sha256_file(self.v1_path)
        self.assertEqual(before, after)

    def test_output_contains_no_absolute_paths_or_false_metrics(self) -> None:
        result = self.validate()
        rendered_result = json.dumps(result, ensure_ascii=False, sort_keys=True)
        self.assertNotIn("/Users/", rendered_result)
        for rel in validate_module.OUTPUT_RELS:
            text = (self.repo_root / rel).read_text(encoding="utf-8")
            for term in validate_module.FORBIDDEN_PATH_TERMS:
                self.assertNotIn(term, text)
            for term in validate_module.FORBIDDEN_METRIC_TERMS:
                self.assertNotIn(term, text)

    def test_same_input_validation_result_is_stable(self) -> None:
        self.assertEqual(self.validate(), self.validate())


if __name__ == "__main__":
    unittest.main()
