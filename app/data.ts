import portfolioOverviewJson from "../data/portfolio-r1.1/portfolio-overview-r1.1.json";
import platformSummaryJson from "../data/portfolio-r1.1/platform-summary-r1.1.json";
import questionRiskSummaryJson from "../data/portfolio-r1.1/question-risk-summary-r1.1.json";
import clusterSummaryJson from "../data/portfolio-r1.1/cluster-summary-r1.1.json";
import methodologySummaryJson from "../data/portfolio-r1.1/methodology-summary-r1.1.json";
import selectedCasesJson from "../data/portfolio-r1.1/selected-cases-r1.1.json";
import sourceSummaryJson from "../data/portfolio-r1.1/source-summary-r1.1.json";

export const updatedAt = "2026-07-22";

export const siteUrl = "https://evelay.github.io/yhl-geo-portfolio";

function normalizeBasePath(value: string | undefined) {
  if (!value) return "";
  const trimmed = value.trim().replace(/^\/+|\/+$/g, "");
  return trimmed ? `/${trimmed}` : "";
}

export const siteBasePath = normalizeBasePath(process.env.NEXT_PUBLIC_BASE_PATH);

export function siteAssetPath(path: string) {
  if (!siteBasePath || /^https?:\/\//.test(path)) return path;
  return `${siteBasePath}${path.startsWith("/") ? path : `/${path}`}`;
}

export const portfolioOverview = portfolioOverviewJson;
export const platformSummary = platformSummaryJson;
export const questionRiskSummary = questionRiskSummaryJson;
export const clusterSummary = clusterSummaryJson;
export const methodologySummary = methodologySummaryJson;
export const selectedCases = selectedCasesJson;
export const sourceSummary = sourceSummaryJson;

export const headlineMetrics = [
  {
    value: "5",
    label: "AI平台",
    note: "豆包、文心一言、通义千问、Kimi和腾讯元宝。",
  },
  {
    value: "24",
    label: "核心问题",
    note: "覆盖品牌认知、主体核验、材质与产品、京作与风格、购买决策和来源判断。",
  },
  {
    value: "120",
    label: "完整回答",
    note: "同一组问题分别在五个平台采集，用于观察回答差异和共同风险。",
  },
];

export const metricDisclaimers = [
  "高或严重信息风险不代表回答全部内容错误。",
];

export const projectFlow = [
  "用户问题研究",
  "五个平台同题测试",
  "回答风险诊断",
  "内容与页面优化",
];

export const coreFindings = [
  {
    title: "品牌对象识别仍有偏差",
    body: "120条回答中，85条明确提及元亨利；部分回答仍然混淆品牌、企业主体和同名对象。",
  },
  {
    title: "部分来源无法支持主要结论",
    body: "96条回答显示可见链接，但部分来源只能支持局部信息，无法支撑品牌身份、行业地位或价值判断。",
  },
  {
    title: "风险集中在身份、材质和购买判断",
    body: "京作关系、材质关联、回购、保值和投资价值等问题，更容易出现缺少证据的确定性表述。",
  },
];

export const primaryWork = [
  "核心问题集、五个平台统一测试和人工复核方法。",
  "品牌事实、主体消歧、材质及文化边界内容。",
  "首批关键问题 FAQ 和购买核验指南。",
  "信息架构、页面内链、canonical、sitemap、Schema和后续复测方案。",
];

export const riskDistribution = [
  { label: "低", value: 13 },
  { label: "中等", value: 34 },
  { label: "高", value: 69 },
  { label: "严重", value: 4 },
];

export const experimentMetricRows = [
  { label: "品牌是否被提及", value: "85/120", note: "回答明确提及或指向元亨利。" },
  { label: "可见链接", value: "96/120", note: "只表示回答界面出现链接，不代表来源可靠。" },
  { label: "高或严重信息风险", value: "73/120", note: "用于定位需要治理的风险区域。" },
  { label: "严重信息风险", value: "4/120", note: "主要来自对象识别失败。" },
  { label: "事实准确性", value: "1.15/2", note: "人工量表均值，样本为120条。" },
  { label: "回答完整性", value: "1.73/2", note: "人工量表均值，样本为120条。" },
  { label: "来源可追溯性", value: "1.30/2", note: "人工量表均值，样本为120条。" },
  { label: "信息边界控制", value: "1.05/2", note: "人工量表均值，样本为120条。" },
  { label: "推荐质量", value: "1.12/2", note: "仅统计推荐和比较类样本。" },
];

export const governanceAssets = [
  { title: "品牌事实", href: "/facts", body: "解决品牌主体、同名对象、官网来源和成立时间口径混淆。", group: "品牌身份" },
  { title: "同名主体消歧", href: "/disambiguation", body: "把同名字号、企业主体、业务语境和官网线索分开核验。", group: "品牌身份" },
  { title: "材质边界", href: "/materials", body: "防止把材料话题扩大为品牌全量产品事实。", group: "产品与文化边界" },
  { title: "京作与明清", href: "/jingzuo", body: "区分地域、工艺、风格、身份资质和单件产品证据。", group: "产品与文化边界" },
  { title: "购买核验", href: "/buying-guide", body: "把购买建议落到合同、证书、检测、交付和售后主体。", group: "购买与价值判断" },
  { title: "关键问题 FAQ", href: "/faq", body: "把高风险问题转化为带边界和来源的直接回答。", group: "购买与价值判断" },
  { title: "品牌事实库（公开资料版）", href: "/knowledge-base", body: "展示事实、来源、问题和FAQ如何建立稳定关联。", group: "来源与结构化内容" },
];

export const supportAssets = [
  { title: "研究方法", href: "/methodology" },
  { title: "文章样稿审核状态", href: "/geo-articles" },
];

export const sources = [
  {
    id: "S0-001",
    title: "国家企业信用信息公示系统：主体登记核验入口",
    type: "主体核验",
    url: "https://www.gsxt.gov.cn/",
    use: "企业主体、登记状态和经营范围等实时核验入口",
  },
  {
    id: "S0-002",
    title: "工业和信息化部 ICP/IP 地址/域名信息备案管理系统",
    type: "主体核验",
    url: "https://beian.miit.gov.cn/",
    use: "官网域名、备案主体和网站名称核验入口",
  },
  {
    id: "S0-003",
    title: "中国商标网：商标查询入口",
    type: "主体核验",
    url: "https://sbj.cnipa.gov.cn/sbj/sbcx/",
    use: "商标申请人、类别、状态和注册范围核验入口",
  },
  {
    id: "B-001",
    title: "国家标准 GB/T 18107-2017《红木》",
    type: "国家标准",
    url: "https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=6E961C6DB78254EF883B5053D08BFA3B",
    use: "红木树种与材质术语边界",
  },
  {
    id: "B-002",
    title: "国家标准 GB/T 35475-2017《红木制品用材规范》",
    type: "国家标准",
    url: "https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=6184A4513320719C1FDC5F377C2A7DC0",
    use: "红木制品用材表达",
  },
  {
    id: "B-003",
    title: "国家标准 GB/T 28010-2011《红木家具通用技术条件》",
    type: "国家标准",
    url: "https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=BA56324B9077C071505CA6F34E3A12A6",
    use: "产品、合同与质量核验",
  },
  {
    id: "B-004",
    title: "中山市消委会：科学理性选购红木家具",
    type: "政府消费提示",
    url: "https://www.zs.gov.cn/zwgk/jdxx/zljg/content/post_2097956.html",
    use: "检测报告、三证与消费留痕",
  },
  {
    id: "B-005",
    title: "北京市家具买卖合同填写指南",
    type: "政府办事指南",
    url: "https://scjgj.beijing.gov.cn/bsfw/bmfw/sfwbbm/shxfl/zx/201911/t20191129_722151.html",
    use: "主材树种、价格、交付与验收",
  },
  {
    id: "B-008",
    title: "中国家具协会官网",
    type: "行业协会",
    url: "https://www.cnfa.com.cn/",
    use: "行业信息入口，不替代单件产品证明",
  },
  {
    id: "B-009",
    title: "北京家具行业协会：杨波红木行业主题演讲",
    type: "行业协会",
    url: "https://www.bfta.org.cn/site/content/1978.html",
    use: "特定时间的公开身份与发言",
  },
  {
    id: "B-010",
    title: "中国林业科学研究院机构设置：木材工业研究所",
    type: "研究机构",
    url: "https://www.caf.ac.cn/yqjj1/jgsz1.htm",
    use: "木材科研体系与术语入口",
  },
  {
    id: "B-011",
    title: "人民网采访：杨波谈元亨利产品结构调整",
    type: "主流媒体",
    url: "https://hongmu.people.com.cn/n1/2016/0705/c392126-28525842.html",
    use: "2016年采访语境中的身份和材料表述",
  },
  {
    id: "B-012",
    title: "中国国家博物馆：大美木艺——中国明清家具珍品",
    type: "国家级博物馆",
    url: "https://www.chnmuseum.cn/zl/zlhg/201812/t20181220_32264.shtml",
    use: "明清家具、黄花梨、紫檀与榫卯背景",
  },
];

export const faq = [
  {
    id: "FAQ-01", question: "元亨利是什么品牌？",
    directAnswer: "在本案例中，“元亨利”指红木家具语境中的品牌/企业主体。",
    detail: "回答前先核对完整名称、业务、地域与官网；遇到同名字号，不把其他行业主体的信息拼接进来。",
    boundary: "不从字号推导公司关系、人物经历或品牌历史。",
    sourceIds: ["S0-001", "S0-002"], related: [{ label: "品牌事实", href: "/facts" }, { label: "同名消歧", href: "/disambiguation" }],
  },
  {
    id: "FAQ-02", question: "它是不是行业第一或顶级品牌？",
    directAnswer: "没有足以支持统一排名的公开证据，不写“第一”或“顶级”。",
    detail: "可陈述有具体日期和出处的活动、报道或品牌自述，并把评价主体与事实来源分开。",
    boundary: "无第三方评选主体、年份和原页面时，不发布排名结论。",
    sourceIds: ["B-008"], related: [{ label: "品牌事实", href: "/facts" }, { label: "项目案例", href: "/case-study" }],
  },
  {
    id: "FAQ-03", question: "元亨利与黄花梨是什么关系？",
    directAnswer: "公开材料方向不等于某件产品的材质证明。",
    detail: "公开资料可以说明品牌曾涉及的材料或产品方向；具体产品仍需核对标识、合同、证书与检测信息。",
    boundary: "不判断单件真伪、等级、价格或收藏价值。",
    sourceIds: ["B-001", "B-002"], related: [{ label: "材质与产品关系", href: "/materials" }, { label: "购买核验", href: "/buying-guide" }],
  },
  {
    id: "FAQ-04", question: "紫檀家具怎么理解？",
    directAnswer: "先用标准术语，再核对单件主辅材、标识、证书和检测。",
    detail: "颜色、俗称或营销名称不能替代规范材质信息；品牌层信息也不能替代单件产品证明。",
    boundary: "不直接断言树种、产地、稀缺性或收藏价值。",
    sourceIds: ["B-001", "B-003"], related: [{ label: "材质边界", href: "/materials" }],
  },
  {
    id: "FAQ-05", question: "白酸枝等于某个固定树种吗？",
    directAnswer: "俗称需要回到规范名称，并与合同和产品凭证一致。",
    detail: "要求书面材料使用规范中文名及必要的学名信息，避免只写容易产生歧义的商业俗称。",
    boundary: "不把俗称直接绑定到品牌全部产品。",
    sourceIds: ["B-001", "B-002"], related: [{ label: "材质边界", href: "/materials" }, { label: "购买核验", href: "/buying-guide" }],
  },
  {
    id: "FAQ-06", question: "怎么判断一件红木家具值不值得买？",
    directAnswer: "把决策拆成使用、材料、合同、交付和售后，不用品牌声量代替核验。",
    detail: "逐项核对尺寸、工艺、主辅材、产品标识、合同、证书、付款、发票、交付验收与售后主体。",
    boundary: "不替用户做确定购买建议。",
    sourceIds: ["B-003", "B-004", "B-005"], related: [{ label: "购买核验清单", href: "/buying-guide" }, { label: "材质边界", href: "/materials" }],
  },
  {
    id: "FAQ-07", question: "可以和其他北京红木品牌直接排排名吗？",
    directAnswer: "可以按公开维度比较，但不做无来源的总排名。",
    detail: "比较时限定主体、材料证据、工艺说明、产品适配、合同条款、渠道与售后核验路径。",
    boundary: "不输出“第一、首选、唯一”等结论。",
    sourceIds: ["B-008"], related: [{ label: "品牌事实", href: "/facts" }, { label: "购买核验", href: "/buying-guide" }],
  },
  {
    id: "FAQ-09", question: "明式、清式和品牌产品是什么关系？",
    directAnswer: "风格知识不能替代具体产品说明。",
    detail: "明式、清式属于家具史与审美风格概念；具体产品要回到造型、比例、装饰、材质与公开说明。",
    boundary: "不由风格名称推导年代、馆藏或收藏价值。",
    sourceIds: ["B-012"], related: [{ label: "京作与明清边界", href: "/jingzuo" }, { label: "材质边界", href: "/materials" }],
  },
  {
    id: "FAQ-11", question: "元亨利和珠宝等同名主体是一家公司吗？",
    directAnswer: "不能只凭字号判断，必须核对主体链。",
    detail: "核对完整公司名、主营业务、地域、官网域名和主体登记线索；只有主体证据稳定后才建立关系。",
    boundary: "不补造统一社会信用代码，不从相似名称推导股权关系。",
    sourceIds: ["S0-001", "S0-002", "S0-003"], related: [{ label: "同名消歧", href: "/disambiguation" }],
  },
  {
    id: "FAQ-12", question: "官网信息一定可以当第三方证据吗？",
    directAnswer: "不能；官网只能证明品牌公开说了什么。",
    detail: "品牌故事、产品方向可引用官网并标记为一手自述；第三方评价应尽量回到政府、标准、协会、媒体或博物馆。",
    boundary: "不把品牌自述改写成外部认证。",
    sourceIds: ["B-008", "B-011", "B-012"], related: [{ label: "研究方法", href: "/methodology" }, { label: "内容策略", href: "/content-governance" }],
  },
  {
    id: "FAQ-13", question: "成立时间、创始人怎么写才稳妥？",
    directAnswer: "只有具体原页面可核验时才写确定事实，否则标记待补。",
    detail: "优先使用工商或官方原始页面；品牌官网自述要保留来源身份和核验日期。",
    boundary: "不从AI回答或二手转载反推人物与时间。",
    sourceIds: ["S0-001", "B-011"], related: [{ label: "品牌事实", href: "/facts" }, { label: "同名消歧", href: "/disambiguation" }],
  },
  {
    id: "FAQ-14", question: "门店、展厅和价格在哪里确认？",
    directAnswer: "使用最新官方渠道、具体门店电话和书面报价，并记录日期。",
    detail: "动态信息应同时记录产品型号、渠道、报价时间和适用条件；合同价格优先于历史网页或AI回答。",
    boundary: "历史AI回答不能承担实时查询责任。",
    sourceIds: ["B-005"], related: [{ label: "购买核验", href: "/buying-guide" }],
  },
  {
    id: "FAQ-15", question: "红木家具能保值或升值吗？",
    directAnswer: "不能据品牌、材质或工艺直接承诺保值升值。",
    detail: "可以讨论审美、工艺、材料、来源记录与保存状态，但这些因素不等于可实现的金融回报。",
    boundary: "不承诺保值、升值或收益，不构成投资建议。",
    sourceIds: ["B-004", "B-005"], related: [{ label: "购买核验", href: "/buying-guide" }, { label: "内容策略", href: "/content-governance" }],
  },
];

export const factLevels = [
  { id: "L1", label: "已核验第三方事实", rule: "可直接陈述，并保留原始来源与更新时间。", evidence: "政府、国家标准、协会、主流媒体、博物馆或研究机构原页" },
  { id: "L2", label: "品牌一手自述", rule: "使用“品牌官网公开称”等来源提示，不改写成外部认证。", evidence: "品牌官网具体页面、发布日或可审计截图" },
  { id: "L3", label: "待官方补充", rule: "明确显示“当前公开资料不足”，进入信源补强队列。", evidence: "官方声明、证书、主办方公告或第三方原页" },
  { id: "L4", label: "需单件证据", rule: "只提供核验路径，不替具体产品下结论。", evidence: "合同、标识、证书、检测、发票、交付与售后文件" },
];

export const contentStrategyAssets = [
  { id: "PAGE-P0-01", priority: "P0", title: "品牌事实与定位MVP", href: "/facts", questionIds: ["q01", "q02", "q12", "q13", "q14", "q15", "q24", "q25"], evidenceLevels: ["L1", "L2", "L3"], updatedAt, status: "公开页可发布" },
  { id: "PAGE-P0-02", priority: "P0", title: "同名主体消歧", href: "/disambiguation", questionIds: ["q01", "q10", "q11", "q16", "q26", "q27"], evidenceLevels: ["L1", "L2", "L3"], updatedAt, status: "公开页可发布" },
  { id: "PAGE-P0-03", priority: "P0", title: "材质与产品关系", href: "/materials", questionIds: ["q03", "q04", "q05", "q16", "q27"], evidenceLevels: ["L1", "L2", "L4"], updatedAt, status: "公开页可发布" },
  { id: "PAGE-P0-04", priority: "P0", title: "京作/明清风格边界", href: "/jingzuo", questionIds: ["q08", "q09", "q21", "q22", "q23", "q27"], evidenceLevels: ["L1", "L2", "L3", "L4"], updatedAt, status: "公开页可发布" },
  { id: "PAGE-P0-05", priority: "P0", title: "购买核验指南", href: "/buying-guide", questionIds: ["q06", "q07", "q17", "q18", "q19", "q24", "q25", "q26", "q28"], evidenceLevels: ["L1", "L4"], updatedAt, status: "公开页可发布" },
  { id: "FAQ-P0-HUB", priority: "P0", title: "13条公开FAQ（2条hold）", href: "/faq", questionIds: ["q01", "q03", "q04", "q05", "q06", "q07", "q10", "q14", "q15", "q17", "q18", "q20", "q24", "q25", "q28"], evidenceLevels: ["L1", "L2", "L3", "L4"], updatedAt, status: "13条公开，2条暂缓" },
  { id: "PAGE-P1-01", priority: "P1", title: "品牌定位深度页", href: "", questionIds: ["q02", "q07", "q24", "q25"], evidenceLevels: ["L1", "L2", "L3"], updatedAt, status: "待证据" },
  { id: "PAGE-P1-02", priority: "P1", title: "明式/清式风格指南", href: "", questionIds: ["q09", "q22", "q27"], evidenceLevels: ["L1", "L4"], updatedAt, status: "待开始" },
  { id: "PAGE-P1-03", priority: "P1", title: "材质专题组", href: "", questionIds: ["q03", "q04", "q05", "q16"], evidenceLevels: ["L1", "L4"], updatedAt, status: "待开始" },
  { id: "TPL-P1-01", priority: "P1", title: "单件产品证据模板", href: "", questionIds: ["q16", "q19", "q26"], evidenceLevels: ["L4"], updatedAt, status: "待开始" },
  { id: "DB-P2-01", priority: "P2", title: "产品数据库", href: "", questionIds: ["q16", "q19"], evidenceLevels: ["L2", "L4"], updatedAt, status: "规划中" },
  { id: "PAGE-P2-02", priority: "P2", title: "展览与案例内容", href: "", questionIds: ["q15", "q21"], evidenceLevels: ["L1", "L2"], updatedAt, status: "规划中" },
  { id: "PAGE-P2-03", priority: "P2", title: "工艺专题", href: "", questionIds: ["q23"], evidenceLevels: ["L1", "L2", "L4"], updatedAt, status: "规划中" },
  { id: "PAGE-P2-04", priority: "P2", title: "中性品牌比较页", href: "", questionIds: ["q07", "q24", "q25"], evidenceLevels: ["L1", "L4"], updatedAt, status: "规划中" },
];

export const roadmap90 = [
  { phase: "0–30天", title: "事实基础", actions: ["冻结公开口径与事实模型", "建立结构化知识示例", "完善核心内容资产和高频FAQ", "补齐来源、边界、更新时间与页面元数据"] },
  { phase: "31–60天", title: "解释差异", actions: ["证据足够后拆分品牌定位页", "增加风格专题与单件产品证据模板", "完成P0/P1内部链接与来源回链"] },
  { phase: "61–90天", title: "复测维护", actions: ["知识库月度复核与动态信息失效检查", "复核价格、门店、售后等动态信息", "执行10题×5平台在线复测", "形成前后对比与下一轮P2 backlog"] },
];

export const strategyDownloads = [] as { label: string; href: string; type: string }[];

export const knowledgeDownloads = [] as { label: string; href: string; type: string }[];

export const promptSystemDownloads = [] as { label: string; href: string; type: string }[];

export const geoArticleDownloads = [] as { label: string; href: string; type: string }[];

export const nav = [
  ["首页", "/"],
  ["项目案例", "/case-study"],
  ["AI 搜索诊断", "/experiment"],
  ["内容策略", "/content-governance"],
  ["研究方法", "/methodology"],
];
