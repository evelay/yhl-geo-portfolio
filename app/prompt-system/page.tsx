import type { Metadata } from "next";
import Link from "next/link";
import { ArrowIcon, Eyebrow, Metric, ProjectDisclaimer, SiteShell } from "../components";
import { knowledgeDownloads, updatedAt } from "../data";
import knowledgeBase from "../knowledge-base/knowledge-base-public.json";

export const metadata: Metadata = {
  title: "提示词体系公开说明",
  description: "元亨利 GEO 作品集中的提示词体系公开说明：方法、流程、输入输出结构、审核节点和使用边界。",
};

const kb = knowledgeBase as {
  summary: Record<string, number>;
};

const designGoals = [
  "让回答先回到公开事实和来源，再组织面向用户的表达。",
  "把品牌自述、第三方资料和单件购买证据分开处理。",
  "遇到排名、荣誉、价格、售后、收藏结果等高风险内容时，优先停在核验路径。",
  "保留人工审核节点，不把示范内容写成品牌官方发布稿。",
];

const workflow = [
  "接收用户问题",
  "识别问题类别",
  "查找公开知识库",
  "核对来源与事实边界",
  "生成克制回答",
  "人工发布检查",
];

const inputGroups = [
  { title: "用户问题", detail: "原始问法、场景和是否涉及购买或评价。" },
  { title: "公开事实", detail: "已审核事实、可用 source_id、更新时间和适用范围。" },
  { title: "边界信息", detail: "品牌自述、动态信息、单件证据、不可确认项。" },
  { title: "发布目标", detail: "FAQ、页面摘要、研究说明或内部审核记录。" },
];

const outputStructure = [
  { title: "直接回答", detail: "用一句话回答可以确认的部分。" },
  { title: "可核验依据", detail: "列出公开来源或说明需要回到哪类原始凭证。" },
  { title: "事实边界", detail: "说明哪些内容不能写成确定事实。" },
  { title: "下一步核验", detail: "给出可执行的查询、合同、证书或日期复核动作。" },
];

const reviewNodes = [
  "source_id 是否存在且可追溯。",
  "是否误用了待复核事实或不可用来源。",
  "是否出现未经确认的排名、荣誉、人物、成立时间或主体关系。",
  "是否包含保值、升值、推荐、收录、曝光或销售效果承诺。",
  "是否会被误解为品牌官方提示词或正式发布稿。",
];

const usageLimits = [
  "公开页面只说明方法，不提供完整可复制的企业提示词。",
  "完整版本为内部研究资产，不公开展示。",
  "示例仅用于解释结构，不可直接用于批量生成品牌内容。",
  "输出仍需人工审核后才能进入公开页面或下载文件。",
];

