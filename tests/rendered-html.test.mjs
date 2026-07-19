import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { access, mkdir, mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { scanPublicArtifacts } from "../scripts/scan-public-artifacts.mjs";

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

function stripTags(value) {
  return value.replace(/<[^>]*>/g, "").replace(/\s+/g, " ").trim();
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

async function sha256(url) {
  const content = await readFile(url);
  return createHash("sha256").update(content).digest("hex");
}

test("server-renders all public GEO portfolio routes", async () => {
  const routes = [
    "/",
    "/facts",
    "/disambiguation",
    "/materials",
    "/jingzuo",
    "/buying-guide",
    "/faq",
    "/strategy",
    "/knowledge-base",
    "/prompt-system",
    "/geo-articles",
    "/method",
  ];

  for (const route of routes) {
    const html = await assertAccessible(route);
    assert.match(html, /元亨利 GEO|元亨利红木家具|元亨利/);
    assert.match(html, /不代表(?:品牌)?官方|不代表元亨利官方/);
  }
});

test("homepage discloses project identity and baseline data version", async () => {
  const html = await assertAccessible("/");

  assert.match(html, /公开研究首页｜元亨利 GEO/);
  assert.match(html, /独立 GEO 研究案例/);
  assert.match(html, /基于公开资料/);
  assert.match(html, /未受元亨利委托/);
  assert.match(html, /不代表品牌官方立场/);
  assert.match(html, /数据版本：baseline 基线，尚未完成复测/);
  assert.match(html, /2026-07-13/);
  assert.match(html, /Excel 序列值 46216/);
  assert.match(html, /人工评分，不是模型自动评分/);
  assert.match(html, /元亨利GEO_投递版数据与分析\.xlsx/);
  assert.match(html, /当前指标不代表优化后增长或长期趋势/);
  assert.match(html, /13条公开FAQ/);
  assert.match(html, /FAQ-08、FAQ-10继续hold/);
});

test("H1 summaries and visible breadcrumbs follow 07C2 decisions", async () => {
  const home = await assertAccessible("/");
  const facts = await assertAccessible("/facts");
  const buyingGuide = await assertAccessible("/buying-guide");

  assert.deepEqual(extractH1s(home), ["元亨利红木家具 GEO 诊断与可核验内容体系"]);
  assert.match(home, /本页呈现基于公开资料完成、未受元亨利委托且不代表品牌官方立场的独立 GEO 研究/);
  assert.equal(extractBreadcrumbNavs(home).length, 0);
  assert.equal(nodesOfType(extractJsonLd(home), "BreadcrumbList").length, 0);

  const expectedPages = [
    {
      route: "/facts",
      html: facts,
      h1: "元亨利品牌事实、来源与信息边界",
      summary: "本页汇总元亨利可公开核验的品牌事实、来源与信息边界，并区分已确认、需谨慎表述和暂不应公开推断的内容。",
      breadcrumbName: "品牌事实与定位",
      canonical: "https://evelay.github.io/yhl-geo-portfolio/facts/",
    },
    {
      route: "/buying-guide",
      html: buyingGuide,
      h1: "元亨利红木家具购买核验指南",
      summary: "本页提供评估元亨利红木家具时可执行的核验框架，重点关注材质、工艺、来源、单件证据和信息边界，不构成购买或投资建议。",
      breadcrumbName: "购买核验指南",
      canonical: "https://evelay.github.io/yhl-geo-portfolio/buying-guide/",
    },
  ];

  for (const page of expectedPages) {
    assert.deepEqual(extractH1s(page.html), [page.h1], `${page.route} should have one exact H1`);
    assert.match(page.html, new RegExp(page.summary.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")));
    assert.match(page.html, new RegExp(`<link rel="canonical" href="${page.canonical.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}"`));
    assert.doesNotMatch(page.html, /\/Users\//);

    const breadcrumbNavs = extractBreadcrumbNavs(page.html);
    assert.equal(breadcrumbNavs.length, 1, `${page.route} should have one visible breadcrumb nav`);
    assert.match(breadcrumbNavs[0], /<ol>/);
    assert.match(breadcrumbNavs[0], /<li><a href="\/">首页<\/a><\/li>/);
    assert.match(breadcrumbNavs[0], new RegExp(`<li aria-current="page">${page.breadcrumbName}</li>`));

    const breadcrumbLists = extractJsonLd(page.html).filter((item) => item["@type"] === "BreadcrumbList");
    assert.equal(breadcrumbLists.length, 1, `${page.route} should have one BreadcrumbList`);
    assert.equal(breadcrumbLists[0].itemListElement[1].name, page.breadcrumbName);
    assert.equal(breadcrumbLists[0].itemListElement[1].item, page.canonical);
  }
});

test("homepage renders the approved WebSite and WebPage JSON-LD graph", async () => {
  const html = await assertAccessible("/");
  const jsonLd = extractJsonLd(html);
  const nodes = jsonLdNodes(jsonLd);
  const website = nodesOfType(jsonLd, "WebSite");
  const webpage = nodesOfType(jsonLd, "WebPage");
  const expectedName = "元亨利红木家具 GEO 诊断与可核验内容体系";
  const expectedDescription = "本页呈现基于公开资料完成、未受元亨利委托且不代表品牌官方立场的独立 GEO 研究案例，围绕 AI 回答基线、品牌事实治理、内容体系和页面技术优化，诊断认知与证据缺口。";
  const expectedCanonical = "https://evelay.github.io/yhl-geo-portfolio/";
  const forbiddenTypes = new Set([
    "Organization",
    "Brand",
    "Person",
    "SearchAction",
    "BreadcrumbList",
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
  assert.equal(jsonLd[0]["@graph"].length, 2);
  assert.deepEqual(jsonLd[0]["@graph"].map((node) => node["@type"]), ["WebSite", "WebPage"]);
  assert.equal(website.length, 1);
  assert.equal(webpage.length, 1);

  for (const node of nodes) {
    assert.equal(node.url, expectedCanonical);
    assert.equal(node.name, expectedName);
    assert.equal(node.description, expectedDescription);
    assert.equal(node.inLanguage, "zh-CN");
  }

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

test("knowledge base page only links the safety-filtered public JSON", async () => {
  const html = await assertAccessible("/knowledge-base");

  assert.match(html, /企业知识库｜元亨利 GEO/);
  assert.match(html, /安全过滤后的公开快照/);
  assert.match(html, /在线查看知识库/);
  assert.match(html, /事实原子库/);
  assert.match(html, /实体主表/);
  assert.match(html, /信源主表/);
  assert.match(html, /30题映射/);
  assert.match(html, /公开FAQ映射/);
  assert.match(html, /FACT-0001/);
  assert.match(html, /黄花梨/);
  assert.match(html, /11张表/);
  assert.match(html, /六个典型查询/);
  assert.match(html, /yhl-geo-knowledge-base-public\.json/);
  assert.doesNotMatch(html, /yhl-geo-brand-fact-knowledge-base\.xlsx/);
  assert.doesNotMatch(html, /yhl-geo-90-day-content-execution\.xlsx/);
  assert.match(html, /application\/ld\+json/);
});

test("prompt system page is a public summary without full prompts", async () => {
  const html = await assertAccessible("/prompt-system");

  assert.match(html, /提示词体系公开说明｜元亨利 GEO/);
  assert.match(html, /讲方法/);
  assert.match(html, /不公开完整提示词/);
  assert.match(html, /工作流程/);
  assert.match(html, /输入与输出结构/);
  assert.match(html, /人工审核节点/);
  assert.match(html, /脱敏短示例/);
  assert.match(html, /yhl-geo-knowledge-base-public\.json/);
  assert.doesNotMatch(html, /yhl-geo-enterprise-prompt-system\.md/);
  assert.doesNotMatch(html, /PROMPT-01/);
  assert.doesNotMatch(html, /required_fact_ids/);
  assert.doesNotMatch(html, /risk_flags/);
  assert.doesNotMatch(html, /answer_mode/);
  assert.match(html, /application\/ld\+json/);
});

test("GEO article page is review-only without unpublished full bodies", async () => {
  const html = await assertAccessible("/geo-articles");

  assert.match(html, /GEO文章样稿审核状态｜元亨利 GEO/);
  assert.match(html, /只展示标题、研究目的和审核状态/);
  assert.match(html, /暂缓公开完整正文/);
  assert.match(html, /<strong>0<\/strong><span>公开完整正文<\/span>/);
  assert.match(html, /完整文章 Markdown 已移入内部复核区/);
  assert.match(html, /yhl-geo-knowledge-base-public\.json/);
  assert.doesNotMatch(html, /yhl-geo-full-article-samples\.md/);
  assert.doesNotMatch(html, /yhl-geo-article-matrix\.md/);
  assert.doesNotMatch(html, /资质认证体系/);
  assert.doesNotMatch(html, /研发机构、技术团队构成/);
  assert.doesNotMatch(html, /question_id/);
  assert.doesNotMatch(html, /fact_id/);
  assert.doesNotMatch(html, /source_id/);
  assert.match(html, /application\/ld\+json/);
});

test("FAQ page only renders approved public FAQ entries", async () => {
  const html = await assertAccessible("/faq");

  assert.match(html, /当前公开 <!-- -->13<!-- --> 条已通过来源与发布检查的 FAQ/);
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

  assert.match(explorer, /placeholder="试试 FACT-0001、黄花梨、B-001、q03"/);
  assert.match(explorer, /const levelOptions = \["全部等级", "L1", "L2", "L4"\]/);
  assert.match(explorer, /const sourceOptions = \["全部信源", "可用信源"\]/);
  assert.doesNotMatch(explorer, /"L3"/);
  assert.doesNotMatch(explorer, /待补信源/);
  assert.match(explorer, /const mappingOptions = \["全部映射", "完整回答", "边界回答", "研究方法结论"\]/);
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
  const internalEntries = manifest.files.filter((file) => file.publication_status === "internal-review");
  assert.deepEqual(publicEntries.map((file) => file.filename), ["yhl-geo-knowledge-base-public.json"]);
  assert.doesNotMatch(manifestText, /\/Users\//);
  assert.doesNotMatch(manifestText, /file:\/\//);
  assert.doesNotMatch(manifestText, /New project/);
  assert.doesNotMatch(manifestText, /yhl_geo_portfolio_delivery/);
  assert.doesNotMatch(manifestText, /internal-review\/downloads/);

  for (const file of publicEntries) {
    assert.match(file.public_url, new RegExp(`/downloads/${file.filename.replaceAll(".", "\\.")}$`));
    assert.match(file.review_status, /^(approved|conditional)$/);
    assert.equal(await sha256(new URL(`public/downloads/${file.filename}`, root)), file.sha256);
    assert.equal("source_file" in file, false);
    assert.ok(file.source_id);
    assert.ok(file.source_label);
    assert.ok(file.source_scope);
    assert.ok(file.source_version);
    assert.ok(file.last_verified);
    assert.ok(file.disclaimer);
  }

  const expectedInternalFiles = new Set([
    "yhl-geo-brand-content-optimization-plan.pdf",
    "yhl-geo-brand-content-optimization-plan.docx",
    "yhl-geo-enterprise-prompt-system.md",
    "yhl-geo-article-matrix.md",
    "yhl-geo-full-article-samples.md",
    "yhl-geo-brand-fact-knowledge-base.xlsx",
    "yhl-geo-90-day-content-execution.xlsx",
    "yhl-geo-knowledge-base-public.json",
  ]);
  for (const filename of expectedInternalFiles) {
    assert.ok(internalEntries.some((file) => file.filename === filename), `${filename} should be listed as internal-review`);
  }

  for (const file of internalEntries) {
    assert.equal(file.public_url, "");
    assert.equal(file.review_status, "blocked");
    assert.equal("source_file" in file, false);
    assert.ok(file.source_id);
    assert.ok(file.source_label);
    assert.ok(file.source_scope);
    assert.ok(file.source_version);
    try {
      const publicHash = await sha256(new URL(`public/downloads/${file.filename}`, root));
      assert.notEqual(publicHash, file.sha256, `${file.filename} internal hash must not be public`);
      assert.ok(publicEntries.some((entry) => entry.filename === file.filename), `${file.filename} public copy must be represented separately`);
    } catch (error) {
      assert.equal(error.code, "ENOENT");
    }
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

  for (const route of ["/", "/strategy", "/knowledge-base", "/prompt-system", "/geo-articles"]) {
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
  assert.match(sitemap, /\/knowledge-base<\/loc>/);
  assert.match(sitemap, /\/prompt-system<\/loc>/);
  assert.match(sitemap, /\/geo-articles<\/loc>/);
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
