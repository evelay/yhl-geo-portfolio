import Link from "next/link";
import type { Metadata } from "next";
import { ArrowIcon, Eyebrow, SiteShell, VisibleBreadcrumbs } from "../components";
import { governanceAssets, siteAssetPath, siteUrl } from "../data";

export const metadata: Metadata = {
  title: "内容策略",
  description: "内容策略：将五平台回答诊断中的品牌身份、材质关系、京作与风格、购买核验和价值判断风险转化为品牌事实、关键问题 FAQ、购买核验指南和结构化内容页面。",
  alternates: { canonical: `${siteUrl}/content-governance/` },
};

const schema = {
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "WebPage",
      "@id": `${siteUrl}/content-governance/#webpage`,
      url: `${siteUrl}/content-governance/`,
      name: "内容策略",
      description: "把回答诊断转化为品牌事实、关键问题 FAQ、购买核验指南和结构化内容页面。",
      inLanguage: "zh-CN",
    },
    {
      "@type": "BreadcrumbList",
      itemListElement: [
        { "@type": "ListItem", position: 1, name: "首页", item: `${siteUrl}/` },
        { "@type": "ListItem", position: 2, name: "内容策略", item: `${siteUrl}/content-governance/` },
      ],
    },
  ],
};

const schemaJson = JSON.stringify(schema).replace(/</g, "\\u003c");

const priorities = [
  {
    title: "品牌身份",
    body: "品牌、企业主体、同名对象、官网来源和成立时间容易被混为一谈。",
  },
  {
    title: "产品与文化边界",
    body: "材料、工艺、地域和风格概念容易被扩大为品牌身份或全部产品事实。",
  },
  {
    title: "购买与价值判断",
    body: "品牌声誉容易替代合同、材质、检测和单件产品核验，并被进一步推导为回购、保值或投资价值。",
  },
  {
    title: "来源与内容结构",
    body: "回答中虽然经常出现链接，但来源和主要结论之间不一定存在直接对应关系。",
  },
];

const strategySections = [
  {
    title: "品牌身份",
    problem: "品牌、企业主体、同名对象和官网来源容易被混用。",
    strategy: "分开整理品牌名称、企业主体、时间口径和官方信息核验。",
    formed: "品牌事实页、同名主体消歧、品牌身份相关FAQ。",
    href: "/facts",
    pageName: "品牌事实页",
    image: "/screenshots/page-previews/facts.png",
  },
  {
    title: "产品与文化边界",
    problem: "材料、工艺、地域和风格概念容易被扩大为品牌身份或全部产品事实。",
    strategy: "区分行业通用知识、品牌公开表达和单件产品证据。",
    formed: "材质与文化边界页、京作与明清说明、材质类FAQ。",
    href: "/materials",
    pageName: "材质与文化边界页",
    image: "/screenshots/page-previews/materials.png",
  },
  {
    title: "购买与价值判断",
    problem: "品牌声誉容易被直接推导为回购、保值或投资价值。",
    strategy: "把判断拆回合同主体、材质信息、产品证据和售后承诺。",
    formed: "购买核验指南、购买类FAQ、收藏与投资边界说明。",
    href: "/buying-guide",
    pageName: "购买核验指南",
    image: "/screenshots/page-previews/buying-guide.png",
  },
  {
    title: "来源与内容结构",
    problem: "回答中虽然经常出现链接，但来源和主要结论之间不一定直接对应。",
    strategy: "记录事实内容、主要来源、适用范围、相关问题和不可外推结论。",
    formed: "品牌事实库（公开资料版）、事实与来源关联、FAQ和页面内链。",
    href: "/knowledge-base",
    pageName: "品牌事实库（公开资料版）",
    image: "/screenshots/page-previews/knowledge-base.png",
  },
];

const sourceRules = [
  "权威第三方资料：用于企业主体、标准、正式名录和行业基础事实",
  "品牌公开资料：用于品牌自述、活动和产品表达，但不自动等同独立验证",
  "单件产品资料：用于判断具体产品，不能扩大为品牌全部产品结论",
];

const faqQuestions = [
  "元亨利是什么品牌？",
  "如何区分元亨利品牌和同名对象？",
  "元亨利与京作红木家具有什么关系？",
  "白酸枝家具和元亨利可能有哪些关联？",
  "购买红木家具时需要核验哪些信息？",
  "是否可以直接判断具有收藏或投资价值？",
];

const pageTechItems = [
  "信息架构",
  "页面内链",
  "结构化数据",
  "基础技术设置",
];

