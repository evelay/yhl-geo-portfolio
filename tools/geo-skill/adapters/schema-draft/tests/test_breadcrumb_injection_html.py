import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[5]

EXPECTED = {
    "/facts": {
        "html_path": "out/facts/index.html",
        "h1": "元亨利品牌事实、来源与信息边界",
        "summary": "本页汇总元亨利可公开核验的品牌事实、来源与信息边界，并区分已确认、需谨慎表述和暂不应公开推断的内容。",
        "breadcrumb_name": "品牌事实与定位",
        "canonical": "https://evelay.github.io/yhl-geo-portfolio/facts/",
    },
    "/buying-guide": {
        "html_path": "out/buying-guide/index.html",
        "h1": "元亨利红木家具购买核验指南",
        "summary": "本页提供评估元亨利红木家具时可执行的核验框架，重点关注材质、工艺、来源、单件证据和信息边界，不构成购买或投资建议。",
        "breadcrumb_name": "购买核验指南",
        "canonical": "https://evelay.github.io/yhl-geo-portfolio/buying-guide/",
    },
}


class StaticPageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.canonical = ""
        self.h1_values = []
        self.json_ld_raw = []
        self._capture_h1 = False
        self._h1_parts = []
        self._capture_json_ld = False
        self._json_ld_parts = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = {name.lower(): value or "" for name, value in attrs}
        if tag.lower() == "link" and "canonical" in attrs_dict.get("rel", "").lower().split():
            self.canonical = attrs_dict.get("href", "")
        if tag.lower() == "h1":
            self._capture_h1 = True
            self._h1_parts = []
        if tag.lower() == "script" and "ld+json" in attrs_dict.get("type", "").lower():
            self._capture_json_ld = True
            self._json_ld_parts = []

    def handle_endtag(self, tag):
        if tag.lower() == "h1" and self._capture_h1:
            self.h1_values.append("".join(self._h1_parts).strip())
            self._capture_h1 = False
        if tag.lower() == "script" and self._capture_json_ld:
            self.json_ld_raw.append("".join(self._json_ld_parts).strip())
            self._capture_json_ld = False

    def handle_data(self, data):
        if self._capture_h1:
            self._h1_parts.append(data)
        if self._capture_json_ld:
            self._json_ld_parts.append(data)


def parse_static_page(route):
    path = REPO_ROOT / route["html_path"]
    html = path.read_text(encoding="utf-8")
    parser = StaticPageParser()
    parser.feed(html)
    json_ld = [json.loads(raw) for raw in parser.json_ld_raw]
    return html, parser, json_ld


def schema_types(items):
    values = []
    for item in items:
        value = item.get("@type")
        if isinstance(value, list):
            values.extend(value)
        elif value:
            values.append(value)
    return values


def visible_breadcrumb_navs(html):
    return re.findall(r'<nav[^>]*aria-label="面包屑导航"[^>]*>(.*?)</nav>', html, re.S)


class BreadcrumbInjectionHTMLTests(unittest.TestCase):
    def assert_no_forbidden_html(self, html):
        self.assertNotIn("/Users/", html)
        self.assertNotIn("chatgpt.site", html)
        self.assertNotIn("localhost", html)
        self.assertNotIn("/yhl-geo-portfolio/yhl-geo-portfolio", html)

    def test_facts_and_buying_guide_have_one_valid_breadcrumb_list(self):
        for route, expected in EXPECTED.items():
            with self.subTest(route=route):
                html, parser, json_ld = parse_static_page(expected)
                breadcrumb_lists = [item for item in json_ld if item.get("@type") == "BreadcrumbList"]

                self.assert_no_forbidden_html(html)
                self.assertEqual(parser.h1_values, [expected["h1"]])
                self.assertEqual(parser.canonical, expected["canonical"])
                self.assertIn(expected["summary"], html)
                self.assertEqual(len(breadcrumb_lists), 1)
                self.assertEqual(schema_types(json_ld), ["BreadcrumbList"])

                breadcrumb = breadcrumb_lists[0]
                self.assertEqual(breadcrumb["@context"], "https://schema.org")
                items = breadcrumb["itemListElement"]
                self.assertEqual([item["@type"] for item in items], ["ListItem", "ListItem"])
                self.assertEqual([item["position"] for item in items], [1, 2])
                self.assertEqual(items[0]["name"], "首页")
                self.assertEqual(items[0]["item"], "https://evelay.github.io/yhl-geo-portfolio/")
                self.assertEqual(items[1]["name"], expected["breadcrumb_name"])
                self.assertEqual(items[1]["item"], expected["canonical"])

                navs = visible_breadcrumb_navs(html)
                self.assertEqual(len(navs), 1)
                self.assertIn("<ol>", navs[0])
                self.assertEqual(navs[0].count("<li"), 2)
                self.assertIn('<a href="/yhl-geo-portfolio/">首页</a>', navs[0])
                self.assertIn(f'<li aria-current="page">{expected["breadcrumb_name"]}</li>', navs[0])

    def test_homepage_has_no_breadcrumb_list(self):
        html, _parser, json_ld = parse_static_page({"html_path": "out/index.html"})

        self.assert_no_forbidden_html(html)
        self.assertEqual([item for item in json_ld if item.get("@type") == "BreadcrumbList"], [])
        self.assertEqual(visible_breadcrumb_navs(html), [])


if __name__ == "__main__":
    unittest.main()