export default function PromptSystemPage() {
  const promptJsonLd = {
    "@context": "https://schema.org",
    "@type": "CreativeWork",
    name: "元亨利 GEO 提示词体系公开说明",
    description: "基于公开知识库的提示词方法说明、工作流程、输入输出结构和使用边界。",
    dateModified: updatedAt,
    isBasedOn: "安全过滤版公开知识库快照",
    license: "Personal portfolio research; not official brand prompt",
    additionalProperty: [
      { "@type": "PropertyValue", name: "publicFacts", value: kb.summary.facts },
      { "@type": "PropertyValue", name: "publicSources", value: kb.summary.sources },
      { "@type": "PropertyValue", name: "publicFaq", value: kb.summary.faq },
    ],
  };

  return (
    <SiteShell>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(promptJsonLd) }} />
      <section className="prompt-hero">
        <div>
          <Eyebrow>Prompt system · Public summary</Eyebrow>
          <h1>提示词体系公开说明</h1>
          <p>本页只展示提示词体系的方法、流程和审核边界，用来说明 GEO 内容如何从公开知识库生成可核验回答。完整版本为内部研究资产，不公开展示。</p>
          <ProjectDisclaimer />
          <div className="button-row">
            {knowledgeDownloads.map((file) => <a className="button primary" href={file.href} download key={file.href}>{file.label}<ArrowIcon /></a>)}
            <Link className="button" href="/knowledge-base">查看知识库<ArrowIcon /></Link>
            <Link className="button" href="/geo-articles">查看文章审核状态<ArrowIcon /></Link>
          </div>
        </div>
        <aside className="prompt-verdict">
          <span>公开边界</span>
          <strong>讲方法，<br />不公开完整提示词</strong>
          <p>公开内容只保留可解释的结构和示例，不提供可复制的企业级操作细节。</p>
        </aside>
      </section>

      <section className="section alt">
        <div className="section-head">
          <div><Eyebrow>01 / Goals</Eyebrow><h2>设计目标</h2></div>
          <p>提示词体系的核心是降低无来源扩写风险，而不是制造更强的营销语气。</p>
        </div>
        <div className="metric-grid">
          <Metric value={`${kb.summary.facts}`} label="公开事实" note="来自安全快照" />
          <Metric value={`${kb.summary.sources}`} label="公开信源" note="source_id 可追溯" />
          <Metric value={`${kb.summary.faq}`} label="公开FAQ映射" note="仅保留已审核项" />
          <Metric value="1" label="脱敏示例" note="不可用于批量生产" />
        </div>
        <div className="prompt-rule-grid">
          {designGoals.map((goal, index) => <article key={goal}><span>{`G-${index + 1}`}</span><p>{goal}</p></article>)}
        </div>
      </section>

      <section className="section">
        <div className="section-head">
          <div><Eyebrow>02 / Workflow</Eyebrow><h2>工作流程</h2></div>
          <p>从用户问题到公开回答，中间必须经过来源、事实边界和人工审核。</p>
        </div>
        <div className="prompt-flow">
          {workflow.map((step, index) => (
            <article key={step}>
              <span>{String(index + 1).padStart(2, "0")}</span>
              <b>{step}</b>
            </article>
          ))}
        </div>
      </section>

      <section className="section alt">
        <div className="section-head">
          <div><Eyebrow>03 / Interface</Eyebrow><h2>输入与输出结构</h2></div>
          <p>公开版只展示字段类别，不暴露完整内部字段、审查逻辑或可复制提示词。</p>
        </div>
        <div className="prompt-template-grid">
          {inputGroups.map((item) => <article key={item.title}><span>输入类别</span><h3>{item.title}</h3><p>{item.detail}</p></article>)}
        </div>
        <div className="prompt-template-grid prompt-output-grid">
          {outputStructure.map((item) => <article key={item.title}><span>输出段落</span><h3>{item.title}</h3><p>{item.detail}</p></article>)}
        </div>
      </section>

      <section className="section dark">
        <div className="section-head">
          <div><Eyebrow>04 / Human review</Eyebrow><h2>人工审核节点</h2></div>
          <p>公开发布前，审核人需要确认每个结论仍停在公开资料可以支持的范围内。</p>
        </div>
        <div className="prompt-rule-grid">
          {reviewNodes.map((node, index) => <article key={node}><span>{`R-${index + 1}`}</span><p>{node}</p></article>)}
        </div>
      </section>

      <section className="section alt">
        <div className="section-head">
          <div><Eyebrow>05 / Sanitized sample</Eyebrow><h2>脱敏短示例</h2></div>
          <p>示例只展示回答形态，不包含提示词全文或可批量复用的操作细节。</p>
        </div>
        <div className="prompt-disclaimer">
          <b>示例问题</b>
          <p>“这个红木家具品牌适合购买吗？”</p>
        </div>
        <div className="prompt-disclaimer prompt-article-entry">
          <b>公开示例输出</b>
          <p>先核对主体、官网与公开来源，再查看具体产品的合同、主辅材、证书、检测、发票和售后主体。公开研究不能替用户作出确定购买建议，也不能承诺价格、保值、升值或平台展示效果。</p>
        </div>
      </section>

      <section className="section">
        <div className="section-head">
          <div><Eyebrow>06 / Boundaries</Eyebrow><h2>使用边界</h2></div>
          <p>本页保留方法透明度，同时把完整提示词、内部操作细节和未审核输出留在内部复核链路。</p>
        </div>
        <div className="prompt-template-grid">
          {usageLimits.map((limit) => <article key={limit}><span>边界</span><h3>公开限制</h3><p>{limit}</p></article>)}
        </div>
      </section>
    </SiteShell>
  );
}
