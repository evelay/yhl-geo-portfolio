import Link from "next/link";
import type { Metadata } from "next";
import { ArrowIcon, Eyebrow, SiteShell } from "./components";
import { coreFindings, headlineMetrics, metricDisclaimers, projectFlow, siteUrl } from "./data";

export const metadata: Metadata = {
  title: { absolute: "元亨利红木家具 GEO 诊断与内容优化项目" },
  description: "元亨利红木家具 GEO 诊断与内容优化项目：五个平台同题测试、AI回答诊断、品牌事实、关键问题 FAQ和结构化内容页面。",
  alternates: { canonical: `${siteUrl}/` },
};

const homeSchema = {
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "WebSite",
      "@id": `${siteUrl}/#website`,
      url: `${siteUrl}/`,
      name: "元亨利红木家具 GEO 诊断与内容优化项目",
      description: "基于公开资料完成的独立 GEO 项目，展示 GEO 问题研究、AI 回答诊断、内容策略和页面优化方法。",
      inLanguage: "zh-CN",
    },
    {
      "@type": "WebPage",
      "@id": `${siteUrl}/#webpage`,
      url: `${siteUrl}/`,
      name: "元亨利红木家具 GEO 诊断与内容优化项目",
      description: "五个平台同题测试、AI回答诊断、品牌事实、关键问题 FAQ和结构化内容页面。",
      inLanguage: "zh-CN",
      isPartOf: {
        "@id": `${siteUrl}/#website`,
      },
    },
    {
      "@type": "BreadcrumbList",
      itemListElement: [
        { "@type": "ListItem", position: 1, name: "首页", item: `${siteUrl}/` },
      ],
    },
  ],
};

const homeSchemaJson = JSON.stringify(homeSchema).replace(/</g, "\\u003c");

