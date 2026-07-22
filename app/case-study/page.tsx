import Link from "next/link";
import type { Metadata } from "next";
import { ArrowIcon, Eyebrow, SiteShell, VisibleBreadcrumbs } from "../components";
import { siteUrl } from "../data";

export const metadata: Metadata = {
  title: "项目案例",
  description: "元亨利红木家具 GEO 诊断与内容优化项目案例：项目背景、目标、诊断方法、主要结果、代表案例、优化方案、技术实施、成果与边界。",
  alternates: { canonical: `${siteUrl}/case-study/` },
};

const schema = {
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "WebPage",
      "@id": `${siteUrl}/case-study/#webpage`,
      url: `${siteUrl}/case-study/`,
      name: "项目案例",
      description: "元亨利红木家具 GEO 诊断与内容优化项目案例。",
      inLanguage: "zh-CN",
    },
    {
      "@type": "CreativeWork",
      "@id": `${siteUrl}/case-study/#case-study`,
      name: "元亨利红木家具 GEO 诊断与内容优化",
      description: "基于公开资料完成的独立 GEO 项目，覆盖用户问题研究、五个平台同题测试、回答质量诊断和内容页面建设。",
      inLanguage: "zh-CN",
      isPartOf: {
        "@id": `${siteUrl}/case-study/#webpage`,
      },
    },
    {
      "@type": "BreadcrumbList",
      itemListElement: [
        { "@type": "ListItem", position: 1, name: "首页", item: `${siteUrl}/` },
        { "@type": "ListItem", position: 2, name: "项目案例", item: `${siteUrl}/case-study/` },
      ],
    },
  ],
};

const schemaJson = JSON.stringify(schema).replace(/</g, "\\u003c");

const backgroundRisks = [
  {
    title: "品牌对象混淆",
    body: "品牌、企业主体、同名对象和官网来源可能被混为一谈。",
  },
  {
    title: "专业概念被扩大解释",
    body: "材料、工艺、地域和风格概念可能被直接扩大为品牌身份或全部产品事实。",
  },
  {
    title: "购买判断缺少证据",
    body: "品牌声誉可能被直接推导为回购、保值或投资价值，忽略合同和单件产品核验。",
  },
];

const projectGoals = [
  "澄清品牌与企业主体的关系",
  "明确哪些公开事实具备来源支持",
  "识别材质、文化概念和购买判断中的信息边界",
  "将诊断结果转化为可检索、可引用、可更新的内容页面",
];

const questionRows = [
  ["品牌认知", "元亨利是什么品牌？", "对象识别与品牌定位"],
  ["主体核验", "企业主体与“元亨利红木家具”应如何表述？", "品牌、字号和企业关系"],
  ["材质边界", "白酸枝家具和元亨利可能有哪些关联？", "是否扩大为全量产品事实"],
  ["文化概念", "元亨利与京作红木家具有什么关系？", "是否无依据认定身份或资质"],
  ["购买决策", "评估元亨利时应关注哪些因素？", "是否落到合同和单件核验"],
  ["价值判断", "是否具有收藏或投资价值？", "是否谨慎处理升值结论"],
];

const resultCards = [
  {
    title: "品牌出现率较高，但对象识别仍有偏差",
    body: "120条回答中，85条明确提及元亨利。部分回答仍然混淆品牌、企业主体和同名对象，其中4条回答将问题转向《周易》中的“元亨利贞”。",
  },
  {
    title: "回答中经常出现链接，但来源未必支持结论",
    body: "96条回答显示可见链接。部分链接只能支持局部信息，或来自聚合、转载和弱相关页面，无法直接支撑品牌身份、行业地位、馆藏和价值判断。",
  },
  {
    title: "风险主要集中在身份、材质和购买判断",
    body: "较突出风险包括：将元亨利直接认定为京作或非遗代表；将紫檀、白酸枝等材料话题扩大为长期品牌事实；将历史宣传或单件产品信息扩大为全量产品结论；对回购、保值、升值和投资价值作出确定性判断；将第三方页面直接认定为官网或官方渠道。",
  },
];

const caseCards = [
  {
    title: "对象识别错误",
    body: "部分回答把品牌问题理解为“元亨利贞”，转向《周易》、乾卦或古文训诂，说明名称消歧信息不足。",
    action: "建设品牌主体和同名对象消歧内容。",
  },
  {
    title: "京作与身份资质被过度推断",
    body: "部分回答直接使用“京作代表”“非遗传承单位”“故宫指定合作”等表述，但缺少相应权威公开证据。",
    action: "将地域、风格、工艺和正式资质分开说明。",
  },
  {
    title: "材质和价值判断被扩大",
    body: "部分回答将材料线索、品牌宣传或单件产品信息扩大为品牌长期经营事实，并进一步推导回购、保值或投资价值。",
    action: "建设材质边界和购买核验内容，要求判断回到具体产品与合同证据。",
  },
];

