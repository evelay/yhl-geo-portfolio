import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


MODULE_PATH = Path(__file__).resolve().parents[1] / "build_brand_graph.py"
SPEC = importlib.util.spec_from_file_location("build_brand_graph", MODULE_PATH)
brand_graph = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = brand_graph
SPEC.loader.exec_module(brand_graph)


def minimal_public_kb():
    sources = [
        ("S0-001", "国家企业信用信息公示系统：北京元亨利硬木家具有限公司查询入口", "主体核验/工商", "S0"),
        ("A-004", "元亨利官网企业介绍页", "品牌一手来源/官网自述", "A"),
        ("B-001", "国家标准 GB/T 18107-2017《红木》", "权威第三方/国家标准", "B"),
        ("B-002", "国家标准 GB/T 35475-2017《红木制品用材规范》", "权威第三方/国家标准", "B"),
        ("B-003", "国家标准 GB/T 28010-2011《红木家具通用技术条件》", "权威第三方/国家标准", "B"),
        ("B-005", "北京市家具买卖合同填写指南", "权威第三方/主流媒体", "B"),
        ("B-008", "中国家具协会官网", "权威第三方/行业协会", "B"),
        ("B-009", "北京家具行业协会：杨波红木行业主题演讲", "权威第三方/行业协会", "B"),
        ("B-011", "人民网采访：杨波谈元亨利产品结构调整", "权威第三方/媒体报道", "B"),
        ("B-012", "中国国家博物馆：大美木艺——中国明清家具珍品", "权威第三方/出版物", "B"),
    ]
    source_rows = [
        {
            "id": sid,
            "title": title,
            "type": typ,
            "url": "https://example.com/" + sid.lower(),
            "grade": grade,
            "status": "可用（测试）",
            "usable": True,
            "proves": title,
            "boundary": "测试边界",
            "updatedAt": "2026-07-17",
        }
        for sid, title, typ, grade in sources
    ]
    for sid in ["S0-002", "S0-003", "S0-004", "A-001", "A-002", "A-003", "A-005", "A-006", "A-007", "A-008", "A-009", "A-010", "B-004", "B-010"]:
        source_rows.append(
            {
                "id": sid,
                "title": "测试来源 " + sid,
                "type": "品牌一手来源/官网",
                "url": "https://example.com/" + sid.lower(),
                "grade": "A",
                "status": "可用（测试）",
                "usable": True,
                "proves": "测试",
                "boundary": "测试边界",
                "updatedAt": "2026-07-17",
            }
        )
    entities = [
        ("ENT-0001", "品牌", "元亨利红木家具", "红木家具语境中的品牌识别对象", "与同名字号主体分开核验"),
        ("ENT-0002", "企业", "北京元亨利硬木家具有限公司", "官网与主体核验涉及的企业名称", "工商细节以实时查询结果为准"),
        ("ENT-0004", "官网/域名", "bjyuanhengli.com", "项目用于识别官网和备案核验的域名", "备案和域名状态需按日期复核"),
        ("ENT-0005", "材料概念", "红木", "国家标准和红木家具内容的基础材料概念", "标准术语不等于单件材质证明"),
        ("ENT-0006", "材料概念", "黄花梨", "明清家具与红木材料语境中出现的材料名称", "俗称和规范名称需分开"),
        ("ENT-0007", "材料概念", "紫檀", "明清家具与红木材料语境中出现的材料名称", "不能替代产品证书"),
        ("ENT-0008", "材料概念", "酸枝", "红木材料语境中常见名称", "商业俗称需回到规范名称"),
        ("ENT-0010", "风格", "明式家具", "家具史与审美风格概念", "不能由风格词推导年代"),
        ("ENT-0011", "风格", "清式家具", "家具史与审美风格概念", "不能由风格词推导馆藏"),
        ("ENT-0015", "机构", "中国家具协会", "行业信息入口", "不直接证明品牌排名"),
        ("ENT-0016", "机构", "北京家具行业协会", "行业协会与公开活动来源", "只证明特定页面语境"),
        ("ENT-0017", "机构", "木材工业研究所", "木材科研体系背景来源", "不证明品牌产品材质"),
        ("ENT-0018", "媒体", "人民网", "公开采访来源", "只适用于报道时间与文本语境"),
        ("ENT-0022", "产品类别", "红木家具", "本项目内容承接的产品类别", "购买需单件证据"),
    ]
    facts = [
        ("FACT-0001", "ENT-0002", "北京元亨利硬木家具有限公司", "L1", "主体核验", ["S0-001"], ["EV-006"]),
        ("FACT-0005", "ENT-0002", "北京元亨利硬木家具有限公司", "L2", "官方联系", ["A-001"], []),
        ("FACT-0006", "ENT-0004", "bjyuanhengli.com", "L2", "官方网站", ["A-001"], []),
        ("FACT-0007", "ENT-0001", "元亨利红木家具", "L2", "产品栏目", ["A-002"], []),
        ("FACT-0008", "ENT-0001", "元亨利红木家具", "L2", "品牌介绍", ["A-003"], []),
        ("FACT-0009", "ENT-0001", "元亨利红木家具", "L2", "品牌自述", ["A-004"], ["EV-002", "EV-004"]),
        ("FACT-0012", "ENT-0001", "元亨利红木家具", "L2", "工艺自述", ["A-007"], []),
        ("FACT-0013", "ENT-0001", "元亨利红木家具", "L2", "工艺自述", ["A-007"], []),
        ("FACT-0014", "ENT-0001", "元亨利红木家具", "L2", "工艺自述", ["A-007"], []),
        ("FACT-0015", "ENT-0001", "元亨利红木家具", "L2", "工艺自述", ["A-007"], []),
        ("FACT-0018", "ENT-0001", "元亨利红木家具", "L2", "渠道入口", ["A-009"], ["EV-010"]),
        ("FACT-0021", "ENT-0005", "红木", "L1", "材料标准", ["B-001"], ["EV-007"]),
        ("FACT-0022", "ENT-0005", "红木", "L1", "用材规范", ["B-002"], ["EV-007"]),
        ("FACT-0023", "ENT-0022", "红木家具", "L1", "技术条件", ["B-003"], []),
        ("FACT-0024", "ENT-0022", "红木家具", "L1", "消费核验", ["B-004"], ["EV-011", "EV-012"]),
        ("FACT-0025", "ENT-0022", "红木家具", "L1", "合同核验", ["B-005"], ["EV-009", "EV-010"]),
        ("FACT-0028", "ENT-0015", "中国家具协会", "L1", "行业入口", ["B-008"], ["EV-002"]),
        ("FACT-0029", "ENT-0016", "北京家具行业协会", "L1", "协会活动", ["B-009"], []),
        ("FACT-0031", "ENT-0018", "人民网", "L1", "媒体报道", ["B-011"], ["EV-001"]),
        ("FACT-0032", "ENT-0019", "中国国家博物馆", "L1", "明清背景", ["B-012"], []),
        ("FACT-0033", "ENT-0006", "黄花梨", "L1", "材料边界", ["B-001", "B-012"], []),
        ("FACT-0034", "ENT-0007", "紫檀", "L1", "材料边界", ["B-001", "B-012"], []),
        ("FACT-0035", "ENT-0008", "酸枝", "L1", "材料边界", ["B-001", "B-002"], []),
        ("FACT-0037", "ENT-0010", "明式家具", "L4", "风格边界", ["B-012"], []),
        ("FACT-0038", "ENT-0011", "清式家具", "L4", "风格边界", ["B-012"], []),
        ("FACT-0039", "ENT-0022", "红木家具", "L4", "单件证据", ["B-002", "B-003", "B-005"], ["EV-007", "EV-008"]),
        ("FACT-0040", "ENT-0022", "红木家具", "L4", "动态信息", ["B-005", "A-009"], ["EV-009", "EV-010"]),
        ("FACT-0041", "ENT-0022", "红木家具", "L4", "收藏风险", ["B-004", "B-005"], ["EV-011", "EV-012"]),
    ]
    return {
        "version": "1.1-public-filtered",
        "updatedAt": "2026-07-19",
        "generatedAt": "2026-07-19T14:40:43+08:00",
        "metadata": {
            "publication_scope": "public-filtered: reviewed public records with valid source_id only",
            "excluded_statuses": ["level_three_review_required", "source_review_required", "unreviewed", "non_public"],
            "record_count": 36,
            "excluded_fact_count": 5,
        },
        "entities": [
            {"id": eid, "type": typ, "name": name, "description": desc, "sourceIds": [], "boundary": boundary, "updatedAt": "2026-07-17"}
            for eid, typ, name, desc, boundary in entities
        ],
        "facts": [
            {
                "id": fid,
                "entityId": eid,
                "entityName": entity_name,
                "evidenceLevel": level,
                "type": typ,
                "statement": typ,
                "sourceIds": source_ids,
                "sourceUrls": [],
                "evidenceIds": evidence_ids,
                "questionIds": [],
                "allowedWording": "",
                "boundary": "",
                "updatedAt": "2026-07-17",
            }
            for fid, eid, entity_name, level, typ, source_ids, evidence_ids in facts
        ],
        "sources": source_rows,
        "mappings": {
            "questions": [
                {"mapId": "MAP-Q-04", "question": "紫檀理解", "factIds": ["FACT-0021", "FACT-0034"], "sourceIds": ["B-001"], "evidenceIds": ["EV-007"], "boundary": "说明材质", "questionId": "q04"},
                {"mapId": "MAP-Q-05", "question": "白酸枝关联", "factIds": ["FACT-0035"], "sourceIds": ["B-001"], "evidenceIds": ["EV-003"], "boundary": "避免泛化", "questionId": "q05"},
                {"mapId": "MAP-Q-11", "question": "同名主体区分", "factIds": ["FACT-0001"], "sourceIds": ["S0-001"], "evidenceIds": ["EV-006"], "boundary": "区分", "questionId": "q11"},
                {"mapId": "MAP-Q-28", "question": "收藏/投资价值", "factIds": ["FACT-0041"], "sourceIds": ["B-004"], "evidenceIds": ["EV-012"], "boundary": "不承诺", "questionId": "q28"},
            ],
            "faq": [
                {"mapId": "MAP-F-03", "question": "元亨利与黄花梨是什么关系？", "factIds": ["FACT-0033"], "sourceIds": ["B-001"], "evidenceIds": [], "boundary": "不判断", "faqId": "FAQ-03"},
            ],
        },
    }


class BrandGraphAdapterTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / ".git").mkdir()
        (self.root / "package.json").write_text("{}", encoding="utf-8")
        (self.root / "public/downloads").mkdir(parents=True)
        (self.root / "app").mkdir()
        (self.root / "internal-review").mkdir()
        (self.root / "app/marker.txt").write_text("app", encoding="utf-8")
        (self.root / "public/marker.txt").write_text("public", encoding="utf-8")
        (self.root / "public/downloads/yhl-geo-knowledge-base-public.json").write_text(
            json.dumps(minimal_public_kb(), ensure_ascii=False),
            encoding="utf-8",
        )
        (self.root / "tools/geo-skill/adapters/brand-graph").mkdir(parents=True)
        self.config_path = self.root / "tools/geo-skill/adapters/brand-graph/graph-config.json"
        self.config_path.write_text(
            json.dumps(
                {
                    "input_json": "public/downloads/yhl-geo-knowledge-base-public.json",
                    "report_dir": "tools/geo-skill/reports/brand-graph-pilot",
                    "docs_outputs": {
                        "entity_ledger": "docs/07a-entity-ledger.csv",
                        "relation_ledger": "docs/07a-relation-ledger.csv",
                        "disambiguation_table": "docs/07a-disambiguation-table.csv",
                        "schema_input_candidates": "docs/07a-schema-input-candidates.csv",
                        "method_doc": "docs/07a-brand-graph-method.md",
                    },
                    "skill_source": {
                        "repo": "https://github.com/yaojingang/yao-geo-skills",
                        "commit": "test-commit",
                        "skill_path": "skills/yao-geo-brand-graph",
                        "license": "MIT",
                    },
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    def tearDown(self):
        self.tmp.cleanup()

    def run_adapter(self):
        return brand_graph.run_build(
            self.root,
            self.config_path,
            generated_at="2026-07-19T17:20:00+08:00",
            run_id="test-run",
            branch="refactor/portfolio-v2",
            commit="abc123",
        )

    def test_public_json_can_parse_and_has_review_markers(self):
        result = self.run_adapter()
        validation = result["input"]["snapshot_validation"]
        self.assertEqual(validation["version"], "1.1-public-filtered")
        self.assertTrue(validation["fact_records_have_evidence_level"])
        self.assertTrue(validation["source_records_have_status"])

    def test_rejects_blocked_input_statuses(self):
        data = minimal_public_kb()
        data["facts"][0]["evidenceLevel"] = "L3"
        (self.root / "public/downloads/yhl-geo-knowledge-base-public.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        with self.assertRaises(ValueError):
            self.run_adapter()

    def test_every_entity_has_entity_id(self):
        result = self.run_adapter()
        self.assertTrue(all(entity["entity_id"] for entity in result["entities"]))

    def test_every_relation_subject_and_object_exist(self):
        result = self.run_adapter()
        entity_ids = {entity["entity_id"] for entity in result["entities"]}
        for relation in result["relations"]:
            self.assertIn(relation["subject_id"], entity_ids)
            self.assertIn(relation["object_id"], entity_ids)

    def test_source_confirmed_relations_have_evidence_id(self):
        result = self.run_adapter()
        for relation in result["relations"]:
            if relation["evidence_status"] == "source-confirmed":
                self.assertTrue(relation["evidence_ids"])

    def test_inferred_relations_are_not_public_safe(self):
        result = self.run_adapter()
        inferred = [relation for relation in result["relations"] if relation["evidence_status"] == "inferred"]
        self.assertTrue(inferred)
        self.assertTrue(all(relation["publication_safety"] != "public-safe" for relation in inferred))

    def test_evidence_gap_does_not_enter_mermaid(self):
        self.run_adapter()
        mermaid = (self.root / "tools/geo-skill/reports/brand-graph-pilot/brand-graph.mmd").read_text(encoding="utf-8")
        self.assertNotIn("evidence-gap", mermaid)
        self.assertNotIn("inferred", mermaid)
        self.assertNotIn("no_public_jingzuo_identity_evidence_in_allowed_input", mermaid)

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

    def test_outputs_do_not_contain_absolute_user_paths(self):
        self.run_adapter()
        report = (self.root / "tools/geo-skill/reports/brand-graph-pilot/brand-graph.json").read_text(encoding="utf-8")
        metadata = (self.root / "tools/geo-skill/reports/brand-graph-pilot/run-metadata.json").read_text(encoding="utf-8")
        self.assertNotIn("/Users/", report)
        self.assertNotIn("/Users/", metadata)

    def test_repeat_run_structure_is_stable(self):
        first = self.run_adapter()
        second = self.run_adapter()
        self.assertEqual([entity["entity_id"] for entity in first["entities"]], [entity["entity_id"] for entity in second["entities"]])
        self.assertEqual([relation["relation_id"] for relation in first["relations"]], [relation["relation_id"] for relation in second["relations"]])
        self.assertEqual(first["counts"], second["counts"])

    def test_no_production_json_ld_is_generated(self):
        self.run_adapter()
        report_dir = self.root / "tools/geo-skill/reports/brand-graph-pilot"
        self.assertFalse(list(report_dir.glob("*.jsonld")))
        payload = (report_dir / "brand-graph.json").read_text(encoding="utf-8")
        self.assertNotIn('"@context"', payload)
        self.assertNotIn("application/ld+json", payload)

    def test_no_forbidden_public_safe_fact_is_generated(self):
        result = self.run_adapter()
        for relation in result["relations"]:
            if relation["publication_safety"] == "public-safe":
                self.assertNotIn("官方委托", relation["relation_interpretation"])
                self.assertNotIn("行业第一", relation["relation_interpretation"])
                self.assertNotIn("升值保证", relation["relation_interpretation"])

    def test_csv_headers_are_complete(self):
        self.run_adapter()
        self.assertEqual((self.root / "docs/07a-entity-ledger.csv").read_text(encoding="utf-8").splitlines()[0], ",".join(brand_graph.ENTITY_FIELDS))
        self.assertEqual((self.root / "docs/07a-relation-ledger.csv").read_text(encoding="utf-8").splitlines()[0], ",".join(brand_graph.RELATION_FIELDS))


if __name__ == "__main__":
    unittest.main()
