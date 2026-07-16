import Link from "next/link";
import { nav, sources, updatedAt } from "./data";

export function ArrowIcon() {
  return (
    <svg aria-hidden="true" viewBox="0 0 24 24" width="18" height="18">
      <path d="M5 12h13M13 6l6 6-6 6" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

export function ExternalIcon() {
  return (
    <svg aria-hidden="true" viewBox="0 0 24 24" width="15" height="15">
      <path d="M13 5h6v6M19 5l-9 9M17 13v5a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1V8a1 1 0 0 1 1-1h5" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

export function Header() {
  return (
    <header className="site-header">
      <Link href="/" className="brand-mark" aria-label="返回研究首页">
        <span className="seal">元</span>
        <span><b>元亨利 GEO</b><small>公开研究案例</small></span>
      </Link>
      <nav aria-label="主导航">
        {nav.map(([label, href]) => <Link key={href} href={href}>{label}</Link>)}
      </nav>
    </header>
  );
}

export function Footer() {
  return (
    <footer className="site-footer">
      <div>
        <b>研究声明</b>
        <p>本项目为公开资料研究与求职作品集，不代表元亨利官方，不声称已提升AI收录、曝光或销售。</p>
      </div>
      <div className="footer-meta">
        <span>更新：{updatedAt}</span>
        <Link href="/method">方法、来源与限制</Link>
      </div>
    </footer>
  );
}

export function SiteShell({ children }: { children: React.ReactNode }) {
  return <><Header /><main>{children}</main><Footer /></>;
}

export function Eyebrow({ children }: { children: React.ReactNode }) {
  return <div className="eyebrow"><span />{children}</div>;
}

export function BarChart({ data, max, unit = "", accent = false }: { data: {label:string; value:number}[]; max: number; unit?: string; accent?: boolean }) {
  return (
    <div className={`bar-chart ${accent ? "bar-chart-accent" : ""}`}>
      {data.map((item) => (
        <div className="bar-row" key={item.label}>
          <span className="bar-label">{item.label}</span>
          <span className="bar-track"><i style={{width: `${Math.min(100, item.value / max * 100)}%`}} /></span>
          <b>{item.value.toFixed(Number.isInteger(item.value) ? 0 : 1)}{unit}</b>
        </div>
      ))}
    </div>
  );
}

export function Metric({ value, label, note }: { value: string; label: string; note?: string }) {
  return <div className="metric"><strong>{value}</strong><span>{label}</span>{note && <small>{note}</small>}</div>;
}

export function SourceLinks({ ids }: { ids: string[] }) {
  const selected = sources.filter((s) => ids.includes(s.id));
  return (
    <div className="source-links">
      {selected.map((s) => (
        <a href={s.url} target="_blank" rel="noreferrer" key={s.id}>
          <span><small>{s.id} · {s.type}</small>{s.title}</span><ExternalIcon />
        </a>
      ))}
    </div>
  );
}

export type ArticleSection = { title: string; body: React.ReactNode };

export function ArticlePage({
  index,
  title,
  directAnswer,
  boundary,
  sections,
  sourceIds,
  related,
}: {
  index: string;
  title: string;
  directAnswer: string;
  boundary: string;
  sections: ArticleSection[];
  sourceIds: string[];
  related: { label: string; href: string }[];
}) {
  return (
    <SiteShell>
      <section className="article-hero">
        <Eyebrow>内容资产 {index}</Eyebrow>
        <h1>{title}</h1>
        <p className="lede">{directAnswer}</p>
        <div className="answer-box"><b>直接答案</b><p>{directAnswer}</p></div>
      </section>
      <div className="article-layout">
        <article className="article-body">
          {sections.map((section) => <section key={section.title}><h2>{section.title}</h2><div>{section.body}</div></section>)}
          <section><h2>事实边界</h2><div className="boundary-box">{boundary}</div></section>
          <section><h2>可核验来源</h2><SourceLinks ids={sourceIds} /></section>
        </article>
        <aside className="article-aside">
          <div className="aside-card"><span>更新时间</span><b>{updatedAt}</b></div>
          <div className="aside-card"><span>内容承接</span><b>30题问题矩阵</b><p>页面只回答已有证据支持的部分；动态商业信息提示重新核验。</p></div>
          <div className="aside-card"><span>相关问题</span>{related.map((r) => <Link href={r.href} key={r.href}>{r.label}<ArrowIcon /></Link>)}</div>
        </aside>
      </div>
    </SiteShell>
  );
}
