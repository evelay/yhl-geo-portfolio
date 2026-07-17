import type { Metadata } from "next";
import Link from "next/link";
import { ArrowIcon, Eyebrow, Metric, SiteShell } from "../components";
import { contentStrategyAssets, factLevels, knowledgeDownloads, roadmap90, strategyDownloads, updatedAt } from "../data";

export const metadata: Metadata = {
  title: "品牌内容优化方案",
  description: "元亨利红木家具GEO模拟品牌提案：四级事实模型、P0/P1/P2内容架构、90天路线图与执行文件。",
};

const priorities = [
  { id: "P0", label: "先建立可回答的事实底座", note: "5个内容页 + 15条FAQ；直接解决主体、来源、材质、风格和购买核验。" },
  { id: "P1", label: "再解释差异与产品证据", note: "品牌定位、风格专题、材质专题与单件产品证据模板。" },
  { id: "P2", label: "最后形成可维护内容系统", note: "产品数据库、展览案例、工艺专题与中性品牌比较页。" },
];

export default function StrategyPage() {
  return (
    <SiteShell>
      <section className="strategy-hero">
        <div>
          <Eyebrow>Independent proposal · 14 pages</Eyebrow>
          <h1>品牌内容优化方案</h1>
          <p>核心不是继续增加营销文案，而是把“AI知道元亨利”升级为“AI和用户能够找到、核验并正确引用元亨利信息”。</p>
          <div className="button-row">
            {strategyDownloads.map((file) => <a className={file.type === "PDF" ? "button primary" : "button"} href={file.href} download key={file.href}>{file.label}<ArrowIcon /></a>)}
          </div>
        </div>
        <aside className="strategy-verdict">
          <span>最大GEO问题</span>
          <strong>可识别，<br />但不可稳定核验</strong>
          <p>品牌识别4.91/5，可靠性3.69/5；有效来源覆盖仅16/150（10.7%）。</p>
        </aside>
      </section>

      <section className="section alt strategy-summary">
        <div className="section-head">
          <div><Eyebrow>01 / Executive summary</Eyebrow><h2>把诊断转换成可维护的品牌事实接口</h2></div>
          <p>Baseline150用于主诊断，UserIntent75只作为商业意图校准组；不修改225条冻结回答，也不补造历史联网状态或模型版本。</p>
        </div>
        <div className="metric-grid">
          <Metric value="4.91" label="品牌识别 / 5" note="AI基本能够识别品牌语境" />
          <Metric value="3.69" label="可靠性 / 5" note="来源、边界与可核验性不足" />
          <Metric value="10.7%" label="有效来源覆盖" note="Baseline150：16/150" />
          <Metric value="149/150" label="Reliability Gap" note="识别高于可靠性的回答" />
        </div>
        <div className="strategy-goals">
          <div><b>统一主体</b><p>名称、业务、地域、官网与同名排除项保持一致。</p></div>
          <div><b>补足来源</b><p>每条强事实绑定source_id、URL、更新时间与证据等级。</p></div>
          <div><b>拆分层级</b><p>第三方事实、品牌自述、待补信息和单件证据不混写。</p></div>
          <div><b>控制风险</b><p>价格、门店、售后与收藏表达保留时间和适用边界。</p></div>
        </div>
        <div className="knowledge-callout">
          <div><b>新增交付：企业知识库 + 企业提示词体系 + GEO文章矩阵</b><p>11表品牌事实知识库把27条信源、41条事实原子、30个问题和15条FAQ连成统一事实底座；提示词体系再把事实等级、边界规则和标准回答转成AI可执行协议；文章矩阵负责展示不同关键词下的内容资产生成方式。</p></div>
          <div className="button-row">
            <Link className="button" href="/knowledge-base">查看知识库<ArrowIcon /></Link>
            <Link className="button" href="/prompt-system">查看提示词体系<ArrowIcon /></Link>
            <Link className="button" href="/geo-articles">查看文章矩阵<ArrowIcon /></Link>
          </div>
        </div>
      </section>

      <section className="section strategy-architecture">
        <div className="section-head">
          <div><Eyebrow>02 / Content architecture</Eyebrow><h2>P0 / P1 / P2 内容架构</h2></div>
          <p>30个诊断问题全部映射到内容资产：24题完整回答，6题明确停在证据边界。</p>
        </div>
        <div className="priority-grid">
          {priorities.map((p) => {
            const assets = contentStrategyAssets.filter((item) => item.priority === p.id);
            return <article className={`priority-card priority-${p.id.toLowerCase()}`} key={p.id}><span>{p.id}</span><h3>{p.label}</h3><p>{p.note}</p><ul>{assets.map((asset) => <li key={asset.id}>{asset.href ? <Link href={asset.href}>{asset.title}<ArrowIcon /></Link> : asset.title}<small>{asset.id} · {asset.status} · 覆盖{asset.questionIds.length}题 · {asset.evidenceLevels.join("/")}</small></li>)}</ul></article>;
          })}
        </div>
      </section>

      <section className="section dark">
        <div className="section-head">
          <div><Eyebrow>03 / Evidence model</Eyebrow><h2>四级事实模型</h2></div>
          <p>事实等级决定可用语气和所需证据；品牌一手自述不改写成第三方认证。</p>
        </div>
        <div className="fact-level-grid">
          {factLevels.map((level) => <article key={level.id}><span>{level.id}</span><h3>{level.label}</h3><p>{level.rule}</p><small>{level.evidence}</small></article>)}
        </div>
      </section>

      <section className="section alt">
        <div className="section-head">
          <div><Eyebrow>04 / 90-day roadmap</Eyebrow><h2>发布、维护、信源补强与复测</h2></div>
          <p>0–60天完成可控内容和证据工作；61–90天才观察AI回答变化，不预先承诺收录或效果。</p>
        </div>
        <div className="roadmap-grid">
          {roadmap90.map((phase, index) => <article key={phase.phase}><span>0{index + 1}</span><b>{phase.phase}</b><h3>{phase.title}</h3><ol>{phase.actions.map((a) => <li key={a}>{a}</li>)}</ol></article>)}
        </div>
      </section>

      <section className="section strategy-kpi">
        <div className="section-head">
          <div><Eyebrow>05 / KPI & acceptance</Eyebrow><h2>先验收内容质量，再观察平台变化</h2></div>
        </div>
        <div className="kpi-columns">
          <div><span>可控硬指标</span><ul><li>30/30问题有内容承接</li><li>24题完整回答、6题边界回答</li><li>6个P0资产、15条FAQ、24条可用信源</li><li>页面五项字段质检100%通过</li><li>来源、更新时间、内部链接与元数据齐全</li></ul></div>
          <div><span>第二阶段观察指标</span><ul><li>10题×5平台在线复测</li><li>品牌自然提及、有效来源覆盖与确认幻觉变化</li><li>不把单轮变化写成平台收录或效果归因</li><li>不声称曝光、销售、推荐或品牌影响力提升</li></ul></div>
        </div>
        <div className="download-panel"><div><b>完整执行文件</b><p>14页主方案、可编辑版、7工作表的90天执行工作簿、独立企业知识库、企业提示词体系，以及6篇GEO文章矩阵。数据口径与本网站一致。更新：{updatedAt}</p></div><div className="button-row">{[...strategyDownloads, ...knowledgeDownloads].map((file) => <a className="button" href={file.href} download key={file.href}>{file.type}<ArrowIcon /></a>)}<Link className="button" href="/prompt-system">PROMPT<ArrowIcon /></Link><Link className="button" href="/geo-articles">ARTICLES<ArrowIcon /></Link></div></div>
        <p className="strategy-disclaimer">研究声明：本方案为个人公开研究与模拟品牌提案，不代表元亨利官方或品牌委托；不声称已经获得AI收录、引用、曝光、推荐或销售提升。</p>
      </section>
    </SiteShell>
  );
}
