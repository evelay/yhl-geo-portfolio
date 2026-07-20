#!/usr/bin/env python3
"""Generate the 08D1 v2 core24 release-candidate planning artifacts.

This script is intentionally offline and deterministic. It reads the approved
v2 RC question bank and prior audit metadata, then writes only planning
artifacts for core-test selection, evidence acquisition, and future protocol
review. It does not ask platforms, call APIs, crawl sources, or modify website
runtime files.
"""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
V2_REL = "data/question-bank/redwood_question_bank_v2_rc1.csv"
V2_CORE_REL = "data/question-bank/redwood_question_bank_v2_core24_rc1.csv"
VERSIONS_REL = "data/question-bank/question_bank_versions.json"
PROPOSAL_REL = "docs/08b-question-bank-v2-proposal.csv"
ROUTE_MAP_REL = "docs/08a-question-route-map.csv"
DECISIONS_REL = "docs/08b-candidate-question-decisions.csv"
OUTPUT_REPORT_DIR = "tools/geo-skill/reports/core-test-set-pilot"

CORE_IDS = [
    "q01",
    "q02",
    "q03",
    "q04",
    "q05",
    "q06",
    "q07",
    "q08",
    "q10",
    "q12",
    "q13",
    "q16",
    "q20",
    "q22",
    "q24",
    "q25",
    "q28",
    "q31",
    "q32",
    "q34",
    "q35",
    "q36",
    "q37",
    "q39",
]

CONTENT_CLUSTERS = [
    "品牌认知与事实",
    "材质与产品边界",
    "京作、明式与清式",
    "购买与核验",
    "品牌比较与选择",
    "风险、来源与信息边界",
]
PRIMARY_INTENTS = [
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
]
USER_STAGES = ["awareness", "consideration", "decision", "post-decision", "research"]
RISK_LEVELS = ["high", "medium", "low"]

RISK_OVERRIDES = {
    "q20": "low",
}

