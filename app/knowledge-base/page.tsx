import type { Metadata } from "next";
import Link from "next/link";
import { ArrowIcon, Eyebrow, Metric, SiteShell } from "../components";
import { knowledgeDownloads, updatedAt } from "../data";
import knowledgeBase from "./knowledge-base-public.json";

export const metadata: Metadata = {
  title: "企业知识库",
  description: "元亨利红木家具GEO品牌事实知识库：11表结构、四级事实模型、27条信源迁移、30题与15条FAQ映射。",
};

type PublicFact = {
  id: string;
  evidenceLevel: string;
  type: string;
  statement: string;
  boundary: string;
  sourceIds: string[];
  questionIds: string[];
};

const kb = knowledgeBase as {
  updatedAt: string;
  disclaimer: string;
  summary: Record<string, number>;
  evidenceLevels: { id: string; label: string; rule: string }[];
  architecture: { order: number; sheet: string }[];
  facts: PublicFact[];
  queryExamples: { id: string; title: string; answer: string }[];
  governance: string[];
};

const levelCounts = kb.evidenceLevels.map((level) => ({
  ...level,
  count: kb.facts.filter((fact) => fact.evidenceLevel === level.id).length,
}));

const queryFacts = kb.facts.filter((fact) => ["FACT-0001", "FACT-0021", "FACT-0039", "FACT-0040", "FACT-0041"].includes(fact.id));

