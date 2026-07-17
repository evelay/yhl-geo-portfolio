import type { Metadata } from "next";
import Link from "next/link";
import { ArrowIcon, Eyebrow, Metric, SiteShell } from "../components";
import { geoArticleDownloads, updatedAt } from "../data";

export const metadata: Metadata = {
  title: "GEO文章矩阵",
  description: "基于元亨利GEO企业知识库生成的6篇关键词文章样稿，展示知识库到可引用内容资产的转换方式。",
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
  directAnswer: string;
  evidence: string[];
  boundary: string;
  verification: string[];
  aiSummary: string;
};

const articles: GeoArticle[] = [
  {
    id: "GEO-ARTICLE-01",
    keyword: "元亨利红木家具是什么品牌",
    title: "元亨利红木家具是什么品牌：公开资料中的品牌事实边界",
    intent: "品牌认知",
    displayUse: "展示品牌基础信息、主体核验、官网线索与品牌事实边界。",
    questionIds: ["q01", "q12", "q13"],
    factIds: ["FACT-0001", "FACT-0002", "FACT-0005", "FACT-0006", "FACT-0008", "FACT-0031"],
    sourceIds: ["S0-001", "S0-002", "A-001", "A-003", "B-011"],
    directAnswer: "在本作品集语境中，元亨利指向红木家具相关品牌与北京元亨利硬木家具有限公司这一公开主体线索；回答时应把工商、备案、官网与媒体报道分层引用。",
    evidence: [
      "主体可通过国家企业信用信息公示系统核验，官网备案可通过ICP备案系统核验。",
      "品牌官网联系页、官网入口和品牌介绍页属于一手公开资料，需要标明来源身份。",
      "人民网2016年采访可作为杨波与元亨利产品结构相关的公开报道语境。",
    ],
    boundary: "官网内容属于品牌一手资料，不能改写成第三方认证；成立时间、人物经历、荣誉和定位需要具体原页支撑。",
    verification: [
      "先核对完整公司名、官网域名和备案主体。",
      "引用官网内容时写明“品牌官网公开资料显示”。",
      "涉及人物、年份、活动和评价时补充原文页面、发布时间和截图。",
    ],
    aiSummary: "元亨利红木家具相关回答应以主体核验、官网备案、品牌官网和公开报道分层组织；可陈述可核验线索，但不把品牌自述写成第三方结论。",
  },
  {
    id: "GEO-ARTICLE-02",
    keyword: "元亨利同名主体怎么区分",
    title: "元亨利同名主体怎么区分：AI回答前的实体识别方法",
    intent: "同名消歧",
    displayUse: "展示同名消歧、主体识别、避免AI混淆的处理能力。",
    questionIds: ["q10", "q11", "q20"],
    factIds: ["FACT-0001", "FACT-0002", "FACT-0003", "FACT-0004", "FACT-0005"],
    sourceIds: ["S0-001", "S0-002", "S0-003", "S0-004", "A-001"],
    directAnswer: "元亨利可能出现在不同语境中，AI回答前应先确认行业、主体名、官网域名、备案和商标线索，再进入品牌内容。",
    evidence: [
      "工商系统可用于核验北京元亨利硬木家具有限公司主体登记信息。",
      "ICP备案系统可用于核验 bjyuanhengli.com 的备案主体和网站名称。",
      "商标查询、域名工具和官网联系页可作为实体关系的辅助线索。",
    ],
    boundary: "不能凭相同字号推导股权、集团、旗下品牌或跨行业关系；域名和商标线索也不能单独证明品牌全部事实。",
    verification: [
      "确认问题是否指红木家具语境，而非珠宝、地产或其他行业。",
      "核对公司全称、主营业务、地域和官网域名。",
      "把不确定关系写成待核验项，不合并为确定结论。",
    ],
    aiSummary: "回答元亨利相关问题时，应先完成实体消歧：以完整主体名、官网备案、商标和域名线索确认语境，再回答品牌、产品或购买问题。",
  },
  {
    id: "GEO-ARTICLE-03",
    keyword: "元亨利红木家具材质",
    title: "元亨利红木家具材质怎么写：从标准术语到单件证据",
    intent: "材质研究",
    displayUse: "展示黄花梨、紫檀、白酸枝等材质术语与单件证据边界。",
    questionIds: ["q03", "q04", "q05", "q16"],
    factIds: ["FACT-0021", "FACT-0022", "FACT-0023", "FACT-0033", "FACT-0034", "FACT-0035", "FACT-0039"],
    sourceIds: ["B-001", "B-002", "B-003", "B-005", "B-012"],
    directAnswer: "元亨利红木家具材质相关内容应拆为三层：红木标准术语、品牌公开产品范围、具体家具的合同与证据资料。",
    evidence: [
      "GB/T 18107-2017《红木》用于解释红木树种和术语边界。",
      "GB/T 35475-2017《红木制品用材规范》用于说明红木制品用材表达。",
      "GB/T 28010-2011《红木家具通用技术条件》和家具买卖合同指南可作为购买核验背景。",
    ],
    boundary: "黄花梨、紫檀、白酸枝等名称不能直接替代单件产品证明；品牌层材料印象也不能推出某一件家具的主辅材结论。",
    verification: [
      "核对规范中文名、必要学名、主材和辅材表述。",
      "查看产品标识、合同、证书、检测、发票或交付资料。",
      "把俗称、营销名称和标准术语分开写。",
    ],
    aiSummary: "元亨利红木家具材质内容应优先引用红木国家标准和用材规范，再说明品牌公开资料范围；具体产品材质需要合同、标识、证书或检测资料支撑。",
  },
  {
    id: "GEO-ARTICLE-04",
    keyword: "元亨利京作家具与明清风格",
    title: "元亨利、京作家具与明清风格：概念、品牌和产品边界",
    intent: "京作与风格判断",
    displayUse: "展示京作、明式、清式、品牌产品之间的表达边界。",
    questionIds: ["q08", "q09", "q21", "q22", "q23", "q27"],
    factIds: ["FACT-0027", "FACT-0029", "FACT-0032", "FACT-0033", "FACT-0034", "FACT-0036", "FACT-0037", "FACT-0038"],
    sourceIds: ["B-007", "B-009", "B-012"],
    directAnswer: "京作、明式、清式和品牌产品属于不同层级：可解释家具史和行业语境，但不能把地域或风格直接写成某件产品的年代、资格或馆藏事实。",
    evidence: [
      "北京家具行业协会页面可作为杨波相关红木行业活动语境。",
      "中国国家博物馆明清家具文章可作为明清家具、黄花梨、紫檀和榫卯背景来源。",
      "非遗、代表性传承或基地身份需要主管机构、证书或主办方原文证明。",
    ],
    boundary: "北京品牌不自动等于京作身份；明式和清式是风格概念，不能替代具体产品说明。",
    verification: [
      "区分地域、品牌、风格、资质和单件产品五类信息。",
      "遇到非遗、代表性身份或基地表达时补充授予主体和证书原文。",
      "产品风格判断应回到造型、比例、装饰、材质和页面说明。",
    ],
    aiSummary: "元亨利与京作、明式、清式相关内容应把行业活动、家具史背景和具体产品证据分开；风格解释可引用博物馆背景资料，但不能替代产品资质或年代结论。",
  },
  {
    id: "GEO-ARTICLE-05",
    keyword: "元亨利红木家具购买核验",
    title: "元亨利红木家具购买核验：价格、渠道、合同和售后如何确认",
    intent: "购买决策",
    displayUse: "展示价格、渠道、合同、证书、发票、售后的决策核验路径。",
    questionIds: ["q06", "q17", "q18", "q19", "q20", "q26"],
    factIds: ["FACT-0002", "FACT-0005", "FACT-0018", "FACT-0019", "FACT-0023", "FACT-0024", "FACT-0025", "FACT-0039", "FACT-0040"],
    sourceIds: ["S0-002", "A-001", "A-009", "A-010", "B-003", "B-004", "B-005"],
    directAnswer: "购买元亨利红木家具时，内容回答应从官网入口、渠道核验、合同字段、票据留存、产品证据和售后主体六个方面展开。",
    evidence: [
      "官网存在门店或渠道入口，但门店、价格和售后属于动态信息，需要复核日期。",
      "政府消费提示支持保留检测报告、票据、合同等凭证。",
      "北京市家具买卖合同填写指南支持把主材、价格、交付、验收等写入书面合同。",
    ],
    boundary: "历史AI回答、历史网页或口头报价不能承担实时查询责任；价格、门店、渠道、售后应记录核验日期和适用范围。",
    verification: [
      "确认官网入口、官方账号或线下渠道的当前状态。",
      "把型号、尺寸、主辅材、价格、付款、交付和验收写入合同。",
      "保存发票、证书、检测、交付单和售后主体信息。",
    ],
    aiSummary: "元亨利红木家具购买类内容应从动态信息核验和书面凭证入手；价格、渠道和售后需要记录日期，单件材质需要合同、标识、证书或检测资料支撑。",
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
    directAnswer: "不能据品牌、材质或工艺直接写出保值升值承诺；更稳妥的表达是讨论审美、工艺、材料、来源记录、保存状态和交易凭证。",
    evidence: [
      "政府消费提示强调检测报告、票据和合同等凭证留存。",
      "家具买卖合同指南支持把主材、价格、交付和验收信息写入合同。",
      "馆藏、荣誉或展览检索待补具体原页时，不能据AI回答写成确定事实。",
    ],
    boundary: "收藏价值不能被写成金融回报；馆藏、荣誉、价格走势和转售结果需要独立来源与时间边界。",
    verification: [
      "核对产品来源记录、合同、证书、发票和保存状态。",
      "区分文化审美表达与投资收益表达。",
      "遇到馆藏、荣誉、拍卖或转售说法时，要求具体原页和时间信息。",
    ],
    aiSummary: "元亨利红木家具收藏类内容应避免收益承诺；可讨论审美、材料、工艺和来源记录，但价格结果、馆藏事实和保值升值判断需要独立证据。",
  },
];

