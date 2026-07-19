export const updatedAt = "2026-07-17";

function normalizeBasePath(value: string | undefined) {
  if (!value) return "";
  const trimmed = value.trim().replace(/^\/+|\/+$/g, "");
  return trimmed ? `/${trimmed}` : "";
}

function inferBasePath() {
  const explicit = process.env.NEXT_PUBLIC_BASE_PATH;
  if (explicit !== undefined) return normalizeBasePath(explicit);

  if (process.env.GITHUB_PAGES !== "true") return "";

  const repository = process.env.GITHUB_REPOSITORY;
  if (!repository) return "";

  const [owner, repo] = repository.split("/");
  if (!owner || !repo || repo === `${owner}.github.io`) return "";

  return normalizeBasePath(repo);
}

const basePath = inferBasePath();

function downloadPath(fileName: string) {
  return `${basePath}/downloads/${fileName}`;
}

export const platformScores = [
  { label: "豆包", value: 17.93 },
  { label: "文心一言", value: 16.03 },
  { label: "通义千问", value: 16.87 },
  { label: "Kimi", value: 17.53 },
  { label: "腾讯元宝", value: 17.57 },
];

export const naturalMentionByPlatform = [
  { label: "豆包", value: 50.0 },
  { label: "文心一言", value: 100.0 },
  { label: "通义千问", value: 33.3 },
  { label: "Kimi", value: 83.3 },
  { label: "腾讯元宝", value: 66.7 },
];

export const categoryScoresV2 = [
  { label: "品牌认知类", value: 15.76 },
  { label: "材质类", value: 16.75 },
  { label: "京作与风格类", value: 17.13 },
  { label: "购买决策类", value: 17.98 },
  { label: "风险边界类", value: 17.48 },
];

export const riskAndMissingTags = [
  { label: "缺少可追溯来源", value: 99 },
  { label: "时间/适用边界", value: 99 },
  { label: "强定位", value: 89 },
  { label: "收藏价值", value: 77 },
  { label: "同名混淆", value: 76 },
  { label: "年份", value: 75 },
  { label: "荣誉", value: 74 },
  { label: "发票", value: 31 },
  { label: "售后", value: 31 },
  { label: "材质标准名", value: 30 },
];

export const hallucinationByDataset = [
  { label: "豆包", baseline: 6.7, userIntent: 26.7 },
  { label: "文心一言", baseline: 10.0, userIntent: 40.0 },
  { label: "通义千问", baseline: 10.0, userIntent: 53.3 },
  { label: "Kimi", baseline: 10.0, userIntent: 46.7 },
  { label: "腾讯元宝", baseline: 10.0, userIntent: 46.7 },
];

export const sourceCoverageByPlatform = [
  { label: "豆包", value: 13.3 },
  { label: "文心一言", value: 0.0 },
  { label: "通义千问", value: 6.7 },
  { label: "Kimi", value: 16.7 },
  { label: "腾讯元宝", value: 16.7 },
];

