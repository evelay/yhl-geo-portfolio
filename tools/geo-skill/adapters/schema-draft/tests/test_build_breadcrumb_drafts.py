import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[5]
MODULE_PATH = REPO_ROOT / "tools/geo-skill/adapters/schema-draft/build_breadcrumb_drafts.py"
CONFIG_PATH = REPO_ROOT / "tools/geo-skill/adapters/schema-draft/breadcrumb-config.json"


def load_module():
    spec = importlib.util.spec_from_file_location("build_breadcrumb_drafts", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class BuildBreadcrumbDraftsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_module()
        cls.config = cls.module.load_config(CONFIG_PATH)

    def test_builds_expected_breadcrumb_jsonld(self):
        with tempfile.TemporaryDirectory() as tmp:
            files = self.module.build_outputs(self.config, REPO_ROOT, Path(tmp))

        facts = json.loads(files["facts-breadcrumb.jsonld"])
        buying = json.loads(files["buying-guide-breadcrumb.jsonld"])
        validation = json.loads(files["breadcrumb-validation.json"])

        self.assertEqual(validation["validation_status"], "valid")
        self.assertEqual(facts["@context"], "https://schema.org")
        self.assertEqual(facts["@type"], "BreadcrumbList")
        self.assertEqual(
            facts["itemListElement"],
            [
                {
                    "@type": "ListItem",
                    "position": 1,
                    "name": "首页",
                    "item": "https://evelay.github.io/yhl-geo-portfolio/",
                },
                {
                    "@type": "ListItem",
                    "position": 2,
                    "name": "品牌事实与定位",
                    "item": "https://evelay.github.io/yhl-geo-portfolio/facts/",
                },
            ],
        )
        self.assertEqual(
            buying["itemListElement"][1],
            {
                "@type": "ListItem",
                "position": 2,
                "name": "购买核验指南",
                "item": "https://evelay.github.io/yhl-geo-portfolio/buying-guide/",
            },
        )

    def test_repeated_output_is_stable(self):
        with tempfile.TemporaryDirectory() as first_tmp, tempfile.TemporaryDirectory() as second_tmp:
            first = self.module.build_outputs(self.config, REPO_ROOT, Path(first_tmp))
            second = self.module.build_outputs(self.config, REPO_ROOT, Path(second_tmp))

        self.assertEqual(first, second)

    def test_validation_rejects_forbidden_schema_type(self):
        drafts = self.module.build_drafts(self.config)
        drafts["facts-breadcrumb.jsonld"]["@type"] = "Organization"

        validation, _signals = self.module.validate(
            self.config,
            drafts,
            REPO_ROOT,
            Path("tools/geo-skill/reports/schema-draft-pilot"),
        )

        self.assertEqual(validation["validation_status"], "invalid")
        failed = {check["id"] for check in validation["checks"] if check["status"] == "fail"}
        self.assertIn("/facts_jsonld_type", failed)
        self.assertIn("/facts_no_forbidden_schema_types", failed)

    def test_planned_outputs_do_not_target_app_or_public(self):
        files = [
            page["draft_file"] for page in self.config["pages"]
        ] + [
            self.module.DEFAULT_REPORT_NAME,
            self.module.DEFAULT_VALIDATION_NAME,
            self.module.DEFAULT_METADATA_NAME,
        ]
        targets = self.module.output_targets(
            REPO_ROOT,
            Path("tools/geo-skill/reports/schema-draft-pilot"),
            files,
        )
        self.assertTrue(self.module.targets_avoid_app_public(REPO_ROOT, targets))


if __name__ == "__main__":
    unittest.main()

