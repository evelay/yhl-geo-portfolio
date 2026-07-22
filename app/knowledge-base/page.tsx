import type { Metadata } from "next";
import Link from "next/link";
import { ArrowIcon, Eyebrow, SiteShell, VisibleBreadcrumbs } from "../components";
import { siteUrl } from "../data";
import knowledgeBase from "./knowledge-base-public.json";

export const metadata: Metadata = {
  title: "品牌事实库（公开资料版）",
  description: "品牌事实库（公开资料版）：展示如何将分散资料整理成可核验、可关联、可复用的事实结构。",
  alternates: { canonical: `${siteUrl}/knowledge-base/` },
};

type PublicFact = {
  id: string;
  entityName: string;
  evidenceLevel: string;
  type: string;
  statement: string;
  boundary: string;
};

const kb = knowledgeBase as {
  updatedAt: string;
  summary: Record<string, number>;
  facts: PublicFact[];
  queryExamples: { id: string; title: string; answer: string }[];
};

const schema = {
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "WebPage",
      "@id": `${siteUrl}/knowledge-base/#webpage`,
      url: `${siteUrl}/knowledge-base/`,
      name: "品牌事实库（公开资料版）",
      description: "展示如何把分散资料整理成可核验、可关联、可复用的事实结构。",
      inLanguage: "zh-CN",
    },
    {
      "@type": "BreadcrumbList",
      itemListElement: [
        { "@type": "ListItem", position: 1, name: "首页", item: `${siteUrl}/` },
        { "@type": "ListItem", position: 2, name: "内容策略", item: `${siteUrl}/content-governance/` },
        { "@type": "ListItem", position: 3, name: "品牌事实库（公开资料版）", item: `${siteUrl}/knowledge-base/` },
      ],
    },
  ],
};

const schemaJson = JSON.stringify(schema).replace(/</g, "\\u003c");

const structureGroups = [
  {
    title: "品牌主体",
    body: "记录品牌、企业主体、同名对象和业务语境，先解决“说的是谁”。",
  },
  {
    title: "事实与来源",
    body: "把可写事实与来源证明范围放在一起，避免结论脱离证据。",
  },
  {
    title: "产品证据",
    body: "把材料、合同、证书、检测和交付信息留给单件核验。",
  },
  {
    title: "动态信息",
    body: "门店、价格、库存和售后等信息必须带日期重新确认。",
  },
  {
    title: "FAQ关联",
    body: "让高频问题能直接找到可用事实、边界和来源类型。",
  },
  {
    title: "版本审核",
    body: "保留公开内容的审核状态和更新时间，避免旧信息继续被引用。",
  },
];

const sourceCategories = [
  {
    title: "权威第三方事实",
    count: 17,
    body: "政府、国家标准、协会、主流媒体、博物馆和研究机构等来源。",
  },
  {
    title: "品牌公开自述",
    count: 14,
    body: "官网或官方账号公开表述，只证明品牌如何自述，不自动升级为第三方认证。",
  },
  {
    title: "单件产品证据",
    count: 5,
    body: "合同、标识、证书、检测、发票、交付和售后文件。",
  },
];

function evidenceCategory(level: string) {
  if (level === "L1") return "权威第三方事实";
  if (level === "L2") return "品牌公开自述";
  return "单件产品证据";
}

export default function KnowledgeBasePage() {
  const factSamples = kb.facts.filter((fact) => ["FACT-0001", "FACT-0021", "FACT-0039", "FACT-0040", "FACT-0041"].includes(fact.id));

  return (
    <SiteShell>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: schemaJson }} />
      <section className="kb-hero">
        <div>
          <Eyebrow>结构化内容资产</Eyebrow>
          <VisibleBreadcrumbs items={[{ label: "首页", href: "/" }, { label: "内容策略", href: "/content-governance" }, { label: "品牌事实库（公开资料版）" }]} />
          <h1>品牌事实库（公开资料版）</h1>
          <p>该结构用于解决品牌事实分散、来源与结论脱节、FAQ无法稳定引用等问题。</p>
          <p>公开版保留可核验、可关联、可复用的事实结构，用于说明品牌事实如何被 FAQ 和内容页面调用。</p>
          <div className="button-row">
            <Link className="button primary" href="/content-governance">返回内容策略<ArrowIcon /></Link>
            <Link className="button" href="/faq">查看关键问题 FAQ<ArrowIcon /></Link>
          </div>
        </div>
        <aside className="kb-verdict">
          <span>解决的问题</span>
          <strong>能回答，<br />也要能核验</strong>
          <p>每条结论都应知道它来自哪里、能证明什么、不能外推到哪里。</p>
        </aside>
      </section>

      <section className="section alt">
        <div className="section-head">
          <div><Eyebrow>01 / 结构范围</Eyebrow><h2>从资料到事实结构</h2></div>
          <p>页面只展示公开层级的结构样例，不提供完整内部数据包。</p>
        </div>
        <div className="metric-grid">
          <div className="metric"><strong>{kb.summary.entities}</strong><span>品牌主体与对象</span><small>用于区分主体、业务和同名风险</small></div>
          <div className="metric"><strong>{kb.summary.facts}</strong><span>可核验事实</span><small>只展示可公开引用的事实样例</small></div>
          <div className="metric"><strong>{kb.summary.sources}</strong><span>公开来源</span><small>用于说明事实证明范围</small></div>
          <div className="metric"><strong>{kb.summary.faq}</strong><span>FAQ关联</span><small>把问题映射到事实与边界</small></div>
        </div>
      </section>

      <section className="section">
        <div className="section-head">
          <div><Eyebrow>02 / 知识结构</Eyebrow><h2>六类公开结构</h2></div>
          <p>公开表达保留可理解的结构，不展示后台结构或存储方式。</p>
        </div>
        <div className="kb-architecture public-kb-architecture">
          {structureGroups.map((item, index) => (
            <article key={item.title}>
              <span>{String(index + 1).padStart(2, "0")}</span>
              <b>{item.title}</b>
              <p>{item.body}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="section dark">
        <div className="section-head">
          <div><Eyebrow>03 / 来源类别</Eyebrow><h2>三类来源证明范围</h2></div>
          <p>来源类别用直观中文表达，不公开内部等级编号。</p>
        </div>
        <div className="kb-level-grid public-level-grid">
          {sourceCategories.map((item) => (
            <article key={item.title}>
              <h3>{item.title}</h3>
              <strong>{item.count}条</strong>
              <p>{item.body}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="section alt">
        <div className="section-head">
          <div><Eyebrow>04 / 问题关联</Eyebrow><h2>典型问题如何落到边界</h2></div>
          <p>这些样例说明：FAQ不是普通知识文章，而是诊断问题转化后的直接回答资产。</p>
        </div>
        <div className="kb-query-grid">
          {kb.queryExamples.map((item) => (
            <article key={item.id}>
              <span>典型问题</span>
              <h3>{item.title}</h3>
              <p>{item.answer}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="section">
        <div className="section-head">
          <div><Eyebrow>05 / 事实样例</Eyebrow><h2>可核验事实样例</h2></div>
          <p>这里展示少量样例，帮助理解“事实、来源类别、边界”如何同时出现。</p>
        </div>
        <div className="kb-fact-list public-fact-list">
          {factSamples.map((fact) => (
            <article key={fact.id}>
              <div><span>{evidenceCategory(fact.evidenceLevel)}</span><h3>{fact.type}</h3></div>
              <p>{fact.statement}</p>
              <small>边界：{fact.boundary}</small>
            </article>
          ))}
        </div>
      </section>
    </SiteShell>
  );
}