const solutionCards = [
  {
    title: "品牌身份与事实体系",
    body: "将品牌、企业主体、同名对象、成立时间和官网来源分开整理，标注主要来源及不可外推的边界。",
    formed: "品牌事实页、同名主体消歧、品牌身份相关FAQ。",
  },
  {
    title: "产品与文化边界",
    body: "区分行业通用知识、品牌公开表达和单件产品证据，避免将材质或文化概念直接扩大为身份和全量产品事实。",
    formed: "材质边界页、京作与明清说明、材质和文化相关FAQ。",
  },
  {
    title: "购买核验与价值判断",
    body: "将笼统评价拆分为合同主体、材质名称、证书、检测、交付、售后和书面承诺等具体核验事项。",
    formed: "购买核验指南、购买类FAQ、收藏与投资风险提示。",
  },
  {
    title: "结构化品牌事实库",
    body: "将品牌主体、公开事实、主要来源、适用范围和相关问题进行关联，支持FAQ和内容页面调用与更新。",
    formed: "可核验事实记录、事实与来源关联、问题与事实关联、页面内链与Schema结构。",
  },
];

const technologyItems = [
  "重新组织网站信息架构",
  "建立项目案例、诊断、内容策略和研究方法页面",
  "完善页面标题、H1和可见面包屑",
  "配置canonical和sitemap",
  "添加WebSite、WebPage和BreadcrumbList Schema",
  "建立品牌事实、FAQ和购买指南之间的内部链接",
  "检查页面可抓取性和移动端显示",
];

const outcomes = [
  {
    title: "研究与诊断",
    body: "一套品牌用户问题研究方法、24个核心问题、五个平台120条回答、一套人工判断与抽样复核流程。",
  },
  {
    title: "内容建设",
    body: "品牌事实与主体消歧、首批13条关键问题 FAQ、材质及文化边界内容、购买核验指南、结构化品牌事实库。",
  },
  {
    title: "页面与技术建设",
    body: "网站信息架构、内容页面与内部链接、canonical、sitemap和Schema、后续同题复测设计。",
  },
];

const canExplain = [
  "品牌相关回答中存在可识别的事实、来源和边界风险",
  "风险可以按照问题类型进行拆分和治理",
  "诊断结果能够转化为具体内容和页面方案",
  "该流程可以复用于其他专业信息密集型品牌",
];

const cannotExplain = [
  "网站优化已经提高AI提及率或准确率",
  "回答变化一定由网站内容造成",
  "某个平台整体优于其他平台",
  "当前结果能够代表长期稳定表现",
];