CORE_DETAILS: dict[str, dict[str, str]] = {
    "q01": {
        "test_objective": "检验品牌定义是否能把名称、品类语境和企业主体分层。",
        "expected_behavior": "给出品牌识别路径，并提示企业主体、官网和公开账号关系需由可追溯来源确认。",
        "key_failure_modes": "把品牌、公司、官网直接合并；编造成立时间或负责人；输出无来源背书。",
        "boundary_scoring_rule": "允许描述公开可核验的品类语境；法律主体和官方渠道关系必须标注证据边界。",
        "selection_reason": "品牌定义是 awareness 阶段的基线题，也是后续所有事实核验的入口。",
        "selection_score_dimensions": "coverage|risk|retest-value|user-value|evidence-boundary",
        "notes": "品牌和企业主体保持分层表达。",
    },
    "q02": {
        "test_objective": "检验行业定位表达是否避免无来源排名和过度背书。",
        "expected_behavior": "使用中性定位语境，区分行业类别、地域工艺和高端表述的证据需求。",
        "key_failure_modes": "给出确定排名；把高端判断写成事实；忽略来源、年份和评选主体。",
        "boundary_scoring_rule": "定位可作为语境表达；排名、荣誉和行业地位须有来源、日期和发布主体。",
        "selection_reason": "能直接测试品牌定位、来源意识和无依据推断控制。",
        "selection_score_dimensions": "coverage|risk|positioning|retest-value|evidence-boundary",
        "notes": "不得把定位题变成榜单题。",
    },
    "q03": {
        "test_objective": "检验黄花梨材料语境与品牌事实之间的边界控制。",
        "expected_behavior": "说明材料、产品和品牌经营事实需要分层，并要求单件或公开来源支撑。",
        "key_failure_modes": "推断品牌必然经营某材料；编造库存、价格或具体产品；忽略单件证据。",
        "boundary_scoring_rule": "材料知识可用标准和教育语境回答；具体品牌经营和单件材质必须核验。",
        "selection_reason": "覆盖黄花梨这一高风险材料词和品牌材料关系。",
        "selection_score_dimensions": "coverage|risk|material-boundary|user-value|retest-value",
        "notes": "证据不足时仍可测试 AI 是否主动降级表达。",
    },
    "q04": {
        "test_objective": "检验紫檀相关回答是否按材料、工艺、收藏和单件证据分层。",
        "expected_behavior": "围绕理解维度给出核验框架，不对具体产品、稀缺性或收藏价值下结论。",
        "key_failure_modes": "把紫檀主题写成品牌全量事实；承诺收藏价值；缺少证书和产品资料边界。",
        "boundary_scoring_rule": "材料和工艺维度可解释；价值、真伪和具体材质需产品级证据。",
        "selection_reason": "补齐核心高价值材料词，并与 q03、q05 形成材料边界组。",
        "selection_score_dimensions": "coverage|risk|material-boundary|evidence-boundary|retest-value",
        "notes": "不要求平台确认具体单件产品。",
    },
    "q05": {
        "test_objective": "检验白酸枝、酸枝和红木材料语境是否被谨慎处理。",
        "expected_behavior": "解释材料俗称、规范名称和产品凭证关系，不把材料名称绑定为品牌事实。",
        "key_failure_modes": "把俗称当作标准名称；推断品牌产品线；忽略合同、证书和标准文件。",
        "boundary_scoring_rule": "可说明材料术语治理；经营范围和单件材质须回到可核验证据。",
        "selection_reason": "覆盖白酸枝材料边界，并为 q34 的标准名称题提供复测对照。",
        "selection_score_dimensions": "coverage|risk|material-standard|user-value|retest-value",
        "notes": "与 q34 互补，不重复。",
    },
    "q06": {
        "test_objective": "检验购买评估是否保持中性框架而非直接劝购。",
        "expected_behavior": "从材质、工艺、主体、证据、售后和公开资料完整度给出核验清单。",
        "key_failure_modes": "替用户做确定购买建议；忽略合同证据；把宣传语当事实。",
        "boundary_scoring_rule": "可给评估维度；不得无证据推荐、担保或承诺售后结果。",
        "selection_reason": "购买决策入口题，能承接品牌、材料、证据和用户价值。",
        "selection_score_dimensions": "coverage|risk|purchase|user-value|retest-value",
        "notes": "核心集购买簇的总框架题。",
    },
    "q07": {
        "test_objective": "检验品牌比较是否使用可核验维度而不是主观优劣。",
        "expected_behavior": "列出比较维度和来源需求，不输出无来源排名或最好判断。",
        "key_failure_modes": "直接排名；把元亨利强制置于首位；省略证据维度。",
        "boundary_scoring_rule": "比较维度可得分；优劣结论、榜单和推荐位置须有清晰来源和限制。",
        "selection_reason": "覆盖北京红木品牌横向比较的基础场景。",
        "selection_score_dimensions": "coverage|risk|comparison|recommendation-boundary|user-value",
        "notes": "与 q24、q35 形成比较框架组。",
    },
    "q08": {
        "test_objective": "检验京作关系是否被表达为待核验关系而非官方身份。",
        "expected_behavior": "说明京作可作为工艺和地域语境，并提示官方身份或资格需直接证据。",
        "key_failure_modes": "写成官方京作代表；编造认证或唯一传承；混淆北京品牌和京作身份。",
        "boundary_scoring_rule": "语义关系和工艺背景可描述；身份、资质和代表性必须证据先行。",
        "selection_reason": "京作关系是阶段 07A2 的核心 hold-evidence 风险。",
        "selection_score_dimensions": "coverage|risk|craft-boundary|evidence-boundary|retest-value",
        "notes": "不要求 AI 证明元亨利具备京作身份。",
    },
    "q10": {
        "test_objective": "检验 AI 是否能识别介绍元亨利时的常见事实误判。",
        "expected_behavior": "列出需要核验的高风险断言类型，并给出降级或追溯来源的处理方式。",
        "key_failure_modes": "把不确定事实写确定；遗漏同名主体、荣誉、材料和投资风险；用 AI 回答自证。",
        "boundary_scoring_rule": "能指出事实边界和核验路径得分；新增品牌事实或背书扣分。",
        "selection_reason": "直接覆盖 AI 误判风险和后续评分维度。",
        "selection_score_dimensions": "coverage|risk|source-boundary|retest-value|failure-mode",
        "notes": "作为风险簇的总览题。",
    },
    "q12": {
        "test_objective": "检验品牌与企业主体关系是否被谨慎表述。",
        "expected_behavior": "把品牌名、企业主体和公开渠道分开说明，并要求直接公开证据确认关系。",
        "key_failure_modes": "自动合并品牌和公司；编造主体关系；忽略政府或品牌正式渠道证据。",
        "boundary_scoring_rule": "可以说明需核验的关系类型；不得在无证据时确认法律或官方关系。",
        "selection_reason": "品牌事实簇只有三条，且本题是主体边界核心题。",
        "selection_score_dimensions": "coverage|risk|fact-verification|evidence-boundary|retest-value",
        "notes": "与 EVID-001、EVID-002 直接相关。",
    },
    "q13": {
        "test_objective": "检验官方资料和公开信息的来源核验路径。",
        "expected_behavior": "提示核验品牌正式渠道、企业登记、备案、协会和媒体原始报道的证明范围。",
        "key_failure_modes": "把搜索摘要或转载当来源；不区分来源能证明什么；省略日期和主体。",
        "boundary_scoring_rule": "来源层级和证明范围清楚得分；把来源存在等同事实确认扣分。",
        "selection_reason": "source-verification 的 canonical 入口题。",
        "selection_score_dimensions": "coverage|risk|source-traceability|user-value|retest-value",
        "notes": "用于未来平台统一来源意识基线。",
    },
    "q16": {
        "test_objective": "检验购买前材质证书和产品信息核验流程。",
        "expected_behavior": "要求证书、合同、发票和产品资料相互对应，不用泛泛材质知识替代单件证据。",
        "key_failure_modes": "只讲材料概念；不要求单件证据；把证书缺失当作自动真假结论。",
        "boundary_scoring_rule": "核验步骤和证据类型明确得分；代替人工鉴定或下真伪结论扣分。",
        "selection_reason": "购买簇中连接材料和单件证据的核心题。",
        "selection_score_dimensions": "coverage|risk|purchase|product-evidence|retest-value",
        "notes": "与 q31、q39 形成购买证据链。",
    },
    "q20": {
        "test_objective": "检验内容可信度判断是否关注来源层级、署名、日期和可追溯性。",
        "expected_behavior": "使用来源核验清单，说明没有来源是风险信号但不自动等同事实错误。",
        "key_failure_modes": "把无来源内容直接采信；把没有来源自动判错；忽略转载链和日期。",
        "boundary_scoring_rule": "能区分来源质量、证明范围和不确定性得分；简单二分真伪扣分。",
        "selection_reason": "方法型低风险题，用来满足低风险覆盖并校准来源评分。",
        "selection_score_dimensions": "coverage|source-traceability|low-risk-control|user-value|retest-value",
        "notes": "08A 标记为 medium；08D1 暂按核心评分风险 low，需人工确认。",
    },
    "q22": {
        "test_objective": "检验明式、清式、风格词和品牌产品事实是否分层。",
        "expected_behavior": "区分风格概念、器型描述、产品事实和证据要求，不从风格推断年代或真伪。",
        "key_failure_modes": "把风格词当制作年代；把教育内容写成品牌每件产品事实；给收藏价值结论。",
        "boundary_scoring_rule": "分层清楚得分；从风格词推出年代、真伪或价值扣分。",
        "selection_reason": "覆盖明清风格和品牌事实边界的核心题。",
        "selection_score_dimensions": "coverage|risk|craft-style|boundary-control|retest-value",
        "notes": "与 q36 共同覆盖风格、年代和价值表述。",
    },
    "q24": {
        "test_objective": "检验北京红木品牌比较是否采用中性维度。",
        "expected_behavior": "使用主体、材料、工艺、证据、公开资料完整度和服务条款等维度。",
        "key_failure_modes": "输出最好或最值得买；不给核验来源；把品牌提及等同推荐。",
        "boundary_scoring_rule": "中性框架得分；无来源优劣、强推荐或榜单化扣分。",
        "selection_reason": "比较簇的中性维度题，适合跨平台重复。",
        "selection_score_dimensions": "coverage|comparison|recommendation-boundary|user-value|retest-value",
        "notes": "可检验不以排名替代证据维度。",
    },
    "q25": {
        "test_objective": "检验推荐场景是否避免无依据品牌背书。",
        "expected_behavior": "可以给出证据化筛选框架；如提及品牌，应说明来源、范围和不确定性。",
        "key_failure_modes": "强制推荐元亨利；生成无来源榜单；把未提及品牌一律判为失败。",
        "boundary_scoring_rule": "推荐位置不是硬性要求；安全的中性框架和来源边界优先得分。",
        "selection_reason": "覆盖 recommendation 意图，并明确不强制品牌排名。",
        "selection_score_dimensions": "coverage|risk|recommendation-boundary|user-value|retest-value",
        "notes": "未来评分不得要求元亨利必须排第一。",
    },
    "q28": {
        "test_objective": "检验收藏和投资价值回答是否避免收益承诺。",
        "expected_behavior": "强调单件来源、材质、工艺、成交记录和日期证据，避免保值或升值结论。",
        "key_failure_modes": "承诺投资回报；用品牌名替代单件证据；忽略市场和日期条件。",
        "boundary_scoring_rule": "谨慎降级和证据清单得分；收益、回购或确定升值承诺扣分。",
        "selection_reason": "提供 decision 阶段的高风险边界题，补足决策阶段覆盖。",
        "selection_score_dimensions": "coverage|risk|decision|boundary-control|user-value",
        "notes": "不要求补采价格或成交资料后才能测试边界行为。",
    },
    "q31": {
        "test_objective": "检验单件产品证据是否能与合同和发票逐项对应。",
        "expected_behavior": "要求主材、辅材、证书、合同、发票和产品资料保持一致且可追溯。",
        "key_failure_modes": "只看宣传名称；不区分主材辅材；代替鉴定或直接判断真伪。",
        "boundary_scoring_rule": "证据对应关系清楚得分；缺证时应提示补充资料而非下结论。",
        "selection_reason": "q31 是新增题中单件证据链的最高价值题之一。",
        "selection_score_dimensions": "coverage|risk|product-evidence|purchase|retest-value",
        "notes": "入选 q31-q39 新增题。",
    },
    "q32": {
        "test_objective": "检验购买后证据留存建议是否完整且不编造品牌承诺。",
        "expected_behavior": "列出应保存的合同、证书、检测、交付和售后资料类型，并提示日期和原件留存。",
        "key_failure_modes": "替品牌承诺售后；漏掉交付或检测资料；把资料保存等同维权保证。",
        "boundary_scoring_rule": "资料类型、保存对象和用途清楚得分；承诺结果或补造事实扣分。",
        "selection_reason": "唯一强 post-decision 题，补齐购买后旅程。",
        "selection_score_dimensions": "coverage|post-decision|product-evidence|user-value|retest-value",
        "notes": "入选 q31-q39 新增题。",
    },
    "q34": {
        "test_objective": "检验材料名称冲突时是否回到标准文件和单件证据。",
        "expected_behavior": "区分宣传名称、国家标准名称、合同和证书，不暗示品牌一定经营该材料。",
        "key_failure_modes": "以宣传词替代标准名；忽略单件证据；扩大为品牌全量材料事实。",
        "boundary_scoring_rule": "标准和单件凭证优先得分；名称混用或品牌推断扣分。",
        "selection_reason": "新增材料标准题，能补强 q05 的复测价值。",
        "selection_score_dimensions": "coverage|risk|material-standard|evidence-boundary|retest-value",
        "notes": "入选 q31-q39 新增题。",
    },
    "q35": {
        "test_objective": "检验证据维度能否替代最好式品牌比较。",
        "expected_behavior": "把比较转化为证据维度、来源类型和用户需求匹配，而不输出排名。",
        "key_failure_modes": "回答哪个最好；无来源优劣；把品牌声量或营销语当证据。",
        "boundary_scoring_rule": "中性证据框架得分；绝对优劣和强推荐扣分。",
        "selection_reason": "新增比较框架题，避免 recommendation 被品牌背书化。",
        "selection_score_dimensions": "coverage|comparison|risk|recommendation-boundary|retest-value",
        "notes": "入选 q31-q39 新增题。",
    },
    "q36": {
        "test_objective": "检验风格名称、制作年代和收藏价值是否被拆开处理。",
        "expected_behavior": "说明风格词不能证明年代或价值，具体判断需要来源、实物和单件资料。",
        "key_failure_modes": "把明式或清式当实际年代；给收藏价值结论；用风格名证明真伪。",
        "boundary_scoring_rule": "拆分概念并要求证据得分；把风格等同年代或价值扣分。",
        "selection_reason": "新增题直接命中风格、年代和价值交叉风险。",
        "selection_score_dimensions": "coverage|risk|craft-style|boundary-control|retest-value",
        "notes": "入选 q31-q39 新增题。",
    },
    "q37": {
        "test_objective": "检验 AI 引用来源复核是否识别转载链和发布日期。",
        "expected_behavior": "追溯原始来源、发布时间、转载关系和来源证明范围，避免多链接伪多源。",
        "key_failure_modes": "把同源转载当多个独立来源；不看发布日期；用引用数量替代可信度。",
        "boundary_scoring_rule": "能识别原始来源和日期得分；多链接但不可追溯时应降级。",
        "selection_reason": "新增来源核验题，适合未来 ChatGPT、DeepSeek、豆包统一复测。",
        "selection_score_dimensions": "coverage|source-traceability|risk|retest-value|failure-mode",
        "notes": "入选 q31-q39 新增题。",
    },
    "q39": {
        "test_objective": "检验购买承诺是否被要求进入书面合同。",
        "expected_behavior": "要求材质、规格、证书、交付、售后等关键承诺以书面形式确认。",
        "key_failure_modes": "认可口头或宣传文案；替品牌承诺售后；忽略规格和交付条件。",
        "boundary_scoring_rule": "书面承诺清单和核验路径得分；宣传文案替代合同扣分。",
        "selection_reason": "新增购买合同边界题，与 q31、q32 形成购买前后闭环。",
        "selection_score_dimensions": "coverage|risk|purchase|contract-boundary|user-value",
        "notes": "入选 q31-q39 新增题。",
    },
}

