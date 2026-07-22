import Link from "next/link";
import type { Metadata } from "next";
import { ArrowIcon, Eyebrow, SiteShell, VisibleBreadcrumbs } from "../components";
import { siteUrl } from "../data";

export const metadata: Metadata = {
  title: "研究方法",
  description: "研究方法：说明问题从哪里来、为什么选择24个核心问题、为什么选择五个平台、如何采集、如何评分与复核、当前限制与下一轮验证。",
  alternates: { canonical: `${siteUrl}/methodology/` },
};

const schema = {
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "WebPage",
      "@id": `${siteUrl}/methodology/#webpage`,
      url: `${siteUrl}/methodology/`,
      name: "研究方法",
      description: "解释问题设计、平台选择、采集方式、评分复核、当前限制与下一轮验证。",
      inLanguage: "zh-CN",
    },
    {
      "@type": "BreadcrumbList",
      itemListElement: [
        { "@type": "ListItem", position: 1, name: "首页", item: `${siteUrl}/` },
        { "@type": "ListItem", position: 2, name: "研究方法", item: `${siteUrl}/methodology/` },
      ],
    },
  ],
};

const schemaJson = JSON.stringify(schema).replace(/</g, "\\u003c");

const framework = ["定义业务问题", "设计测试问题", "统一采集回答", "进行人工判断", "抽样复核与结果分析"];

const questionSources = [
  {
    title: "品牌公开资料中的信息歧义",
    body: "主体、时间、官网、同名对象和公开荣誉等信息需要分开核验。",
  },
  {
    title: "用户购买决策路径",
    body: "用户会围绕材质、风格、合同、证书、检测、售后和价值判断继续追问。",
  },
  {
    title: "AI回答中的常见错误",
    body: "对象错配、来源不支撑、强品牌背书和边界越界会反复出现。",
  },
];

const questionFilters = [
  "与品牌理解或用户决策相关",
  "容易出现事实或边界问题",
  "可以跨平台统一测试",
  "适合后续同题复测",
];

const scenarioRows = [
  ["品牌认知与事实", "元亨利是什么品牌？", "对象识别与品牌定位"],
  ["主体与来源核验", "企业主体和“元亨利红木家具”应如何表述？", "品牌、字号、企业和官网来源"],
  ["材质与产品边界", "白酸枝家具和元亨利可能有哪些关联？", "是否扩大为全量产品事实"],
  ["京作与风格概念", "元亨利与京作红木家具有什么关系？", "是否无依据认定身份或资质"],
  ["购买与品牌比较", "评估元亨利时应关注哪些因素？", "是否落到合同和单件核验"],
  ["来源价值与信息边界", "是否具有收藏或投资价值？", "是否谨慎处理升值结论"],
];

const collectionSteps = [
  "使用相同问题",
  "保存完整回答",
  "记录可见来源",
  "固定采集窗口",
  "不对回答进行二次追问",
];

const scoringDimensions = [
  "品牌是否被提及",
  "品牌定位是否准确",
  "事实准确性",
  "回答完整性",
  "来源可追溯性",
  "信息边界控制",
  "推荐质量",
  "信息风险等级",
];

const scoreRules = [
  ["0分", "明显错误、严重缺失或清楚越界"],
  ["1分", "部分满足，但存在疑点、来源不足或边界不完整"],
  ["2分", "主要内容相对稳健，来源和边界较清楚"],
  ["空白", "指标不适用于当前问题，不按零分计算"],
];

const biasControls = ["评分校准", "同题横向判断", "保留具体判断依据", "抽样复核"];

const consistencyItems = [
  "保存原始回答",
  "分离回答和评分",
  "保留修正记录",
  "使用固定分析口径",
];

const limitations = [
  "数据来自特定时间",
  "单人评分存在主观性",
  "可见链接不等于来源已验证",
  "不是品牌官方项目",
  "目前不是严格前后测",
];

const nextValidation = [
  "使用同一问题集",
  "使用同一平台范围",
  "保持相近提问方式",
  "使用相同判断标准",
  "记录外部变化",
  "获得授权后增加真实业务数据",
];

const validationFlow = ["内容上线", "等待抓取", "同题复测", "人工评分", "对比变化", "核查外部因素"];