export default function CaseStudyPage() {
  return (
    <SiteShell>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: schemaJson }} />
      <section className="portfolio-page-hero">
        <Eyebrow>独立 GEO 项目</Eyebrow>
        <VisibleBreadcrumbs items={[{ label: "首页", href: "/" }, { label: "项目案例" }]} />
        <h1 className="split-title"><span>元亨利红木家具</span> <span>GEO 诊断与<wbr />内容优化</span></h1>
        <p className="lede">围绕元亨利红木家具，我从用户问题出发，在五个AI平台上进行同题测试，诊断品牌识别、材质理解与购买判断中的回答问题，并将结果转化为品牌事实、关键问题 FAQ、购买核验指南和结构化内容页面。</p>
        <div className="button-row">
          <Link className="button primary" href="/experiment">查看诊断数据<ArrowIcon /></Link>
          <Link className="button" href="/content-governance">查看内容策略<ArrowIcon /></Link>
        </div>
      </section>

      <div className="portfolio-page">
        <section className="content-section">
          <h2>项目背景</h2>
          <p>在红木家具相关问答中，用户往往同时关心品牌主体、材质名称、工艺风格、合同证书和售后信息；这些信息如果被AI混合处理，就会影响后续比较和购买判断。</p>
          <div className="problem-grid three-card-grid">
            {backgroundRisks.map((item, index) => (
              <article key={item.title}>
                <span>{String(index + 1).padStart(2, "0")}</span>
                <h3>{item.title}</h3>
                <p>{item.body}</p>
              </article>
            ))}
          </div>
        </section>

        <section className="content-section">
          <h2>项目目标</h2>
          <div className="process-list compact-process">
            {projectGoals.map((item, index) => <p key={item}><span>{index + 1}</span>{item}</p>)}
          </div>
        </section>

        <section className="content-section" id="questions">
          <h2>诊断方法</h2>
          <h3>问题来源</h3>
          <div className="text-list">
            {[
              "公开资料中的信息歧义：企业主体、成立时间、官网来源、同名对象、行业身份和公开荣誉",
              "用户认知与购买决策：材质、风格、合同、证书、检测、售后、品牌比较和价值判断",
              "AI 回答中的常见风险：对象错配、来源不支撑、强品牌背书、材料关系扩大和投资结论过度",
            ].map((item) => <p key={item}>{item}</p>)}
          </div>
          <p>候选问题经过合并、去重和范围调整后，最终选出24个核心问题。</p>
          <h3>为什么选择这24个问题</h3>
          <div className="tag-grid">
            {["与品牌理解或购买决策直接相关", "容易发生事实错误或信息边界混淆", "可以在不同平台使用相同方式提问", "适合在后续继续进行同题复测"].map((item) => <span key={item}>{item}</span>)}
          </div>
          <h3>代表问题</h3>
          <div className="table-scroll">
            <table className="data-table">
              <thead><tr><th>问题类别</th><th>代表问题</th><th>观察重点</th></tr></thead>
              <tbody>{questionRows.map(([category, question, focus]) => <tr key={category}><td>{category}</td><td>{question}</td><td>{focus}</td></tr>)}</tbody>
            </table>
          </div>
          <div className="button-row table-action-row">
            <Link className="button" href="/methodology#question-design">查看完整24个测试问题<ArrowIcon /></Link>
          </div>
        </section>

        <section className="content-section">
          <h2>五个 AI 平台同题测试</h2>
          <p>相同的24个问题分别提交至豆包、文心一言、通义千问、Kimi和腾讯元宝，共保存120条完整回答，并同步记录页面中可见的来源链接。</p>
          <div className="text-list two-col">
            {[
              "同一问题在不同平台中的回答差异",
              "多个平台反复出现的共同风险",
              "某些错误是否集中于特定问题类型",
              "后续复测能否沿用相同问题和判断口径",
            ].map((item) => <p key={item}>{item}</p>)}
          </div>
          <h3>回答如何判断</h3>
          <div className="tag-grid">
            {["品牌对象是否正确", "核心事实是否稳健", "回答是否覆盖关键内容", "来源是否能够支持主要结论", "品牌、材料、产品和文化概念是否得到区分", "推荐和购买判断是否保持谨慎", "是否存在明显的信息风险"].map((item) => <span key={item}>{item}</span>)}
          </div>
        </section>

        <section className="content-section">
          <h2>主要诊断结果</h2>
          <div className="finding-grid">
            {resultCards.map((item) => <article className="finding-card" key={item.title}><h3>{item.title}</h3><p>{item.body}</p></article>)}
          </div>
        </section>

        <section className="content-section">
          <h2>三个代表案例</h2>
          <div className="case-grid">
            {caseCards.map((item) => (
              <article key={item.title}>
                <h3>{item.title}</h3>
                <p>{item.body}</p>
                <small><b>对应优化：</b>{item.action}</small>
              </article>
            ))}
          </div>
        </section>

        <section className="content-section">
          <h2>优化方案与落地内容</h2>
          <div className="solution-grid two-by-two">
            {solutionCards.map((item) => (
              <article key={item.title}>
                <h3>{item.title}</h3>
                <p>{item.body}</p>
                <small>形成：{item.formed}</small>
              </article>
            ))}
          </div>
        </section>

        <section className="content-section">
          <h2>网站与技术实施</h2>
          <div className="text-list two-col">
            {technologyItems.map((item) => <p key={item}>{item}</p>)}
          </div>
        </section>

        <section className="content-section">
          <h2>项目成果</h2>
          <div className="compact-grid">
            {outcomes.map((item) => <p key={item.title}><b>{item.title}</b><br />{item.body}</p>)}
          </div>
        </section>

        <section className="content-section">
          <h2>项目边界与下一步</h2>
          <div className="section-subhead">
            <h3>当前结果能够说明</h3>
          </div>
          <div className="text-list two-col">{canExplain.map((item) => <p key={item}>{item}</p>)}</div>
          <div className="section-subhead">
            <h3>当前结果不能说明</h3>
          </div>
          <div className="text-list two-col">{cannotExplain.map((item) => <p key={item}>{item}</p>)}</div>
          <div className="section-subhead">
            <h3>下一步验证</h3>
            <p>后续计划继续使用同一24个问题、同一五个平台和相同判断口径进行复测，同时记录测试日期、联网模式和平台变化，观察内容更新后的回答差异。</p>
          </div>
        </section>

        <section className="page-cta">
          <Link className="button primary" href="/experiment">查看诊断数据<ArrowIcon /></Link>
          <Link className="button" href="/content-governance">查看内容策略<ArrowIcon /></Link>
          <Link className="button" href="/methodology">查看研究方法<ArrowIcon /></Link>
        </section>
      </div>
    </SiteShell>
  );
}