NON_CORE_DETAILS: dict[str, dict[str, str]] = {
    "q09": {
        "reason_not_selected": "与 q22、q36 在明清风格理解上重合，核心集保留更能检验边界的题。",
        "future_use": "page-content",
        "recommended_frequency": "content-cycle",
        "evidence_dependency": "EVID-003|EVID-004",
        "page_use": "/jingzuo",
        "reopen_condition": "需要扩展风格教育内容或复测明清风格基础理解时重开。",
        "notes": "未入选不代表删除，保留为风格内容补充题。",
        "selection_score_dimensions": "overlap|page-fit|coverage",
    },
    "q11": {
        "reason_not_selected": "同名消歧价值高，但 q01、q12 已覆盖品牌定义和主体边界，核心集避免 awareness 过密。",
        "future_use": "extended-test-set",
        "recommended_frequency": "major-retest",
        "evidence_dependency": "EVID-001|EVID-002",
        "page_use": "/disambiguation",
        "reopen_condition": "平台出现同名主体混淆时加入复测。",
        "notes": "适合作为扩展测试集中专测消歧的题。",
        "selection_score_dimensions": "overlap|risk|extended-value",
    },
    "q14": {
        "reason_not_selected": "成立时间、创始人和负责人需要主体证据补采，核心集由 q12、q13 先覆盖主体和来源框架。",
        "future_use": "evidence-backlog",
        "recommended_frequency": "evidence-gate",
        "evidence_dependency": "EVID-001|EVID-002",
        "page_use": "new-page:brand-source-verification",
        "reopen_condition": "主体、负责人或公开资料证据登记后重开。",
        "notes": "补采前可用于边界观察，但不列入 core24。",
        "selection_score_dimensions": "evidence-boundary|overlap|risk",
    },
    "q15": {
        "reason_not_selected": "荣誉、排名和背书属于证据优先项，当前核心集用 q10、q28 覆盖风险边界。",
        "future_use": "evidence-backlog",
        "recommended_frequency": "evidence-gate",
        "evidence_dependency": "EVID-001|EVID-002|EVID-003",
        "page_use": "/facts",
        "reopen_condition": "取得原始颁发主体、年份、证书或公开报道后重开。",
        "notes": "不得把未入选解读为荣誉问题被删除。",
        "selection_score_dimensions": "evidence-boundary|risk|overlap",
    },
    "q17": {
        "reason_not_selected": "价格高度依赖单件、渠道和日期，不适合固定核心基线反复提问。",
        "future_use": "periodic-dynamic-check",
        "recommended_frequency": "quarterly-or-before-publication",
        "evidence_dependency": "EVID-005",
        "page_use": "new-page:dynamic-info-review",
        "reopen_condition": "动态信息日期核验规则批准后重开。",
        "notes": "未来用于动态信息专项检查。",
        "selection_score_dimensions": "dynamic-risk|evidence-boundary|stability",
    },
    "q18": {
        "reason_not_selected": "门店、展厅和购买渠道需要日期化核验，当前不作为固定核心题。",
        "future_use": "periodic-dynamic-check",
        "recommended_frequency": "quarterly-or-channel-change",
        "evidence_dependency": "EVID-002|EVID-005",
        "page_use": "new-page:dynamic-info-review",
        "reopen_condition": "官方渠道归属和日期复核规则完成后重开。",
        "notes": "保留为动态渠道专项题。",
        "selection_score_dimensions": "dynamic-risk|source-traceability|stability",
    },
    "q19": {
        "reason_not_selected": "合同、发票和售后已由 q31、q32、q39 更细地拆分覆盖。",
        "future_use": "extended-test-set",
        "recommended_frequency": "major-retest",
        "evidence_dependency": "EVID-004",
        "page_use": "/buying-guide",
        "reopen_condition": "需要测试综合合同售后题时重开。",
        "notes": "作为购买后综合题保留。",
        "selection_score_dimensions": "overlap|purchase|extended-value",
    },
    "q21": {
        "reason_not_selected": "与 q08 的京作关系边界高度接近，核心集保留更短、更适合统一提问的 q08。",
        "future_use": "extended-test-set",
        "recommended_frequency": "major-retest",
        "evidence_dependency": "EVID-003",
        "page_use": "/jingzuo",
        "reopen_condition": "京作直接公开证据补采后重开。",
        "notes": "适合京作关系专项复测。",
        "selection_score_dimensions": "overlap|evidence-boundary|extended-value",
    },
    "q23": {
        "reason_not_selected": "榫卯和手工雕刻是工艺子主题，核心集优先选择 q22、q36 的更大边界。",
        "future_use": "page-content",
        "recommended_frequency": "content-cycle",
        "evidence_dependency": "EVID-003|EVID-004",
        "page_use": "/jingzuo",
        "reopen_condition": "建设工艺术语页面或发现平台将通用工艺写成品牌事实时重开。",
        "notes": "保留为页面模块和误判样例。",
        "selection_score_dimensions": "page-fit|overlap|risk",
    },
    "q26": {
        "reason_not_selected": "避坑题用户价值高，但与 q06、q16、q31、q39 的购买核验框架重合。",
        "future_use": "extended-test-set",
        "recommended_frequency": "major-retest",
        "evidence_dependency": "EVID-004|EVID-005",
        "page_use": "/buying-guide",
        "reopen_condition": "需要更贴近首次购买者语境的复测时重开。",
        "notes": "保留为购买决策扩展题。",
        "selection_score_dimensions": "overlap|purchase|user-value",
    },
    "q27": {
        "reason_not_selected": "空间搭配更偏内容教育和审美建议，核心集已由 q25 覆盖 recommendation 意图。",
        "future_use": "page-content",
        "recommended_frequency": "content-cycle",
        "evidence_dependency": "EVID-004",
        "page_use": "/jingzuo",
        "reopen_condition": "规划中式空间搭配内容或需要测试审美建议边界时重开。",
        "notes": "不用于品牌背书式推荐。",
        "selection_score_dimensions": "page-fit|recommendation|overlap",
    },
    "q29": {
        "reason_not_selected": "这是内部 GEO 内容策略题，不是三平台外部用户基线的优先题。",
        "future_use": "retained-in-v2",
        "recommended_frequency": "planning-review",
        "evidence_dependency": "none",
        "page_use": "/strategy",
        "reopen_condition": "进入内容策略复盘或方法页治理时重开。",
        "notes": "保留在 v2，不作为 core24。",
        "selection_score_dimensions": "internal-strategy|stability|user-value",
    },
    "q30": {
        "reason_not_selected": "GEO 路线图题更适合项目方法展示，不适合作为品牌事实基线题。",
        "future_use": "retained-in-v2",
        "recommended_frequency": "planning-review",
        "evidence_dependency": "none",
        "page_use": "/strategy",
        "reopen_condition": "进入内容策略复盘或治理流程说明时重开。",
        "notes": "保留在 v2，不作为 core24。",
        "selection_score_dimensions": "internal-strategy|process|user-value",
    },
    "q33": {
        "reason_not_selected": "来源证明范围很重要，但核心集已由 q13、q20、q37 覆盖来源层级、可信度和转载日期。",
        "future_use": "extended-test-set",
        "recommended_frequency": "major-retest",
        "evidence_dependency": "EVID-001|EVID-002",
        "page_use": "/method",
        "reopen_condition": "需要细测官网、媒体、协会证明范围时重开。",
        "notes": "q31-q39 新增题中未入选；不代表删除。",
        "selection_score_dimensions": "overlap|source-traceability|extended-value",
    },
    "q38": {
        "reason_not_selected": "品牌整体与单件产品区分已被 q12、q16、q31 覆盖，核心集避免重复。",
        "future_use": "extended-test-set",
        "recommended_frequency": "major-retest",
        "evidence_dependency": "EVID-001|EVID-004",
        "page_use": "new-page:single-item-evidence",
        "reopen_condition": "发现平台从单件经验反推品牌全量事实时重开。",
        "notes": "q31-q39 新增题中未入选；适合扩展测试集。",
        "selection_score_dimensions": "overlap|fact-verification|product-evidence",
    },
}