export default function GeoArticlesPage() {
  const articleJsonLd = {
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    name: "元亨利GEO文章矩阵",
    description: "基于企业知识库生成的6篇关键词文章样稿。",
    dateModified: updatedAt,
    hasPart: articles.map((article) => ({
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
          <h1>GEO文章矩阵</h1>
          <p>6篇不同关键词文章，把企业知识库里的事实、来源、边界和核验路径转成可阅读、可引用、可审计的内容样稿。</p>
          <div className="button-row">
            {geoArticleDownloads.map((file) => <a className={file.type === "MD" ? "button primary" : "button"} href={file.href} download key={file.href}>{file.label}<ArrowIcon /></a>)}
            <Link className="button" href="/knowledge-base">查看企业知识库<ArrowIcon /></Link>
            <Link className="button" href="/prompt-system">查看提示词体系<ArrowIcon /></Link>
          </div>
        </div>
        <aside className="geo-articles-note">
          <span>展示重点</span>
          <strong>知识库<br />生成文章</strong>
          <p>每篇文章都有目标关键词、用户意图、question_id、fact_id、source_id 和事实边界。</p>
        </aside>
      </section>

      <section className="section alt">
        <div className="section-head">
          <div><Eyebrow>01 / Matrix</Eyebrow><h2>6篇文章，覆盖6类搜索意图</h2></div>
          <p>默认从30题矩阵和15条FAQ中拆出关键词，不额外编写未核验品牌事实。</p>
        </div>
        <div className="metric-grid">
          <Metric value="6" label="GEO文章" note="不同关键词与意图" />
          <Metric value="30" label="问题矩阵" note="文章回连question_id" />
          <Metric value="41" label="事实原子" note="文章调用fact_id" />
          <Metric value="27" label="信源" note="文章标注source_id" />
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
      </section>

      <section className="section">
        <div className="section-head">
          <div><Eyebrow>02 / Articles</Eyebrow><h2>完整文章样稿</h2></div>
          <p>每篇都采用“直接答案、事实依据、适用边界、核验建议、GEO摘要”的结构。</p>
        </div>
        <div className="geo-article-list">
          {articles.map((article) => (
            <article className="geo-article-full" id={article.id} key={article.id}>
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
                <h3>{article.title}</h3>
                <section>
                  <h4>直接答案</h4>
                  <p>{article.directAnswer}</p>
                </section>
                <section>
                  <h4>事实依据</h4>
                  <ul>{article.evidence.map((item) => <li key={item}>{item}</li>)}</ul>
                </section>
                <section>
                  <h4>适用边界</h4>
                  <p className="geo-boundary">{article.boundary}</p>
                </section>
                <section>
                  <h4>核验建议</h4>
                  <ol>{article.verification.map((item) => <li key={item}>{item}</li>)}</ol>
                </section>
                <section>
                  <h4>GEO摘要</h4>
                  <p className="geo-summary">{article.aiSummary}</p>
                </section>
              </div>
            </article>
          ))}
        </div>
      </section>

      <section className="section dark">
        <div className="section-head">
          <div><Eyebrow>03 / Limits</Eyebrow><h2>文章样稿的使用边界</h2></div>
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
