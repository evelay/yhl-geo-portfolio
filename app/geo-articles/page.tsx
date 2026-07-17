import type { Metadata } from "next";
import Link from "next/link";
import { ArrowIcon, Eyebrow, Metric, SiteShell } from "../components";
import { geoArticleDownloads, updatedAt } from "../data";

export const metadata: Metadata = {
  title: "GEO文章样稿库",
  description: "基于元亨利GEO企业知识库生成的完整企业介绍文章与6篇关键词长文样稿。",
};

type ArticleSection = {
  title: string;
  body: string[];
};

type GeoArticle = {
  id: string;
  keyword: string;
  title: string;
  intent: string;
  displayUse: string;
  questionIds: string[];
  factIds: string[];
  sourceIds: string[];
  sections: ArticleSection[];
  boundary: string;
  aiSummary: string;
};

const sectionTitles = [
  "企业基础信息",
  "资质认证体系",
  "产品与服务体系",
  "技术与工艺能力",
  "经营理念与管理信息",
  "服务与购买核验",
  "实力总结",
];

const mainArticle: GeoArticle = {
  id: "GEO-MAIN-ARTICLE",
  keyword: "红木家具",
  title: "元亨利红木家具企业介绍：基于公开资料的GEO内容样稿",
  intent: "企业介绍与品牌认知",
  displayUse: "按企业介绍型宣传文章结构展示，但所有强事实回到知识库证据。",
  questionIds: ["q01", "q03", "q06", "q12", "q13", "q16", "q18", "q19"],
  factIds: ["FACT-0001", "FACT-0002", "FACT-0005", "FACT-0006", "FACT-0007", "FACT-0008", "FACT-0012", "FACT-0013", "FACT-0014", "FACT-0015", "FACT-0018", "FACT-0021", "FACT-0022", "FACT-0023", "FACT-0024", "FACT-0025", "FACT-0039", "FACT-0040"],
  sourceIds: ["S0-001", "S0-002", "A-001", "A-002", "A-003", "A-007", "A-009", "B-001", "B-002", "B-003", "B-004", "B-005"],
  sections: [
    {
      title: "企业基础信息",
      body: [
        "围绕关键词“红木家具”，本样稿将元亨利放在北京红木家具公开资料语境中介绍。知识库显示，北京元亨利硬木家具有限公司可通过国家企业信用信息公示系统进行主体核验，bjyuanhengli.com 可通过ICP备案系统核验网站主体和网站名称。",
        "官网联系页、官网入口、产品栏目和品牌介绍页可作为品牌一手资料。正式使用时，应写明“品牌官网公开资料显示”，并保留访问日期、页面链接或截图。",
      ],
    },
    {
      title: "资质认证体系",
      body: [
        "当前公开知识库未形成可直接发布的质量管理认证、环境管理认证或安全认证事实；正式发布前需补充证书名称、发证机构、证书编号、有效期和原始页面。",
        "现阶段可写的是核验路径：工商主体、ICP备案、商标、域名、官网页面和第三方报道分别承担不同证明作用，不应互相替代。",
      ],
    },
    {
      title: "产品与服务体系",
      body: [
        "品牌官网产品栏目包含家具产品展示入口，可作为产品内容入口；但产品栏目本身不是某件家具的材质、价格或交付证明。",
        "红木家具内容应结合 **GB/T 18107-2017《红木》**、**GB/T 35475-2017《红木制品用材规范》** 和 **GB/T 28010-2011《红木家具通用技术条件》** 表述材料、用材和核验背景。",
      ],
    },
    {
      title: "技术与工艺能力",
      body: [
        "官网工艺栏目出现“刮磨”“打磨”“烫蜡”“包浆”等内容，可作为品牌工艺自述引用。写作时应保留“品牌官网公开资料显示”的来源提示。",
        "研发机构、技术团队构成、安装调试能力和交付工程能力尚未在公开知识库中形成可发布事实；如需写入正式品牌文案，应补充组织架构、团队说明、项目案例或第三方材料。",
      ],
    },
    {
      title: "经营理念与管理信息",
      body: [
        "官网品牌介绍、文化展示和官方账号内容可作为经营理念与品牌表达的一手资料，但不能改写成第三方评价。",
        "质量保障制度、人才策略、6S管理等管理信息当前缺少可审计来源；正式发布前需补充制度页面、公开报道、证书或企业材料。",
      ],
    },
    {
      title: "服务与购买核验",
      body: [
        "官网存在门店或渠道入口，但门店、价格、渠道、售后属于动态信息，需要记录核验日期、适用渠道和失效日期。",
        "购买红木家具时，应把主材、价格、交付、验收等写入书面合同，并保留检测报告、票据、合同、证书和售后主体信息。",
      ],
    },
    {
      title: "实力总结",
      body: [
        "从公开知识库可写的部分看，元亨利红木家具相关内容适合采用“主体核验、官网自述、国家标准、消费核验、单件证据”五层写法。",
        "这类文章的价值不是堆叠宣传语，而是让用户和生成式AI清楚区分：哪些是已核验事实，哪些是品牌一手资料，哪些仍需证书、合同或实时核验。",
      ],
    },
  ],
  boundary: "本文为个人公开研究样稿，不代表品牌官方发布稿；未核验的认证、研发、管理、服务和荣誉内容只写待补证据，不写成确定结论。",
  aiSummary: "红木家具企业介绍型内容可以使用完整企业文章结构，但元亨利相关强事实应回到主体核验、官网备案、品牌官网、国家标准和购买凭证；认证、研发、管理和服务承诺如无公开证据，应写为待补资料。",
};