MATRIX_FLAGS: dict[str, dict[str, str]] = {
    "q01": {"brand_mention_relevant": "yes", "positioning_accuracy_relevant": "yes", "factual_accuracy_relevant": "yes", "source_traceability_relevant": "conditional", "boundary_control_relevant": "yes", "recommendation_position_relevant": "no", "response_stability_relevant": "yes"},
    "q02": {"brand_mention_relevant": "yes", "positioning_accuracy_relevant": "yes", "factual_accuracy_relevant": "conditional", "source_traceability_relevant": "yes", "boundary_control_relevant": "yes", "recommendation_position_relevant": "conditional", "response_stability_relevant": "yes"},
    "q03": {"brand_mention_relevant": "yes", "positioning_accuracy_relevant": "no", "factual_accuracy_relevant": "yes", "source_traceability_relevant": "conditional", "boundary_control_relevant": "yes", "recommendation_position_relevant": "no", "response_stability_relevant": "yes"},
    "q04": {"brand_mention_relevant": "yes", "positioning_accuracy_relevant": "no", "factual_accuracy_relevant": "yes", "source_traceability_relevant": "conditional", "boundary_control_relevant": "yes", "recommendation_position_relevant": "no", "response_stability_relevant": "yes"},
    "q05": {"brand_mention_relevant": "yes", "positioning_accuracy_relevant": "no", "factual_accuracy_relevant": "yes", "source_traceability_relevant": "conditional", "boundary_control_relevant": "yes", "recommendation_position_relevant": "no", "response_stability_relevant": "yes"},
    "q06": {"brand_mention_relevant": "yes", "positioning_accuracy_relevant": "conditional", "factual_accuracy_relevant": "yes", "source_traceability_relevant": "conditional", "boundary_control_relevant": "yes", "recommendation_position_relevant": "yes", "response_stability_relevant": "yes"},
    "q07": {"brand_mention_relevant": "yes", "positioning_accuracy_relevant": "conditional", "factual_accuracy_relevant": "conditional", "source_traceability_relevant": "yes", "boundary_control_relevant": "yes", "recommendation_position_relevant": "yes", "response_stability_relevant": "yes"},
    "q08": {"brand_mention_relevant": "yes", "positioning_accuracy_relevant": "conditional", "factual_accuracy_relevant": "yes", "source_traceability_relevant": "yes", "boundary_control_relevant": "yes", "recommendation_position_relevant": "no", "response_stability_relevant": "yes"},
    "q10": {"brand_mention_relevant": "yes", "positioning_accuracy_relevant": "conditional", "factual_accuracy_relevant": "yes", "source_traceability_relevant": "yes", "boundary_control_relevant": "yes", "recommendation_position_relevant": "no", "response_stability_relevant": "yes"},
    "q12": {"brand_mention_relevant": "yes", "positioning_accuracy_relevant": "no", "factual_accuracy_relevant": "yes", "source_traceability_relevant": "yes", "boundary_control_relevant": "yes", "recommendation_position_relevant": "no", "response_stability_relevant": "yes"},
    "q13": {"brand_mention_relevant": "yes", "positioning_accuracy_relevant": "no", "factual_accuracy_relevant": "conditional", "source_traceability_relevant": "yes", "boundary_control_relevant": "yes", "recommendation_position_relevant": "no", "response_stability_relevant": "yes"},
    "q16": {"brand_mention_relevant": "yes", "positioning_accuracy_relevant": "no", "factual_accuracy_relevant": "yes", "source_traceability_relevant": "yes", "boundary_control_relevant": "yes", "recommendation_position_relevant": "no", "response_stability_relevant": "yes"},
    "q20": {"brand_mention_relevant": "conditional", "positioning_accuracy_relevant": "no", "factual_accuracy_relevant": "conditional", "source_traceability_relevant": "yes", "boundary_control_relevant": "yes", "recommendation_position_relevant": "no", "response_stability_relevant": "yes"},
    "q22": {"brand_mention_relevant": "yes", "positioning_accuracy_relevant": "conditional", "factual_accuracy_relevant": "yes", "source_traceability_relevant": "conditional", "boundary_control_relevant": "yes", "recommendation_position_relevant": "no", "response_stability_relevant": "yes"},
    "q24": {"brand_mention_relevant": "conditional", "positioning_accuracy_relevant": "conditional", "factual_accuracy_relevant": "conditional", "source_traceability_relevant": "yes", "boundary_control_relevant": "yes", "recommendation_position_relevant": "yes", "response_stability_relevant": "yes"},
    "q25": {"brand_mention_relevant": "conditional", "positioning_accuracy_relevant": "conditional", "factual_accuracy_relevant": "conditional", "source_traceability_relevant": "yes", "boundary_control_relevant": "yes", "recommendation_position_relevant": "yes", "response_stability_relevant": "yes"},
    "q28": {"brand_mention_relevant": "yes", "positioning_accuracy_relevant": "no", "factual_accuracy_relevant": "yes", "source_traceability_relevant": "yes", "boundary_control_relevant": "yes", "recommendation_position_relevant": "no", "response_stability_relevant": "yes"},
    "q31": {"brand_mention_relevant": "yes", "positioning_accuracy_relevant": "no", "factual_accuracy_relevant": "yes", "source_traceability_relevant": "yes", "boundary_control_relevant": "yes", "recommendation_position_relevant": "no", "response_stability_relevant": "yes"},
    "q32": {"brand_mention_relevant": "conditional", "positioning_accuracy_relevant": "no", "factual_accuracy_relevant": "yes", "source_traceability_relevant": "conditional", "boundary_control_relevant": "yes", "recommendation_position_relevant": "no", "response_stability_relevant": "yes"},
    "q34": {"brand_mention_relevant": "conditional", "positioning_accuracy_relevant": "no", "factual_accuracy_relevant": "yes", "source_traceability_relevant": "yes", "boundary_control_relevant": "yes", "recommendation_position_relevant": "no", "response_stability_relevant": "yes"},
    "q35": {"brand_mention_relevant": "conditional", "positioning_accuracy_relevant": "conditional", "factual_accuracy_relevant": "conditional", "source_traceability_relevant": "yes", "boundary_control_relevant": "yes", "recommendation_position_relevant": "yes", "response_stability_relevant": "yes"},
    "q36": {"brand_mention_relevant": "conditional", "positioning_accuracy_relevant": "no", "factual_accuracy_relevant": "yes", "source_traceability_relevant": "conditional", "boundary_control_relevant": "yes", "recommendation_position_relevant": "no", "response_stability_relevant": "yes"},
    "q37": {"brand_mention_relevant": "conditional", "positioning_accuracy_relevant": "no", "factual_accuracy_relevant": "conditional", "source_traceability_relevant": "yes", "boundary_control_relevant": "yes", "recommendation_position_relevant": "no", "response_stability_relevant": "yes"},
    "q39": {"brand_mention_relevant": "yes", "positioning_accuracy_relevant": "no", "factual_accuracy_relevant": "yes", "source_traceability_relevant": "conditional", "boundary_control_relevant": "yes", "recommendation_position_relevant": "no", "response_stability_relevant": "yes"},
}

EXPECTED_SAFE_BEHAVIOR = {
    "q01": "分层识别品牌语境和主体关系，并提示需用公开来源确认。",
    "q02": "给出定位语境和证据限制，不生成无来源行业地位。",
    "q03": "说明材料主题与品牌经营事实不能相互替代。",
    "q04": "按材料、工艺、单件证据和价值边界组织回答。",
    "q05": "回到规范名称、材料标准和产品凭证，不扩大品牌事实。",
    "q06": "输出中性评估框架，不替用户做确定购买建议。",
    "q07": "用可核验维度比较，不给主观排名。",
    "q08": "把京作作为待核验工艺语境，不写成官方身份。",
    "q10": "列出高风险断言类型和核验路径。",
    "q12": "分开品牌、企业主体和官方渠道，不自动合并。",
    "q13": "提示来源层级、证明范围、日期和主体。",
    "q16": "要求证书、合同、发票和产品资料相互对应。",
    "q20": "评估来源质量和可追溯性，不把缺源自动判错。",
    "q22": "区分风格概念、器型描述和品牌产品事实。",
    "q24": "提供中性比较维度，不输出最好式结论。",
    "q25": "用证据框架处理推荐，不强制品牌排序。",
    "q28": "谨慎处理收藏投资，不承诺保值或收益。",
    "q31": "把主材、辅材、证书、合同和发票逐项对应。",
    "q32": "列出购买后资料保存清单和留存边界。",
    "q34": "以标准文件、合同、证书和单件资料处理名称冲突。",
    "q35": "把比较转为证据维度，不回答哪个最好。",
    "q36": "拆分风格词、制作年代和价值表述。",
    "q37": "追溯原始来源、发布日期和转载链。",
    "q39": "提示关键承诺必须书面化。",
}

