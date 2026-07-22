import Link from "next/link";
import type { Metadata } from "next";
import { ArrowIcon, Eyebrow, GroupedMetricChart, PlatformMetricCards, SiteShell, StackedRiskBar, VisibleBreadcrumbs } from "../components";
import {
  platformSummary,
  portfolioOverview,
  riskDistribution,
  siteUrl,
} from "../data";

export const metadata: Metadata = {
  title: "AI 搜索诊断",
  description: "AI 搜索诊断：围绕元亨利品牌身份、材质与产品、京作与风格、购买核验和价值判断进行五平台同题测试。",
  alternates: { canonical: `${siteUrl}/experiment/` },
};

const schema = {
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "WebPage",
      "@id": `${siteUrl}/experiment/#webpage`,
      url: `${siteUrl}/experiment/`,
      name: "AI 搜索诊断",
      description: "五个平台、24个核心问题、120条完整回答的聚合诊断页面。",
      inLanguage: "zh-CN",
    },
    {
      "@type": "Dataset",
      "@id": `${siteUrl}/experiment/#dataset`,
      name: "元亨利五平台 AI 回答聚合诊断数据",
      description: "5个平台、24个核心问题、120条回答的公开聚合指标和短案例，不包含回答全文。",
      inLanguage: "zh-CN",
      isPartOf: {
        "@id": `${siteUrl}/experiment/#webpage`,
      },
    },
    {
      "@type": "BreadcrumbList",
      itemListElement: [
        { "@type": "ListItem", position: 1, name: "首页", item: `${siteUrl}/` },
        { "@type": "ListItem", position: 2, name: "AI 搜索诊断", item: `${siteUrl}/experiment/` },
      ],
    },
  ],
};

const schemaJson = JSON.stringify(schema).replace(/</g, "\\u003c");

const diagnosticGoals = [
  {
    title: "AI是否真正理解了品牌",
    body: "检查回答是否区分元亨利红木家具品牌、相关企业主体、其他同名机构和《周易》中的“元亨利贞”。",
  },
  {
    title: "回答中的事实是否可靠",
    body: "判断成立时间、官网、材质、行业身份、馆藏和荣誉等内容是否与公开资料一致，并有来源支持。",
  },
  {
    title: "专业信息是否保持边界",
    body: "检查AI是否会把材料线索扩大为品牌全部产品，把京作或明清风格写成正式身份或年代证明，把品牌宣传扩大为长期经营事实。",
  },
  {
    title: "购买建议是否足够谨慎",
    body: "购买建议应回到合同主体、材质、证书、检测、交付和售后，而不是直接从品牌声誉推导回购、保值或投资价值。",
  },
];

const questionSources = [
  {
    title: "品牌公开信息中的歧义",
    body: "企业主体、成立时间、官网来源、同名对象、行业身份和公开荣誉。",
  },
  {
    title: "用户了解与购买红木家具的决策路径",
    body: "材质、风格、合同、证书、检测、售后、品牌比较和价值判断。",
  },
  {
    title: "AI回答中容易出现的错误模式",
    body: "对象错配、来源不支撑、强品牌背书、材料关系扩大和投资判断过度。",
  },
];

const questionFilters = [
  "与品牌理解或用户决策相关",
  "容易出现事实或边界问题",
  "可以跨平台统一测试",
  "适合后续同题复测",
];

const scenarioRows = [
  ["品牌认知", "元亨利是什么品牌？", "是否识别正确对象和品牌定位"],
  ["主体与来源", "企业主体和“元亨利红木家具”应如何表述？", "是否区分企业、品牌和官网来源"],
  ["材质与产品", "白酸枝家具和元亨利可能有哪些关联？", "是否把材料线索扩大为全量产品事实"],
  ["京作与风格", "元亨利与京作红木家具有什么关系？", "是否无依据认定身份、资质或传承关系"],
  ["购买核验", "评估元亨利时应关注哪些因素？", "是否回到合同、材质和单件产品证据"],
  ["价值判断", "是否具有收藏或投资价值？", "是否谨慎处理保值和升值结论"],
];