export default function KnowledgeBasePage() {
  const datasetJsonLd = {
    "@context": "https://schema.org",
    "@type": "Dataset",
    name: "元亨利GEO品牌事实知识库公开快照",
    description: "个人公开研究和作品集执行版知识库，连接实体、事实、来源、证据、内容页面与FAQ。",
    dateModified: kb.updatedAt,
    license: "Personal portfolio research; not official brand data",
    variableMeasured: ["entity_id", "fact_id", "source_id", "evidence_id", "content_id", "faq_id", "question_id"],
    distribution: knowledgeDownloads.map((file) => ({ "@type": "DataDownload", encodingFormat: file.type, contentUrl: file.href })),
    additionalProperty: [
      { "@type": "PropertyValue", name: "knowledgeSheets", value: kb.summary.entities ? 11 : 0 },
      { "@type": "PropertyValue", name: "evidenceLevels", value: kb.evidenceLevels.map((level) => `${level.id}:${level.label}`).join(";") },
      { "@type": "PropertyValue", name: "mappedQuestions", value: kb.summary.diagnosticQuestions },
      { "@type": "PropertyValue", name: "mappedFaq", value: kb.summary.faq },
    ],
  };

  return (
    <SiteShell>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(datasetJsonLd) }} />
      <section className="kb-hero">
        <div>
          <Eyebrow>Knowledge base · Portfolio execution</Eyebrow>
          <h1>企业知识库</h1>
          <p>这不是后台系统，而是一份可审计的品牌事实底座：把实体、事实、来源、证据、FAQ和内容页面连起来，让“能回答”变成“能核验”。</p>
          <div className="button-row">
            {knowledgeDownloads.map((file) => <a className={file.type === "XLSX" ? "button primary" : "button"} href={file.href} download key={file.href}>{file.label}<ArrowIcon /></a>)}
            <Link className="button" href="/strategy">返回优化方案<ArrowIcon /></Link>
          </div>
        </div>
        <aside className="kb-verdict">
          <span>最大问题</span>
          <strong>可识别，<br />但不可稳定核验</strong>
          <p>知识库用事实ID、来源ID和边界字段，专门补这个缺口。</p>
        </aside>
      </section>

      <section className="section alt">
        <div className="section-head">
          <div><Eyebrow>01 / Snapshot</Eyebrow><h2>当前知识库完整度</h2></div>
          <p>Excel是事实主库；JSON是公开快照，不输出内部备注、负责人、审核意见或未来企业内部资料。</p>
        </div>
        <div className="metric-grid">
          <Metric value="11" label="工作表" note="独立知识库结构" />
          <Metric value={`${kb.summary.sources}`} label="信源迁移" note={`${kb.summary.usableSources}可用 / ${kb.summary.pendingSources}待补`} />
          <Metric value={`${kb.summary.facts}`} label="事实原子" note={`${kb.summary.publicFacts}条进入公开快照`} />
          <Metric value="45" label="映射记录" note="30题 + 15条FAQ" />
        </div>
        <div className="kb-download-panel">
          <div>
            <b>下载入口</b>
            <p>工作簿用于投递和复盘；JSON用于网站公开展示。两者均更新于 {updatedAt}。</p>
          </div>
          <div className="button-row">
            {knowledgeDownloads.map((file) => <a className="button" href={file.href} download key={file.href}>{file.type}<ArrowIcon /></a>)}
          </div>
        </div>
      </section>

      <section className="section kb-architecture-section">
        <div className="section-head">
          <div><Eyebrow>02 / Architecture</Eyebrow><h2>11张表，分别管不同问题</h2></div>
          <p>结构上保留真实企业知识库的治理逻辑，但不假装拥有品牌内部SKU、合同、证书、价格或售后资料。</p>
        </div>
        <div className="kb-architecture">
          {kb.architecture.map((item) => <article key={item.sheet}><span>{String(item.order).padStart(2, "0")}</span><b>{item.sheet}</b></article>)}
        </div>
      </section>

      <section className="section dark">
        <div className="section-head">
          <div><Eyebrow>03 / Evidence model</Eyebrow><h2>四级事实模型</h2></div>
          <p>事实等级决定能不能写、怎么写、写到哪里停。</p>
        </div>
        <div className="kb-level-grid">
          {levelCounts.map((level) => <article key={level.id}><span>{level.id}</span><h3>{level.label}</h3><strong>{level.count}条</strong><p>{level.rule}</p></article>)}
        </div>
      </section>

      <section className="section alt">
        <div className="section-head">
          <div><Eyebrow>04 / Query examples</Eyebrow><h2>六个典型查询，能直接落到事实边界</h2></div>
          <p>招聘方不用打开Excel，也能看懂这套知识库如何回答高风险问题。</p>
        </div>
        <div className="kb-query-grid">
          {kb.queryExamples.map((item) => <article key={item.id}><span>{item.id}</span><h3>{item.title}</h3><p>{item.answer}</p></article>)}
        </div>
      </section>

      <section className="section">
        <div className="section-head">
          <div><Eyebrow>05 / Facts</Eyebrow><h2>公开事实样例</h2></div>
          <p>这里展示的是公开快照中的样例，不包含内部负责人、审核意见或未来企业内部资料。</p>
        </div>
        <div className="kb-fact-list">
          {queryFacts.map((fact) => (
            <article key={fact.id}>
              <div><span>{fact.id} · {fact.evidenceLevel}</span><h3>{fact.type}</h3></div>
              <p>{fact.statement}</p>
              <small>边界：{fact.boundary}</small>
              <small>source_id：{fact.sourceIds.join(" / ")} · question_id：{fact.questionIds.join(" / ") || "未直接绑定"}</small>
            </article>
          ))}
        </div>
      </section>

      <section className="section dark">
        <div className="section-head">
          <div><Eyebrow>06 / Governance</Eyebrow><h2>治理流程和限制</h2></div>
          <p>知识库的价值不是把话写满，而是控制哪些话不能被写成确定事实。</p>
        </div>
        <div className="kb-governance">
          {kb.governance.map((rule, index) => <article key={rule}><span>{String(index + 1).padStart(2, "0")}</span><p>{rule}</p></article>)}
        </div>
        <p className="kb-disclaimer">{kb.disclaimer}</p>
      </section>
    </SiteShell>
  );
}