export default function ContentGovernancePage() {
  return (
    <SiteShell>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: schemaJson }} />
      <section className="portfolio-page-hero">
        <Eyebrow>内容策略</Eyebrow>
        <VisibleBreadcrumbs items={[{ label: "首页", href: "/" }, { label: "内容策略" }]} />
        <h1>内容策略</h1>
        <p className="lede">五个平台的回答诊断显示，元亨利相关信息风险主要集中在品牌身份、材质关系、京作与风格、购买核验和价值判断等问题。</p>
        <p className="lede">针对这些问题，本项目将分散的公开资料重新组织为品牌事实、关键问题 FAQ、购买核验指南和结构化内容页面，使重要结论能够对应来源、适用范围和信息边界。</p>
        <div className="button-row">
          <Link className="button primary" href="/facts">查看品牌事实<ArrowIcon /></Link>
          <Link className="button" href="/faq">查看关键问题 FAQ<ArrowIcon /></Link>
        </div>
      </section>

      <div className="portfolio-page">
        <section className="content-section">
          <h2>优先解决的四类问题</h2>
          <div className="strategy-module-grid priority-module-grid">
            {priorities.map((item) => <article className="strategy-module-card" key={item.title}><h3>{item.title}</h3><p>{item.body}</p></article>)}
          </div>
        </section>

        {strategySections.map((section) => (
          <section className="content-section" key={section.title}>
            <h2>{section.title}</h2>
            <div className="strategy-visual-card">
              <div className="strategy-flow-column" aria-label={`${section.title}内容策略流程`}>
                <article>
                  <span>诊断中发现的问题</span>
                  <p>{section.problem}</p>
                </article>
                <article>
                  <span>对应内容策略</span>
                  <p>{section.strategy}</p>
                </article>
                <article>
                  <span>已形成的内容页面</span>
                  <p>{section.formed}</p>
                </article>
              </div>
              <Link className="strategy-preview-card" href={section.href}>
                <div className="page-preview-frame">
                  <img src={siteAssetPath(section.image)} alt={`${section.pageName}缩略图`} loading="lazy" />
                </div>
                <h3>{section.pageName}</h3>
                <span>查看页面<ArrowIcon /></span>
              </Link>
            </div>
            {section.title === "来源与内容结构" && (
              <>
                <div className="section-subhead"><h3>来源使用原则</h3></div>
                <div className="source-level-grid">
                  {sourceRules.map((item, index) => <article key={item}><span>{String(index + 1).padStart(2, "0")}</span><p>{item}</p></article>)}
                </div>
              </>
            )}
          </section>
        ))}

        <section className="content-section">
          <h2>关键问题 FAQ 如何产生</h2>
          <p>FAQ并非根据搜索量排名生成。</p>
          <p>首批问题来自：五个平台测试中反复出现的对象和事实问题；材质、京作、购买和价值判断中的高风险问题；能够通过公开资料形成相对稳健回答的问题。</p>
          <p>经过事实核验和内容边界整理后，形成首批13条关键问题 FAQ。</p>
          <div className="text-list two-col">
            {["直接回答", "信息边界", "主要来源", "相关内容"].map((item) => <p key={item}>{item}</p>)}
          </div>
          <div className="section-subhead"><h3>代表问题</h3></div>
          <div className="tag-grid">
            {faqQuestions.map((item) => <span key={item}>{item}</span>)}
          </div>
        </section>

        <section className="content-section">
          <h2>品牌事实库（公开资料版）</h2>
          <p>每条记录包括：事实主题、事实内容、主要来源、信息边界、相关问题、更新时间。</p>
          <div className="fact-example-card">
            <p><b>事实主题：</b>品牌创办时间</p>
            <p><b>可核验结论：</b>行业协会公开资料使用“1996年创办”的表述。</p>
            <p><b>信息边界：</b>品牌创办时间不等同于企业工商登记日期，不应将两个时间口径直接混为一谈。</p>
            <p><b>可支持的问题：</b>元亨利创办于哪一年？为什么不同资料中的时间不一致？品牌和企业主体应如何表述？</p>
          </div>
          <div className="content-chain-flow" aria-label="品牌事实库到FAQ和页面的流程">
            {["公开来源", "可核验事实", "关键问题 FAQ", "品牌与购买内容页面"].map((item, index) => (
              <article key={item}>
                <span>{String(index + 1).padStart(2, "0")}</span>
                <b>{item}</b>
              </article>
            ))}
          </div>
        </section>

        <section className="content-section">
          <h2>页面与技术支持</h2>
          <div className="tag-grid">{pageTechItems.map((item) => <span key={item}>{item}</span>)}</div>
          <div className="content-stack-flow" aria-label="内容事实层到技术表达层">
            {["内容事实层", "页面组织层", "技术表达层"].map((item, index) => (
              <article key={item}>
                <span>{String(index + 1).padStart(2, "0")}</span>
                <b>{item}</b>
              </article>
            ))}
          </div>
        </section>

        <section className="content-section">
          <h2>内容资产入口</h2>
          <div className="asset-directory">
            {governanceAssets.map((asset) => (
              <Link href={asset.href} className="asset-directory-card" key={asset.href}>
                <span>{asset.group}</span>
                <h3>{asset.title}</h3>
                <p>{asset.body}</p>
                <b>打开资产<ArrowIcon /></b>
              </Link>
            ))}
          </div>
        </section>
      </div>
    </SiteShell>
  );
}