export default function MethodologyPage() {
  return (
    <SiteShell>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: schemaJson }} />
      <section className="portfolio-page-hero">
        <Eyebrow>方法与限制</Eyebrow>
        <VisibleBreadcrumbs items={[{ label: "首页", href: "/" }, { label: "研究方法" }]} />
        <h1>研究方法</h1>
        <p className="lede">本项目从品牌公开信息、用户购买决策和 AI 回答风险出发，建立统一的问题集、采集方式和人工判断标准。</p>
        <p className="lede">研究重点不是单纯统计品牌出现次数，而是进一步检查回答能否识别正确对象、使用可核验事实、匹配有效来源，并在材质、购买和价值判断中保持必要边界。</p>
      </section>

      <div className="portfolio-page">
        <section className="content-section">
          <h2>整体研究框架</h2>
          <div className="methodology-timeline" aria-label="整体研究框架">
            {framework.map((step, index) => (
              <article key={step}>
                <span>{String(index + 1).padStart(2, "0")}</span>
                <b>{step}</b>
              </article>
            ))}
          </div>
        </section>

        <section className="content-section" id="question-design">
          <h2>测试问题如何设计</h2>
          <h3>问题来源</h3>
          <div className="problem-grid three-card-grid">
            {questionSources.map((item, index) => (
              <article key={item.title}>
                <span>{String(index + 1).padStart(2, "0")}</span>
                <h3>{item.title}</h3>
                <p>{item.body}</p>
              </article>
            ))}
          </div>
          <h3>如何筛选核心问题</h3>
          <div className="tag-grid">
            {questionFilters.map((item) => <span key={item}>{item}</span>)}
          </div>
          <p>最终选出24个核心问题。</p>
          <h3>六类测试场景、代表问题及观察重点</h3>
          <div className="table-scroll">
            <table className="data-table compact-table">
              <thead><tr><th>测试场景</th><th>代表问题</th><th>观察重点</th></tr></thead>
              <tbody>{scenarioRows.map(([scenario, question, focus]) => <tr key={scenario}><td>{scenario}</td><td>{question}</td><td>{focus}</td></tr>)}</tbody>
            </table>
          </div>
        </section>

        <section className="content-section">
          <h2>为什么选择这五个AI平台</h2>
          <p>平台：豆包、文心一言、通义千问、Kimi、腾讯元宝。</p>
          <div className="text-list two-col">
            {["面向中文用户", "可以统一手动测试", "回答和来源呈现方式存在差异", "便于后续复测"].map((item) => <p key={item}>{item}</p>)}
          </div>
          <p className="safe-note">平台模型和功能会持续更新。本项目记录的是特定时间和使用模式下的回答表现，不将结果解释为平台长期能力排名。</p>
        </section>

        <section className="content-section">
          <h2>回答如何采集</h2>
          <div className="tag-grid">
            {collectionSteps.map((item) => <span key={item}>{item}</span>)}
          </div>
          <p>结构：24个问题 × 5个平台 = 120条回答。</p>
        </section>

        <section className="content-section">
          <h2>回答如何判断</h2>
          <div className="tag-grid scoring-tags">{scoringDimensions.map((item) => <span key={item}>{item}</span>)}</div>
          <div className="section-subhead"><h3>评分如何理解</h3></div>
          <div className="score-rule-grid">
            {scoreRules.map(([score, rule]) => <article key={score}><b>{score}</b><p>{rule}</p></article>)}
          </div>
          <p className="safe-note">这套量表为本项目设计，用于统一判断口径，不是行业通用GEO评分标准，也不合并为一个总览分值。</p>
        </section>

        <section className="content-section">
          <h2>如何减少评分偏差</h2>
          <div className="content-chain-flow" aria-label="评分偏差控制流程">
            {biasControls.map((item, index) => (
              <article key={item}>
                <span>{String(index + 1).padStart(2, "0")}</span>
                <b>{item}</b>
              </article>
            ))}
          </div>
          <p className="safe-note">初评完成后抽取19条代表样本进行复核，其中7条评分或评语得到修正，并形成最终分析结果。</p>
        </section>

        <section className="content-section">
          <h2>数据如何保持一致</h2>
          <div className="text-list two-col">
            {consistencyItems.map((item) => <p key={item}>{item}</p>)}
          </div>
        </section>

        <section className="content-section">
          <h2>当前方法的限制</h2>
          <div className="text-list two-col">
            {limitations.map((item) => <p key={item}>{item}</p>)}
          </div>
        </section>

        <section className="content-section">
          <h2>下一轮如何验证优化效果</h2>
          <div className="text-list two-col">
            {nextValidation.map((item) => <p key={item}>{item}</p>)}
          </div>
          <div className="content-chain-flow six-step-flow" aria-label="下一轮验证流程">
            {validationFlow.map((item, index) => (
              <article key={item}>
                <span>{String(index + 1).padStart(2, "0")}</span>
                <b>{item}</b>
              </article>
            ))}
          </div>
        </section>

        <section className="page-cta">
          <Link className="button primary" href="/experiment">查看AI 搜索诊断<ArrowIcon /></Link>
          <Link className="button" href="/case-study">返回项目案例<ArrowIcon /></Link>
          <Link className="button" href="/prompt-system">提示词流程附录<ArrowIcon /></Link>
        </section>
      </div>
    </SiteShell>
  );
}
