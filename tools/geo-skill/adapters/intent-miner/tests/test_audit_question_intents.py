from __future__ import annotations

import csv
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "audit_question_intents.py"
SPEC = importlib.util.spec_from_file_location("audit_question_intents", MODULE_PATH)
audit_module = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(audit_module)


class IntentAuditTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repo_root = audit_module.REPO_ROOT
        config = audit_module.read_config()
        self.canonical_path = (self.repo_root / config["inputs"]["canonical_question_bank"]).resolve()

    def run_in_tmp(self):
        tmp = tempfile.TemporaryDirectory()
        output_root = Path(tmp.name)
        result = audit_module.generate(repo_root=self.repo_root, output_root=output_root)
        self.addCleanup(tmp.cleanup)
        return output_root, result

    def read_csv(self, path: Path) -> list[dict[str, str]]:
        with path.open("r", encoding="utf-8", newline="") as handle:
            return list(csv.DictReader(handle))

    def test_canonical_csv_readable_and_has_30_questions(self) -> None:
        rows = audit_module.read_questions(self.canonical_path)
        self.assertEqual(30, len(rows))
        self.assertEqual([f"q{index:02d}" for index in range(1, 31)], [row["question_id"] for row in rows])

    def test_generated_audit_preserves_ids_and_question_text(self) -> None:
        output_root, _ = self.run_in_tmp()
        generated = self.read_csv(output_root / "docs/08a-question-intent-audit.csv")
        canonical = audit_module.read_questions(self.canonical_path)
        self.assertEqual([row["question_id"] for row in canonical], [row["question_id"] for row in generated])
        self.assertEqual([row["question"] for row in canonical], [row["question"] for row in generated])

    def test_canonical_csv_not_written(self) -> None:
        before = audit_module.sha256_file(self.canonical_path)
        _, result = self.run_in_tmp()
        after = audit_module.sha256_file(self.canonical_path)
        self.assertEqual(before, after)
        self.assertTrue(result["metadata"]["canonical_hash_unchanged"])

    def test_every_question_has_core_classification(self) -> None:
        output_root, _ = self.run_in_tmp()
        rows = self.read_csv(output_root / "docs/08a-question-intent-audit.csv")
        for row in rows:
            self.assertIn(row["primary_intent"], audit_module.ALLOWED_PRIMARY_INTENTS)
            self.assertIn(row["user_stage"], audit_module.ALLOWED_USER_STAGES)
            self.assertIn(row["risk_level"], audit_module.ALLOWED_RISKS)
            self.assertTrue(row["evidence_requirements"])

    def test_candidate_question_limits_and_ids(self) -> None:
        output_root, _ = self.run_in_tmp()
        candidates = self.read_csv(output_root / "docs/08a-candidate-questions.csv")
        self.assertLessEqual(len(candidates), 18)
        canonical_ids = {f"q{index:02d}" for index in range(1, 31)}
        for row in candidates:
            self.assertNotIn(row["candidate_id"], canonical_ids)
            self.assertEqual("candidate", row["status"])
            self.assertIn(row["recommended_action"], audit_module.ALLOWED_CANDIDATE_ACTIONS)

    def test_high_risk_candidates_have_evidence_requirements(self) -> None:
        output_root, _ = self.run_in_tmp()
        candidates = self.read_csv(output_root / "docs/08a-candidate-questions.csv")
        for row in candidates:
            if row["risk_level"] == "high":
                self.assertTrue(row["evidence_requirements"])

    def test_no_internal_review_or_app_public_writes(self) -> None:
        _, result = self.run_in_tmp()
        metadata = result["metadata"]
        self.assertFalse(metadata["internal_review_read"])
        self.assertFalse(metadata["app_written"])
        self.assertFalse(metadata["public_written"])
        for item in metadata["inputs_read"]:
            self.assertNotIn("internal-review", item)
        for item in metadata["outputs_written"].values():
            self.assertFalse(item.startswith("app/"))
            self.assertFalse(item.startswith("public/"))

    def test_stage_outputs_have_no_absolute_user_paths_or_false_effect_metrics(self) -> None:
        output_root, _ = self.run_in_tmp()
        stage_files = [
            output_root / "docs/08a-question-intent-audit.csv",
            output_root / "docs/08a-follow-up-chains.csv",
            output_root / "docs/08a-candidate-questions.csv",
            output_root / "docs/08a-intent-coverage-matrix.csv",
            output_root / "docs/08a-question-route-map.csv",
            output_root / "docs/08a-intent-miner-method.md",
            output_root / "tools/geo-skill/reports/intent-miner-pilot/report.md",
            output_root / "tools/geo-skill/reports/intent-miner-pilot/report.json",
            output_root / "tools/geo-skill/reports/intent-miner-pilot/run-metadata.json",
        ]
        forbidden_terms = [
            "/Users/",
            "搜索趋势",
            "用户数量",
            "市场需求比例",
            "AI 引用概率",
            "AI引用概率",
            "排名分数",
            "品牌声量",
            "转化率预测",
        ]
        for path in stage_files:
            text = path.read_text(encoding="utf-8")
            for term in forbidden_terms:
                self.assertNotIn(term, text)

    def test_json_outputs_parse_and_csv_fields_complete(self) -> None:
        output_root, _ = self.run_in_tmp()
        json.loads((output_root / "tools/geo-skill/reports/intent-miner-pilot/report.json").read_text(encoding="utf-8"))
        json.loads((output_root / "tools/geo-skill/reports/intent-miner-pilot/run-metadata.json").read_text(encoding="utf-8"))
        expected = {
            "docs/08a-question-intent-audit.csv": audit_module.AUDIT_FIELDS,
            "docs/08a-follow-up-chains.csv": audit_module.FOLLOW_UP_FIELDS,
            "docs/08a-candidate-questions.csv": audit_module.CANDIDATE_FIELDS,
            "docs/08a-intent-coverage-matrix.csv": audit_module.MATRIX_FIELDS,
            "docs/08a-question-route-map.csv": audit_module.ROUTE_FIELDS,
        }
        for rel, fields in expected.items():
            rows = self.read_csv(output_root / rel)
            self.assertEqual(fields, list(rows[0].keys()))

    def test_repeated_runs_are_structurally_stable(self) -> None:
        output_a, _ = self.run_in_tmp()
        output_b, _ = self.run_in_tmp()
        audit_a = self.read_csv(output_a / "docs/08a-question-intent-audit.csv")
        audit_b = self.read_csv(output_b / "docs/08a-question-intent-audit.csv")
        cand_a = self.read_csv(output_a / "docs/08a-candidate-questions.csv")
        cand_b = self.read_csv(output_b / "docs/08a-candidate-questions.csv")
        self.assertEqual([row["question_id"] for row in audit_a], [row["question_id"] for row in audit_b])
        self.assertEqual([row["candidate_id"] for row in cand_a], [row["candidate_id"] for row in cand_b])
        report_a = json.loads((output_a / "tools/geo-skill/reports/intent-miner-pilot/report.json").read_text(encoding="utf-8"))
        report_b = json.loads((output_b / "tools/geo-skill/reports/intent-miner-pilot/report.json").read_text(encoding="utf-8"))
        self.assertEqual(report_a["counts"], report_b["counts"])


if __name__ == "__main__":
    unittest.main()
