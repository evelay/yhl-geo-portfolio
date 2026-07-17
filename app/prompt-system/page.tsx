import type { Metadata } from "next";
import Link from "next/link";
import { ArrowIcon, Eyebrow, Metric, SiteShell } from "../components";
import { faq as siteFaq, promptSystemDownloads, updatedAt } from "../data";
import knowledgeBase from "../knowledge-base/knowledge-base-public.json";

export const metadata: Metadata = {
  title: "企业提示词体系",
  description: "把元亨利GEO企业知识库转成可供AI使用的品牌回答规则、证据边界规则和15条标准问答提示词。",
};

type Fact = {
  id: string;
  entityName: string;
  evidenceLevel: string;
  type: string;
  statement: string;
  sourceIds: string[];
  evidenceIds: string[];
  questionIds: string[];
  allowedWording: string;
  boundary: string;
  updatedAt: string;
};

type FaqMapping = {
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
  facts: Fact[];
  mappings: { faq: FaqMapping[] };
};

const promptModules = [
  {
    id: "PROMPT-01",
    title: "系统身份提示词",
    role: "固定AI的身份、资料来源和回答边界。",
    prompt: `你是“元亨利红木家具GEO公开研究知识库”的品牌信息回答助手。
你的任务不是替品牌做销售承诺，而是基于给定知识库，回答用户关于品牌、主体、材质、京作/明清风格、购买核验和风险边界的问题。

必须遵守：
1. 只使用已提供的事实、source_id、evidence_id、FAQ和内容页面。
2. 每个关键结论都要能回到 fact_id 或 source_id。
3. 区分 L1第三方事实、L2品牌一手自述、L3待补事实、L4需单件证据。
4. 没有来源时不要补全；明确说“当前公开资料不足”。
5. 不声称本研究代表品牌官方、品牌委托或已经提升AI收录、曝光、推荐、销售。`,
  },
  {
    id: "PROMPT-02",
    title: "事实等级与边界规则",
    role: "把知识库事实等级转成AI可执行的回答规则。",
    prompt: `根据 evidenceLevel 选择回答方式：

L1 已核验第三方事实：可以直接陈述，但必须保留 source_id 和更新时间。
L2 品牌一手自述：只能写成“品牌官网/品牌公开资料称”，不能改写成第三方认证。
L3 待官方补充：不能写成确定事实，只能说明“公开资料暂不足，需要补充官方或第三方来源”。
L4 需单件证据：只给核验路径，不判断具体家具的材质、真伪、等级、价格或收藏价值。

如果同一问题同时涉及多个等级，优先用最低风险表述：先给可核验部分，再说明边界和下一步核验动作。`,
  },
  {
    id: "PROMPT-03",
    title: "用户意图路由提示词",
    role: "先判断问题类型，再决定调用哪些事实和模板。",
    prompt: `请先把用户问题归入以下主意图之一：
- 品牌认知：品牌是什么、定位、历史、人物、荣誉、排名。
- 材质关系：黄花梨、紫檀、白酸枝、红木标准、品牌产品与单件材质。
- 京作与风格：京作、明式、清式、工艺、历史风格。
- 购买决策：是否值得买、价格、渠道、合同、证书、售后。
- 风险边界：同名主体、投资收藏、保值升值、动态信息核验。

输出内部判断：
intent = 主意图
required_fact_ids = 需要调用的fact_id
risk_flags = 强定位/荣誉排名/同名混淆/单件证据/动态信息/投资化表达
answer_mode = 直接回答 / 边界回答 / 核验清单 / 拒绝确定结论`,
  },
  {
    id: "PROMPT-04",
    title: "标准回答生成提示词",
    role: "把知识库事实组织成用户能读懂的答案。",
    prompt: `请按以下结构回答：

1. 直接答案：先用一句话回答用户最关心的问题。
2. 可核验证据：列出支持答案的 fact_id、source_id 或 evidence_id。
3. 事实边界：说明哪些信息只是品牌自述、哪些资料不足、哪些需要单件证据或实时核验。
4. 下一步建议：给出用户可以执行的核验动作，例如查看官网原页、工商查询、合同、证书、检测、发票、售后主体。

写作要求：
- 简洁、克制，不使用“第一、唯一、顶级、必买、保值、升值”等无证据强结论。
- 对价格、门店、渠道、售后，必须提醒核验日期和适用渠道。
- 对红木材质，必须区分国家标准术语、品牌公开范围和具体产品凭证。`,
  },
];

