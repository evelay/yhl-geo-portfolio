import type { Metadata } from "next";
import Link from "next/link";
import { ArrowIcon, Eyebrow, ProjectDisclaimer, SiteShell, SourceLinks } from "../components";
import { faq, updatedAt } from "../data";

export const metadata: Metadata = { title: "公开FAQ", description: "元亨利红木家具GEO项目中已完成公开发布检查的高频FAQ与事实边界。" };

export default function FaqPage() {
  return (
    <SiteShell>
      <section className="faq-page">
        <Eyebrow>Reviewed direct answers</Eyebrow>
        <h1>高频问题 FAQ</h1>
        <p className="intro">当前公开 {faq.length} 条已通过来源与发布检查的 FAQ；未完成 source_id 或事实等级审核的问答暂不展示，并保留在审计记录中。</p>
        <ProjectDisclaimer />
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
