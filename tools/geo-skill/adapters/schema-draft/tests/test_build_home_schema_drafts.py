import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[5]
MODULE_PATH = REPO_ROOT / "tools/geo-skill/adapters/schema-draft/build_home_schema_drafts.py"
CONFIG_PATH = REPO_ROOT / "tools/geo-skill/adapters/schema-draft/home-schema-config.json"


def load_module():
    spec = importlib.util.spec_from_file_location("build_home_schema_drafts", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class BuildHomeSchemaDraftsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_module()
        cls.config = cls.module.load_config(CONFIG_PATH)

    def test_builds_expected_homepage_schema_options(self):
        with tempfile.TemporaryDirectory() as tmp:
            files = self.module.build_outputs(self.config, REPO_ROOT, Path(tmp))

        website_only = json.loads(files["website-only.jsonld"])
        website_webpage = json.loads(files["website-webpage-graph.jsonld"])
        website_collection = json.loads(files["website-collectionpage-graph.jsonld"])
        validation = json.loads(files["validation.json"])

        self.assertEqual(validation["validation_status"], "valid")
        self.assertEqual(website_only["@context"], "https://schema.org")
        self.assertEqual(website_only["@type"], "WebSite")
        self.assertEqual(website_only["@id"], "https://evelay.github.io/yhl-geo-portfolio/#website")
        self.assertEqual(website_only["url"], "https://evelay.github.io/yhl-geo-portfolio/")
        self.assertEqual(website_only["name"], "元亨利红木家具 GEO 诊断与可核验内容体系")
        self.assertEqual(website_only["inLanguage"], "zh-CN")
        self.assertIn("未受元亨利委托", website_only["description"])

        self.assertEqual(
            [node["@type"] for node in website_webpage["@graph"]],
            ["WebSite", "WebPage"],
        )
        self.assertEqual(
            website_webpage["@graph"][1]["isPartOf"],
            {"@id": "https://evelay.github.io/yhl-geo-portfolio/#website"},
        )
        self.assertEqual(
            [node["@type"] for node in website_collection["@graph"]],
            ["WebSite", "CollectionPage"],
        )

    def test_repeated_output_is_stable(self):
        with tempfile.TemporaryDirectory() as first_tmp, tempfile.TemporaryDirectory() as second_tmp:
            first = self.module.build_outputs(self.config, REPO_ROOT, Path(first_tmp))
            second = self.module.build_outputs(self.config, REPO_ROOT, Path(second_tmp))

        self.assertEqual(first, second)

    def test_validation_rejects_forbidden_publisher_and_search_action(self):
        drafts = self.module.build_drafts(self.config)
        draft = drafts["website-webpage-graph.jsonld"]
        draft["@graph"][0]["publisher"] = {"@type": "Organization", "name": "元亨利"}
        draft["@graph"][0]["potentialAction"] = {"@type": "SearchAction"}

        validation, _signals = self.module.validate(
            self.config,
            drafts,
            REPO_ROOT,
            Path("tools/geo-skill/reports/home-schema-draft-pilot"),
        )

        self.assertEqual(validation["validation_status"], "invalid")
        failed = {check["id"] for check in validation["checks"] if check["status"] == "fail"}
        self.assertIn("07D1-B_no_forbidden_schema_types", failed)
        self.assertIn("07D1-B_no_forbidden_properties", failed)
        self.assertIn("07D1-B_no_search_action", failed)

    def test_validation_rejects_unconfirmed_description(self):
        drafts = self.module.build_drafts(self.config)
        drafts["website-only.jsonld"]["description"] = "元亨利官方网站，已帮助元亨利提升 AI 引用。"

        validation, _signals = self.module.validate(
            self.config,
            drafts,
            REPO_ROOT,
            Path("tools/geo-skill/reports/home-schema-draft-pilot"),
        )

        self.assertEqual(validation["validation_status"], "invalid")
        failed = {check["id"] for check in validation["checks"] if check["status"] == "fail"}
        self.assertIn("07D1-A_description_matches_public_summary", failed)
        self.assertIn("07D1-A_no_false_effect_or_official_claim", failed)

    def test_planned_outputs_do_not_target_app_or_public(self):
        files = [
            option["draft_file"] for option in self.config["options"]
        ] + [
            self.module.DEFAULT_COMPARISON_NAME,
            self.module.DEFAULT_VALIDATION_NAME,
            self.module.DEFAULT_METADATA_NAME,
        ]
        targets = self.module.output_targets(
            REPO_ROOT,
            Path("tools/geo-skill/reports/home-schema-draft-pilot"),
            files,
        )
        self.assertTrue(self.module.targets_avoid_app_public(REPO_ROOT, targets))

    def test_generated_outputs_do_not_contain_local_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            files = self.module.build_outputs(self.config, REPO_ROOT, Path(tmp))

        all_text = "\n".join(files.values())
        self.assertNotIn("/Users/", all_text)
        self.assertNotIn("localhost", all_text)
        self.assertNotIn("chatgpt.site", all_text)
        self.assertNotIn("/yhl-geo-portfolio/yhl-geo-portfolio", all_text)


if __name__ == "__main__":
    unittest.main()
