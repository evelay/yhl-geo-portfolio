import type { Metadata } from "next";
import Link from "next/link";
import { ArrowIcon, Eyebrow, Metric, SiteShell, VisibleBreadcrumbs } from "../components";
import { siteUrl, updatedAt } from "../data";

export const metadata: Metadata = {
  title: "GEO文章样稿审核状态",
  description: "元亨利 GEO 作品集文章样稿的公开审核状态页：示范稿、非官方内容，未审核正文暂不公开。",
  alternates: { canonical: `${siteUrl}/geo-articles/` },
};

const articleReviews = [
  {
    id: "GEO-MAIN-ARTICLE",
    keyword: "红木家具",
    title: "元亨利红木家具企业介绍：基于公开资料的GEO内容样稿",
    purpose: "企业介绍与品牌认知示范稿，验证公开知识库如何组织企业基础信息、产品语境和购买核验边界。",
    reviewStatus: "暂缓公开完整正文：缺少文章级公开发布审核记录。",
  },
  {
    id: "GEO-ARTICLE-01",
    keyword: "元亨利红木家具是什么品牌",
    title: "企业基础信息与来源边界",
    purpose: "展示品牌基础信息、主体核验、官网线索与品牌事实边界。",
    reviewStatus: "暂缓公开完整正文：需完成来源、事实边界和非官方身份审核。",
  },
  {
    id: "GEO-ARTICLE-02",
    keyword: "元亨利同名主体怎么区分",
    title: "企业内容发布前的实体识别",
    purpose: "展示同名消歧、主体识别和避免 AI 混淆的处理方式。",
    reviewStatus: "暂缓公开完整正文：需完成文章级发布审核。",
  },
  {
    id: "GEO-ARTICLE-03",
    keyword: "元亨利红木家具材质",
    title: "从红木标准到单件证据",
    purpose: "展示材质术语、国家标准、品牌公开资料和单件证据的分层关系。",
    reviewStatus: "暂缓公开完整正文：需确认所有来源与单件证据边界。",
  },
  {
    id: "GEO-ARTICLE-04",
    keyword: "元亨利京作家具与明清风格",
    title: "行业语境、风格概念与产品资料",
    purpose: "展示京作、明式、清式、品牌产品之间的表达边界。",
    reviewStatus: "暂缓公开完整正文：包含需进一步复核的事实链路。",
  },
  {
    id: "GEO-ARTICLE-05",
    keyword: "元亨利红木家具购买核验",
    title: "合同、票据、证书与售后主体",
    purpose: "展示价格、渠道、合同、证书、发票和售后的决策核验路径。",
    reviewStatus: "暂缓公开完整正文：需完成人工发布检查。",
  },
  {
    id: "GEO-ARTICLE-06",
    keyword: "元亨利红木家具保值升值吗",
    title: "收藏表达的证据边界",
    purpose: "展示收藏价值、投资化表达和风险边界控制能力。",
    reviewStatus: "暂缓公开完整正文：涉及高风险收藏表达，需单独审核。",
  },
];

const schema = {
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "WebPage",
      "@id": `${siteUrl}/geo-articles/#webpage`,
      url: `${siteUrl}/geo-articles/`,
      name: "GEO文章样稿审核状态",
      description: "元亨利 GEO 作品集文章样稿的公开审核状态页；示范稿、非官方内容，未审核正文暂不公开。",
      inLanguage: "zh-CN",
      isPartOf: {
        "@id": `${siteUrl}/content-governance/#webpage`,
      },
      hasPart: articleReviews.map((article) => ({
        "@type": "CreativeWork",
        name: article.title,
        keywords: article.keyword,
        creativeWorkStatus: article.reviewStatus,
      })),
      dateModified: updatedAt,
    },
    {
      "@type": "BreadcrumbList",
      itemListElement: [
        { "@type": "ListItem", position: 1, name: "首页", item: `${siteUrl}/` },
        { "@type": "ListItem", position: 2, name: "内容策略", item: `${siteUrl}/content-governance/` },
        { "@type": "ListItem", position: 3, name: "GEO文章样稿审核状态", item: `${siteUrl}/geo-articles/` },
      ],
    },
  ],
};

const schemaJson = JSON.stringify(schema).replace(/</g, "\\u003c");

export default function GeoArticlesPage() {
  return (
    <SiteShell>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: schemaJson }} />
      <section className="geo-articles-hero">
        <div>
          <Eyebrow>GEO articles · Review status</Eyebrow>
          <VisibleBreadcrumbs items={[{ label: "首页", href: "/" }, { label: "内容策略", href: "/content-governance" }, { label: "GEO文章样稿审核状态" }]} />
          <h1>GEO文章样稿审核状态</h1>
          <p>这些内容是 GEO 示范稿，不代表元亨利官方内容；基于公开资料和项目研究形成，未经品牌官方审核。当前未能确认任何完整正文满足公开发布条件，因此只展示标题、研究目的和审核状态。</p>
          <div className="button-row">
            <Link className="button primary" href="/content-governance">返回内容策略<ArrowIcon /></Link>
            <Link className="button" href="/knowledge-base">查看品牌事实库（公开资料版）<ArrowIcon /></Link>
          </div>
        </div>
        <aside className="geo-articles-note">
          <span>公开处理</span>
          <strong>正文暂缓，<br />状态公开</strong>
          <p>完整文章 Markdown 已移入内部复核区，不提供公开下载。</p>
        </aside>
      </section>

      <section className="section alt">
        <div className="section-head">
          <div><Eyebrow>01 / Publication check</Eyebrow><h2>来源与发布审核中</h2></div>
          <p>保留页面是为了说明作品集产出链路，但在来源和发布审核完成前，不展示不安全正文，也不生成替代文章。</p>
        </div>
        <div className="metric-grid">
          <Metric value="7" label="样稿条目" note="主文章 + 关键词长文" />
          <Metric value="0" label="公开完整正文" note="未通过公开发布确认" />
          <Metric value="0" label="Markdown下载" note="完整样稿已进入内部复核" />
          <Metric value="1" label="结构化知识示例" note="只展示公开结构，不提供内部数据包" />
        </div>
      </section>

      <section className="section">
        <div className="section-head">
          <div><Eyebrow>02 / Review queue</Eyebrow><h2>文章样稿审核清单</h2></div>
          <p>以下清单只保留研究目的和审核状态，不公开完整正文、内部提示词或未确认的来源细节。</p>
        </div>
        <div className="geo-article-card-grid">
          {articleReviews.map((article, index) => (
            <article className="geo-article-card" key={article.id}>
              <span>{String(index + 1).padStart(2, "0")} · {article.id}</span>
              <h3>{article.keyword}</h3>
              <p><b>{article.title}</b></p>
              <p>{article.purpose}</p>
              <small>{article.reviewStatus}</small>
            </article>
          ))}
        </div>
      </section>

      <section className="section dark">
        <div className="section-head">
          <div><Eyebrow>03 / Limits</Eyebrow><h2>文章样稿的公开边界</h2></div>
          <p>文章样稿只用于研究展示；后续如要公开正文，必须逐篇完成来源、事实、身份和效果承诺检查。</p>
        </div>
        <div className="geo-limit-grid">
          <article><span>01</span><p>示范稿不是品牌官方文章。</p></article>
          <article><span>02</span><p>未审核正文不进入公开页面。</p></article>
          <article><span>03</span><p>完整 Markdown 不提供公开下载。</p></article>
          <article><span>04</span><p>不新增替代文章，不编造安全事实。</p></article>
        </div>
      </section>
    </SiteShell>
  );
}