const resultCards = [
  {
    value: "70.8%",
    title: "85/120条回答明确提及元亨利",
    body: "品牌在多数回答中出现，但部分回答仍然存在对象、主体和定位混淆。",
  },
  {
    value: "80.0%",
    title: "96/120条回答显示可见链接",
    body: "可见链接较为常见，但链接存在不等于来源能够支持回答中的主要结论。",
  },
  {
    value: "60.8%",
    title: "73/120条回答被标记为高或严重信息风险",
    body: "风险主要来自对象错配、事实冲突、强背书、来源不支撑和边界不足，不代表这些回答的全部内容都错误。",
  },
  {
    value: "4条",
    title: "出现严重对象识别错误",
    body: "其中4条回答将品牌问题转向《周易》中的“元亨利贞”。",
  },
];

const riskFocus = [
  "品牌对象与常见误判",
  "京作与身份资质",
  "紫檀与白酸枝关系",
  "购买与售后承诺",
  "收藏与投资判断",
];

const cases = [
  {
    type: "对象识别",
    summary: "部分回答将“元亨利”理解为“元亨利贞”，内容转向乾卦、训诂和古文解释。",
    optimization: "建设品牌事实页和同名主体消歧内容。",
  },
  {
    type: "身份资质",
    summary: "部分回答直接使用“京作代表”“非遗单位”或其他正式身份表述，却没有相应权威来源。",
    optimization: "建设京作与明清概念边界内容，并为身份类结论设置来源要求。",
  },
  {
    type: "价值判断",
    summary: "部分回答将紫檀、白酸枝、品牌历史或工艺描述，进一步推导为回购、保值和升值能力。",
    optimization: "建设材质边界、购买核验指南和收藏投资风险提示。",
  },
];

