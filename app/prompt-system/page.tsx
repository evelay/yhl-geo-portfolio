import type { Metadata } from "next";
import Link from "next/link";
import { ArrowIcon, Eyebrow, SiteShell, VisibleBreadcrumbs } from "../components";
import { siteUrl, updatedAt } from "../data";

export const metadata: Metadata = {
  title: "提示词体系公开说明",
  description: "提示词体系公开说明：作为研究方法附录，只保留从用户问题到人工发布审核的简化流程。",
  alternates: { canonical: `${siteUrl}/prompt-system/` },
};

const schema = {
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "WebPage",
      "@id": `${siteUrl}/prompt-system/#webpage`,
      url: `${siteUrl}/prompt-system/`,
      name: "提示词体系公开说明",
      description: "作为研究方法附录，只保留从用户问题到人工发布审核的简化流程。",
      inLanguage: "zh-CN",
    },
    {
      "@type": "BreadcrumbList",
      itemListElement: [
        { "@type": "ListItem", position: 1, name: "首页", item: `${siteUrl}/` },
        { "@type": "ListItem", position: 2, name: "研究方法", item: `${siteUrl}/methodology/` },
        { "@type": "ListItem", position: 3, name: "提示词体系公开说明", item: `${siteUrl}/prompt-system/` },
      ],
    },
  ],
};

const schemaJson = JSON.stringify(schema).replace(/</g, "\\u003c");

const workflow = [
  "用户问题",
  "匹配可核验事实",
  "检查来源与边界",
  "生成回答",
  "人工发布审核",
];

const reviewPoints = [
  "回答是否锁定正确品牌主体和业务语境。",
  "结论是否能回到公开来源或单件产品凭证。",
  "品牌自述、第三方事实和动态信息是否被分开表述。",
  "是否避免排名、保值、升值、回购或效果承诺。",
];

export default function PromptSystemPage() {
  return (
    <SiteShell>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: schemaJson }} />
      <section className="prompt-hero compact-appendix-hero">
        <div>
          <Eyebrow>方法附录</Eyebrow>
          <VisibleBreadcrumbs items={[{ label: "首页", href: "/" }, { label: "研究方法", href: "/methodology" }, { label: "提示词体系公开说明" }]} />
          <h1>提示词体系公开说明</h1>
          <p>提示词体系不是本项目的核心公开资产。本页只保留简化流程，说明诊断后的事实、来源和边界如何进入人工审核的回答生产链路。</p>
          <div className="button-row">
            <Link className="button primary" href="/methodology">返回研究方法<ArrowIcon /></Link>
            <Link className="button" href="/content-governance">查看内容策略<ArrowIcon /></Link>
          </div>
        </div>
        <aside className="prompt-verdict">
          <span>公开定位</span>
          <strong>流程附录，<br />不是主资产</strong>
          <p>完整提示词和内部审核细节不作为公开页面重点。</p>
        </aside>
      </section>

      <section className="section alt">
        <div className="section-head">
          <div><Eyebrow>01 / 简化流程</Eyebrow><h2>从问题到发布审核</h2></div>
          <p>公开版只展示从问题到发布审核的流程，不展示完整提示词结构。</p>
        </div>
        <div className="prompt-flow compact-flow">
          {workflow.map((step, index) => (
            <article key={step}>
              <span>{String(index + 1).padStart(2, "0")}</span>
              <b>{step}</b>
            </article>
          ))}
        </div>
      </section>

      <section className="section">
        <div className="section-head">
          <div><Eyebrow>02 / 人工审核</Eyebrow><h2>发布前检查什么</h2></div>
          <p>提示词只负责生成候选回答，公开发布仍需要人工确认事实和边界。</p>
        </div>
        <div className="text-list two-col">
          {reviewPoints.map((item) => <p key={item}>{item}</p>)}
        </div>
        <p className="safe-note">更新：{updatedAt}。该附录已从主要公开入口降级，核心流程已合并到研究方法页。</p>
      </section>
    </SiteShell>
  );
}
