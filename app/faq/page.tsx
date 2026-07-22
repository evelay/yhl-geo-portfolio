import type { Metadata } from "next";
import Link from "next/link";
import { ArrowIcon, Eyebrow, SiteShell, SourceLinks, VisibleBreadcrumbs } from "../components";
import { faq, siteUrl, updatedAt } from "../data";

export const metadata: Metadata = {
  title: "关键问题 FAQ",
  description: "元亨利红木家具GEO项目中已完成公开发布检查的关键问题 FAQ与事实边界。",
  alternates: { canonical: `${siteUrl}/faq/` },
};

const schema = {
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "WebPage",
      "@id": `${siteUrl}/faq/#webpage`,
      url: `${siteUrl}/faq/`,
      name: "关键问题 FAQ",
      description: "将AI搜索中的品牌主体、材质、购买和价值判断问题转化为带边界和来源的直接回答。",
      inLanguage: "zh-CN",
    },
    {
      "@type": "BreadcrumbList",
      itemListElement: [
        { "@type": "ListItem", position: 1, name: "首页", item: `${siteUrl}/` },
        { "@type": "ListItem", position: 2, name: "内容策略", item: `${siteUrl}/content-governance/` },
        { "@type": "ListItem", position: 3, name: "关键问题 FAQ", item: `${siteUrl}/faq/` },
      ],
    },
  ],
};

const schemaJson = JSON.stringify(schema).replace(/</g, "\\u003c");

type FaqItem = (typeof faq)[number];

function FaqCard({ item }: { item: FaqItem }) {
  return (
    <article className="faq-item">
      <span>{item.id}</span>
      <h2>{item.question}</h2>
      <strong>{item.directAnswer}</strong>
      <div className="faq-boundary"><b>信息边界</b>{item.boundary}</div>
      {item.sourceIds.length > 0 ? <SourceLinks ids={item.sourceIds.slice(0, 2)} /> : <p className="faq-source-note">来源状态：项目方法结论，未补造外部来源。</p>}
      <div className="faq-meta"><span>更新 {updatedAt}</span><div>{item.related.slice(0, 2).map((r) => <Link href={r.href} key={r.href}>{r.label}<ArrowIcon /></Link>)}</div></div>
    </article>
  );
}

export default function FaqPage() {
  const featuredFaq = faq.slice(0, 8);
  const remainingFaq = faq.slice(8);

  return (
    <SiteShell>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: schemaJson }} />
      <section className="faq-page">
        <Eyebrow>结构化内容资产</Eyebrow>
        <VisibleBreadcrumbs items={[{ label: "首页", href: "/" }, { label: "内容策略", href: "/content-governance" }, { label: "关键问题 FAQ" }]} />
        <h1>关键问题 FAQ</h1>
        <p className="intro">该FAQ用于回应AI搜索中常见的品牌主体、材质、购买和价值判断问题，是诊断结果转化成的结构化内容资产。</p>
        <p className="faq-summary">默认展示{featuredFaq.length}个代表问题；其余已审核问题保留在下方完整列表中。</p>
        <div className="faq-list">
          {featuredFaq.map((item) => <FaqCard item={item} key={item.id} />)}
        </div>
        <details className="faq-more">
          <summary>查看完整问题列表（另有{remainingFaq.length}条）</summary>
          <div className="faq-list compact-faq-list">
            {remainingFaq.map((item) => <FaqCard item={item} key={item.id} />)}
          </div>
        </details>
      </section>
    </SiteShell>
  );
}
