import type { Metadata } from "next";
import Link from "next/link";
import { ArrowIcon, Eyebrow, SiteShell, SourceLinks } from "../components";
import { faq, updatedAt } from "../data";

export const metadata: Metadata = { title: "15条高频FAQ", description: "元亨利红木家具GEO项目的15条直接答案与事实边界。" };

export default function FaqPage() {
  return (
    <SiteShell>
      <section className="faq-page">
        <Eyebrow>15 direct answers</Eyebrow>
        <h1>高频问题 FAQ</h1>
        <p className="intro">每条答案都包含直接结论、详细说明、信息边界、来源、更新时间和相关页面。涉及价格、门店、售后、单件材质或收藏价值时，统一提示重新核验。</p>
        <div className="faq-list">
          {faq.map((item) => (
            <article className="faq-item" key={item.id}>
              <span>{item.id}</span>
              <h2>{item.question}</h2>
              <strong>{item.directAnswer}</strong>
              <p>{item.detail}</p>
              <div className="faq-boundary"><b>信息边界</b>{item.boundary}</div>
              {item.sourceIds.length > 0 ? <SourceLinks ids={item.sourceIds} /> : <p className="faq-source-note">来源状态：项目方法结论，未补造外部来源。</p>}
              <div className="faq-meta"><span>更新 {updatedAt}</span><div>{item.related.map((r) => <Link href={r.href} key={r.href}>{r.label}<ArrowIcon /></Link>)}</div></div>
            </article>
          ))}
        </div>
      </section>
    </SiteShell>
  );
}