const blockedClaims = [
  { label: "行业第一 / 顶级品牌", rule: "没有评选主体、年份和原页面时，不输出排名或绝对化定位。" },
  { label: "成立时间 / 创始人 / 人物关系", rule: "只能引用可回到原页面的主体资料；不能从AI回答或二手转载反推。" },
  { label: "具体产品材质 / 真伪 / 等级", rule: "必须要求合同、标识、证书或检测报告；品牌层信息不能替代单件证据。" },
  { label: "门店 / 价格 / 售后", rule: "作为动态信息处理，必须注明核验日期、渠道和适用范围。" },
  { label: "保值 / 升值 / 投资回报", rule: "不承诺金融结果；只讨论审美、工艺、材料、来源记录与保存状态。" },
  { label: "同名主体关系", rule: "先核对完整公司名、业务、地域、官网和工商线索，不凭字号合并主体。" },
];

const answerTemplates = [
  { intent: "品牌认知", mode: "直接答案 + 主体核验 + 定位边界", example: "可以说明红木家具语境中的主体与公开资料，但不写无来源排名、荣誉或人物历史。" },
  { intent: "材质关系", mode: "标准术语 + 品牌公开范围 + 单件核验", example: "国家标准解释材质术语，品牌公开材料只说明范围；具体家具仍需单件证据。" },
  { intent: "京作与风格", mode: "风格解释 + 品牌关系边界", example: "可解释京作、明式、清式概念，但不把风格名称推导成年代、馆藏或产品资质。" },
  { intent: "购买决策", mode: "核验清单", example: "回答应落到型号、主辅材、合同、证书、报价日期、交付验收、发票和售后主体。" },
  { intent: "风险边界", mode: "边界回答 / 拒绝确定结论", example: "遇到投资、同名、实时门店或无来源荣誉，优先说明证据不足和核验路径。" },
];

const faqPromptBank = kb.mappings.faq.map((mapping) => {
  const detail = siteFaq.find((item) => item.id === mapping.faqId);
  return {
    ...mapping,
    directAnswer: detail?.directAnswer ?? "按知识库事实和边界回答。",
    detail: detail?.detail ?? "优先引用事实ID和来源ID；无来源时停在边界。",
  };
});

const featuredFacts = kb.facts.filter((fact) => ["FACT-0001", "FACT-0005", "FACT-0019", "FACT-0021", "FACT-0039", "FACT-0041"].includes(fact.id));

