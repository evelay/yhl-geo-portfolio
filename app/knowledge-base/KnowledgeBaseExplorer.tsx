"use client";

import { useMemo, useState } from "react";

type Entity = {
  id: string;
  type: string;
  name: string;
  description: string;
  sourceIds: string[];
  boundary: string;
  updatedAt: string;
};

type Fact = {
  id: string;
  entityId: string;
  entityName: string;
  type: string;
  statement: string;
  evidenceLevel: string;
  sourceIds: string[];
  sourceUrls: string[];
  evidenceIds: string[];
  questionIds: string[];
  allowedWording: string;
  boundary: string;
  updatedAt: string;
};

type Source = {
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

type KnowledgeBaseData = {
  facts: Fact[];
  entities: Entity[];
  sources: Source[];
  mappings: {
    questions: QuestionMapping[];
    faq: FaqMapping[];
  };
};

type TabKey = "facts" | "entities" | "sources" | "questions" | "faq";

const tabs: { key: TabKey; label: string }[] = [
  { key: "facts", label: "可核验事实" },
  { key: "entities", label: "品牌主体" },
  { key: "sources", label: "来源记录" },
  { key: "questions", label: "问题与事实关联" },
  { key: "faq", label: "FAQ关联" },
];

const levelOptions = ["全部类别", "权威第三方事实", "品牌公开自述", "单件产品证据"];
const sourceOptions = ["全部来源", "可用来源"];
const mappingOptions = ["全部关联", "完整回答", "边界回答", "研究方法结论"];

function textOf(value: unknown): string {
  if (Array.isArray(value)) return value.join(" ");
  if (value && typeof value === "object") return Object.values(value).map(textOf).join(" ");
  return String(value ?? "");
}

function matchesQuery(item: unknown, query: string) {
  if (!query.trim()) return true;
  return textOf(item).toLowerCase().includes(query.trim().toLowerCase());
}

function joinIds(ids: string[], fallback = "未绑定") {
  return ids.length ? ids.join(" / ") : fallback;
}

function levelLabel(level: string) {
  const labels: Record<string, string> = {
    L1: "权威第三方事实",
    L2: "品牌公开自述",
    L4: "单件产品证据",
  };
  return labels[level] ?? level;
}

function levelIdFromLabel(label: string) {
  const levels: Record<string, string> = {
    权威第三方事实: "L1",
    品牌公开自述: "L2",
    单件产品证据: "L4",
  };
  return levels[label] ?? label;
}

function DetailRow({ label, value }: { label: string; value: string }) {
  return <p><b>{label}</b><span>{value}</span></p>;
}

export function KnowledgeBaseExplorer({ data }: { data: KnowledgeBaseData }) {
  const [activeTab, setActiveTab] = useState<TabKey>("facts");
  const [query, setQuery] = useState("");
  const [levelFilter, setLevelFilter] = useState("全部类别");
  const [sourceFilter, setSourceFilter] = useState("全部来源");
  const [mappingFilter, setMappingFilter] = useState("全部关联");
  const [expandedId, setExpandedId] = useState<string | null>("FACT-0001");

  const rows = useMemo(() => {
    if (activeTab === "facts") {
      return data.facts.filter((item) => {
        const byLevel = levelFilter === "全部类别" || item.evidenceLevel === levelIdFromLabel(levelFilter);
        return byLevel && matchesQuery(item, query);
      });
    }
    if (activeTab === "entities") return data.entities.filter((item) => matchesQuery(item, query));
    if (activeTab === "sources") {
      return data.sources.filter((item) => {
        const byStatus =
          sourceFilter === "全部来源" ||
          (sourceFilter === "可用来源" && item.usable);
        return byStatus && matchesQuery(item, query);
      });
    }
    if (activeTab === "questions") {
      return data.mappings.questions.filter((item) => {
        const byCoverage =
          mappingFilter === "全部关联" ||
          (mappingFilter === "完整回答" && item.coverageStatus.includes("完整")) ||
          (mappingFilter === "边界回答" && item.coverageStatus.includes("边界"));
        return byCoverage && matchesQuery(item, query);
      });
    }
    return data.mappings.faq.filter((item) => {
      const byMethod = mappingFilter !== "研究方法结论" || item.methodConclusion;
      return byMethod && matchesQuery(item, query);
    });
  }, [activeTab, data, levelFilter, mappingFilter, query, sourceFilter]);

  const counts = {
    facts: data.facts.length,
    entities: data.entities.length,
    sources: data.sources.length,
    questions: data.mappings.questions.length,
    faq: data.mappings.faq.length,
  };

  function resetExpand(tab: TabKey) {
    setActiveTab(tab);
    setExpandedId(null);
  }

  return (
    <div className="kb-explorer">
      <div className="kb-explorer-toolbar">
        <div>
          <span>结构示例</span>
          <h3>查看事实、来源和问题关联</h3>
        </div>
        <label>
          <span>搜索</span>
          <input
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="试试黄花梨、购买、官网"
          />
        </label>
      </div>

      <div className="kb-explorer-tabs" role="tablist" aria-label="知识库视图">
        {tabs.map((tab) => (
          <button
            className={activeTab === tab.key ? "active" : ""}
            key={tab.key}
            onClick={() => resetExpand(tab.key)}
            type="button"
          >
            {tab.label}<small>{counts[tab.key]}</small>
          </button>
        ))}
      </div>

      <div className="kb-explorer-filters">
        <label>
          <span>来源类别</span>
          <select value={levelFilter} onChange={(event) => setLevelFilter(event.target.value)}>
            {levelOptions.map((option) => <option key={option}>{option}</option>)}
          </select>
        </label>
        <label>
          <span>来源状态</span>
          <select value={sourceFilter} onChange={(event) => setSourceFilter(event.target.value)}>
            {sourceOptions.map((option) => <option key={option}>{option}</option>)}
          </select>
        </label>
        <label>
          <span>关联类型</span>
          <select value={mappingFilter} onChange={(event) => setMappingFilter(event.target.value)}>
            {mappingOptions.map((option) => <option key={option}>{option}</option>)}
          </select>
        </label>
        <p>当前显示 <b>{rows.length}</b> 条。筛选只作用于对应视图，其余视图保留搜索。</p>
      </div>

      <div className="kb-explorer-results">
        {activeTab === "facts" && (rows as Fact[]).map((fact) => (
          <article className="kb-record" key={fact.id}>
            <button type="button" onClick={() => setExpandedId(expandedId === fact.id ? null : fact.id)}>
              <span className={`kb-pill level-${fact.evidenceLevel.toLowerCase()}`}>{levelLabel(fact.evidenceLevel)}</span>
              <b>{fact.id} · {fact.entityName}</b>
              <small>{fact.type}</small>
            </button>
            <p>{fact.statement}</p>
            {expandedId === fact.id && <div className="kb-record-detail">
              <DetailRow label="来源线索" value={joinIds(fact.sourceIds)} />
              <DetailRow label="证据线索" value={joinIds(fact.evidenceIds)} />
              <DetailRow label="关联问题" value={joinIds(fact.questionIds)} />
              <DetailRow label="可写表述" value={fact.allowedWording} />
              <DetailRow label="事实边界" value={fact.boundary} />
              <DetailRow label="更新时间" value={fact.updatedAt} />
            </div>}
          </article>
        ))}

        {activeTab === "entities" && (rows as Entity[]).map((entity) => (
          <article className="kb-record" key={entity.id}>
            <button type="button" onClick={() => setExpandedId(expandedId === entity.id ? null : entity.id)}>
              <span className="kb-pill neutral">{entity.type}</span>
              <b>{entity.id} · {entity.name}</b>
              <small>{joinIds(entity.sourceIds)}</small>
            </button>
            <p>{entity.description}</p>
            {expandedId === entity.id && <div className="kb-record-detail">
              <DetailRow label="来源线索" value={joinIds(entity.sourceIds)} />
              <DetailRow label="事实边界" value={entity.boundary} />
              <DetailRow label="更新时间" value={entity.updatedAt} />
            </div>}
          </article>
        ))}

        {activeTab === "sources" && (rows as Source[]).map((source) => (
          <article className="kb-record" key={source.id}>
            <button type="button" onClick={() => setExpandedId(expandedId === source.id ? null : source.id)}>
              <span className={`kb-pill ${source.usable ? "usable" : "review"}`}>{source.usable ? "可用" : "需复核"}</span>
              <b>{source.id} · {source.title}</b>
              <small>{source.grade} · {source.type}</small>
            </button>
            <p>{source.proves}</p>
            {expandedId === source.id && <div className="kb-record-detail">
              <DetailRow label="URL" value={source.url} />
              <DetailRow label="投递状态" value={source.status} />
              <DetailRow label="不能证明" value={source.boundary} />
              <DetailRow label="更新时间" value={source.updatedAt} />
            </div>}
          </article>
        ))}

        {activeTab === "questions" && (rows as QuestionMapping[]).map((item) => (
          <article className="kb-record" key={item.mapId}>
            <button type="button" onClick={() => setExpandedId(expandedId === item.mapId ? null : item.mapId)}>
              <span className={`kb-pill ${item.coverageStatus.includes("完整") ? "usable" : "review"}`}>{item.coverageStatus}</span>
              <b>{item.questionId} · {item.question}</b>
              <small>{joinIds(item.contentIds)}</small>
            </button>
            <p>关联事实：{joinIds(item.factIds)}</p>
            {expandedId === item.mapId && <div className="kb-record-detail">
              <DetailRow label="来源线索" value={joinIds(item.sourceIds)} />
              <DetailRow label="证据线索" value={joinIds(item.evidenceIds)} />
              <DetailRow label="内容关联" value={joinIds(item.contentIds)} />
              <DetailRow label="事实边界" value={item.boundary} />
              <DetailRow label="更新时间" value={item.updatedAt} />
            </div>}
          </article>
        ))}

        {activeTab === "faq" && (rows as FaqMapping[]).map((item) => (
          <article className="kb-record" key={item.mapId}>
            <button type="button" onClick={() => setExpandedId(expandedId === item.mapId ? null : item.mapId)}>
              <span className={`kb-pill ${item.methodConclusion ? "review" : "usable"}`}>{item.methodConclusion ? "方法结论" : "事实映射"}</span>
              <b>{item.faqId} · {item.question}</b>
              <small>{joinIds(item.relatedPages, "无相关页面")}</small>
            </button>
            <p>关联事实：{item.methodConclusion ? "研究方法结论" : joinIds(item.factIds)}</p>
            {expandedId === item.mapId && <div className="kb-record-detail">
              <DetailRow label="来源线索" value={joinIds(item.sourceIds)} />
              <DetailRow label="相关页面" value={joinIds(item.relatedPages)} />
              <DetailRow label="事实边界" value={item.boundary} />
              <DetailRow label="更新时间" value={item.updatedAt} />
            </div>}
          </article>
        ))}
      </div>
    </div>
  );
}
