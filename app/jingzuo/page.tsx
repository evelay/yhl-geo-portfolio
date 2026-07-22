import type { Metadata } from "next";
import { ArticlePage } from "../components";

export const metadata: Metadata = {
  title: "京作 / 明清风格边界",
  description: "区分京作地域/行业语境、明清家具知识、品牌事实和单件产品风格。",
  alternates: { canonical: "https://evelay.github.io/yhl-geo-portfolio/jingzuo/" },
};

export default function JingzuoPage() {
  return <ArticlePage
    index="04"
    title="京作 / 明清风格边界"
    summary="该资产解决AI把地域、工艺、风格和身份资质混写的问题，避免把背景知识误写成品牌或单件产品证明。"
    directAnswer="“京作”“明式”“清式”不是同一个维度：京作可能指地域、工艺传统或行业语境；明式、清式属于家具史与审美风格。品牌是否具备特定资格、单件产品属于何种风格，都需要单独证据。"
    boundary="国家博物馆展览资料可用于明清家具背景，不证明元亨利某件产品的风格、年代或收藏价值；“北京品牌”也不自动等于“京作非遗代表”。"
    assetProblem="解决地域、工艺、风格和身份资质混淆，把京作、明式、清式与品牌事实和单件产品证据分开。"
    breadcrumbs={[{ label: "首页", href: "/" }, { label: "内容策略", href: "/content-governance" }, { label: "京作与明清风格边界" }]}
    schemaPath="/jingzuo/"
    sourceIds={["B-009","B-012"]}
    related={[{label:"品牌定位怎么写？",href:"/facts"},{label:"材质与单件证据",href:"/materials"},{label:"收藏价值FAQ",href:"/faq"}]}
    sections={[
      { title:"四个概念分开", body:<><h3>地域</h3><p>企业或活动位于北京，是主体和地域事实。</p><h3>行业/工艺语境</h3><p>“京作”可作为行业表达，但具体定义、传承和资格要看来源。</p><h3>风格</h3><p>“明式”“清式”应从造型、比例、装饰、构件和历史语境描述，不能只靠商品名。</p><h3>产品事实</h3><p>某件产品是否采用对应设计语言，要回到产品图、尺寸、结构和正式说明。</p></> },
      { title:"更稳妥的写法", body:<ul><li>写“在北京红木家具行业语境中被讨论”，替代没有资格证明的“国家级京作代表”。</li><li>写“借鉴明式家具的简练比例/清式家具的装饰语言”，前提是产品说明与视觉证据支持。</li><li>把历史知识放在背景区，把品牌和单件事实放在证据区，避免相互背书。</li></ul> },
      { title:"对应AI搜索问题", body:<p>本页承接京作关系、明式与清式意义、京作可核验关系、风格与产品事实、榫卯和手工雕刻等问题。</p> },
    ]}
  />;
}
