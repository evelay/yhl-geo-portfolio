import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { access, readFile } from "node:fs/promises";
import test from "node:test";

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

  const publicEntries = manifest.files.filter((file) => file.publication_status === "public");
  const internalEntries = manifest.files.filter((file) => file.publication_status === "internal-review");
  assert.deepEqual(publicEntries.map((file) => file.filename), ["yhl-geo-knowledge-base-public.json"]);

  for (const file of publicEntries) {
    assert.match(file.public_url, new RegExp(`/downloads/${file.filename.replaceAll(".", "\\.")}$`));
    assert.match(file.review_status, /^(approved|conditional)$/);
    assert.equal(await sha256(new URL(`public/downloads/${file.filename}`, root)), file.sha256);
    assert.ok(file.source_file);
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
    await access(new URL(`internal-review/downloads/${filename}`, root));
  }

  for (const file of internalEntries) {
    assert.equal(file.public_url, "");
    assert.equal(file.review_status, "blocked");
    assert.equal(await sha256(new URL(`internal-review/downloads/${file.filename}`, root)), file.sha256);
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