export default function ExperimentPage() {
  const sample = portfolioOverview.sample;
  const groupedMetricData = platformSummary.platforms.map((platform) => ({
    platform: platform.platform_name,
    metrics: [
      { label: "事实准确性", value: platform.public_metric_averages.factReliability },
      { label: "回答完整性", value: platform.public_metric_averages.answerCompleteness },
      { label: "来源可追溯性", value: platform.public_metric_averages.sourceSupport },
      { label: "信息边界控制", value: platform.public_metric_averages.boundaryControl },
    ],
  }));

  return (
    <SiteShell>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: schemaJson }} />
      <section className="portfolio-page-hero">
        <Eyebrow>{sample.platform_count}个AI平台 / {sample.question_count}个核心问题 / {sample.response_count}条完整回答</Eyebrow>
        <VisibleBreadcrumbs items={[{ label: "首页", href: "/" }, { label: "AI 搜索诊断" }]} />
        <h1>AI 搜索诊断</h1>
        <p className="lede">我使用24个核心问题，在豆包、文心一言、通义千问、Kimi和腾讯元宝上采集120条完整回答，观察AI能否识别正确对象、提供稳健事实、引用有效来源，并在购买判断中保持必要边界。</p>
        <div className="sample-strip" aria-label="诊断样本">
          {["豆包", "文心一言", "通义千问", "Kimi", "腾讯元宝", "24个核心问题", "120条完整回答"].map((item) => <span key={item}>{item}</span>)}
        </div>
      </section>

      <div className="portfolio-page">
        <section className="content-section">
          <h2>五个平台关键维度对比</h2>
          <div className="chart-card full-chart-card">
            <h3>事实、完整性、来源与边界</h3>
            <p>事实准确性、回答完整性、来源可追溯性、信息边界控制。指标范围0—2分，来自项目自定义人工量表。</p>
            <GroupedMetricChart data={groupedMetricData} />
            <PlatformMetricCards data={groupedMetricData} />
          </div>
          <p className="safe-note">各指标来自项目自定义人工量表。本页的平台排列仅为固定展示顺序，不用于比较平台整体优劣。</p>
        </section>

        <section className="content-section">
          <h2>回答风险等级分布</h2>
          <div className="chart-card full-chart-card">
            <h3>低、中等、高、严重风险</h3>
            <p>低风险=核心对象和事实相对稳健；中等风险=方向基本可用但存在缺证或边界不足；高风险=可能影响品牌认知或购买判断；严重风险=对象明显错误或核心任务完全偏离。</p>
            <StackedRiskBar data={riskDistribution} />
          </div>
          <p className="safe-note">风险等级用于信息质量诊断；各项指标分别呈现，不合并为单一总分，也不形成平台整体优劣结论。</p>
        </section>

        <section className="content-section">
          <h2>诊断目标</h2>
          <div className="compact-grid">
            {diagnosticGoals.map((item) => <p key={item.title}><b>{item.title}</b><br />{item.body}</p>)}
          </div>
        </section>

        <section className="content-section">
          <h2>测试问题如何产生</h2>
          <div className="problem-grid three-card-grid">
            {questionSources.map((item, index) => (
              <article key={item.title}>
                <span>{String(index + 1).padStart(2, "0")}</span>
                <h3>{item.title}</h3>
                <p>{item.body}</p>
              </article>
            ))}
          </div>
          <div className="section-subhead"><h3>24个核心问题的筛选依据</h3></div>
          <div className="tag-grid">
            {questionFilters.map((item) => <span key={item}>{item}</span>)}
          </div>
        </section>

        <section className="content-section">
          <h2>核心问题覆盖场景</h2>
          <div className="table-scroll">
            <table className="data-table">
              <thead><tr><th>测试场景</th><th>代表问题</th><th>主要观察内容</th></tr></thead>
              <tbody>{scenarioRows.map(([scenario, question, focus]) => <tr key={scenario}><td>{scenario}</td><td>{question}</td><td>{focus}</td></tr>)}</tbody>
            </table>
          </div>
        </section>

        <section className="content-section">
          <h2>回答如何判断</h2>
          <div className="tag-grid scoring-tags">
            {["品牌对象", "事实准确性", "回答完整性", "来源可追溯性", "信息边界控制", "推荐质量", "信息风险等级"].map((item) => <span key={item}>{item}</span>)}
          </div>
          <p className="safe-note">各项指标采用项目自定义人工量表。部分指标只适用于特定问题，空白表示不适用，不按零分计算。</p>
        </section>

        <section className="content-section">
          <h2>整体诊断结果</h2>
          <div className="metric-list-grid">
            {resultCards.map((item) => (
              <article key={item.title}>
                <strong>{item.value}</strong>
                <h3>{item.title}</h3>
                <p>{item.body}</p>
              </article>
            ))}
          </div>
        </section>

        <section className="content-section">
          <h2>风险集中在哪些问题</h2>
          <div className="tag-grid">{riskFocus.map((item) => <span key={item}>{item}</span>)}</div>
        </section>

        <section className="content-section">
          <h2>三个代表案例</h2>
          <div className="case-grid">
            {cases.map((item) => (
              <article key={item.type}>
                <span>问题类型</span>
                <h3>{item.type}</h3>
                <p><b>风险摘要：</b>{item.summary}</p>
                <small><b>对应内容优化：</b>{item.optimization}</small>
              </article>
            ))}
          </div>
        </section>

        <section className="content-section">
          <h2>诊断如何转化为内容优化</h2>
          <div className="text-list two-col">
            {["品牌主体与同名消歧", "材质与文化概念边界", "购买与价值判断", "事实与来源对应"].map((item) => <p key={item}>{item}</p>)}
          </div>
          <div className="button-row table-action-row">
            <Link className="button primary" href="/content-governance">查看内容策略<ArrowIcon /></Link>
            <Link className="button" href="/facts">查看品牌事实<ArrowIcon /></Link>
            <Link className="button" href="/buying-guide">查看购买核验指南<ArrowIcon /></Link>
          </div>
        </section>

        <section className="content-section">
          <h2>方法说明与限制</h2>
          <p>本轮数据来自特定时间、问题集和平台模式。评分采用项目自定义人工量表，并经过抽样复核。平台模型、联网结果和检索来源可能随时间变化，因此本轮结果用于诊断问题，不用于生成跨平台优劣结论或前后效果归因。</p>
        </section>
      </div>
    </SiteShell>
  );
}
