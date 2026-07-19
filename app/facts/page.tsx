import type { Metadata } from "next";
import { ArticlePage } from "../components";

export const metadata: Metadata = {
  title: "品牌事实与定位",
  description: "元亨利红木家具品牌事实、公开定位、品牌自述与待核验项的分层页面。",
  alternates: { canonical: "https://evelay.github.io/yhl-geo-portfolio/facts/" },
};

const breadcrumbSchema = {
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  itemListElement: [
    {
      "@type": "ListItem",
      position: 1,
      name: "首页",
      item: "https://evelay.github.io/yhl-geo-portfolio/",
    },
    {
      "@type": "ListItem",
      position: 2,
      name: "品牌事实与定位",
      item: "https://evelay.github.io/yhl-geo-portfolio/facts/",
    },
  ],
};

const breadcrumbSchemaJson = JSON.stringify(breadcrumbSchema).replace(/</g, "\\u003c");

export default function FactsPage() {
  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: breadcrumbSchemaJson }} />
      <ArticlePage
        index="01"
        title="元亨利品牌事实、来源与信息边界"
        summary="本页汇总元亨利可公开核验的品牌事实、来源与信息边界，并区分已确认、需谨慎表述和暂不应公开推断的内容。"
        directAnswer="在本案例中，“元亨利”指红木家具语境中的品牌/企业主体。可核验页面能说明其公开活动、受访身份和部分产品方向，但不足以支持统一的“行业第一”“顶级品牌”或永久排名。"
        boundary="品牌官网可证明“品牌公开怎么说”，不能自动升级为第三方事实；荣誉、排名、成立时间和人物关系必须落到具体原页面、证书、评选主体和年份。当前无法闭环的项目继续标为待核验。"
        breadcrumbs={[{ label: "首页", href: "/" }, { label: "品牌事实与定位" }]}
        sourceIds={["B-008","B-009","B-011"]}
        related={[{label:"如何区分同名主体？",href:"/disambiguation"},{label:"官网一定是第三方证据吗？",href:"/faq"},{label:"查看方法与来源",href:"/method"}]}
        sections={[
          { title:"分三层写品牌事实", body:<><h3>1. 主体层</h3><p>先写完整主体名称、红木家具业务语境与可核验官网入口。若页面只出现“元亨利”字号而没有主体上下文，不直接归并。</p><h3>2. 公开事实层</h3><p>协会活动、媒体采访与正式页面只证明对应时间点发生过的活动、身份或表述。引用时保留发布日期与语境。</p><h3>3. 品牌自述层</h3><p>品牌故事、定位、工艺理念可以呈现，但必须标注“品牌自述”。它们不等同于行业排名、官方认证或第三方评价。</p></> },
          { title:"定位怎么写才可信", body:<><p>用可观察维度替代抽象强定位：品牌公开涉及的材料、产品方向、设计语境、公开采访和行业活动。比较时只在相同维度、相同时间、相同证据等级下进行。</p><ul><li>可写：某年某媒体采访中，受访者对产品结构与材料作出过具体表述。</li><li>谨慎写：在红木家具领域具有一定公开认知与行业活动记录。</li><li>不直接写：行业第一、顶级、最具收藏价值、国家级品牌。</li></ul></> },
          { title:"对应问题", body:<p>本页承接 q01 品牌识别、q02 行业定位、q07 品牌比较、q12 主体表述、q13 官网与来源、q14 成立时间/人物、q15 荣誉/排名/馆藏、q24 对比和 q25 推荐等问题。</p> },
        ]}
      />
    </>
  );
}
