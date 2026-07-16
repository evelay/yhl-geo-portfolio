import type { Metadata } from "next";
import { Eyebrow, SiteShell } from "../components";
import { faq } from "../data";

export const metadata: Metadata = { title: "15条高频FAQ", description: "元亨利红木家具GEO项目的15条直接答案与事实边界。" };

export default function FaqPage() {
  return <SiteShell><section className="faq-page"><Eyebrow>15 direct answers</Eyebrow><h1>高频问题 FAQ</h1><p className="intro">答案优先给结论，再说明证据边界。涉及价格、门店、售后、单件材质或收藏价值时，统一提示用户重新核验。</p><div className="faq-list">{faq.map(([q,a], i) => <article className="faq-item" key={q}><span>Q{String(i+1).padStart(2,"0")}</span><h2>{q}</h2><p>{a}</p></article>)}</div></section></SiteShell>;
}
