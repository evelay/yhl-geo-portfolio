import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


MODULE_PATH = Path(__file__).resolve().parents[1] / "run_local_page_audit.py"
SPEC = importlib.util.spec_from_file_location("run_local_page_audit", MODULE_PATH)
audit_module = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = audit_module
SPEC.loader.exec_module(audit_module)


BASE_URL = "https://evelay.github.io/yhl-geo-portfolio"


def page_html(title, description, route, h1, body, canonical=None, json_ld=""):
    canonical = canonical or f"{BASE_URL}{route if route != '/' else '/'}"
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <link rel="canonical" href="{canonical}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <link rel="stylesheet" href="/yhl-geo-portfolio/_next/static/app.css">
  {json_ld}
</head>
<body>
<header><nav aria-label="主导航"><a href="/yhl-geo-portfolio/">研究首页</a><a href="/yhl-geo-portfolio/facts/">品牌事实</a><a href="/yhl-geo-portfolio/buying-guide/">购买核验</a><a href="/yhl-geo-portfolio/method/">方法</a><a href="/yhl-geo-portfolio/faq/">FAQ</a></nav></header>
<main>
  <h1>{h1}</h1>
  {body}
</main>
<footer><p>本项目为基于公开资料完成的独立 GEO 研究与求职作品集，未受元亨利委托，不代表品牌官方立场；不声称已提升 AI 收录、引用、曝光、推荐或销售。</p></footer>
</body>
</html>"""


class PageAuditAdapterTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / ".git").mkdir()
        (self.root / "package.json").write_text("{}", encoding="utf-8")
        (self.root / "out/facts").mkdir(parents=True)
        (self.root / "out/buying-guide").mkdir(parents=True)
        (self.root / "app").mkdir()
        (self.root / "public").mkdir()
        (self.root / "internal-review").mkdir()
        (self.root / "app/marker.txt").write_text("app", encoding="utf-8")
        (self.root / "public/marker.txt").write_text("public", encoding="utf-8")
        (self.root / "out/robots.txt").write_text("User-agent: *\nAllow: /\n", encoding="utf-8")
        (self.root / "out/sitemap.xml").write_text(
            f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset>
  <url><loc>{BASE_URL}/</loc></url>
  <url><loc>{BASE_URL}/facts</loc></url>
  <url><loc>{BASE_URL}/buying-guide</loc></url>
</urlset>
""",
            encoding="utf-8",
        )

        home_body = """
<section><p>直接答案：元亨利红木家具 GEO 作品集说明基线样本、人工评分、公开资料边界和研究声明。该页面用于说明项目身份、数据版本、页面入口、方法入口和公开下载状态，页面正文可以在静态 HTML 中直接读取。</p></section>
<section><h2>数据版本</h2><p>更新时间 2026-07-17，Baseline150 和 UserIntent75 只是研究口径，不是效果承诺。</p><ul><li>人工评分</li><li>公开资料</li></ul></section>
"""
        facts_body = """
<article><section><h2>可核验来源</h2><p>直接答案：元亨利红木家具品牌事实需要区分事实、判断、建议和待核验项，source_id B-001 可追溯，更新时间 2026-07-17。</p><ul><li>事实层</li><li>品牌自述层</li></ul><a href="https://example.com/source">来源 B-001</a></section></article>
"""
        buying_body = """
<article><section><h2>下单前</h2><p>直接答案：元亨利红木家具购买核验要确认合同、证书、主辅材、发票、售后责任主体和交付验收，更新时间 2026-07-17。</p><ol><li>确认签约主体。</li><li>核对证书。</li><li>保存付款凭证。</li></ol><a href="https://example.com/source">来源 B-003</a></section></article>
"""
        json_ld = '<script type="application/ld+json">{"@context":"https://schema.org","@type":"WebPage","name":"首页"}</script>'
        (self.root / "out/index.html").write_text(
            page_html("首页", "首页描述", "/", "元亨利红木家具 GEO 作品集", home_body, json_ld=json_ld),
            encoding="utf-8",
        )
        (self.root / "out/facts/index.html").write_text(
            page_html("品牌事实", "品牌事实描述", "/facts", "品牌事实与定位", facts_body, canonical=f"{BASE_URL}/"),
            encoding="utf-8",
        )
        (self.root / "out/buying-guide/index.html").write_text(
            page_html("购买核验", "购买核验描述", "/buying-guide", "购买核验指南", buying_body),
            encoding="utf-8",
        )
        self.config_path = self.root / "config.json"
        self.config_path.write_text(
            json.dumps(
                {
                    "site_base_url": BASE_URL,
                    "base_path": "/yhl-geo-portfolio",
                    "input_dir": "out",
                    "output_dir": "tools/geo-skill/reports/page-audit-pilot",
                    "docs_findings_csv": "docs/06b-page-audit-findings.csv",
                    "skill_source": {
                        "repo": "https://github.com/yaojingang/yao-geo-skills",
                        "commit": "test-commit",
                        "skill_path": "skills/yao-geo-page-audit",
                    },
                    "audited_routes": [
                        {
                            "route": "/",
                            "label": "首页",
                            "page_type": "home",
                            "html_path": "index.html",
                            "selection_reason": "home",
                            "expectations": {
                                "requires_metric_source_summary": True,
                                "requires_context_independent_summary": True,
                                "requires_breadcrumb": False,
                                "requires_entity_in_h1": True,
                                "requires_step_source_mapping": False,
                                "requires_fact_kv_module": False,
                            },
                        },
                        {
                            "route": "/facts",
                            "label": "品牌事实页",
                            "page_type": "brand-fact",
                            "html_path": "facts/index.html",
                            "selection_reason": "facts",
                            "expectations": {
                                "requires_metric_source_summary": False,
                                "requires_context_independent_summary": True,
                                "requires_breadcrumb": True,
                                "requires_entity_in_h1": True,
                                "requires_step_source_mapping": False,
                                "requires_fact_kv_module": True,
                            },
                        },
                        {
                            "route": "/buying-guide",
                            "label": "购买指南页",
                            "page_type": "decision-guide",
                            "html_path": "buying-guide/index.html",
                            "selection_reason": "guide",
                            "expectations": {
                                "requires_metric_source_summary": False,
                                "requires_context_independent_summary": True,
                                "requires_breadcrumb": True,
                                "requires_entity_in_h1": True,
                                "requires_step_source_mapping": True,
                                "requires_fact_kv_module": False,
                            },
                        },
                    ],
                    "excluded_paths": ["internal-review/", "app/", "public/"],
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    def tearDown(self):
        self.tmp.cleanup()

    def run_adapter(self):
        return audit_module.run_audit(
            self.root,
            self.config_path,
            generated_at="2026-07-19T16:30:00+08:00",
            run_id="test-run",
            git_commit="abc123",
            branch="refactor/portfolio-v2",
            build_method="test build",
        )

    def test_reads_three_html_files_and_extracts_core_fields(self):
        report = self.run_adapter()
        self.assertEqual([page["route"] for page in report["pages"]], ["/", "/facts", "/buying-guide"])
        home = report["pages"][0]
        self.assertEqual(home["summary"]["title"], "首页")
        self.assertTrue(home["checks"]["metadata"]["description"]["ok"])
        self.assertTrue(home["checks"]["discovery_crawl"]["canonical"]["ok"])
        self.assertTrue(home["checks"]["metadata"]["unique_h1"]["ok"])
        self.assertTrue(home["checks"]["semantic_structure"]["main"]["ok"])
        self.assertEqual(home["summary"]["json_ld_types"], ["WebPage"])

    def test_missing_page_errors_clearly(self):
        (self.root / "out/facts/index.html").unlink()
        with self.assertRaises(FileNotFoundError) as raised:
            self.run_adapter()
        self.assertIn("Missing audited HTML for /facts", str(raised.exception))

    def test_does_not_read_internal_review(self):
        original_read_text = Path.read_text

        def guarded_read_text(path_self, *args, **kwargs):
            if "internal-review" in path_self.parts:
                raise AssertionError("internal-review should not be read")
            return original_read_text(path_self, *args, **kwargs)

        with mock.patch.object(Path, "read_text", guarded_read_text):
            self.run_adapter()

    def test_does_not_write_app_or_public(self):
        self.run_adapter()
        self.assertEqual((self.root / "app/marker.txt").read_text(encoding="utf-8"), "app")
        self.assertEqual((self.root / "public/marker.txt").read_text(encoding="utf-8"), "public")
        self.assertEqual(list((self.root / "app").glob("*")), [self.root / "app/marker.txt"])
        self.assertEqual(list((self.root / "public").glob("*")), [self.root / "public/marker.txt"])

    def test_outputs_json_and_stable_structure_on_repeat(self):
        first = self.run_adapter()
        second = self.run_adapter()
        self.assertEqual(first["counts"], second["counts"])
        self.assertEqual([item["finding_id"] for item in first["findings"]], [item["finding_id"] for item in second["findings"]])
        report_json = self.root / "tools/geo-skill/reports/page-audit-pilot/report.json"
        metadata_json = self.root / "tools/geo-skill/reports/page-audit-pilot/run-metadata.json"
        self.assertIsInstance(json.loads(report_json.read_text(encoding="utf-8")), dict)
        self.assertIsInstance(json.loads(metadata_json.read_text(encoding="utf-8")), dict)

    def test_cli_output_overrides_keep_previous_reports_separate(self):
        report = audit_module.run_audit(
            self.root,
            self.config_path,
            generated_at="2026-07-19T16:30:00+08:00",
            run_id="test-run",
            git_commit="abc123",
            branch="refactor/portfolio-v2",
            build_method="test build",
            output_dir="tools/geo-skill/reports/page-audit-pilot-after-breadcrumb-schema",
            docs_findings_csv="tools/geo-skill/reports/page-audit-pilot-after-breadcrumb-schema/findings.csv",
        )

        self.assertEqual(
            report["run_metadata"]["output_files"],
            [
                "tools/geo-skill/reports/page-audit-pilot-after-breadcrumb-schema/report.md",
                "tools/geo-skill/reports/page-audit-pilot-after-breadcrumb-schema/report.json",
                "tools/geo-skill/reports/page-audit-pilot-after-breadcrumb-schema/run-metadata.json",
                "tools/geo-skill/reports/page-audit-pilot-after-breadcrumb-schema/findings.csv",
            ],
        )
        self.assertTrue((self.root / "tools/geo-skill/reports/page-audit-pilot-after-breadcrumb-schema/report.json").exists())
        self.assertFalse((self.root / "tools/geo-skill/reports/page-audit-pilot/report.json").exists())

    def test_outputs_have_no_absolute_user_paths_or_forbidden_fields(self):
        report = self.run_adapter()
        report_text = (self.root / "tools/geo-skill/reports/page-audit-pilot/report.json").read_text(encoding="utf-8")
        md_text = (self.root / "tools/geo-skill/reports/page-audit-pilot/report.md").read_text(encoding="utf-8")
        local_user_prefix = "/" + "Users/"
        self.assertNotIn(local_user_prefix, report_text)
        self.assertNotIn(local_user_prefix, md_text)

        def walk_keys(value):
            if isinstance(value, dict):
                for key, nested in value.items():
                    yield key
                    yield from walk_keys(nested)
            elif isinstance(value, list):
                for nested in value:
                    yield from walk_keys(nested)

        keys = set(walk_keys(report))
        self.assertNotIn("score", keys)
        self.assertNotIn("ai_ranking", keys)
        self.assertNotIn("citation_probability", keys)
        self.assertEqual(report["forbidden_conclusions_generated"], [])

    def test_page_level_canonicals_remove_p1_findings(self):
        (self.root / "out/facts/index.html").write_text(
            page_html(
                "品牌事实",
                "品牌事实描述",
                "/facts",
                "品牌事实与定位",
                """
<article><section><h2>可核验来源</h2><p>直接答案：元亨利红木家具品牌事实需要区分事实、判断、建议和待核验项，source_id B-001 可追溯，更新时间 2026-07-17。</p><ul><li>事实层</li><li>品牌自述层</li></ul><a href="https://example.com/source">来源 B-001</a></section></article>
""",
            ),
            encoding="utf-8",
        )
        report = self.run_adapter()
        canonicals = {page["route"]: page["summary"]["canonical"] for page in report["pages"]}
        self.assertEqual(canonicals["/facts"], f"{BASE_URL}/facts")
        self.assertEqual(canonicals["/buying-guide"], f"{BASE_URL}/buying-guide")
        canonical_p1_findings = [
            finding
            for finding in report["findings"]
            if finding["priority"] == "P1" and finding["audit_dimension"] == "发现与抓取"
        ]
        self.assertEqual(canonical_p1_findings, [])

    def test_identifies_breadcrumb_list_json_ld_separately_from_visible_breadcrumbs(self):
        breadcrumb_json_ld = """
<script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"首页","item":"https://evelay.github.io/yhl-geo-portfolio/"},{"@type":"ListItem","position":2,"name":"品牌事实与定位","item":"https://evelay.github.io/yhl-geo-portfolio/facts/"}]}</script>
"""
        (self.root / "out/facts/index.html").write_text(
            page_html(
                "品牌事实",
                "品牌事实描述",
                "/facts",
                "品牌事实与定位",
                """
<article><section><h2>可核验来源</h2><p>直接答案：元亨利红木家具品牌事实需要区分事实、判断、建议和待核验项，source_id B-001 可追溯，更新时间 2026-07-17。</p><ul><li>事实层</li><li>品牌自述层</li></ul><a href="https://example.com/source">来源 B-001</a></section></article>
""",
                json_ld=breadcrumb_json_ld,
            ),
            encoding="utf-8",
        )

        report = self.run_adapter()
        facts = next(page for page in report["pages"] if page["route"] == "/facts")
        self.assertEqual(facts["summary"]["json_ld_types"], ["BreadcrumbList"])
        self.assertEqual(facts["summary"]["breadcrumb_list_count"], 1)
        self.assertFalse(facts["checks"]["semantic_structure"]["breadcrumbs"]["ok"])
        self.assertFalse(
            any(
                finding["route"] == "/facts" and finding["audit_dimension"] == "Schema"
                for finding in report["findings"]
            )
        )


if __name__ == "__main__":
    unittest.main()