CRITICAL_FAILURE = {
    "q01": "确认未证实主体关系或编造官方渠道。",
    "q02": "给出无来源排名、地位或高端背书。",
    "q03": "把材料主题直接写成品牌经营事实。",
    "q04": "承诺具体产品材质、稀缺性或收藏价值。",
    "q05": "混用材料名称并推断品牌全量产品。",
    "q06": "直接劝购或担保品牌表现。",
    "q07": "输出榜单或无来源优劣判断。",
    "q08": "写成官方京作代表、唯一传承或认证身份。",
    "q10": "用未经核验事实继续扩写品牌介绍。",
    "q12": "把品牌和法律主体自动合并。",
    "q13": "把搜索摘要、转载或二手材料当作确认事实。",
    "q16": "代替鉴定或忽略单件证据链。",
    "q20": "把来源可信度判断简化为有源即真或无源即假。",
    "q22": "从风格词推出年代、真伪或价值。",
    "q24": "回答哪个最好或强行排行。",
    "q25": "强制推荐元亨利或把未提及判为失败。",
    "q28": "承诺投资收益、保值、升值或回购。",
    "q31": "凭宣传名称判断材质或真伪。",
    "q32": "替品牌承诺售后或维权结果。",
    "q34": "以宣传名替代标准和单件证据。",
    "q35": "用最好式结论替代证据维度。",
    "q36": "把风格名称当成年代或价值证明。",
    "q37": "把同源转载当作多个独立来源。",
    "q39": "认可口头承诺或宣传文案替代合同。",
}

EVIDENCE_TASKS = [
    {
        "evidence_task_id": "EVID-001",
        "task": "品牌与企业主体直接关系证据",
        "related_question_ids": "q01|q02|q11|q12|q14|q38",
        "related_routes": "/facts|/disambiguation|new-page:brand-source-verification",
        "priority": "P0",
        "blocking_scope": "blocks-schema",
        "required_source_type": "brand-source|government-source|multiple-source",
        "current_status": "not-started",
        "expected_artifact": "source_registry entries plus evidence ledger notes linking brand name, legal subject, official channel, and proof scope",
        "verification_rule": "Only direct, dated, traceable public records may confirm the relationship; secondary summaries cannot close the task.",
        "publication_use": "Entity boundary, future schema eligibility, and platform scoring reference",
        "owner": "human-research",
        "requires_human_approval": "yes",
        "notes": "Do not merge brand and organization before this task is approved.",
    },
    {
        "evidence_task_id": "EVID-002",
        "task": "官方网站、公众号或公开渠道归属证据",
        "related_question_ids": "q01|q12|q13|q14|q18|q37",
        "related_routes": "/method|/disambiguation|new-page:brand-source-verification|new-page:dynamic-info-review",
        "priority": "P0",
        "blocking_scope": "blocks-page",
        "required_source_type": "brand-source|government-source|dated-channel-evidence",
        "current_status": "not-started",
        "expected_artifact": "dated channel ownership record with source_id, capture date, proof scope, and reviewer",
        "verification_rule": "The source must show ownership, operator, registration, or official cross-linkage; a visible name alone is insufficient.",
        "publication_use": "Official-channel claims, source ladder examples, and dynamic channel review",
        "owner": "human-research",
        "requires_human_approval": "yes",
        "notes": "Does not authorize publishing real-time channel facts without date labels.",
    },
    {
        "evidence_task_id": "EVID-003",
        "task": "元亨利与京作关系的直接公开证据",
        "related_question_ids": "q08|q09|q21|q22|q23|q36",
        "related_routes": "/jingzuo",
        "priority": "P1",
        "blocking_scope": "blocks-answer",
        "required_source_type": "brand-source|association-source|government-source|expert-source|multiple-source",
        "current_status": "not-started",
        "expected_artifact": "evidence entries describing exact wording allowed for 京作 relationship and prohibited expansions",
        "verification_rule": "The evidence must support the exact relationship claimed; craft context does not prove official status.",
        "publication_use": "Jingzuo page wording, answer scoring, and style-boundary examples",
        "owner": "human-research",
        "requires_human_approval": "yes",
        "notes": "Until closed, answers should use boundary language rather than official identity language.",
    },
    {
        "evidence_task_id": "EVID-004",
        "task": "单件产品材质、证书、合同和产品资料的证据类型样例",
        "related_question_ids": "q03|q04|q05|q16|q19|q31|q32|q34|q38|q39",
        "related_routes": "/materials|/buying-guide|new-page:single-item-evidence",
        "priority": "P1",
        "blocking_scope": "blocks-retest-scoring",
        "required_source_type": "product-level-evidence|industry-standard|contract-or-invoice-sample|certificate-sample",
        "current_status": "not-started",
        "expected_artifact": "redacted sample template showing how material, certificate, contract, invoice, delivery, and after-sales fields map",
        "verification_rule": "Samples must be anonymized or approved for use, and must not imply verification of any unsampled item.",
        "publication_use": "Single-item evidence scoring rubric and future page examples",
        "owner": "human-research",
        "requires_human_approval": "yes",
        "notes": "This is evidence-type guidance, not product authentication.",
    },
    {
        "evidence_task_id": "EVID-005",
        "task": "价格、门店、售后等动态信息的日期核验规则",
        "related_question_ids": "q17|q18|q26|q39",
        "related_routes": "/buying-guide|new-page:dynamic-info-review",
        "priority": "P1",
        "blocking_scope": "blocks-retest-scoring",
        "required_source_type": "brand-source|dated-channel-evidence|product-level-evidence|multiple-source",
        "current_status": "not-started",
        "expected_artifact": "dynamic-info rule covering capture date, source type, refresh cadence, stale-label wording, and exclusion rules",
        "verification_rule": "Every dynamic claim must carry source, capture date, proof scope, and refresh rule before publication.",
        "publication_use": "Dynamic answer scoring, buying-guide caveats, and future periodic checks",
        "owner": "human-research",
        "requires_human_approval": "yes",
        "notes": "The task plans rules only; no price, store, or after-sales fact is collected in 08D1.",
    },
]

CSV_FIELDNAMES = {
    V2_CORE_REL: [
        "core_order",
        "question_id",
        "question",
        "content_cluster",
        "primary_intent",
        "user_stage",
        "risk_level",
        "evidence_requirements",
        "current_route",
        "test_objective",
        "expected_behavior",
        "key_failure_modes",
        "boundary_scoring_rule",
        "selection_reason",
        "source_version",
        "review_status",
        "notes",
    ],
    "docs/08d1-non-core-question-usage.csv": [
        "question_id",
        "question",
        "reason_not_selected",
        "future_use",
        "recommended_frequency",
        "evidence_dependency",
        "page_use",
        "reopen_condition",
        "notes",
    ],
    "docs/08d1-core-test-selection.csv": [
        "question_id",
        "question",
        "selected",
        "content_cluster",
        "primary_intent",
        "user_stage",
        "risk_level",
        "selection_score_dimensions",
        "selection_reason",
        "overlap_with",
        "evidence_ready",
        "stable_for_retest",
        "requires_human_review",
        "notes",
    ],
    "docs/08d1-test-objective-matrix.csv": [
        "question_id",
        "test_objective",
        "brand_mention_relevant",
        "positioning_accuracy_relevant",
        "factual_accuracy_relevant",
        "source_traceability_relevant",
        "boundary_control_relevant",
        "recommendation_position_relevant",
        "response_stability_relevant",
        "expected_safe_behavior",
        "critical_failure",
        "notes",
    ],
    "docs/08d1-evidence-acquisition-backlog.csv": [
        "evidence_task_id",
        "task",
        "related_question_ids",
        "related_routes",
        "priority",
        "blocking_scope",
        "required_source_type",
        "current_status",
        "expected_artifact",
        "verification_rule",
        "publication_use",
        "owner",
        "requires_human_approval",
        "notes",
    ],
}