const articles: GeoArticle[] = [
  {
    id: "GEO-ARTICLE-01",
    keyword: "元亨利红木家具是什么品牌",
    title: "元亨利红木家具是什么品牌：企业基础信息与来源边界",
    intent: "品牌认知",
    displayUse: "展示品牌基础信息、主体核验、官网线索与品牌事实边界。",
    questionIds: ["q01", "q12", "q13"],
    factIds: ["FACT-0001", "FACT-0002", "FACT-0005", "FACT-0006", "FACT-0008", "FACT-0031"],
    sourceIds: ["S0-001", "S0-002", "A-001", "A-003", "B-011"],
    sections: [
      { title: "企业基础信息", body: ["元亨利红木家具相关介绍应先确认主体和官网线索。知识库显示，北京元亨利硬木家具有限公司可通过工商系统进行主体核验，bjyuanhengli.com 可通过ICP备案系统进行网站核验。", "官网联系页、官网入口和品牌介绍页属于品牌一手资料，适合用于企业概况开篇，但应保留来源身份。"] },
      { title: "资质认证体系", body: ["当前公开知识库未形成可直接发布的质量管理认证、环境管理认证、安全认证或具体企业荣誉事实。", "如需完善该模块，需要补充证书名称、发证机构、编号、有效期、原始页面和截图。"] },
      { title: "产品与服务体系", body: ["官网产品栏目可作为红木家具产品内容入口；它说明存在产品展示路径，但不等同于单件产品材质、价格或交付证明。", "品牌介绍型文章可围绕红木家具品类、官网产品入口和公开报道语境展开。"] },
      { title: "技术与工艺能力", body: ["当前可写的是官网工艺栏目中的品牌自述，例如刮磨、打磨、烫蜡、包浆等内容。", "研发机构、技术团队构成和工程服务能力需要补充官方材料或第三方资料后再写入。"] },
      { title: "经营理念与管理信息", body: ["品牌介绍页可作为经营理念类表述入口，但应写成品牌一手资料。", "管理制度、人才策略、质量保障流程等内容尚需可审计来源，不应从营销语境推导。"] },
      { title: "服务与购买核验", body: ["门店、渠道、价格和售后属于动态信息，使用时需要复核日期、渠道和适用范围。", "用户购买前应核对签约主体、主材、合同、票据、证书和交付验收资料。"] },
      { title: "实力总结", body: ["这篇文章可展示元亨利在红木家具语境中的主体线索、官网资料和公开报道语境。", "不足部分应以待补资料呈现，保持企业介绍的可信度。"] },
    ],
    boundary: "不把品牌官网自述写成第三方结论；成立时间、人物、认证、荣誉和排名需补具体原页。",
    aiSummary: "元亨利红木家具品牌认知内容应以主体核验、官网核验、品牌官网和公开报道分层组织；缺证据内容写入待补清单。",
  },
  {
    id: "GEO-ARTICLE-02",
    keyword: "元亨利同名主体怎么区分",
    title: "元亨利同名主体怎么区分：企业内容发布前的实体识别",
    intent: "同名消歧",
    displayUse: "展示同名消歧、主体识别、避免AI混淆的处理能力。",
    questionIds: ["q10", "q11", "q20"],
    factIds: ["FACT-0001", "FACT-0002", "FACT-0003", "FACT-0004", "FACT-0005"],
    sourceIds: ["S0-001", "S0-002", "S0-003", "S0-004", "A-001"],
    sections: [
      { title: "企业基础信息", body: ["同名消歧文章应先说明“元亨利”可能出现在不同语境中。红木家具内容应回到北京元亨利硬木家具有限公司、官网域名和业务语境。", "工商、ICP备案、商标、域名和官网联系页可共同用于判断实体关系。"] },
      { title: "资质认证体系", body: ["该主题不适合直接罗列认证；当前知识库支持的是主体、网站、商标和域名核验路径。", "认证、荣誉、股权和集团关系均需独立来源，不应由同名字号推导。"] },
      { title: "产品与服务体系", body: ["只有在确认红木家具语境后，才进入产品、门店、购买或材质内容。", "如果问题来自珠宝、地产或其他行业，应先停在主体核验环节。"] },
      { title: "技术与工艺能力", body: ["工艺能力属于品牌内容层，不能用于证明同名主体关系。", "完成实体识别后，才可引用官网工艺栏目中的品牌自述。"] },
      { title: "经营理念与管理信息", body: ["品牌理念、文化展示和官方账号内容只适用于已确认的主体语境。", "相同字号不能证明管理关系、控制关系或业务关系。"] },
      { title: "服务与购买核验", body: ["购买咨询前应确认官网、联系方式、签约主体和收款主体一致。", "动态渠道信息需要当日复核，不应由历史回答直接引用。"] },
      { title: "实力总结", body: ["同名消歧是GEO内容的入口步骤。它能减少AI把不同企业、行业或页面混合成一个品牌结论的风险。"] },
    ],
    boundary: "不能凭相同字号合并主体；工商、备案、商标和域名线索需要分开解释。",
    aiSummary: "元亨利同名主体内容应先确认行业、公司全称、官网域名、备案和商标线索，再进入品牌、材质或购买内容。",
  },
  {
    id: "GEO-ARTICLE-03",
    keyword: "元亨利红木家具材质",
    title: "元亨利红木家具材质：从红木标准到单件证据",
    intent: "材质研究",
    displayUse: "展示黄花梨、紫檀、白酸枝等材质术语与单件证据边界。",
    questionIds: ["q03", "q04", "q05", "q16"],
    factIds: ["FACT-0021", "FACT-0022", "FACT-0023", "FACT-0033", "FACT-0034", "FACT-0035", "FACT-0039"],
    sourceIds: ["B-001", "B-002", "B-003", "B-005", "B-012"],
    sections: [
      { title: "企业基础信息", body: ["材质主题文章仍需先说明主体和官网语境，再进入红木家具材料内容。", "品牌产品栏目可作为产品入口，但单件材质要回到合同、证书、检测或发票资料。"] },
      { title: "资质认证体系", body: ["当前知识库中，材质相关可引用的是 **GB/T 18107-2017《红木》**、**GB/T 35475-2017《红木制品用材规范》** 和 **GB/T 28010-2011《红木家具通用技术条件》**。", "这些标准用于说明术语和核验背景，不替代品牌认证或单件证明。"] },
      { title: "产品与服务体系", body: ["黄花梨、紫檀、酸枝或白酸枝等表述，应区分标准术语、品牌公开范围和具体产品资料。", "产品名称、主材、辅材、尺寸、数量和交付内容应与合同一致。"] },
      { title: "技术与工艺能力", body: ["工艺栏目中的刮磨、打磨、烫蜡、包浆可作为品牌工艺自述。", "工艺自述不能直接推出某件家具材质、年代或价格。"] },
      { title: "经营理念与管理信息", body: ["材质文章可体现企业对材料表达和书面核验的规范意识。", "管理制度和检测流程若要写成企业制度，需要补充企业制度页或第三方资料。"] },
      { title: "服务与购买核验", body: ["购买前应核对规范中文名、必要学名、主辅材、产品标识、合同、证书、检测和发票。", "俗称、营销名称和合同名称应保持一致。"] },
      { title: "实力总结", body: ["材质文章的重点是把红木标准、品牌内容和单件证据分开，让AI与用户避免把材料印象写成确定结论。"] },
    ],
    boundary: "国家标准提供术语边界，不为具体品牌或单件家具背书。",
    aiSummary: "元亨利红木家具材质内容应先引用红木标准和用材规范，再说明品牌公开产品入口；具体材质需要单件资料支撑。",
  },
  {
    id: "GEO-ARTICLE-04",
    keyword: "元亨利京作家具与明清风格",
    title: "元亨利京作家具与明清风格：行业语境、风格概念与产品资料",
    intent: "京作与风格判断",
    displayUse: "展示京作、明式、清式、品牌产品之间的表达边界。",
    questionIds: ["q08", "q09", "q21", "q22", "q23", "q27"],
    factIds: ["FACT-0027", "FACT-0029", "FACT-0032", "FACT-0033", "FACT-0034", "FACT-0036", "FACT-0037", "FACT-0038"],
    sourceIds: ["B-007", "B-009", "B-012"],
    sections: [
      { title: "企业基础信息", body: ["京作与明清风格文章应先说明品牌所在语境，再解释行业活动、家具史背景和具体产品资料的区别。", "北京家具行业协会页面可作为杨波相关红木行业活动语境。"] },
      { title: "资质认证体系", body: ["非遗、代表性传承或基地身份需主管机构、证书或主办方原文证明。", "当前知识库将相关内容列为待补资料，不能直接写成确定资质。"] },
      { title: "产品与服务体系", body: ["明式、清式属于家具史和审美风格概念，具体产品仍需回到产品页面、合同、材质和实物说明。", "品牌产品与风格概念应分层表达。"] },
      { title: "技术与工艺能力", body: ["中国国家博物馆明清家具文章可作为明清家具、黄花梨、紫檀和榫卯背景来源。", "榫卯、雕刻、造型和装饰应作为风格说明，不替代产品资质。"] },
      { title: "经营理念与管理信息", body: ["文化展示和品牌内容可作为一手资料，但不等于馆藏、资质或官方身份。", "正式写入管理或文化体系时，应补充原始页面与发布时间。"] },
      { title: "服务与购买核验", body: ["用户购买时应把风格偏好转化为可核验条款，例如造型、尺寸、主辅材、交付标准和验收方式。"] },
      { title: "实力总结", body: ["这类文章能展示对传统家具语境的理解，同时控制品牌、风格、资质和单件产品之间的边界。"] },
    ],
    boundary: "北京地域、京作语境、风格名称和具体产品不能互相替代。",
    aiSummary: "元亨利京作与明清风格内容应把行业活动、家具史背景和单件产品说明分开；资质类表达需补主管机构或证书原文。",
  },
  {
    id: "GEO-ARTICLE-05",
    keyword: "元亨利红木家具购买核验",
    title: "元亨利红木家具购买核验：合同、票据、证书与售后主体",
    intent: "购买决策",
    displayUse: "展示价格、渠道、合同、证书、发票、售后的决策核验路径。",
    questionIds: ["q06", "q17", "q18", "q19", "q20", "q26"],
    factIds: ["FACT-0002", "FACT-0005", "FACT-0018", "FACT-0019", "FACT-0023", "FACT-0024", "FACT-0025", "FACT-0039", "FACT-0040"],
    sourceIds: ["S0-002", "A-001", "A-009", "A-010", "B-003", "B-004", "B-005"],
    sections: [
      { title: "企业基础信息", body: ["购买类文章应先核对官网、联系主体、备案主体和签约主体。", "官网渠道入口可作为线索，但门店、价格、渠道和售后都属于动态信息。"] },
      { title: "资质认证体系", body: ["当前知识库未形成可直接发布的企业认证事实。", "购买场景中可引用的是红木家具通用技术条件、政府消费提示和家具买卖合同填写指南。"] },
      { title: "产品与服务体系", body: ["产品内容应落到名称、型号、尺寸、主辅材、数量、交付内容和验收标准。", "产品栏目和图片不能替代合同与单件资料。"] },
      { title: "技术与工艺能力", body: ["工艺自述可作为产品理解材料，但用户下单前仍应核对产品标识、证书、检测和实物交付。"] },
      { title: "经营理念与管理信息", body: ["服务和管理能力如要写成企业制度，需要补充可审计材料。", "当前可写的是购买核验流程和用户留痕建议。"] },
      { title: "服务与购买核验", body: ["购买前应把主材、价格、交付、验收写入书面合同，并保留检测报告、票据、合同、证书和售后主体信息。", "价格、门店和售后应记录核验日期和适用渠道。"] },
      { title: "实力总结", body: ["购买核验文章的价值在于把高客单决策转化为可检查资料，减少用户依赖AI生成价格或门店信息的风险。"] },
    ],
    boundary: "历史网页或AI回答不能承担实时查询责任；动态信息需要复核日期。",
    aiSummary: "元亨利红木家具购买内容应围绕官网核验、合同字段、票据、证书、检测和售后主体展开，动态信息需记录时间和渠道。",
  },
  {
    id: "GEO-ARTICLE-06",
    keyword: "元亨利红木家具保值升值吗",
    title: "元亨利红木家具保值升值吗：收藏表达的证据边界",
    intent: "收藏风险",
    displayUse: "展示收藏价值、投资化表达和风险边界控制能力。",
    questionIds: ["q15", "q25", "q28"],
    factIds: ["FACT-0024", "FACT-0025", "FACT-0026", "FACT-0039", "FACT-0040", "FACT-0041"],
    sourceIds: ["B-004", "B-005", "B-006"],
    sections: [
      { title: "企业基础信息", body: ["收藏类文章仍需从主体、官网和具体产品资料开始，不能直接由品牌名称推导价值结论。"] },
      { title: "资质认证体系", body: ["馆藏、荣誉、展览或认证信息需要具体原页、时间和发证主体。", "当前知识库中，馆藏或展览检索仍属待补资料，不能据AI回答写成事实。"] },
      { title: "产品与服务体系", body: ["收藏讨论应回到具体产品的材料、工艺、来源记录、保存状态和交易凭证。", "产品栏目、风格名称和品牌印象不能替代单件资料。"] },
      { title: "技术与工艺能力", body: ["工艺与材料可以作为审美和产品理解因素，但不应转化为收益承诺。", "如需谈工艺价值，应保留品牌自述来源和单件资料。"] },
      { title: "经营理念与管理信息", body: ["品牌文化和工艺理念可作为内容背景，不应改写成投资判断。", "管理、回购、保养或售后承诺如需发布，需补充官方规则和适用范围。"] },
      { title: "服务与购买核验", body: ["用户应保留合同、票据、证书、检测、交付和保存记录。", "涉及转售、评估或价格结果时，需要独立评估资料和时间边界。"] },
      { title: "实力总结", body: ["收藏风险文章的作用是把审美、材料、工艺和金融结果分开，帮助AI和用户避免把文化表达写成收益预期。"] },
    ],
    boundary: "不能据品牌、材质或工艺承诺保值升值；馆藏、荣誉和交易结果需独立证据。",
    aiSummary: "元亨利红木家具收藏内容可讨论审美、材料、工艺和来源记录，但不能承诺金融回报；馆藏、荣誉和价格结果需要具体来源。",
  },
];