export const completionAnswers = [
  {
    id: "01",
    question: "哪个平台表现最好？",
    answer: "豆包。Baseline150平均总分17.93/20，五个平台最高。",
    note: "只代表本项目主样本的四维平均分，不代表平台整体能力。",
  },
  {
    id: "02",
    question: "哪个平台最容易编造？",
    answer: "主样本没有唯一最高；UserIntent75中通义最高，确认幻觉8/15（53.3%），并有4条确认错误。",
    note: "Baseline150中，文心、通义、Kimi和腾讯的确认幻觉率均为10%。",
  },
  {
    id: "03",
    question: "哪一类问题最容易出问题？",
    answer: "品牌认知类综合最弱：均分15.76，确认幻觉7/25（28.0%）。",
    note: "如果只看确认错误率，风险边界类最高，为1/25（4.0%）。",
  },
  {
    id: "04",
    question: "品牌哪些信息最容易缺失？",
    answer: "可追溯来源和信息时间/适用边界各99次；其后是发票、售后、材质标准名、证书、合同和单件证据。",
    note: "高风险事实主要集中在年份、人物、定位、荣誉、排名、馆藏与动态商业信息。",
  },
  {
    id: "05",
    question: "信息来源主要来自哪里？",
    answer: "AI回答有效来源覆盖仅16/150（10.7%），主要指向品牌官网，其次是工商/政府查询和国家标准。",
    note: "研究信源库另有11条品牌一手、12条第三方、4条主体核验；24/27当前可用于投递。",
  },
  {
    id: "06",
    question: "元亨利当前最大GEO问题是什么？",
    answer: "不是品牌无法被识别，而是缺少可靠、结构化、可追溯的事实证据。",
    note: "品牌识别4.91/5，可靠性3.69/5；149/150回答存在Reliability Gap。",
  },
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

export const diagnoses = [
  {
    id: "D1",
    title: "品牌识别高，可靠性低一档",
    data: "Baseline150：品牌识别均分 4.91/5，可靠性均分 3.69/5；两者相差 1.22 分。",
    cases: [
      "EV-001｜q01｜Kimi：能识别红木家具语境，但把品牌历史、定位和人物信息组合成未经逐项证实的长回答。",
      "EV-003｜q05｜文心一言：能给出方向性判断，却缺少可核验出处，来源状态为“无可核验来源”。",
    ],
    cause: "模型更容易记住品牌—品类关联；品牌历史、荣誉、人物和单件事实缺少结构化、可引用页面。",
    impact: "用户看到“像真的”完整答案，却无法区分已证实事实、品牌自述和模型补全。",
    source: "证据卡来自冻结工作簿原始回答；历史联网状态、模型模式和引用来源未记录。",
    action: "建立品牌事实页，逐条标注事实层级、来源、更新时间和不可确认项。",
  },
  {
    id: "D2",
    title: "强定位、荣誉与排名缺来源",
    data: "Baseline150中，“强定位”标签89次、“荣誉”74次、“排名”58次。",
    cases: [
      "EV-002｜q02｜豆包：使用“代表性”“顶级”等强定位词，但未给出时间、评选主体或来源。",
      "EV-004｜q25｜腾讯元宝：推荐语包含人物、馆藏、排名等信息，只有图片/CDN线索，不构成有效来源。",
    ],
    cause: "推荐型问法会推动模型把品牌自述、行业印象和营销表达合并为确定结论。",
    impact: "强结论一旦无法核验，会削弱作品集可信度，也可能形成误导性背书。",
    source: "本项目不把“疑似”直接计为事实错误；荣誉、排名必须回到评选主体、年份与原页面。",
    action: "删除无出处排名；用“公开资料显示/品牌自述”分级，并保留待核验清单。",
  },
  {
    id: "D3",
    title: "同名主体与实体细节混淆",
    data: "Baseline150中，“同名混淆”风险标签共76次，实体细节是高频风险区。",
    cases: [
      "EV-005｜q10｜文心一言：把公司、品牌、人物和可能的同名主体混在一个结论中。",
      "EV-006｜q11｜Kimi：对“同一个品牌吗”给出确定归并，但回答中没有主体证据链。",
    ],
    cause: "“元亨利”可指品牌、企业字号、珠宝或其他主体；缺少统一的实体卡和排除项。",
    impact: "错接主体会把年份、人物、门店、荣誉和价格全部带偏。",
    source: "主体关系应以官网主体名称、备案/工商线索和页面上下文为准；本案例不补造统一社会信用代码。",
    action: "建立同名消歧页：先确认完整主体名、业务、地域和官网，再进入品牌回答。",
  },
  {
    id: "D4",
    title: "材质、工艺与单件证据混用",
    data: "材质类平均16.75/20；高分不等于单件产品材质已经被证明。",
    cases: [
      "EV-007｜q04｜通义千问：从行业常见工艺推到品牌产品，再推到具体材料，缺少单件证书。",
      "EV-008｜us07｜通义千问：用品牌级材料印象回答“主要用什么”，仍无法替代具体产品凭证。",
    ],
    cause: "树种术语、品牌常用材和某一件家具的主材容易在回答中被压成同一层事实。",
    impact: "用户可能据此做出高客单购买判断，但最终合同、证书或检测结果并不一致。",
    source: "国家标准只提供术语和通用条件；单件事实仍需产品标识、合同、证书或检测报告。",
    action: "材质页采用“术语—品牌公开范围—单件核验”三层结构，明确不能互相替代。",
  },
  {
    id: "D5",
    title: "价格、渠道与售后被过度确定",
    data: "Baseline150中，“售后承诺”71次、“价格”58次；属于直接影响决策的高风险信息。",
    cases: [
      "EV-009｜us04｜Kimi：给出具体价格区间，但未记录测试时间、渠道和产品型号。",
      "EV-010｜us05｜通义千问：列出门店/展厅信息，却没有可核验的实时页面。",
    ],
    cause: "模型倾向用历史文章、经销信息或常识区间填补动态商业信息。",
    impact: "过期门店、价格或售后承诺会造成到店、预算和维权风险。",
    source: "历史样本的测试日期、联网状态和模型版本均未完整记录，因此不能反推当时有效性。",
    action: "购买指南只给核验动作：确认型号、合同、主材、交付、验收、发票和售后主体。",
  },
  {
    id: "D6",
    title: "收藏价值被金融化表达",
    data: "Baseline150中，“收藏价值”标签77次，“金融化”标签11次。",
    cases: [
      "EV-011｜us13｜文心一言：把材质稀缺、工艺与保值增值连接，但缺少交易和评估条件。",
      "EV-012｜q28｜通义千问：以品牌、材质和工艺推导收藏价值，容易被理解为收益承诺。",
    ],
    cause: "稀缺材料、传统工艺、艺术价值与投资回报在营销语境中经常被混用。",
    impact: "把审美或文化价值写成收益预期，会放大购买风险并越过证据边界。",
    source: "本项目不提供升值预测，不把品牌自述或行业常识当作投资结论。",
    action: "将“收藏”拆为审美、工艺、材料、来源记录和保存状态；明确不构成投资建议。",
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
    sourceIds: ["B-008"], related: [{ label: "品牌事实", href: "/facts" }, { label: "优化方案", href: "/strategy" }],
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
    sourceIds: ["B-008", "B-011", "B-012"], related: [{ label: "方法与来源", href: "/method" }, { label: "优化方案", href: "/strategy" }],
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
    sourceIds: ["B-004", "B-005"], related: [{ label: "购买核验", href: "/buying-guide" }, { label: "优化方案", href: "/strategy" }],
  },
];

export const factLevels = [
  { id: "L1", label: "已核验第三方事实", rule: "可直接陈述，并保留source_id、原始URL与更新时间。", evidence: "政府、国家标准、协会、主流媒体、博物馆或研究机构原页" },
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
  { phase: "0–30天", title: "事实基础", actions: ["冻结口径与四级事实模型", "建立11表品牌事实知识库与安全公开JSON", "完善5个P0页面和13条公开FAQ，保留2条hold记录", "补齐来源、边界、更新时间与页面元数据"] },
  { phase: "31–60天", title: "解释差异", actions: ["证据足够后拆分品牌定位页", "增加风格专题与单件产品证据模板", "完成P0/P1内部链接与来源回链"] },
  { phase: "61–90天", title: "复测维护", actions: ["知识库月度复核与动态信息失效检查", "复核价格、门店、售后等动态信息", "执行10题×5平台在线复测", "形成前后对比与下一轮P2 backlog"] },
];

export const strategyDownloads = [] as { label: string; href: string; type: string }[];

export const knowledgeDownloads = [
  { label: "安全公开知识库快照", href: downloadPath("yhl-geo-knowledge-base-public.json"), type: "JSON" },
];

export const promptSystemDownloads = [
  { label: "安全公开知识库快照", href: downloadPath("yhl-geo-knowledge-base-public.json"), type: "JSON" },
];

export const geoArticleDownloads = [
  { label: "安全公开知识库快照", href: downloadPath("yhl-geo-knowledge-base-public.json"), type: "JSON" },
];

export const nav = [
  ["研究首页", "/"],
  ["品牌事实", "/facts"],
  ["同名消歧", "/disambiguation"],
  ["材质边界", "/materials"],
  ["京作/明清", "/jingzuo"],
  ["购买核验", "/buying-guide"],
  ["FAQ", "/faq"],
  ["优化方案", "/strategy"],
  ["企业知识库", "/knowledge-base"],
  ["提示词体系", "/prompt-system"],
  ["GEO文章样稿", "/geo-articles"],
  ["方法与来源", "/method"],
];