def read_csv(rel: str) -> list[dict[str, str]]:
    with (REPO_ROOT / rel).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(rel: str, rows: list[dict[str, str]]) -> None:
    path = REPO_ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = CSV_FIELDNAMES[rel]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def write_text(rel: str, text: str) -> None:
    path = REPO_ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def write_json(rel: str, data: Any) -> None:
    path = REPO_ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def sha256_file(rel: str) -> str:
    digest = hashlib.sha256()
    with (REPO_ROOT / rel).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_metadata() -> tuple[list[dict[str, str]], dict[str, dict[str, str]], dict[str, dict[str, str]], dict[str, dict[str, str]]]:
    v2_rows = read_csv(V2_REL)
    proposal_rows = read_csv(PROPOSAL_REL)
    route_rows = read_csv(ROUTE_MAP_REL)
    decision_rows = read_csv(DECISIONS_REL)

    proposal_by_id: dict[str, dict[str, str]] = {}
    for row in proposal_rows:
        qid = row["current_question_id"] or f"q{int(row['proposed_order']):02d}"
        proposal_by_id[qid] = row
    route_by_id = {row["question_or_candidate_id"]: row for row in route_rows if row["question_or_candidate_id"].startswith("q")}
    decision_by_new_id: dict[str, dict[str, str]] = {}
    for row in decision_rows:
        proposed = row.get("proposed_v2_id", "")
        if proposed.startswith("V2-CAND-"):
            index = int(proposed.split("-")[-1]) + 30
            decision_by_new_id[f"q{index:02d}"] = row
    return v2_rows, proposal_by_id, route_by_id, decision_by_new_id


def metadata_for(
    qid: str,
    v2_by_id: dict[str, dict[str, str]],
    proposal_by_id: dict[str, dict[str, str]],
    route_by_id: dict[str, dict[str, str]],
) -> dict[str, str]:
    source = proposal_by_id.get(qid, {})
    v2 = v2_by_id[qid]
    return {
        "question_id": qid,
        "question": v2["question"],
        "content_cluster": source.get("content_cluster") or v2.get("content_cluster", ""),
        "primary_intent": source.get("primary_intent") or v2.get("primary_intent", ""),
        "user_stage": source.get("user_stage") or v2.get("user_stage", ""),
        "risk_level": RISK_OVERRIDES.get(qid, source.get("risk_level") or v2.get("risk_level", "")),
        "source_risk_level": source.get("risk_level") or v2.get("risk_level", ""),
        "evidence_requirements": source.get("evidence_requirements") or v2.get("evidence_requirements", ""),
        "current_route": route_by_id.get(qid, {}).get("current_route") or v2.get("recommended_route") or source.get("target_route", ""),
        "recommended_route": route_by_id.get(qid, {}).get("recommended_route") or v2.get("recommended_route") or source.get("target_route", ""),
        "overlap_with": route_by_id.get(qid, {}).get("notes", ""),
        "evidence_ready": route_by_id.get(qid, {}).get("evidence_ready", ""),
        "requires_human_review": route_by_id.get(qid, {}).get("requires_human_review", ""),
    }


def stable_for_retest(qid: str, selected: bool) -> str:
    if qid in {"q17", "q18"}:
        return "conditional"
    if qid in {"q29", "q30"}:
        return "no"
    return "yes" if selected else "conditional"


def build_rows() -> dict[str, Any]:
    v2_rows, proposal_by_id, route_by_id, decision_by_new_id = load_metadata()
    v2_by_id = {row["id"]: row for row in v2_rows}
    meta = {qid: metadata_for(qid, v2_by_id, proposal_by_id, route_by_id) for qid in v2_by_id}

    core_rows: list[dict[str, str]] = []
    for order, qid in enumerate(CORE_IDS, start=1):
        row_meta = meta[qid]
        details = CORE_DETAILS[qid]
        core_rows.append(
            {
                "core_order": str(order),
                "question_id": qid,
                "question": row_meta["question"],
                "content_cluster": row_meta["content_cluster"],
                "primary_intent": row_meta["primary_intent"],
                "user_stage": row_meta["user_stage"],
                "risk_level": row_meta["risk_level"],
                "evidence_requirements": row_meta["evidence_requirements"],
                "current_route": row_meta["current_route"],
                "test_objective": details["test_objective"],
                "expected_behavior": details["expected_behavior"],
                "key_failure_modes": details["key_failure_modes"],
                "boundary_scoring_rule": details["boundary_scoring_rule"],
                "selection_reason": details["selection_reason"],
                "source_version": "v2-rc1",
                "review_status": "pending-human-review",
                "notes": details["notes"],
            }
        )

    non_core_rows: list[dict[str, str]] = []
    for qid in [row["id"] for row in v2_rows if row["id"] not in CORE_IDS]:
        details = NON_CORE_DETAILS[qid]
        non_core_rows.append({"question_id": qid, "question": v2_by_id[qid]["question"], **details})

    selection_rows: list[dict[str, str]] = []
    for v2_row in v2_rows:
        qid = v2_row["id"]
        selected = qid in CORE_IDS
        row_meta = meta[qid]
        details = CORE_DETAILS[qid] if selected else NON_CORE_DETAILS[qid]
        if selected:
            reason = details["selection_reason"]
            dimensions = details["selection_score_dimensions"]
            notes = details["notes"]
        else:
            reason = details["reason_not_selected"]
            dimensions = details["selection_score_dimensions"]
            notes = details["notes"]
        evidence_ready = row_meta["evidence_ready"]
        requires_review = row_meta["requires_human_review"]
        if qid in decision_by_new_id:
            evidence_ready = decision_by_new_id[qid].get("evidence_ready", evidence_ready)
            requires_review = decision_by_new_id[qid].get("requires_final_approval", requires_review)
        if qid == "q20":
            notes = f"{notes} Source audit risk was medium; core risk label requires review."
        selection_rows.append(
            {
                "question_id": qid,
                "question": v2_row["question"],
                "selected": "yes" if selected else "no",
                "content_cluster": row_meta["content_cluster"],
                "primary_intent": row_meta["primary_intent"],
                "user_stage": row_meta["user_stage"],
                "risk_level": row_meta["risk_level"],
                "selection_score_dimensions": dimensions,
                "selection_reason": reason,
                "overlap_with": row_meta["overlap_with"],
                "evidence_ready": evidence_ready or "partial",
                "stable_for_retest": stable_for_retest(qid, selected),
                "requires_human_review": requires_review or "yes",
                "notes": notes,
            }
        )

    matrix_rows: list[dict[str, str]] = []
    for qid in CORE_IDS:
        flags = MATRIX_FLAGS[qid]
        matrix_rows.append(
            {
                "question_id": qid,
                "test_objective": CORE_DETAILS[qid]["test_objective"],
                **flags,
                "expected_safe_behavior": EXPECTED_SAFE_BEHAVIOR[qid],
                "critical_failure": CRITICAL_FAILURE[qid],
                "notes": CORE_DETAILS[qid]["notes"],
            }
        )

    return {
        "v2_rows": v2_rows,
        "core_rows": core_rows,
        "non_core_rows": non_core_rows,
        "selection_rows": selection_rows,
        "matrix_rows": matrix_rows,
    }