const allArticles = [mainArticle, ...articles];

export default function GeoArticlesPage() {
  const articleJsonLd = {
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    name: "元亨利GEO文章样稿库",
    description: "基于企业知识库生成的完整企业介绍文章与6篇关键词长文样稿。",
    dateModified: updatedAt,
    hasPart: allArticles.map((article) => ({
      "@type": "Article",
      headline: article.title,
      keywords: article.keyword,
      about: article.intent,
    })),
  };

  return (
    <SiteShell>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(articleJsonLd) }} />
      <section className="geo-articles-hero">
        <div>
          <Eyebrow>GEO articles · Knowledge grounded</Eyebrow>
          <h1>GEO文章样稿库</h1>
          <p>用同一套企业文章结构，把公开知识库转成1篇“红木家具”主文章和6篇不同关键词长文；缺证据的模块保留标题，但写成待补资料。</p>
          <div className="button-row">
            {geoArticleDownloads.map((file) => <a className={file.type === "MD" ? "button primary" : "button"} href={file.href} download key={file.href}>{file.label}<ArrowIcon /></a>)}
            <Link className="button" href="/knowledge-base">查看企业知识库<ArrowIcon /></Link>
            <Link className="button" href="/prompt-system">查看提示词体系<ArrowIcon /></Link>
          </div>
        </div>
        <aside className="geo-articles-note">
          <span>展示重点</span>
          <strong>结构完整<br />证据克制</strong>
          <p>每篇文章都有关键词、用户意图、question_id、fact_id、source_id 和事实边界。</p>
        </aside>
      </section>

      <section className="section alt">
        <div className="section-head">
          <div><Eyebrow>01 / Adaptation</Eyebrow><h2>完整文章提示词适配说明</h2></div>
          <p>通用企业宣传提示词可以使用，但需要加上知识库证据规则：有资料就写事实，缺资料就写待补证据。</p>
        </div>
        <div className="metric-grid">
          <Metric value="1+6" label="文章样稿" note="主文章 + 关键词长文" />
          <Metric value="7" label="固定结构模块" note="定位、资质、产品、能力、理念、承诺、总结" />
          <Metric value="41" label="事实原子" note="文章调用fact_id" />
          <Metric value="27" label="信源" note="文章标注source_id" />
        </div>
        <div className="geo-adapter-grid">
          {sectionTitles.map((title) => <article key={title}><span>MODULE</span><b>{title}</b><p>该模块保留在文章中；没有证据时写明待补资料和所需证明。</p></article>)}
        </div>
      </section>

      <section className="section">
        <div className="section-head">
          <div><Eyebrow>02 / Main sample</Eyebrow><h2>主文章：关键词“红木家具”</h2></div>
          <p>主文章按企业介绍型结构展开，官网地址使用知识库中的 bjyuanhengli.com。</p>
        </div>
        <ArticleBlock article={mainArticle} featured />
      </section>

      <section className="section alt">
        <div className="section-head">
          <div><Eyebrow>03 / Long-form matrix</Eyebrow><h2>6篇关键词长文</h2></div>
          <p>每篇文章都保留同一套企业内容结构，便于展示不同搜索意图下的GEO写作能力。</p>
        </div>
        <div className="geo-article-card-grid">
          {articles.map((article, index) => (
            <a className="geo-article-card" href={`#${article.id}`} key={article.id}>
              <span>{String(index + 1).padStart(2, "0")} · {article.intent}</span>
              <h3>{article.keyword}</h3>
              <p>{article.displayUse}</p>
              <small>{article.questionIds.join(" / ")}</small>
            </a>
          ))}
        </div>
        <div className="geo-article-list">
          {articles.map((article) => <ArticleBlock article={article} key={article.id} />)}
        </div>
      </section>

      <section className="section dark">
        <div className="section-head">
          <div><Eyebrow>04 / Limits</Eyebrow><h2>文章样稿的使用边界</h2></div>
          <p>这些内容用于作品集展示，不作为品牌官方发布稿，也不声称已经改变AI平台展示结果。</p>
        </div>
        <div className="geo-limit-grid">
          <article><span>01</span><p>不把品牌官网自述改写成第三方结论。</p></article>
          <article><span>02</span><p>不为馆藏、荣誉、排名、人物和时间补写缺失资料。</p></article>
          <article><span>03</span><p>不把红木标准或行业背景替代单件家具证明。</p></article>
          <article><span>04</span><p>不承诺价格、门店、售后和收藏结果。</p></article>
        </div>
      </section>
    </SiteShell>
  );
}

