import assert from "node:assert/strict";
import { access, mkdir, mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { scanPublicArtifacts } from "../scripts/scan-public-artifacts.mjs";

function internalKey(...parts) {
  return parts.join("_");
}

function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function anyValuePattern(values) {
  return new RegExp(values.map(escapeRegExp).join("|"));
}

const sourceFileKey = internalKey("source", "file");
const sourceVersionKey = internalKey("source", "version");
const hashKey = ["sha", "256"].join("");
const internalReviewLabel = ["internal", "review"].join("-");
const hiddenVersionTokens = [
  internalKey("active", "scoring", "version"),
  internalKey("active", "analysis", "version"),
];
const hiddenMetricTokens = [
  internalKey("source", "id"),
  internalKey("brand", "mentioned"),
  internalKey("factual", "accuracy"),
  internalKey("source", "traceability"),
  internalKey("boundary", "control"),
  internalKey("recommendation", "quality"),
  internalKey("hallucination", "risk"),
];
const hiddenPageTokenPattern = anyValuePattern([
  ...hiddenVersionTokens,
  "core24",
  "r1.1",
  "high/critical",
]);
const legacyClaimPattern = anyValuePattern([
  ["Baseline", "150", "平均", "总分"].join(""),
  ["平均", "总分"].join(""),
  ["优化", "提升率"].join(""),
  ["平台", "总", "排名"].join(""),
  ["225", "条"].join(""),
]);
const rankingClaimPattern = anyValuePattern([
  ["平台", "综合", "能力", "排名"].join(""),
  ["平台", "综合", "排名"].join(""),
  ["单一", "综合", "总分"].join(""),
  ["最佳", "平台"].join(""),
  ["最差", "平台"].join(""),
  ["第一", "名"].join(""),
]);

async function render(pathname = "/") {
  const workerUrl = new URL("../dist/server/index.js", import.meta.url);
  workerUrl.searchParams.set("test", `${process.pid}-${Date.now()}-${pathname}`);
  const { default: worker } = await import(workerUrl.href);

  return worker.fetch(
    new Request(`http://localhost${pathname}`, {
      headers: { accept: "text/html" },
    }),
    {
      ASSETS: {
        fetch: async () => new Response("Not found", { status: 404 }),
      },
    },
    {
      waitUntil() {},
      passThroughOnException() {},
    },
  );
}

async function assertAccessible(pathname) {
  const response = await render(pathname);
  assert.equal(response.status, 200, `${pathname} should render`);
  return response.text();
}

async function assertRedirect(pathname, expectedPathname) {
  const response = await render(pathname);
  assert.equal(response.status, 308, `${pathname} should permanently redirect`);
  const location = response.headers.get("location");
  assert.ok(location, `${pathname} should provide a Location header`);
  assert.equal(new URL(location, "http://localhost").pathname, expectedPathname);
}

function stripTags(value) {
  return value.replace(/<wbr\s*\/?>/g, "").replace(/<[^>]*>/g, " ").replace(/\s+/g, " ").trim();
}

function extractH1s(html) {
  return [...html.matchAll(/<h1[^>]*>([\s\S]*?)<\/h1>/g)].map((match) => stripTags(match[1]));
}

function extractJsonLd(html) {
  return [...html.matchAll(/<script type="application\/ld\+json"[^>]*>([\s\S]*?)<\/script>/g)]
    .map((match) => JSON.parse(match[1]));
}

function jsonLdNodes(items) {
  return items.flatMap((item) => Array.isArray(item["@graph"]) ? item["@graph"] : [item]);
}

function nodesOfType(items, typeName) {
  return jsonLdNodes(items).filter((item) => item["@type"] === typeName);
}

function collectKeys(value, keys = new Set()) {
  if (Array.isArray(value)) {
    for (const item of value) collectKeys(item, keys);
    return keys;
  }
  if (value && typeof value === "object") {
    for (const [key, item] of Object.entries(value)) {
      keys.add(key);
      collectKeys(item, keys);
    }
  }
  return keys;
}

function extractBreadcrumbNavs(html) {
  return [...html.matchAll(/<nav[^>]*aria-label="面包屑导航"[^>]*>[\s\S]*?<\/nav>/g)].map((match) => match[0]);
}

test("server-renders all public GEO portfolio routes", async () => {
  const routes = [
    "/",
    "/case-study",
    "/experiment",
    "/content-governance",
    "/methodology",
    "/facts",
    "/disambiguation",
    "/materials",
    "/jingzuo",
    "/buying-guide",
    "/faq",
    "/knowledge-base",
    "/prompt-system",
    "/geo-articles",
  ];

  for (const route of routes) {
    const html = await assertAccessible(route);
    assert.match(html, /元亨利 GEO|元亨利红木家具|元亨利/);
    assert.match(html, /非元亨利品牌官方网站|未受品牌委托|不代表品牌/);
  }
});

test("legacy routes permanently redirect to their replacement pages", async () => {
  await assertRedirect("/strategy", "/content-governance");
  await assertRedirect("/method", "/methodology");
});

test("homepage presents the simplified portfolio IA without internal version language", async () => {
  const html = await assertAccessible("/");

  assert.match(html, /<title>元亨利红木家具 GEO 诊断与内容优化项目<\/title>/);
  assert.match(html, /独立 GEO 项目｜基于公开资料完成/);
  assert.match(html, /问题研究/);
  assert.match(html, /回答诊断/);
  assert.match(html, /内容优化/);
  assert.match(html, /后续复测/);
  assert.match(html, /品牌对象混淆/);
  assert.match(html, /专业概念被扩大解释/);
  assert.match(html, /购买判断缺少证据/);
  assert.match(html, /<strong>5<\/strong><span>AI平台<\/span>/);
  assert.match(html, /<strong>24<\/strong><span>核心问题<\/span>/);
  assert.match(html, /<strong>120<\/strong><span>完整回答<\/span>/);
  assert.match(html, /85\/120/);
  assert.match(html, /96\/120/);
  assert.match(html, /73\/120/);
  assert.match(html, /高或严重信息风险不代表回答全部内容错误。/);
  assert.match(html, /品牌事实页缩略图/);
  assert.match(html, /关键问题 FAQ缩略图/);
  assert.match(html, /购买核验指南缩略图/);
  assert.match(html, /AI搜索诊断页缩略图/);
  assert.match(html, /项目案例/);
  assert.match(html, /AI 搜索诊断/);
  assert.match(html, /内容策略/);
  assert.match(html, /品牌事实库/);
  assert.match(html, /class="mobile-nav-toggle"/);
  assert.match(html, /aria-controls="mobile-primary-nav"/);
  assert.doesNotMatch(html, legacyClaimPattern);
  assert.doesNotMatch(html, /GEO 实验/);
  assert.doesNotMatch(html, /对招聘方来说|本页展示|这不是/);
  assert.doesNotMatch(html, hiddenPageTokenPattern);
});

test("H1 summaries and visible breadcrumbs follow the simplified IA", async () => {
  const home = await assertAccessible("/");
  const caseStudy = await assertAccessible("/case-study");
  const experiment = await assertAccessible("/experiment");
  const governance = await assertAccessible("/content-governance");
  const methodology = await assertAccessible("/methodology");
  const facts = await assertAccessible("/facts");
  const buyingGuide = await assertAccessible("/buying-guide");

  assert.deepEqual(extractH1s(home), ["元亨利红木家具 GEO 诊断与内容优化"]);
  assert.equal(extractBreadcrumbNavs(home).length, 0);
  assert.equal(nodesOfType(extractJsonLd(home), "BreadcrumbList").length, 1);

  const expectedPages = [
    {
      route: "/case-study",
      html: caseStudy,
      h1: "元亨利红木家具 GEO 诊断与内容优化",
      breadcrumbName: "项目案例",
      canonical: "https://evelay.github.io/yhl-geo-portfolio/case-study/",
    },
    {
      route: "/experiment",
      html: experiment,
      h1: "AI 搜索诊断",
      breadcrumbName: "AI 搜索诊断",
      canonical: "https://evelay.github.io/yhl-geo-portfolio/experiment/",
    },
    {
      route: "/content-governance",
      html: governance,
      h1: "内容策略",
      breadcrumbName: "内容策略",
      canonical: "https://evelay.github.io/yhl-geo-portfolio/content-governance/",
    },
    {
      route: "/methodology",
      html: methodology,
      h1: "研究方法",
      breadcrumbName: "研究方法",
      canonical: "https://evelay.github.io/yhl-geo-portfolio/methodology/",
    },
    {
      route: "/facts",
      html: facts,
      h1: "元亨利品牌事实、来源与信息边界",
      summary: "针对AI回答中品牌主体、同名对象、官网来源和成立时间容易混淆的问题，本页将公开资料整理为可核验事实与信息边界。",
      breadcrumbName: "品牌事实与定位",
      parentName: "内容策略",
      canonical: "https://evelay.github.io/yhl-geo-portfolio/facts/",
    },
    {
      route: "/buying-guide",
      html: buyingGuide,
      h1: "元亨利红木家具购买核验指南",
      summary: "该资产解决AI用品牌声誉替代合同、材质和单件证据的问题，把购买建议转化为可执行核验清单。",
      breadcrumbName: "购买核验指南",
      parentName: "内容策略",
      canonical: "https://evelay.github.io/yhl-geo-portfolio/buying-guide/",
    },
  ];

  for (const page of expectedPages) {
    assert.deepEqual(extractH1s(page.html), [page.h1], `${page.route} should have one exact H1`);
    if (page.summary) {
      assert.match(page.html, new RegExp(page.summary.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")));
    }
    assert.match(page.html, new RegExp(`<link rel="canonical" href="${page.canonical.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}"`));
    assert.doesNotMatch(page.html, /\/Users\//);

    const breadcrumbNavs = extractBreadcrumbNavs(page.html);
    assert.equal(breadcrumbNavs.length, 1, `${page.route} should have one visible breadcrumb nav`);
    assert.match(breadcrumbNavs[0], /<ol>/);
    assert.match(breadcrumbNavs[0], /<li><a href="\/">首页<\/a><\/li>/);
    if (page.parentName) assert.match(breadcrumbNavs[0], new RegExp(page.parentName));
    assert.match(breadcrumbNavs[0], new RegExp(`<li aria-current="page">${page.breadcrumbName}</li>`));

    const breadcrumbLists = nodesOfType(extractJsonLd(page.html), "BreadcrumbList");
    assert.equal(breadcrumbLists.length, 1, `${page.route} should have one BreadcrumbList`);
    const lastItem = breadcrumbLists[0].itemListElement.at(-1);
    assert.equal(lastItem.name, page.breadcrumbName);
    assert.equal(lastItem.item, page.canonical);
  }
});

test("homepage renders the approved WebSite and WebPage JSON-LD graph", async () => {
  const html = await assertAccessible("/");
  const jsonLd = extractJsonLd(html);
  const nodes = jsonLdNodes(jsonLd);
  const website = nodesOfType(jsonLd, "WebSite");
  const webpage = nodesOfType(jsonLd, "WebPage");
  const breadcrumbList = nodesOfType(jsonLd, "BreadcrumbList");
  const expectedName = "元亨利红木家具 GEO 诊断与内容优化项目";
  const expectedCanonical = "https://evelay.github.io/yhl-geo-portfolio/";
  const forbiddenTypes = new Set([
    "Organization",
    "Brand",
    "Person",
    "SearchAction",
    "Article",
    "FAQPage",
    "Product",
    "Offer",
    "Review",
    "AggregateRating",
  ]);
  const forbiddenProperties = new Set([
    "publisher",
    "author",
    "creator",
    "copyrightHolder",
    "accountablePerson",
    "logo",
    "sameAs",
    "potentialAction",
  ]);

  assert.equal(jsonLd.length, 1);
  assert.equal(jsonLd[0]["@context"], "https://schema.org");
  assert.equal(jsonLd[0]["@graph"].length, 3);
  assert.deepEqual(jsonLd[0]["@graph"].map((node) => node["@type"]), ["WebSite", "WebPage", "BreadcrumbList"]);
  assert.equal(website.length, 1);
  assert.equal(webpage.length, 1);
  assert.equal(breadcrumbList.length, 1);

  for (const node of [website[0], webpage[0]]) {
    assert.equal(node.url, expectedCanonical);
    assert.equal(node.name, expectedName);
    assert.match(node.description, /公开资料|五平台|结构化内容|页面优化/);
    assert.equal(node.inLanguage, "zh-CN");
  }
  assert.deepEqual(breadcrumbList[0].itemListElement, [
    { "@type": "ListItem", position: 1, name: "首页", item: expectedCanonical },
  ]);

  assert.equal(website[0]["@id"], "https://evelay.github.io/yhl-geo-portfolio/#website");
  assert.equal(webpage[0]["@id"], "https://evelay.github.io/yhl-geo-portfolio/#webpage");
  assert.deepEqual(webpage[0].isPartOf, { "@id": website[0]["@id"] });

  for (const node of nodes) {
    assert.equal(forbiddenTypes.has(node["@type"]), false);
  }
  for (const key of collectKeys(jsonLd)) {
    assert.equal(forbiddenProperties.has(key), false);
  }
});

test("primary pages hide internal scoring and version fields", async () => {
  const forbidden = anyValuePattern([
    ...hiddenVersionTokens,
    ...hiddenMetricTokens,
    "core24",
    "r1.1",
    ["correction", "log"].join(" "),
    "completeness",
    "high/critical",
    ["visible", "URL"].join(" "),
  ]);

  for (const route of ["/", "/case-study", "/experiment", "/content-governance", "/methodology"]) {
    const html = await assertAccessible(route);
    assert.doesNotMatch(html, forbidden, `${route} should not expose internal wording`);
  }
});

test("final primary pages include the required content modules and diagnostic charts", async () => {
  const caseStudy = await assertAccessible("/case-study");
  const experiment = await assertAccessible("/experiment");
  const governance = await assertAccessible("/content-governance");
  const methodology = await assertAccessible("/methodology");

  for (const heading of ["项目背景", "项目目标", "诊断方法", "主要诊断结果", "三个代表案例", "优化方案与落地内容", "网站与技术实施", "项目成果", "项目边界与下一步"]) {
    assert.match(caseStudy, new RegExp(heading));
  }

  assert.match(experiment, /五个平台四项指标/);
  assert.match(experiment, /aria-label="五个平台四项指标分组柱状图，指标范围0到2分"/);
  assert.match(experiment, /aria-label="移动端五个平台指标卡"/);
  assert.match(experiment, /指标范围0—2分/);
  assert.match(experiment, /事实准确性/);
  assert.match(experiment, /回答完整性/);
  assert.match(experiment, /来源可追溯性/);
  assert.match(experiment, /信息边界控制/);
  assert.match(experiment, /1\.00/);
  assert.match(experiment, /1\.83/);
  assert.match(experiment, /1\.50/);
  assert.match(experiment, /1\.25/);
  assert.match(experiment, /aria-label="低、中、高、严重风险横向堆叠条形图，总计120条回答"/);
  assert.match(experiment, /title="低风险：13条"/);
  assert.match(experiment, /title="中等风险：34条"/);
  assert.match(experiment, /title="高风险：69条"/);
  assert.match(experiment, /title="严重风险：4条"/);
  assert.match(experiment, /本页的平台排列仅为固定展示顺序，不用于比较平台整体优劣。/);
  assert.match(experiment, /各项指标分别呈现，不合并为单一总分，也不形成平台整体优劣结论。/);
  assert.doesNotMatch(experiment, rankingClaimPattern);

  assert.match(governance, /关键问题 FAQ 如何产生/);
  assert.match(governance, /FAQ并非根据搜索量排名生成/);
  assert.match(governance, /形成首批13条关键问题 FAQ/);
  assert.match(governance, /品牌事实库（公开资料版）/);
  assert.match(governance, /公开来源/);
  assert.match(governance, /可核验事实/);
  assert.match(governance, /关键问题 FAQ/);

  for (const heading of ["测试问题如何设计", "为什么选择这五个AI平台", "回答如何采集", "回答如何判断", "如何减少评分偏差", "当前方法的限制", "下一轮如何验证优化效果"]) {
    assert.match(methodology, new RegExp(heading));
  }
  assert.match(methodology, /最终选出24个核心问题/);
  assert.match(methodology, /24个问题 × 5个平台 = 120条回答/);
  assert.match(methodology, /不是行业通用GEO评分标准，也不合并为一个总览分值/);
  assert.match(methodology, /提示词流程附录/);
  assert.match(methodology, /class="methodology-timeline"/);
  assert.doesNotMatch(methodology, /class="content-chain-flow five-step-flow" aria-label="整体研究框架"/);
});

test("knowledge base page is a simplified structure example without public JSON download", async () => {
  const html = await assertAccessible("/knowledge-base");

  assert.match(html, /品牌事实库（公开资料版）｜元亨利 GEO/);
  assert.match(html, /该结构用于解决品牌事实分散、来源与结论脱节、FAQ无法稳定引用/);
  assert.match(html, /公开版保留可核验、可关联、可复用的事实结构/);
  assert.match(html, /从资料到事实结构/);
  assert.match(html, /品牌主体与对象/);
  assert.match(html, /可核验事实/);
  assert.match(html, /六类公开结构/);
  assert.match(html, /三类来源证明范围/);
  assert.match(html, /黄花梨/);
  assert.doesNotMatch(html, /结构化知识库示例/);
  assert.doesNotMatch(html, /这不是/);
  assert.doesNotMatch(html, /11张表|字段字典|查询与看板|事实原子|映射记录|30题/);
  assert.doesNotMatch(html, /source_id|fact_id|question_id|evidence_id|content_id/);
  assert.doesNotMatch(html, /yhl-geo-knowledge-base-public\.json/);
  assert.doesNotMatch(html, /yhl-geo-brand-fact-knowledge-base\.xlsx/);
  assert.doesNotMatch(html, /yhl-geo-90-day-content-execution\.xlsx/);
  assert.match(html, /application\/ld\+json/);
});

test("prompt system page is a public summary without full prompts", async () => {
  const html = await assertAccessible("/prompt-system");

  assert.match(html, /提示词体系公开说明｜元亨利 GEO/);
  assert.match(html, /流程附录/);
  assert.match(html, /简化流程/);
  assert.match(html, /从问题到发布审核/);
  assert.match(html, /发布前检查什么/);
  assert.match(html, /匹配可核验事实/);
  assert.doesNotMatch(html, /yhl-geo-knowledge-base-public\.json/);
  assert.doesNotMatch(html, /yhl-geo-enterprise-prompt-system\.md/);
  assert.doesNotMatch(html, /PROMPT-01/);
  assert.doesNotMatch(html, /required_fact_ids/);
  assert.doesNotMatch(html, /risk_flags/);
  assert.doesNotMatch(html, /answer_mode/);
  assert.match(html, /application\/ld\+json/);
});

test("GEO article page is review-only without unpublished full bodies", async () => {
  const html = await assertAccessible("/geo-articles");
  const jsonLd = extractJsonLd(html);

  assert.match(html, /GEO文章样稿审核状态｜元亨利 GEO/);
  assert.match(html, /只展示标题、研究目的和审核状态/);
  assert.match(html, /暂缓公开完整正文/);
  assert.match(html, /<strong>0<\/strong><span>公开完整正文<\/span>/);
  assert.match(html, /完整文章 Markdown 已移入内部复核区/);
  assert.doesNotMatch(html, /yhl-geo-knowledge-base-public\.json/);
  assert.doesNotMatch(html, /yhl-geo-full-article-samples\.md/);
  assert.doesNotMatch(html, /yhl-geo-article-matrix\.md/);
  assert.doesNotMatch(html, /资质认证体系/);
  assert.doesNotMatch(html, /研发机构、技术团队构成/);
  assert.doesNotMatch(html, /question_id/);
  assert.doesNotMatch(html, /fact_id/);
  assert.doesNotMatch(html, /source_id/);
  assert.match(html, /application\/ld\+json/);
  assert.equal(nodesOfType(jsonLd, "WebPage").length, 1);
  assert.equal(nodesOfType(jsonLd, "BreadcrumbList").length, 1);
});

test("FAQ page only renders approved public FAQ entries", async () => {
  const html = await assertAccessible("/faq");

  assert.match(html, /该FAQ用于回应AI搜索中常见的品牌主体、材质、购买和价值判断问题/);
  assert.match(html, /默认展示<!-- -->8<!-- -->个代表问题/);
  assert.match(html, /查看完整问题列表/);
  assert.match(html, /FAQ-01/);
  assert.match(html, /FAQ-15/);
  assert.doesNotMatch(html, /FAQ-08/);
  assert.doesNotMatch(html, /FAQ-10/);
  assert.doesNotMatch(html, /元亨利一定是京作家具吗/);
  assert.doesNotMatch(html, /AI为什么容易把元亨利说错/);
});

test("knowledge base explorer exposes only filtered public levels and usable sources", async () => {
  const root = new URL("../", import.meta.url);
  const explorer = await readFile(new URL("app/knowledge-base/KnowledgeBaseExplorer.tsx", root), "utf8");

  assert.match(explorer, /placeholder="试试黄花梨、购买、官网"/);
  assert.match(explorer, /const levelOptions = \["全部类别", "权威第三方事实", "品牌公开自述", "单件产品证据"\]/);
  assert.match(explorer, /const sourceOptions = \["全部来源", "可用来源"\]/);
  assert.doesNotMatch(explorer, /source_id/);
  assert.doesNotMatch(explorer, /30题/);
  assert.doesNotMatch(explorer, /"L3"/);
  assert.doesNotMatch(explorer, /待补信源/);
  assert.match(explorer, /const mappingOptions = \["全部关联", "完整回答", "边界回答", "研究方法结论"\]/);
  assert.match(explorer, /setExpandedId/);
  assert.match(explorer, /activeTab === "facts"/);
  assert.match(explorer, /activeTab === "entities"/);
  assert.match(explorer, /activeTab === "sources"/);
  assert.match(explorer, /activeTab === "questions"/);
  assert.match(explorer, /activeTab === "faq"/);
});

test("public knowledge base snapshot is safety-filtered", async () => {
  const root = new URL("../", import.meta.url);
  await access(new URL("public/downloads/yhl-geo-knowledge-base-public.json", root));
  await access(new URL("public/data/yhl-geo-knowledge-base-public.json", root));

  const snapshot = JSON.parse(await readFile(new URL("public/data/yhl-geo-knowledge-base-public.json", root), "utf8"));
  const snapshotText = JSON.stringify(snapshot);
  assert.equal(snapshot.summary.sources, 24);
  assert.equal(snapshot.summary.usableSources, 24);
  assert.equal(snapshot.summary.excludedSources, 3);
  assert.equal(snapshot.summary.facts, 36);
  assert.equal(snapshot.summary.excludedFacts, 5);
  assert.equal(snapshot.summary.diagnosticQuestions, 25);
  assert.equal(snapshot.summary.faq, 13);
  assert.equal(snapshot.summary.excludedFaq, 2);
  assert.equal(snapshot.facts.some((fact) => fact.evidenceLevel === "L3"), false);
  assert.equal(snapshot.sources.some((source) => !source.usable), false);
  assert.equal(sourceFileKey in snapshot.metadata, false);
  assert.equal(sourceVersionKey in snapshot.metadata, false);
  assert.equal("architecture" in snapshot, false);
  assert.doesNotMatch(snapshotText, /元亨利GEO品牌事实知识库\.xlsx/);
  assert.doesNotMatch(snapshotText, /版本审核/);
  assert.deepEqual(
    snapshot.mappings.faq.map((item) => item.faqId),
    ["FAQ-01", "FAQ-02", "FAQ-03", "FAQ-04", "FAQ-05", "FAQ-06", "FAQ-07", "FAQ-09", "FAQ-11", "FAQ-12", "FAQ-13", "FAQ-14", "FAQ-15"],
  );
});

test("manifest and download directories match publication decisions", async () => {
  const root = new URL("../", import.meta.url);
  const manifest = JSON.parse(await readFile(new URL("public/downloads/manifest.json", root), "utf8"));
  const manifestText = JSON.stringify(manifest);

  const publicEntries = manifest.files.filter((file) => file.publication_status === "public");
  assert.deepEqual(publicEntries.map((file) => file.filename), ["yhl-geo-knowledge-base-public.json"]);
  assert.equal(manifest.files.length, 1);
  assert.doesNotMatch(manifestText, /\/Users\//);
  assert.doesNotMatch(manifestText, /file:\/\//);
  assert.doesNotMatch(manifestText, /New project/);
  assert.doesNotMatch(manifestText, /yhl_geo_portfolio_delivery/);
  assert.doesNotMatch(manifestText, new RegExp(`${internalReviewLabel}/downloads`));
  assert.doesNotMatch(manifestText, new RegExp(internalReviewLabel));
  assert.doesNotMatch(manifestText, new RegExp(hashKey));
  assert.doesNotMatch(manifestText, new RegExp(sourceVersionKey));
  assert.doesNotMatch(manifestText, new RegExp(sourceFileKey));
  assert.doesNotMatch(manifestText, /工作簿/);
  assert.doesNotMatch(manifestText, /完整 GEO 文章样稿|企业提示词体系|90 天内容执行/);

  for (const file of publicEntries) {
    assert.match(file.public_url, new RegExp(`/downloads/${file.filename.replaceAll(".", "\\.")}$`));
    assert.match(file.review_status, /^(approved|conditional)$/);
    assert.ok(file.source_label);
    assert.ok(file.source_scope);
    assert.ok(file.last_verified);
    assert.ok(file.disclaimer);
    assert.equal(hashKey in file, false);
    assert.equal(sourceFileKey in file, false);
    assert.equal(sourceVersionKey in file, false);
  }

  await assert.rejects(access(new URL("public/downloads/yhl-geo-brand-content-optimization-plan.pdf", root)));
  await assert.rejects(access(new URL("public/downloads/yhl-geo-brand-content-optimization-plan.docx", root)));
  await assert.rejects(access(new URL("public/downloads/yhl-geo-enterprise-prompt-system.md", root)));
  await assert.rejects(access(new URL("public/downloads/yhl-geo-article-matrix.md", root)));
  await assert.rejects(access(new URL("public/downloads/yhl-geo-full-article-samples.md", root)));
  await assert.rejects(access(new URL("public/downloads/yhl-geo-brand-fact-knowledge-base.xlsx", root)));
  await assert.rejects(access(new URL("public/downloads/yhl-geo-90-day-content-execution.xlsx", root)));
});

test("public pages only link approved or conditional public downloads", async () => {
  const root = new URL("../", import.meta.url);
  const manifest = JSON.parse(await readFile(new URL("public/downloads/manifest.json", root), "utf8"));
  const allowed = new Set(
    manifest.files
      .filter((file) => file.publication_status === "public" && /^(approved|conditional)$/.test(file.review_status))
      .map((file) => `/downloads/${file.filename}`),
  );

  for (const route of ["/", "/knowledge-base", "/prompt-system", "/geo-articles"]) {
    const html = await assertAccessible(route);
    const links = [...html.matchAll(/href="([^"]*\/downloads\/[^"]+)"/g)].map((match) => {
      const url = match[1].replace(/^https?:\/\/localhost/, "");
      return url.startsWith("/yhl-geo-portfolio/downloads/")
        ? url.replace("/yhl-geo-portfolio", "")
        : url;
    });
    for (const link of links) {
      assert.ok(allowed.has(link), `${route} links non-public download: ${link}`);
    }
  }

  const sitemap = await readFile(new URL("public/sitemap.xml", root), "utf8");
  assert.match(sitemap, /\/knowledge-base\/?<\/loc>/);
  assert.match(sitemap, /\/prompt-system\/?<\/loc>/);
  assert.match(sitemap, /\/geo-articles\/?<\/loc>/);
  assert.doesNotMatch(sitemap, /\/strategy\/?<\/loc>/);
  assert.doesNotMatch(sitemap, /\/method\/?<\/loc>/);
});

test("public artifact scan keeps business files free of local paths", async () => {
  const rootPath = fileURLToPath(new URL("../", import.meta.url));
  const result = await scanPublicArtifacts(rootPath);

  assert.deepEqual(result.violations, []);
  for (const match of result.matches.filter((item) => item.matched_pattern === "localhost")) {
    assert.equal(match.status, "accepted-third-party-literal");
    assert.equal(match.source_type, "third-party-vendor");
    assert.match(match.artifact, /^out\/_next\/static\/chunks\/[^/]+\.js$/);
  }
});

test("public artifact scanner does not hide localhost in business files", async () => {
  const fixtureRoot = await mkdtemp(join(tmpdir(), "public-scan-"));

  try {
    await mkdir(join(fixtureRoot, "public"), { recursive: true });
    await writeFile(join(fixtureRoot, "public", "bad.json"), '{"url":"http://localhost:3000"}');

    let result = await scanPublicArtifacts(fixtureRoot);
    assert.equal(result.violations.length, 1);
    assert.equal(result.violations[0].source_type, "project-data");
    assert.equal(result.violations[0].status, "manual-review");

    await rm(join(fixtureRoot, "public", "bad.json"));
    await mkdir(join(fixtureRoot, "out", "_next", "static", "chunks"), { recursive: true });
    await writeFile(join(fixtureRoot, "out", "_next", "static", "chunks", "vendor.js"), 'const host = "localhost";');

    result = await scanPublicArtifacts(fixtureRoot);
    assert.equal(result.violations.length, 0);
    assert.equal(result.matches.length, 1);
    assert.equal(result.matches[0].status, "accepted-third-party-literal");
  } finally {
    await rm(fixtureRoot, { recursive: true, force: true });
  }
});