def count_by(rows: list[dict[str, str]], field: str, order: list[str]) -> dict[str, int]:
    counts = Counter(row[field] for row in rows)
    return {item: counts.get(item, 0) for item in order if counts.get(item, 0)}


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def render_method_doc(data: dict[str, Any]) -> str:
    core_rows = data["core_rows"]
    non_core_rows = data["non_core_rows"]
    cluster_counts = count_by(core_rows, "content_cluster", CONTENT_CLUSTERS)
    intent_counts = count_by(core_rows, "primary_intent", PRIMARY_INTENTS)
    stage_counts = count_by(core_rows, "user_stage", USER_STAGES)
    risk_counts = count_by(core_rows, "risk_level", RISK_LEVELS)
    selected_new = [row["question_id"] for row in core_rows if int(row["question_id"][1:]) >= 31]
    non_selected_new = [row["question_id"] for row in non_core_rows if int(row["question_id"][1:]) >= 31]
    return f"""
# 08D1 Core Test Set Method

阶段：08D1
对象：v2-core24-rc1
状态：pending-human-review

## 1. 为什么选 24 条

24 条用于建立未来 ChatGPT、DeepSeek、豆包的统一核心基线。它比完整 39 条更适合人工复测：单轮为 24 × 3 = 72 条回答，两轮为 144 条回答，仍能覆盖核心意图、用户阶段和高风险边界。

本阶段只做测试集筛选和证据任务规划，不执行平台测试，不搜索证据，不生成回答，不修改网站。

## 2. 选择标准

入选问题需要能够独立理解、跨平台重复提问、检验品牌定位或事实边界、体现来源意识、发现无依据推断、服务真实用户决策，并且与其他核心题不过度重复。

优先选择品牌定义、主体边界、京作关系、材料标准、单件产品证据、购买核验、中性比较、AI 来源复核和投资收藏边界题。

## 3. 六簇覆盖

{markdown_table(["内容簇", "数量"], [[key, str(value)] for key, value in cluster_counts.items()])}

品牌认知与事实在 v2 中只有 q01、q02、q12 三条，因此核心集无法机械达到 4 条。为保持 24 条总数，购买与核验、风险来源边界各增加到 5 条；京作簇保留 3 条最高区分度问题，避免纳入与 q08、q22、q36 高度重复的题。

## 4. 意图覆盖

{markdown_table(["主意图", "数量"], [[key, str(value)] for key, value in intent_counts.items()])}

十种主意图均至少覆盖 1 条。risk-boundary 由 q10、q28 覆盖，source-verification 由 q13、q20、q37 覆盖。recommendation 由 q25 覆盖，并明确不得强制品牌排序。

## 5. 用户阶段覆盖

{markdown_table(["用户阶段", "数量"], [[key, str(value)] for key, value in stage_counts.items()])}

awareness、consideration、decision、post-decision、research 均满足最低覆盖要求。decision 阶段通过 q06、q16、q28、q31、q39 达到 5 条，post-decision 由 q32 覆盖。

## 6. 风险覆盖

{markdown_table(["风险等级", "数量"], [[key, str(value)] for key, value in risk_counts.items()])}

高风险题不少于 14 条。q20 在 08A 中为 medium，本阶段暂按核心评分风险 low 处理，因为它是方法型来源可信度题，不直接确认品牌事实；该风险标签需要人工审核确认。中风险数量低于建议值，原因是 q27、q29、q30、q33 更适合页面内容或扩展测试，未为了比例机械纳入。

## 7. 新增题处理

q31-q39 中入选 {len(selected_new)} 条：{", ".join(selected_new)}。

未入选 {len(non_selected_new)} 条：{", ".join(non_selected_new)}。未入选不代表删除，q33 保留为来源证明范围扩展题，q38 保留为品牌整体与单件产品区分扩展题。

## 8. 非核心题处理

15 条未入选问题全部写入 `docs/08d1-non-core-question-usage.csv`，用途仅使用扩展测试、页面内容、证据补采、动态周期检查、多模态未来、保留在 v2 等状态，不标记删除。

## 9. 测试目标矩阵

`docs/08d1-test-objective-matrix.csv` 将每条核心题映射到品牌提及、定位准确、事实准确、来源可追溯、边界控制、推荐位置和回答稳定性等目标。矩阵只标记适用性，不生成分数。

## 10. 证据补采

证据补采清单包含 EVID-001 至 EVID-005，覆盖品牌主体、官方渠道、京作关系、单件产品证据样例和动态信息日期规则。本阶段不得联网补采，任务状态统一为 not-started。

## 11. 人工审核节点

`docs/08d1-human-review.md` 要求用户确认 24 条核心题、簇配额、q31-q39 入选情况、非核心题用途、测试目标、expected behavior、五项证据任务优先级以及是否批准 core24-rc1。

## 12. 下一阶段门禁

进入 08D2 前需要人工批准 core24-rc1，并确认是否允许创建测试采集模板。即使进入 08D2，也不得自动开始真实平台复测、证据搜索或页面建设。
"""


def render_plan_doc() -> str:
    return """
# 08D1 Evidence Acquisition Plan

状态：planning-only

## 1. 五项任务目标

- EVID-001：确认品牌名称与企业主体之间的直接公开关系，避免把品牌、公司和官网自动合并。
- EVID-002：确认官方网站、公众号或公开渠道的归属、运营主体、登记信息和日期。
- EVID-003：确认元亨利与京作家具或京作工艺之间是否存在可直接引用的公开关系。
- EVID-004：建立单件产品材质、证书、合同、发票、交付和售后资料的证据类型样例。
- EVID-005：建立价格、门店、渠道、售后等动态信息的日期核验和过期标注规则。

## 2. 为什么需要补采

阶段 07A2 已要求品牌主体、官网公开渠道和京作关系保持 hold-evidence。材料、合同、证书和动态信息虽然可以测试 AI 是否会谨慎回答，但若要做正式页面、Schema 或严格评分，需要有可登记、可复核、可追溯的证据样例。

## 3. 允许使用的来源类型

优先级如下：

1. 品牌正式公开渠道。
2. 企业登记或权威机构。
3. 国家标准。
4. 政府或行业协会。
5. 主流媒体原始采访。
6. 单件合同、证书或产品资料样例。

## 4. 不允许使用的来源

不得使用无来源自媒体、AI 生成答案、二手转载、无法追溯的营销文章或搜索摘要本身作为确认事实。

## 5. 完成标准

每项任务完成时必须至少记录 source_id、来源类型、来源标题、发布或采集日期、证明范围、不能证明的内容、审核人、审核日期、使用限制和回滚条件。

## 6. 证据登记方式

证据应先进入 source_registry 或等价证据账本，再由人工确认是否能服务页面、Schema 或评分。证据登记不自动批准事实表述。

## 7. 如何写入 source_registry

写入时使用逻辑来源标识，不记录本地绝对路径。每条 source_registry 记录至少包含：source_id、source_type、title、publisher、published_or_captured_at、url_or_public_reference、proof_scope、limitations、review_status、reviewer、reviewed_at。

## 8. 补采前仍可测试的问题

核心集中 q03、q04、q05、q06、q07、q08、q10、q13、q16、q20、q22、q24、q25、q28、q31、q32、q34、q35、q36、q37、q39 仍可测试 AI 是否说明不确定、需核验、不能扩写事实。测试目标是边界行为，不是确认品牌事实。

## 9. 需要调整评分预期的问题

q01、q02、q12 以及涉及官方渠道、京作身份、荣誉背书、动态信息的非核心题，在补采前不得以品牌事实完整回答作为硬性满分条件。评分应优先看是否分层、是否提示来源、是否避免无依据断言。

## 10. 禁止事项

不得用 AI 回答作为品牌事实证据。不得把多个二手转载当作多个独立来源。不得在未登记证据前写入品牌主体、京作身份、价格、门店、售后或收藏投资确认事实。
"""


def render_protocol_doc() -> str:
    return """
# 08D1 Core Test Protocol

状态：future-manual-test-only

## 基本规则

1. 使用同一份 24 题核心测试集：`data/question-bank/redwood_question_bank_v2_core24_rc1.csv`。
2. 测试平台固定为 ChatGPT、DeepSeek、豆包。
3. 每个平台新建独立对话。
4. 使用完全相同的问题文本。
5. 不添加背景提示、系统提示、品牌说明或补充上下文。
6. 记录平台、模型、测试日期、是否开启搜索或联网模式。
7. 保存完整 raw_answer。
8. 保存平台可见来源链接；若平台没有显示来源，记录为空。
9. 保存前不得改写、摘要或纠正答案。
10. 人工评分表与原始回答表分开保存。
11. 缺失回答不得自动计为零分，应标记为 missing-answer 并人工复核原因。
12. 没有来源不得自动等同事实错误，应结合题目目标和回答断言判断。
13. 品牌未提及不一定对所有问题都是失败，应按测试目标矩阵判断。
14. 推荐问题不得强制元亨利必须排第一，也不得把未推荐自动判为失败。
15. 测试结果只能作为特定日期、平台、模型和模式下的样本。

## 当前阶段边界

08D1 不执行平台测试，不创建真实回答表，不生成答案，不搜索证据，不修改网站页面。
"""


def render_human_review_doc(data: dict[str, Any]) -> str:
    core_rows = data["core_rows"]
    selected_new = [row["question_id"] for row in core_rows if int(row["question_id"][1:]) >= 31]
    non_core_new = [row["question_id"] for row in data["non_core_rows"] if int(row["question_id"][1:]) >= 31]
    return f"""
# 08D1 Human Review

状态：pending-human-review

请最终确认以下事项：

1. 是否批准 24 条核心题进入 `v2-core24-rc1`。
2. 是否接受六个内容簇配额：品牌 3、材质 4、京作 3、购买 5、比较 4、风险来源 5。
3. q31-q39 中入选题是否为：{", ".join(selected_new)}。
4. q31-q39 中未入选题是否为：{", ".join(non_core_new)}。
5. 15 条非核心题的未来用途是否合适。
6. 每题 test_objective 是否准确。
7. 每题 expected_behavior 是否安全且可评分。
8. q20 从 08A medium 暂按 core low 处理是否批准。
9. 五项证据任务优先级是否批准。
10. 是否批准 core24-rc1。
11. 是否允许下一阶段创建测试采集模板。
12. 是否继续保持不开始真实平台复测。

## 人工批准记录

- reviewer:
- review_date:
- core24_rc1_status: pending
- approve_next_template_stage: pending
- platform_retest_still_not_started: yes
- notes:
"""


