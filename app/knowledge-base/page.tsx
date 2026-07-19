import type { Metadata } from "next";
import Link from "next/link";
import { ArrowIcon, Eyebrow, Metric, ProjectDisclaimer, SiteShell } from "../components";
import { knowledgeDownloads } from "../data";
import { KnowledgeBaseExplorer } from "./KnowledgeBaseExplorer";
import knowledgeBase from "./knowledge-base-public.json";

export const metadata: Metadata = {
  title: "企业知识库",
  description: "元亨利红木家具GEO品牌事实知识库的安全公开快照：仅展示已审核、可追溯、适合公开发布的记录。",
};

type PublicFact = {
  id: string;
  entityId: string;
  entityName: string;
  evidenceLevel: string;
  type: string;
  statement: string;
  sourceIds: string[];
  sourceUrls: string[];
  evidenceIds: string[];
  questionIds: string[];
  allowedWording: string;
  boundary: string;
  updatedAt: string;
};

type PublicEntity = {
  id: string;
  type: string;
  name: string;
  description: string;
  sourceIds: string[];
  boundary: string;
  updatedAt: string;
};

type PublicSource = {
  id: string;
  title: string;
  type: string;
  url: string;
  grade: string;
  status: string;
  usable: boolean;
  proves: string;
  boundary: string;
  updatedAt: string;
};

type QuestionMapping = {
  mapId: string;
  questionId: string;
  question: string;
  coverageStatus: string;
  factIds: string[];
  sourceIds: string[];
  evidenceIds: string[];
  contentIds: string[];
  boundary: string;
  updatedAt: string;
};

type FaqMapping = {
  mapId: string;
  faqId: string;
  question: string;
  factIds: string[];
  methodConclusion: boolean;
  sourceIds: string[];
  relatedPages: string[];
  boundary: string;
  updatedAt: string;
};

const kb = knowledgeBase as {
  updatedAt: string;
  disclaimer: string;
  summary: Record<string, number>;
  evidenceLevels: { id: string; label: string; rule: string }[];
  architecture: { order: number; sheet: string }[];
  entities: PublicEntity[];
  facts: PublicFact[];
  sources: PublicSource[];
  mappings: { questions: QuestionMapping[]; faq: FaqMapping[] };
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
      { "@type": "PropertyValue", name: "factCount", value: kb.summary.facts },
      { "@type": "PropertyValue", name: "entityCount", value: kb.summary.entities },
      { "@type": "PropertyValue", name: "sourceCount", value: kb.summary.sources },
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
          <p>这不是后台系统，而是一份安全过滤后的公开快照：把已审核的实体、事实、来源、证据、FAQ和内容页面连起来，让“能回答”变成“能核验”。</p>
          <ProjectDisclaimer />
          <div className="button-row">
            {knowledgeDownloads.map((file) => <a className="button primary" href={file.href} download key={file.href}>{file.label}<ArrowIcon /></a>)}
            <Link className="button" href="/prompt-system">企业提示词体系<ArrowIcon /></Link>
            <Link className="button" href="/geo-articles">GEO文章样稿<ArrowIcon /></Link>
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
          <div><Eyebrow>01 / Snapshot</Eyebrow><h2>当前公开快照范围</h2></div>
          <p>外部工作簿是事实主库；本页只读取由主库过滤生成的公开 JSON，不展示待复核事实或不可用信源。</p>
        </div>
        <div className="metric-grid">
          <Metric value="11" label="工作表" note="外部主库结构" />
          <Metric value={`${kb.summary.sources}`} label="公开信源" note="仅保留可用 source_id" />
          <Metric value={`${kb.summary.facts}`} label="公开事实原子" note={`${kb.summary.excludedFacts}条已排除`} />
          <Metric value={`${kb.summary.diagnosticQuestions + kb.summary.faq}`} label="公开映射记录" note={`${kb.summary.diagnosticQuestions}题 + ${kb.summary.faq}条FAQ`} />
        </div>
        <div className="kb-download-panel">
          <div>
            <b>附件下载</b>
            <p>网页已支持在线查看；公开下载仅保留安全过滤版 JSON。完整工作簿进入内部复核，不作为公开附件。更新：{kb.updatedAt}。</p>
          </div>
          <div className="button-row">
            {knowledgeDownloads.map((file) => <a className="button" href={file.href} download key={file.href}>{file.type}<ArrowIcon /></a>)}
          </div>
        </div>
      </section>

      <section className="section kb-online-section" id="online-browser">
        <div className="section-head">
          <div><Eyebrow>02 / Online browser</Eyebrow><h2>不用下载表格，直接在线查</h2></div>
          <p>可按事实ID、实体、问题、来源ID和关键词搜索；也可以筛选事实等级、信源状态和映射类型。</p>
        </div>
        <KnowledgeBaseExplorer data={{ facts: kb.facts, entities: kb.entities, sources: kb.sources, mappings: kb.mappings }} />
        <div className="prompt-callout">
          <div>
            <b>下一层交付：提示词公开说明与文章审核状态</b>
            <p>知识库负责“有哪些事实”；提示词页面只公开方法和边界；文章页面只公开样稿审核状态，不展示未审核完整正文。</p>
          </div>
          <div className="button-row">
            <Link className="button" href="/prompt-system">查看提示词体系<ArrowIcon /></Link>
            <Link className="button" href="/geo-articles">查看文章审核状态<ArrowIcon /></Link>
          </div>
        </div>
      </section>

      <section className="section kb-architecture-section">
        <div className="section-head">
          <div><Eyebrow>03 / Architecture</Eyebrow><h2>11张表，分别管不同问题</h2></div>
          <p>结构上保留真实企业知识库的治理逻辑，但不假装拥有品牌内部SKU、合同、证书、价格或售后资料。</p>
        </div>
        <div className="kb-architecture">
          {kb.architecture.map((item) => <article key={item.sheet}><span>{String(item.order).padStart(2, "0")}</span><b>{item.sheet}</b></article>)}
        </div>
      </section>

      <section className="section dark">
        <div className="section-head">
          <div><Eyebrow>04 / Evidence model</Eyebrow><h2>公开事实等级</h2></div>
          <p>公开快照只保留已通过本阶段检查的事实等级；被排除记录继续留在内部审核链路。</p>
        </div>
        <div className="kb-level-grid">
          {levelCounts.map((level) => <article key={level.id}><span>{level.id}</span><h3>{level.label}</h3><strong>{level.count}条</strong><p>{level.rule}</p></article>)}
        </div>
      </section>

      <section className="section alt">
        <div className="section-head">
          <div><Eyebrow>05 / Query examples</Eyebrow><h2>六个典型查询，能直接落到事实边界</h2></div>
          <p>招聘方不用打开Excel，也能看懂这套知识库如何回答高风险问题。</p>
        </div>
        <div className="kb-query-grid">
          {kb.queryExamples.map((item) => <article key={item.id}><span>{item.id}</span><h3>{item.title}</h3><p>{item.answer}</p></article>)}
        </div>
      </section>

      <section className="section">
        <div className="section-head">
          <div><Eyebrow>06 / Facts</Eyebrow><h2>公开事实样例</h2></div>
          <p>上方在线浏览器可查看完整数据；这里保留5条高频样例，方便快速理解事实边界。</p>
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
          <div><Eyebrow>07 / Governance</Eyebrow><h2>治理流程和限制</h2></div>
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