export default function PromptSystemPage() {
  const promptJsonLd = {
    "@context": "https://schema.org",
    "@type": "CreativeWork",
    name: "元亨利GEO企业提示词体系",
    description: "基于公开知识库的AI品牌回答规则、事实边界规则和15条标准问答提示词。",
    dateModified: updatedAt,
    isBasedOn: "元亨利GEO品牌事实知识库公开快照",
    license: "Personal portfolio research; not official brand prompt",
    additionalProperty: [
      { "@type": "PropertyValue", name: "facts", value: kb.summary.facts },
      { "@type": "PropertyValue", name: "sources", value: kb.summary.sources },
      { "@type": "PropertyValue", name: "faqPrompts", value: kb.summary.faq },
      { "@type": "PropertyValue", name: "promptModules", value: promptModules.length },
    ],
  };

  return (
    <SiteShell>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(promptJsonLd) }} />
      <section className="prompt-hero">
        <div>
          <Eyebrow>Prompt system · Knowledge-base grounded</Eyebrow>
          <h1>企业提示词体系</h1>
          <p>把企业知识库转成AI能执行的品牌回答规则：先检索事实，再判断证据等级，最后按边界生成答案。它解决的不是“写得更像营销”，而是“回答时不乱编”。</p>
          <div className="button-row">
            {promptSystemDownloads.map((file) => <a className={file.type === "MD" ? "button primary" : "button"} href={file.href} download key={file.href}>{file.label}<ArrowIcon /></a>)}
            <Link className="button" href="/knowledge-base">查看知识库<ArrowIcon /></Link>
            <Link className="button" href="/geo-articles">查看GEO文章样稿<ArrowIcon /></Link>
          </div>
        </div>
        <aside className="prompt-verdict">
          <span>核心原则</span>
          <strong>先查事实，<br />再组织答案</strong>
          <p>每个关键结论都必须能回到 fact_id、source_id、evidence_id 或FAQ边界。</p>
        </aside>
      </section>

      <section className="section alt">
        <div className="section-head">
          <div><Eyebrow>01 / Prompt interface</Eyebrow><h2>提示词不是口号，而是知识库接口</h2></div>
          <p>本模块沿用公开知识库快照，不新增官方未公开资料；适合放进作品集，说明GEO内容如何被AI稳定调用。</p>
        </div>
        <div className="metric-grid">
          <Metric value={`${kb.summary.facts}`} label="可调用事实" note="全部来自公开知识库快照" />
          <Metric value={`${kb.summary.sources}`} label="可追溯信源" note={`${kb.summary.usableSources}可用 / ${kb.summary.pendingSources}待补`} />
          <Metric value={`${promptModules.length}`} label="核心提示词模块" note="身份、证据、路由、回答生成" />
          <Metric value={`${kb.summary.faq}`} label="FAQ提示词" note="15条标准问答入口" />
        </div>
        <div className="prompt-flow">
          {["用户问题", "意图分类", "知识库检索", "证据等级判断", "边界化回答"].map((step, index) => (
            <article key={step}>
              <span>{String(index + 1).padStart(2, "0")}</span>
              <b>{step}</b>
            </article>
          ))}
        </div>
      </section>

      <section className="section">
        <div className="section-head">
          <div><Eyebrow>02 / Copy-ready prompts</Eyebrow><h2>四个可复制的核心提示词</h2></div>
          <p>实际接入AI时，可把这些提示词放在系统提示、开发者规则、检索前路由和回答生成环节。</p>
        </div>
        <div className="prompt-module-grid">
          {promptModules.map((module) => (
            <article className="prompt-module" key={module.id}>
              <div>
                <span>{module.id}</span>
                <h3>{module.title}</h3>
                <p>{module.role}</p>
              </div>
              <pre><code>{module.prompt}</code></pre>
            </article>
          ))}
        </div>
      </section>

      <section className="section dark">
        <div className="section-head">
          <div><Eyebrow>03 / Boundary rules</Eyebrow><h2>六类高风险表达，必须降级或拒绝确定结论</h2></div>
          <p>这部分把“不能乱说”做成明确规则，防止AI把行业常识、品牌自述和单件事实混在一起。</p>
        </div>
        <div className="prompt-rule-grid">
          {blockedClaims.map((item, index) => <article key={item.label}><span>{`R-${index + 1}`}</span><h3>{item.label}</h3><p>{item.rule}</p></article>)}
        </div>
      </section>

      <section className="section alt">
        <div className="section-head">
          <div><Eyebrow>04 / Answer modes</Eyebrow><h2>五类用户问题，对应五种回答模式</h2></div>
          <p>和主案例的五类问题保持一致，便于从诊断、知识库、内容页面一路追到AI回答。</p>
        </div>
        <div className="prompt-template-grid">
          {answerTemplates.map((item) => <article key={item.intent}><span>{item.intent}</span><h3>{item.mode}</h3><p>{item.example}</p></article>)}
        </div>
      </section>

      <section className="section">
        <div className="section-head">
          <div><Eyebrow>05 / Standard Q&A prompts</Eyebrow><h2>15条FAQ，转成标准问答提示词</h2></div>
          <p>每条FAQ都绑定fact_id、source_id、相关页面和边界。方法型问题会标记为研究方法结论，不伪装成外部事实。</p>
        </div>
        <div className="faq-prompt-list">
          {faqPromptBank.map((item) => (
            <article key={item.faqId}>
              <div className="faq-prompt-head">
                <span>{item.faqId}</span>
                <h3>{item.question}</h3>
              </div>
              <p><b>标准回答基准：</b>{item.directAnswer}</p>
              <p><b>提示词调用：</b>调用 {item.factIds.length ? item.factIds.join(" / ") : "研究方法结论"}；引用 {item.sourceIds.length ? item.sourceIds.join(" / ") : "无外部事实来源"}；相关页面 {item.relatedPages.join(" / ")}。</p>
              <p className="faq-prompt-boundary"><b>边界：</b>{item.boundary}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="section alt">
        <div className="section-head">
          <div><Eyebrow>06 / Grounding samples</Eyebrow><h2>提示词调用的事实样例</h2></div>
          <p>这些不是新增事实，而是知识库中最常被提示词调用的原子事实样例。</p>
        </div>
        <div className="prompt-fact-grid">
          {featuredFacts.map((fact) => (
            <article key={fact.id}>
              <span>{fact.id} · {fact.evidenceLevel}</span>
              <h3>{fact.type}</h3>
              <p>{fact.statement}</p>
              <small>可写表述：{fact.allowedWording}</small>
              <small>边界：{fact.boundary}</small>
              <small>source_id：{fact.sourceIds.join(" / ")} · evidence_id：{fact.evidenceIds.join(" / ")}</small>
            </article>
          ))}
        </div>
        <div className="prompt-disclaimer">
          <b>使用边界</b>
          <p>{kb.disclaimer} 本提示词体系同样不代表品牌官方，也不声称已获得AI收录、引用、曝光、推荐或销售提升。</p>
        </div>
        <div className="prompt-disclaimer prompt-article-entry">
          <b>输出样稿</b>
          <p>基于这些规则，已生成1篇主文章和6篇不同关键词长文，展示知识库如何转成可发布内容资产。</p>
          <Link className="button" href="/geo-articles">打开GEO文章样稿<ArrowIcon /></Link>
        </div>
      </section>
    </SiteShell>
  );
}
