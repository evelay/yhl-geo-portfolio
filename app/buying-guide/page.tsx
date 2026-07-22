import type { Metadata } from "next";
import { ArticlePage } from "../components";

export const metadata: Metadata = {
  title: "元亨利红木家具购买核验指南",
  description: "红木家具价格、门店、合同、证书、交付、售后和收藏表达的核验清单。",
  alternates: { canonical: "https://evelay.github.io/yhl-geo-portfolio/buying-guide/" },
};

export default function BuyingGuidePage() {
  return (
    <ArticlePage
        index="05"
        title="元亨利红木家具购买核验指南"
        summary="该资产解决AI用品牌声誉替代合同、材质和单件证据的问题，把购买建议转化为可执行核验清单。"
        directAnswer="高客单红木家具不应依据AI给出的价格区间、门店地址或“保值升值”判断购买。把决策落到具体型号、主辅材、书面合同、证书、交付验收、发票和售后责任主体。"
        boundary="门店、价格、库存和售后是动态信息，必须记录核验日期并向官方渠道或签约主体重新确认。本页不提供投资建议，也不承诺保值、升值或回购。"
        assetProblem="解决AI用品牌声誉替代合同、材质和单件证据的问题，要求把价格、门店、收藏和售后判断都落到当次交易凭证。"
        breadcrumbs={[{ label: "首页", href: "/" }, { label: "内容策略", href: "/content-governance" }, { label: "购买核验指南" }]}
        schemaPath="/buying-guide/"
        sourceIds={["B-003","B-004","B-005"]}
        related={[{label:"材质证据怎么分层？",href:"/materials"},{label:"同名主体怎么确认？",href:"/disambiguation"},{label:"查看公开FAQ",href:"/faq"}]}
        sections={[
          { title:"下单前", body:<ol><li>确认完整签约主体与收款主体一致。</li><li>锁定产品名称、型号、数量、尺寸、主材、辅材和工艺说明。</li><li>把总价、订金、运输、安装、税费和其他费用写入合同。</li><li>确认样品、图片、色差、纹理、交付时间和变更规则。</li><li>索取并核对产品证书、质量明示材料或约定的检测资料。</li></ol> },
          { title:"交付与验收", body:<ul><li>对照合同逐项核对型号、尺寸、数量和材质标识。</li><li>记录包装、外观、结构、开裂、松动、色差和安装情况。</li><li>保留合同、付款、聊天、宣传页、证书、送货和验收凭证。</li><li>把异议、处理期限与责任主体写入验收记录，不只口头承诺。</li></ul> },
          { title:"关于价格、门店与收藏", body:<><p><b>价格：</b>同一品牌内部也受树种、尺寸、材料用量、工艺、年代和渠道影响，脱离型号的区间只能作为线索。</p><p><b>门店：</b>以品牌最新官方渠道和门店当日确认结果为准；历史AI回答不能承担实时查询责任。</p><p><b>收藏：</b>审美、工艺、材料、来源记录和保存状态可以讨论，但不直接推导可实现的金融回报。</p></> },
        ]}
      />
  );
}