const brandChoiceCards = [
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

const optimizationCards = [
  {
    title: "品牌身份与事实体系",
    body: "整理品牌、企业主体、同名对象、成立时间和官网来源之间的关系，明确哪些信息能够确认、哪些仍需谨慎表述。",
    href: "/facts",
    label: "查看品牌事实与主体消歧",
  },
  {
    title: "产品与文化边界",
    body: "区分行业知识、品牌公开表达和单件产品证据，避免将材质或文化概念直接扩大为品牌身份和全部产品事实。",
    href: "/materials",
    label: "查看材质与文化边界",
  },
  {
    title: "购买核验与价值判断",
    body: "将笼统品牌评价拆分为合同主体、材质名称、证书、检测、交付和售后等具体核验项目。",
    href: "/buying-guide",
    label: "查看购买核验指南",
  },
  {
    title: "结构化品牌事实库",
    body: "将品牌主体、可核验事实、主要来源、适用范围和相关问题关联起来，供 FAQ 和内容页面复用。",
    href: "/knowledge-base",
    label: "查看品牌事实库",
  },
];

const outputPreviews = [
  { title: "品牌事实页", href: "/facts", image: "/screenshots/page-previews/facts.png", body: "整理品牌、主体、来源和边界。" },
  { title: "关键问题 FAQ", href: "/faq", image: "/screenshots/page-previews/faq.png", body: "把诊断问题转化为直接回答。" },
  { title: "购买核验指南", href: "/buying-guide", image: "/screenshots/page-previews/buying-guide.png", body: "将购买建议落到具体核验项。" },
  { title: "AI搜索诊断页", href: "/experiment", image: "/screenshots/page-previews/experiment.png", body: "展示回答指标和风险分布。" },
];

const deepReadLinks = [
  { title: "项目案例", href: "/case-study", body: "了解项目背景、诊断方法、主要结果和优化方案。" },
  { title: "AI 搜索诊断", href: "/experiment", body: "查看五个平台的回答表现、风险分布和典型问题。" },
  { title: "内容策略", href: "/content-governance", body: "查看诊断结果如何转化为品牌事实、FAQ和购买核验内容。" },
];

export default function Home() {
  return (
    <SiteShell>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: homeSchemaJson }} />

      <section className="hero portfolio-home-hero">
        <div className="hero-grid">
          <div>
            <Eyebrow>独立 GEO 项目｜基于公开资料完成</Eyebrow>
            <h1 className="split-title"><span>元亨利红木家具</span> <span>GEO 诊断与<wbr />内容优化</span></h1>
            <p className="lede">围绕元亨利红木家具，我梳理了品牌识别、材质理解和购买判断中的关键问题，并在豆包、文心一言、通义千问、Kimi和腾讯元宝进行同题测试。诊断结果进一步转化为品牌事实页、关键问题 FAQ、购买核验指南和结构化内容页面。</p>
            <div className="button-row">
              <Link className="button primary" href="/case-study">查看项目案例<ArrowIcon /></Link>
              <Link className="button" href="/experiment">查看 AI 搜索诊断<ArrowIcon /></Link>
            </div>
          </div>
          <aside className="hero-note hero-flow-note" aria-label="项目流程">
            {["问题研究", "回答诊断", "内容优化", "后续复测"].map((item, index) => (
              <div key={item}>
                <span>{String(index + 1).padStart(2, "0")}</span>
                <b>{item}</b>
              </div>
            ))}
          </aside>
        </div>
      </section>

      <section className="section alt" id="why-redwood">
        <div className="section-head">
          <div><Eyebrow>01 / 项目背景</Eyebrow><h2>项目背景</h2></div>
          <p>红木家具属于高客单、低频决策、专业信息密集的品类。用户在了解和购买过程中，需要同时核验品牌主体、材质、工艺、合同、证书和售后等信息。公开资料分散、同名对象混杂和专业概念被放大，容易使AI回答出现对象混用、来源不清和判断越界。</p>
        </div>
        <div className="problem-grid three-card-grid">
          {brandChoiceCards.map((item, index) => (
            <article key={item.title}>
              <span>{String(index + 1).padStart(2, "0")}</span>
              <h3>{item.title}</h3>
              <p>{item.body}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="section" id="process">
        <div className="section-head">
          <div><Eyebrow>02 / 内容流程</Eyebrow><h2>从用户问题到内容优化</h2></div>
        </div>
        <div className="process-strip four-step-strip" aria-label="从用户问题研究到内容与页面优化的流程">
          {projectFlow.map((step, index) => (
            <div className="process-step" key={step}>
              <span>{String(index + 1).padStart(2, "0")}</span>
              <b>{step}</b>
              {index === 0 && <small>从品牌公开资料、红木家具购买决策和 AI 常见误答中整理问题。</small>}
              {index === 1 && <small>在豆包、文心一言、通义千问、Kimi和腾讯元宝使用同一组问题采集回答。</small>}
              {index === 2 && <small>检查品牌对象、事实准确性、来源支持和信息边界。</small>}
              {index === 3 && <small>将诊断结果转化为品牌事实、FAQ、购买指南、内容页面和结构化数据。</small>}
            </div>
          ))}
        </div>
      </section>

      <section className="section alt" id="coverage">
        <div className="section-head">
          <div><Eyebrow>03 / 诊断覆盖</Eyebrow><h2>本轮诊断覆盖</h2></div>
        </div>
        <div className="number-grid three-number-grid">
          {headlineMetrics.map((metric) => (
            <article className="number-card" key={metric.label}>
              <strong>{metric.value}</strong>
              <span>{metric.label}</span>
              <p>{metric.note}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="section" id="findings">
        <div className="section-head">
          <div><Eyebrow>04 / 诊断结果</Eyebrow><h2>主要诊断结果</h2></div>
        </div>
        <div className="finding-grid">
          {coreFindings.map((finding, index) => (
            <article className="finding-card" key={finding.title}>
              <span>{index === 0 ? "85/120" : index === 1 ? "96/120" : "73/120"}</span>
              <h3>{finding.title}</h3>
              <p>{finding.body}</p>
              {index === 2 && metricDisclaimers.map((item) => <small key={item}>{item}</small>)}
            </article>
          ))}
        </div>
      </section>

      <section className="section alt" id="optimization">
        <div className="section-head">
          <div><Eyebrow>05 / 落地内容</Eyebrow><h2>优化方案与落地内容</h2></div>
        </div>
        <div className="solution-grid two-by-two">
          {optimizationCards.map((item) => (
            <article key={item.title}>
              <h3>{item.title}</h3>
              <p>{item.body}</p>
              <Link href={item.href}>{item.label}<ArrowIcon /></Link>
            </article>
          ))}
        </div>
      </section>

      <section className="section" id="outputs">
        <div className="section-head">
          <div><Eyebrow>06 / 成果预览</Eyebrow><h2>成果预览</h2></div>
        </div>
        <div className="page-preview-grid">
          {outputPreviews.map((item) => (
            <Link className="page-preview-card" href={item.href} key={item.href}>
              <div className="page-preview-frame">
                <img src={item.image} alt={`${item.title}缩略图`} loading="lazy" />
              </div>
              <h3>{item.title}</h3>
              <p>{item.body}</p>
              <span>打开页面<ArrowIcon /></span>
            </Link>
          ))}
        </div>
      </section>

      <section className="section alt" id="deep-read">
        <div className="section-head">
          <div><Eyebrow>07 / 深入查看</Eyebrow><h2>深入查看</h2></div>
        </div>
        <div className="deep-read-grid">
          {deepReadLinks.map((item) => (
            <Link className="deep-read-card" href={item.href} key={item.href}>
              <h3>{item.title}</h3>
              <p>{item.body}</p>
              <span>打开页面<ArrowIcon /></span>
            </Link>
          ))}
        </div>
      </section>

      <section className="section alt" id="project-statement">
        <div className="independent-statement">
          <Eyebrow>08 / 项目声明</Eyebrow>
          <h2>项目声明</h2>
          <p>本项目基于公开资料独立完成，用于展示 GEO 问题研究、AI 回答诊断、内容策略和页面优化方法，非元亨利品牌官方网站或官方委托项目。</p>
        </div>
      </section>
    </SiteShell>
  );
}