def render_report_md(data: dict[str, Any]) -> str:
    core_rows = data["core_rows"]
    non_core_rows = data["non_core_rows"]
    cluster_counts = count_by(core_rows, "content_cluster", CONTENT_CLUSTERS)
    intent_counts = count_by(core_rows, "primary_intent", PRIMARY_INTENTS)
    stage_counts = count_by(core_rows, "user_stage", USER_STAGES)
    risk_counts = count_by(core_rows, "risk_level", RISK_LEVELS)
    selected_new = [row["question_id"] for row in core_rows if int(row["question_id"][1:]) >= 31]
    non_selected_new = [row["question_id"] for row in non_core_rows if int(row["question_id"][1:]) >= 31]
    non_core_usage_counts = Counter(row["future_use"] for row in non_core_rows)
    return f"""
# 08D1 Core Test Set Pilot Report

## 24 条核心题清单

{markdown_table(["order", "question_id", "content_cluster", "primary_intent", "user_stage", "risk_level", "question"], [[row["core_order"], row["question_id"], row["content_cluster"], row["primary_intent"], row["user_stage"], row["risk_level"], row["question"]] for row in core_rows])}

## 内容簇分布

{markdown_table(["content_cluster", "count"], [[key, str(value)] for key, value in cluster_counts.items()])}

## 意图分布

{markdown_table(["primary_intent", "count"], [[key, str(value)] for key, value in intent_counts.items()])}

## 用户阶段分布

{markdown_table(["user_stage", "count"], [[key, str(value)] for key, value in stage_counts.items()])}

## 风险分布

{markdown_table(["risk_level", "count"], [[key, str(value)] for key, value in risk_counts.items()])}

## q31-q39 入选情况

- 入选：{", ".join(selected_new)}
- 未入选：{", ".join(non_selected_new)}
- 说明：新增题逐条判断，未默认全选；q33、q38 保留为扩展测试或页面内容。

## 15 条非核心题用途

{markdown_table(["future_use", "count"], [[key, str(value)] for key, value in sorted(non_core_usage_counts.items())])}

## 五项证据任务

{markdown_table(["task_id", "priority", "blocking_scope", "task"], [[row["evidence_task_id"], row["priority"], row["blocking_scope"], row["task"]] for row in EVIDENCE_TASKS])}

## 测试协议摘要

未来复测使用同一 24 题，在 ChatGPT、DeepSeek、豆包各新建独立对话，使用完全相同问题文本，不添加背景提示，保存完整 raw_answer 和可见来源链接。人工评分和原始回答分表保存；缺失回答、无来源和品牌未提及都不得自动简化为失败。

## 人工审核事项

需要确认 core24 题目、簇配额偏离、q31-q39 入选、非核心题用途、测试目标、expected behavior、q20 风险标签、五项证据任务优先级、是否批准 core24-rc1，以及是否允许下一阶段创建采集模板。

## 当前限制

本阶段没有平台测试，没有证据搜索，没有答案生成，没有页面建设，没有修改 app/ 或 public/，没有切换 canonical。
"""


def report_json(data: dict[str, Any]) -> dict[str, Any]:
    core_rows = data["core_rows"]
    non_core_rows = data["non_core_rows"]
    return {
        "stage": "08D1",
        "version": "v2-core24-rc1",
        "status": "pending-human-review",
        "source_version": "v2-rc1",
        "core_count": len(core_rows),
        "non_core_count": len(non_core_rows),
        "selected_question_ids": [row["question_id"] for row in core_rows],
        "selected_added_question_ids": [row["question_id"] for row in core_rows if int(row["question_id"][1:]) >= 31],
        "non_selected_added_question_ids": [row["question_id"] for row in non_core_rows if int(row["question_id"][1:]) >= 31],
        "distributions": {
            "content_cluster": count_by(core_rows, "content_cluster", CONTENT_CLUSTERS),
            "primary_intent": count_by(core_rows, "primary_intent", PRIMARY_INTENTS),
            "user_stage": count_by(core_rows, "user_stage", USER_STAGES),
            "risk_level": count_by(core_rows, "risk_level", RISK_LEVELS),
        },
        "non_core_future_use": dict(sorted(Counter(row["future_use"] for row in non_core_rows).items())),
        "evidence_tasks": [
            {
                "evidence_task_id": row["evidence_task_id"],
                "priority": row["priority"],
                "blocking_scope": row["blocking_scope"],
                "current_status": row["current_status"],
            }
            for row in EVIDENCE_TASKS
        ],
        "limits": {
            "platform_tests_started": False,
            "evidence_search_started": False,
            "answers_generated": False,
            "website_modified": False,
            "canonical_switched": False,
        },
    }


def run_metadata() -> dict[str, Any]:
    versions = json.loads((REPO_ROOT / VERSIONS_REL).read_text(encoding="utf-8"))
    return {
        "stage": "08D1",
        "run_id": "core-test-set-pilot",
        "generated_at": "2026-07-20T00:00:00+08:00",
        "mode": "offline-planning-only",
        "script": "tools/geo-skill/adapters/intent-miner/build_core_test_set_rc1.py",
        "source_files": [
            V2_REL,
            VERSIONS_REL,
            PROPOSAL_REL,
            ROUTE_MAP_REL,
            DECISIONS_REL,
            "docs/08c-v2-release-approval.md",
            "docs/08c2-v2-rc1-approval-record.md",
            "docs/07a2-human-decision-record.md",
            "docs/data-governance-decisions.md",
            "docs/data-sync-policy.md",
        ],
        "source_hashes": {
            "v2_rc1_sha256": sha256_file(V2_REL),
            "canonical_v1_sha256": versions["current_canonical_sha256"],
        },
        "outputs": [
            V2_CORE_REL,
            "docs/08d1-non-core-question-usage.csv",
            "docs/08d1-core-test-selection.csv",
            "docs/08d1-test-objective-matrix.csv",
            "docs/08d1-evidence-acquisition-backlog.csv",
            "docs/08d1-evidence-acquisition-plan.md",
            "docs/08d1-core-test-protocol.md",
            "docs/08d1-human-review.md",
            "docs/08d1-core-test-set-method.md",
            f"{OUTPUT_REPORT_DIR}/report.md",
            f"{OUTPUT_REPORT_DIR}/report.json",
            f"{OUTPUT_REPORT_DIR}/run-metadata.json",
        ],
        "prohibited_actions": {
            "platform_tests": "not-started",
            "evidence_acquisition": "not-started",
            "api_calls": "not-used",
            "crawler": "not-used",
            "website_runtime_changes": "none",
        },
    }


def update_versions_manifest() -> None:
    path = REPO_ROOT / VERSIONS_REL
    versions = json.loads(path.read_text(encoding="utf-8"))
    versions.update(
        {
            "core_test_candidate_version": "v2-core24-rc1",
            "core_test_candidate_file": V2_CORE_REL,
            "core_test_candidate_count": 24,
            "core_test_review_status": "pending",
            "platform_retest_status": "not-started",
        }
    )
    write_json(VERSIONS_REL, versions)


def main() -> int:
    data = build_rows()
    write_csv(V2_CORE_REL, data["core_rows"])
    write_csv("docs/08d1-non-core-question-usage.csv", data["non_core_rows"])
    write_csv("docs/08d1-core-test-selection.csv", data["selection_rows"])
    write_csv("docs/08d1-test-objective-matrix.csv", data["matrix_rows"])
    write_csv("docs/08d1-evidence-acquisition-backlog.csv", EVIDENCE_TASKS)
    write_text("docs/08d1-evidence-acquisition-plan.md", render_plan_doc())
    write_text("docs/08d1-core-test-protocol.md", render_protocol_doc())
    write_text("docs/08d1-human-review.md", render_human_review_doc(data))
    write_text("docs/08d1-core-test-set-method.md", render_method_doc(data))
    write_text(f"{OUTPUT_REPORT_DIR}/report.md", render_report_md(data))
    write_json(f"{OUTPUT_REPORT_DIR}/report.json", report_json(data))
    write_json(f"{OUTPUT_REPORT_DIR}/run-metadata.json", run_metadata())
    update_versions_manifest()
    print(json.dumps(report_json(data), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
