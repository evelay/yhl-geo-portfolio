import Link from "next/link";
import { PrimaryNavigation } from "./PrimaryNavigation";
import { nav, siteUrl, sources, updatedAt } from "./data";

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
      <Link href="/" className="brand-mark" aria-label="返回首页">
        <span className="seal">元</span>
        <span><b>元亨利 GEO 案例</b><small>独立诊断与内容优化</small></span>
      </Link>
      <PrimaryNavigation items={nav} />
    </header>
  );
}

export function Footer() {
  return (
    <footer className="site-footer">
      <div>
        <b>项目声明</b>
        <p>本项目基于公开资料独立完成，用于展示 GEO 问题研究、AI 回答诊断、内容策略和页面优化方法，非元亨利品牌官方网站或官方委托项目。</p>
      </div>
      <div className="footer-meta">
        <span>更新：{updatedAt}</span>
        <Link href="/methodology">研究方法</Link>
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

export function ProjectDisclaimer({ className = "" }: { className?: string }) {
  return (
    <div className={`project-disclaimer ${className}`.trim()}>
      <b>项目声明</b>
      <p>本项目基于公开资料独立完成，用于展示 GEO 问题研究、AI 回答诊断、内容策略和页面优化方法，非元亨利品牌官方网站或官方委托项目。</p>
    </div>
  );
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

export function GroupedMetricChart({
  data,
  max = 2,
}: {
  data: { platform: string; metrics: { label: string; value: number }[] }[];
  max?: number;
}) {
  const legend = data[0]?.metrics.map((metric) => metric.label) || [];

  return (
    <div className="grouped-metric-chart" role="img" aria-label="五个平台四项指标分组柱状图，指标范围0到2分">
      <div className="grouped-metric-legend">
        {legend.map((label, index) => <span className={`metric-key metric-key-${index}`} key={label}>{label}</span>)}
      </div>
      <div className="grouped-metric-bars">
        {data.map((platform) => (
          <div className="metric-platform" key={platform.platform}>
            <div className="metric-platform-bars">
              {platform.metrics.map((metric, index) => (
                <span className={`metric-column metric-column-${index}`} key={metric.label} style={{ height: `${Math.max(3, Math.min(100, metric.value / max * 100))}%` }}>
                  <b>{metric.value.toFixed(2)}</b>
                </span>
              ))}
            </div>
            <strong>{platform.platform}</strong>
          </div>
        ))}
      </div>
      <div className="chart-axis"><span>0</span><span>1</span><span>2</span></div>
    </div>
  );
}

export function PlatformMetricCards({
  data,
  max = 2,
}: {
  data: { platform: string; metrics: { label: string; value: number }[] }[];
  max?: number;
}) {
  return (
    <div className="mobile-platform-metric-cards" aria-label="移动端五个平台指标卡">
      {data.map((platform) => (
        <article className="platform-metric-card" key={platform.platform}>
          <div className="platform-metric-card-head">
            <h3>{platform.platform}</h3>
            <span>指标范围0—2分</span>
          </div>
          <div className="mini-metric-bars">
            {platform.metrics.map((metric, index) => (
              <div className="mini-metric-row" key={metric.label}>
                <span>{metric.label}</span>
                <i>
                  <b
                    className={`mini-metric-fill mini-metric-fill-${index}`}
                    style={{ width: `${Math.max(3, Math.min(100, metric.value / max * 100))}%` }}
                  />
                </i>
                <strong>{metric.value.toFixed(2)}</strong>
              </div>
            ))}
          </div>
        </article>
      ))}
    </div>
  );
}

export function StackedRiskBar({
  data,
}: {
  data: { label: string; value: number }[];
}) {
  const total = data.reduce((sum, item) => sum + item.value, 0);

  return (
    <div className="stacked-risk-chart" role="img" aria-label={`低、中、高、严重风险横向堆叠条形图，总计${total}条回答`}>
      <div className="stacked-risk-track">
        {data.map((item, index) => (
          <span
            className={`risk-segment risk-segment-${index}`}
            key={item.label}
            style={{ width: `${item.value / total * 100}%` }}
            title={`${item.label}风险：${item.value}条`}
          >
            <b>{item.value}</b>
          </span>
        ))}
      </div>
      <div className="stacked-risk-legend">
        {data.map((item, index) => (
          <span className={`risk-key risk-key-${index}`} key={item.label}>
            {item.label}风险 <b>{item.value}条</b>
          </span>
        ))}
      </div>
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
export type VisibleBreadcrumbItem = { label: string; href?: string };

function absoluteSiteUrl(path: string) {
  if (path === "/") return `${siteUrl}/`;
  return `${siteUrl}${path.endsWith("/") ? path : `${path}/`}`;
}

export function VisibleBreadcrumbs({ items }: { items: VisibleBreadcrumbItem[] }) {
  return (
    <nav className="visible-breadcrumbs" aria-label="面包屑导航">
      <ol>
        {items.map((item, index) => {
          const href = item.href;
          const isCurrent = index === items.length - 1 || !href;
          return (
            <li key={`${item.label}-${index}`} {...(isCurrent ? { "aria-current": "page" as const } : {})}>
              {isCurrent ? item.label : <Link href={href}>{item.label}</Link>}
            </li>
          );
        })}
      </ol>
    </nav>
  );
}

export function ArticlePage({
  index,
  title,
  summary,
  directAnswer,
  boundary,
  assetProblem,
  breadcrumbs,
  schemaPath,
  sections,
  sourceIds,
  related,
}: {
  index: string;
  title: string;
  summary?: string;
  directAnswer: string;
  boundary: string;
  assetProblem: string;
  breadcrumbs?: VisibleBreadcrumbItem[];
  schemaPath: string;
  sections: ArticleSection[];
  sourceIds: string[];
  related: { label: string; href: string }[];
}) {
  const canonicalUrl = absoluteSiteUrl(schemaPath);
  const schema = {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "WebPage",
        "@id": `${canonicalUrl}#webpage`,
        url: canonicalUrl,
        name: title,
        description: summary || directAnswer,
        inLanguage: "zh-CN",
      },
      {
        "@type": "BreadcrumbList",
        itemListElement: (breadcrumbs || []).map((item, index) => ({
          "@type": "ListItem",
          position: index + 1,
          name: item.label,
          item: item.href ? absoluteSiteUrl(item.href) : canonicalUrl,
        })),
      },
    ],
  };
  const schemaJson = JSON.stringify(schema).replace(/</g, "\\u003c");

  return (
    <SiteShell>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: schemaJson }} />
      <section className="article-hero">
        <Eyebrow>内容资产 {index}</Eyebrow>
        {breadcrumbs && <VisibleBreadcrumbs items={breadcrumbs} />}
        <h1>{title}</h1>
        <p className="lede">{summary || directAnswer}</p>
        <div className="asset-problem">
          <b>诊断转化</b>
          <p>{assetProblem}</p>
        </div>
        <div className="answer-box"><b>直接答案</b><p>{directAnswer}</p></div>
        <div className="asset-context">
          <b>内容策略资产</b>
          <p>本页已从一级导航降级，作为 <Link href="/content-governance">内容策略</Link> 的子资产保留，用于承接事实、来源和边界核验。</p>
        </div>
      </section>
      <div className="article-layout">
        <article className="article-body">
          {sections.map((section) => <section key={section.title}><h2>{section.title}</h2><div>{section.body}</div></section>)}
          <section><h2>事实边界</h2><div className="boundary-box">{boundary}</div></section>
          <section><h2>可核验来源</h2><SourceLinks ids={sourceIds} /></section>
        </article>
        <aside className="article-aside">
          <div className="aside-card"><span>更新时间</span><b>{updatedAt}</b></div>
          <div className="aside-card"><span>公开定位</span><b>GEO 内容资产</b><p>页面只回答已有证据支持的部分；动态商业信息提示重新核验。</p></div>
          <div className="aside-card"><span>相关问题</span>{related.map((r) => <Link href={r.href} key={r.href}>{r.label}<ArrowIcon /></Link>)}</div>
        </aside>
      </div>
    </SiteShell>
  );
}
