import Link from "next/link";
import type { Metadata } from "next";
import { ArrowIcon, BarChart, Eyebrow, Metric, SiteShell } from "./components";
import { categoryScores, diagnoses, platformScores, riskTags } from "./data";

export const metadata: Metadata = {
  title: "公开研究首页",
  description: "元亨利红木家具GEO公开研究案例：225条AI回答、6项核心诊断、5个内容资产与15条FAQ。",
};

const assets = [
  ["01", "品牌事实与定位", "把主体、公开定位、品牌自述与待核验项分层。", "/facts"],
  ["02", "同名主体消歧", "先确认完整主体、业务、地域和官网，再回答品牌问题。", "/disambiguation"],
  ["03", "材质与产品关系", "区分标准术语、品牌公开范围与单件产品证据。", "/materials"],
  ["04", "京作 / 明清边界", "把地域、风格、品牌产品与资格证明拆开。", "/jingzuo"],
  ["05", "购买核验指南", "价格、门店、合同、证书、交付和售后的核验清单。", "/buying-guide"],
];

export default function Home() {
  return (
    <SiteShell>
      <section className="hero">
        <div className="hero-grid">
          <div>
            <Eyebrow>GEO · Generative Engine Optimization</Eyebrow>
            <h1>让红木家具信息<br />变得<em>可回答、可核验</em></h1>
            <p className="lede">一个不代表品牌官方的公开研究案例：用225条AI回答识别实体、来源与高客单决策风险，再把诊断转化为可引用内容资产。</p>
            <div className="button-row">
              <a className="button primary" href="#diagnoses">查看六项诊断<ArrowIcon /></a>
              <Link className="button" href="/method">方法与来源<ArrowIcon /></Link>
            </div>
          </div>
          <aside className="hero-note">
            <div className="index">75%</div>
            <h3>从审计到投递收口</h3>
            <p>数据与方法已基本完成；本版补齐证据索引、信源边界、四张核心图表、五页内容资产与可公开展示结构。</p>
          </aside>
        </div>
      </section>

      <section className="section alt" id="data">
        <div className="section-head">
          <div><Eyebrow>01 / Research design</Eyebrow><h2>两个样本组，不能混成一个平均值</h2></div>
          <p>Baseline150用于正式诊断；UserIntent75用于商业意图校准。历史联网状态、引用来源和模型版本未记录的字段统一保留“未记录”。</p>
        </div>
        <div className="metric-grid">
          <Metric value="150" label="正式诊断样本" note="30题 × 5平台" />
          <Metric value="75" label="用户搜索校准组" note="15题 × 5平台" />
          <Metric value="17.2" label="Baseline平均总分" note="四维总分，满分20" />
          <Metric value="14.9" label="UserIntent平均总分" note="独立报告，不与主样本合并" />
        </div>
        <div className="chart-grid">
          <div className="chart-card"><h3>五平台平均总分</h3><p>Baseline150；0–20分</p><BarChart data={platformScores} max={20} /></div>
          <div className="chart-card"><h3>品牌词 / 非品牌词明确提及</h3><p>品牌词提示150条；非品牌词自然提及30条</p><div className="mention-chart"><div className="mention-col"><b>100.0%</b><i style={{height:"100%"}}/><span>品牌词提示</span></div><div className="mention-col"><b>66.7%</b><i style={{height:"66.7%"}}/><span>非品牌词自然提及</span></div></div></div>
          <div className="chart-card"><h3>问题类别平均分</h3><p>Baseline150；类别来自30题研究设计</p><BarChart data={categoryScores} max={20} /></div>
          <div className="chart-card"><h3>高频错误与缺失标签</h3><p>225条回答；一条回答可有多个标签</p><BarChart data={riskTags} max={150} accent /></div>
        </div>
      </section>

      <section className="section dark" id="diagnoses">
        <div className="section-head">
          <div><Eyebrow>02 / Findings</Eyebrow><h2>六项诊断不是观点，<br />而是证据链</h2></div>
          <p>每项诊断均连接工作簿原始行、回答摘录、来源状态和优化页面。历史截图无法找回时，证据统一标注为“工作簿原始回答摘录”。</p>
        </div>
        <div className="diagnosis-grid">
          {diagnoses.map((d) => <div className="diagnosis-card" key={d.id}><span className="num">{d.id}</span><h3>{d.title}</h3><p>{d.impact}</p><p className="data-line">{d.data}</p></div>)}
        </div>
        {diagnoses.map((d) => (
          <div className="diagnosis-detail" key={`${d.id}-detail`}>
            <div><b>{d.id} · 数据</b><p>{d.data}</p></div>
            <div><b>两条典型回答</b><ul>{d.cases.map((c) => <li key={c}>{c}</li>)}</ul></div>
            <div><b>可能原因</b><p>{d.cause}</p></div>
            <div><b>用户影响 / 来源</b><p>{d.impact}</p><p>{d.source}</p></div>
            <div><b>对应优化动作</b><p>{d.action}</p></div>
          </div>
        ))}
      </section>

      <section className="section alt" id="content-assets">
        <div className="section-head">
          <div><Eyebrow>03 / Content system</Eyebrow><h2>五个独立页面，承接三十个问题</h2></div>
          <p>每页都有直接答案、来源链接、事实边界、更新时间与相关问题。另设15条FAQ，补充高频问法和边界回答。</p>
        </div>
        <div className="asset-grid">
          {assets.map(([index,title,desc,href]) => <div className="asset-card" data-index={index} key={href}><span>ASSET {index}</span><h3>{title}</h3><p>{desc}</p><Link href={href}>打开页面<ArrowIcon /></Link></div>)}
        </div>
        <div className="coverage-band"><strong>30 / 30</strong><p>优化后所有问题均有承接：24题可在证据边界内完整回答，6题明确提示需补官方、第三方或单件资料；不为追求覆盖而虚构事实。</p><Link className="button" href="/faq">查看15条FAQ<ArrowIcon /></Link></div>
      </section>

      <section className="section dark">
        <div className="section-head">
          <div><Eyebrow>04 / Method & limits</Eyebrow><h2>这是一套可审计的内容作品，<br />不是效果归因报告</h2></div>
        </div>
        <div className="method-grid">
          <div className="method-steps">
            <div className="method-step"><b>冻结原始回答</b><p>不改写225条历史样本；主案例与校准组分表保存。</p></div>
            <div className="method-step"><b>四维评分与标签</b><p>品牌识别、实体准确、属性覆盖、可靠性各0–5分。</p></div>
            <div className="method-step"><b>证据与信源索引</b><p>evidence_id连接原始行、摘录、来源状态与优化页面。</p></div>
            <div className="method-step"><b>内容覆盖验证</b><p>以公开资料为优化前基线，以五页内容与FAQ为优化后。</p></div>
          </div>
          <div className="limit-card"><h3>明确不声称</h3><ul><li>不声称真实曝光、销售或AI推荐提升。</li><li>不声称50条在线复测已经完成。</li><li>不把“疑似幻觉”直接当成确认错误。</li><li>不反推历史联网状态、模型版本或引用来源。</li><li>不把国家标准或行业常识当作单件产品证明。</li></ul><Link className="button" href="/method">查看完整方法与信源<ArrowIcon /></Link></div>
        </div>
      </section>
    </SiteShell>
  );
}