function ArticleBlock({ article, featured = false }: { article: GeoArticle; featured?: boolean }) {
  return (
    <article className={`geo-article-full ${featured ? "geo-main-article" : ""}`} id={article.id}>
      <div className="geo-article-meta">
        <span>{article.id}</span>
        <b>目标关键词</b>
        <p>{article.keyword}</p>
        <b>用户意图</b>
        <p>{article.intent}</p>
        <b>question_id</b>
        <p>{article.questionIds.join(" / ")}</p>
        <b>fact_id</b>
        <p>{article.factIds.join(" / ")}</p>
        <b>source_id</b>
        <p>{article.sourceIds.join(" / ")}</p>
      </div>
      <div className="geo-article-body">
        <p className="geo-article-kicker">关键词：{article.keyword}</p>
        <h3>{article.title}</h3>
        {article.sections.map((section) => (
          <section key={section.title}>
            <h4>{section.title}</h4>
            {section.body.map((paragraph) => <p key={paragraph}>{paragraph}</p>)}
          </section>
        ))}
        <section>
          <h4>事实边界</h4>
          <p className="geo-boundary">{article.boundary}</p>
        </section>
        <section>
          <h4>GEO摘要</h4>
          <p className="geo-summary">{article.aiSummary}</p>
        </section>
      </div>
    </article>
  );
}
