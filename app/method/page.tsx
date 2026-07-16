import type { Metadata } from "next";
import { Eyebrow, SiteShell } from "../components";
import { sources } from "../data";

export const metadata: Metadata = { title: "方法、来源与限制", description: "元亨利GEO公开研究的样本、评分口径、证据索引、来源和限制。" };

export default function MethodPage() {
  return <SiteShell><div className="method-page"><Eyebrow>Audit-ready method</Eyebrow><h1>方法、来源与限制</h1><p className="intro">项目目标是展示可复核的GEO研究与内容设计能力，不替品牌做官方陈述，也不把内容覆盖验证等同于真实AI收录或商业提升。</p>
    <section><h2>研究设计</h2><table className="data-table"><thead><tr><th>数据组</th><th>规模</th><th>用途</th><th>关键边界</th></tr></thead><tbody><tr><td>Baseline150</td><td>30题 × 5平台</td><td>正式诊断与主案例</td><td>所有题目均含品牌词，品牌提及率不用于自然提及结论</td></tr><tr><td>UserIntent75</td><td>15题 × 5平台</td><td>商业意图校准</td><td>仅us08、us09、us10、us11、us14、us15共30条用于非品牌自然提及</td></tr></tbody></table></section>
    <section><h2>评分与标签口径</h2><div className="callout">四个维度各0–5分：品牌识别、实体准确、属性覆盖、可靠性，总分0–20。<b>确认错误</b>仅指 correctness=错误；<b>确认幻觉</b>仅指 hallucination=有；“疑似”单列，不并入确认错误或确认幻觉。有效来源只统计原回答中可回到具体页面的URL或明确官网/政府域名线索，图片/CDN链接不计。</div><p>15条跨平台样本已经形成评分校准记录。评分只用于本项目内的相对诊断，不宣称跨模型、跨时间的通用测量效度。</p></section>
    <section><h2>关键结果</h2><table className="data-table"><thead><tr><th>指标</th><th>Baseline150</th><th>UserIntent75 / 子样本</th></tr></thead><tbody><tr><td>平均总分</td><td>17.2 / 20</td><td>14.9 / 20</td></tr><tr><td>品牌词明确提及率</td><td>100.0%</td><td>不用于自然提及结论</td></tr><tr><td>非品牌词自然提及率</td><td>不适用</td><td>66.7%（20/30）</td></tr><tr><td>确认错误率</td><td>1.3%（2/150）</td><td>5.3%（4/75）</td></tr><tr><td>确认幻觉率</td><td>9.3%（14/150）</td><td>42.7%（32/75）</td></tr><tr><td>疑似幻觉率</td><td>89.3%（134/150）</td><td>54.7%（41/75）</td></tr><tr><td>有效来源覆盖</td><td>10.7%（16/150）</td><td>4.0%（3/75）</td></tr></tbody></table></section>
    <section><h2>证据链</h2><p>12条核心证据使用 EV-001 至 EV-012 编号，连接数据集、原始工作表行、问题、平台、回答摘录、评分、风险标签、来源状态和对应优化页面。历史会话无法找回原平台截图的，统一标注“工作簿原始回答摘录”，不伪装成原平台界面。</p></section>
    <section><h2>已核验第三方/权威来源</h2><table className="data-table"><thead><tr><th>ID</th><th>来源</th><th>用途</th></tr></thead><tbody>{sources.map((s) => <tr key={s.id}><td>{s.id}</td><td><a href={s.url} target="_blank" rel="noreferrer">{s.title}</a><br/><small>{s.type}</small></td><td>{s.use}</td></tr>)}</tbody></table><p>此外，信源审计表保留品牌一手来源及其写作边界。品牌一手来源只支持“品牌自述/品牌公开信息”，不能替代第三方评价。</p></section>
    <section><h2>已知限制</h2><ul><li>历史测试的联网状态、模型模式、模型版本或引用来源没有记录的，统一保留“未记录”。</li><li>本轮没有实施10题×5平台在线复测；它是第二阶段，不阻塞投递。</li><li>优化后验证指30题都有内容承接，其中24题可完整回答、6题边界回答；这不是AI已收录或引用的证据。</li><li>公开网页、标准和报道可能更新；动态门店、价格、售后应以再次核验为准。</li><li>本项目为个人公开研究案例，不代表品牌授权或服务关系。</li></ul></section>
  </div></SiteShell>;
}
