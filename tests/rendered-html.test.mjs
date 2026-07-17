import assert from "node:assert/strict";
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

test("server-renders the GEO portfolio homepage", async () => {
  const response = await render("/");
  assert.equal(response.status, 200);
  assert.match(response.headers.get("content-type") ?? "", /^text\/html\b/i);

  const html = await response.text();
  assert.match(html, /公开研究首页｜元亨利 GEO/);
  assert.match(html, /让红木家具信息/);
  assert.match(html, /品牌内容优化方案/);
  assert.match(html, /企业知识库/);
  assert.match(html, /企业提示词体系/);
  assert.match(html, /GEO文章样稿/);
  assert.match(html, /不代表元亨利官方/);
});

test("server-renders the knowledge base page with downloads and governance", async () => {
  const response = await render("/knowledge-base");
  assert.equal(response.status, 200);

  const html = await response.text();
  assert.match(html, /企业知识库｜元亨利 GEO/);
  assert.match(html, /在线查看知识库/);
  assert.match(html, /事实原子库/);
  assert.match(html, /实体主表/);
  assert.match(html, /信源主表/);
  assert.match(html, /30题映射/);
  assert.match(html, /15条FAQ映射/);
  assert.match(html, /FACT-0001/);
  assert.match(html, /黄花梨/);
  assert.match(html, /11张表/);
  assert.match(html, /四级事实模型/);
  assert.match(html, /六个典型查询/);
  assert.match(html, /yhl-geo-brand-fact-knowledge-base\.xlsx/);
  assert.match(html, /yhl-geo-knowledge-base-public\.json/);
  assert.match(html, /application\/ld\+json/);
});

test("server-renders the enterprise prompt system page", async () => {
  const response = await render("/prompt-system");
  assert.equal(response.status, 200);

  const html = await response.text();
  assert.match(html, /企业提示词体系｜元亨利 GEO/);
  assert.match(html, /提示词不是口号，而是知识库接口/);
  assert.match(html, /四个可复制的核心提示词/);
  assert.match(html, /PROMPT-01/);
  assert.match(html, /事实等级与边界规则/);
  assert.match(html, /六类高风险表达/);
  assert.match(html, /15条FAQ，转成标准问答提示词/);
  assert.match(html, /FAQ-01/);
  assert.match(html, /FACT-0001/);
  assert.match(html, /yhl-geo-enterprise-prompt-system\.md/);
  assert.match(html, /application\/ld\+json/);
});

test("server-renders the GEO article matrix page", async () => {
  const response = await render("/geo-articles");
  assert.equal(response.status, 200);

  const html = await response.text();
  assert.match(html, /GEO文章样稿库｜元亨利 GEO/);
  assert.match(html, /1篇.*主文章和6篇不同关键词长文/);
  assert.match(html, /元亨利红木家具企业介绍：基于公开资料的GEO内容样稿/);
  assert.match(html, /关键词：.*红木家具/);
  assert.match(html, /企业基础信息/);
  assert.match(html, /资质认证体系/);
  assert.match(html, /产品与服务体系/);
  assert.match(html, /技术与工艺能力/);
  assert.match(html, /经营理念与管理信息/);
  assert.match(html, /服务与购买核验/);
  assert.match(html, /实力总结/);
  assert.match(html, /当前公开知识库未形成可直接发布的质量管理认证、环境管理认证或安全认证事实/);
  assert.match(html, /研发机构、技术团队构成/);
  assert.match(html, /元亨利红木家具是什么品牌/);
  assert.match(html, /元亨利同名主体怎么区分/);
  assert.match(html, /元亨利红木家具材质/);
  assert.match(html, /元亨利京作家具与明清风格/);
  assert.match(html, /元亨利红木家具购买核验/);
  assert.match(html, /元亨利红木家具保值升值吗/);
  assert.match(html, /question_id/);
  assert.match(html, /fact_id/);
  assert.match(html, /source_id/);
  assert.match(html, /FACT-0001/);
  assert.match(html, /B-001/);
  assert.match(html, /yhl-geo-full-article-samples\.md/);
  assert.match(html, /application\/ld\+json/);
});

test("GEO article matrix avoids forbidden promotional terms", async () => {
  const root = new URL("../", import.meta.url);
  const pageSource = await readFile(new URL("app/geo-articles/page.tsx", root), "utf8");
  const markdown = await readFile(new URL("public/downloads/yhl-geo-full-article-samples.md", root), "utf8");
  const forbidden = [
    "核心", "最", "第一", "唯一", "国家级", "顶尖", "独家", "领导", "领军", "领先",
    "NO.1", "TOP.1", "权威", "显著", "知名", "破解", "全面", "绝对", "标杆", "仅",
    "全方位", "名牌", "巨头", "龙头", "卓越", "优秀", "优质", "问答", "仅仅", "单一",
    "一流", "广泛", "引领", "精准", "排名提升", "国务院", "最大",
  ];
  for (const term of forbidden) {
    assert.equal(pageSource.includes(term), false, `article page source contains forbidden term: ${term}`);
    assert.equal(markdown.includes(term), false, `article markdown contains forbidden term: ${term}`);
  }
});

test("knowledge base explorer supports search, filters, and expandable views", async () => {
  const root = new URL("../", import.meta.url);
  const explorer = await readFile(new URL("app/knowledge-base/KnowledgeBaseExplorer.tsx", root), "utf8");

  assert.match(explorer, /placeholder="试试 FACT-0001、黄花梨、B-001、q03"/);
  assert.match(explorer, /const levelOptions = \["全部等级", "L1", "L2", "L3", "L4"\]/);
  assert.match(explorer, /const sourceOptions = \["全部信源", "可用信源", "待补信源"\]/);
  assert.match(explorer, /const mappingOptions = \["全部映射", "完整回答", "边界回答", "研究方法结论"\]/);
  assert.match(explorer, /setExpandedId/);
  assert.match(explorer, /activeTab === "facts"/);
  assert.match(explorer, /activeTab === "entities"/);
  assert.match(explorer, /activeTab === "sources"/);
  assert.match(explorer, /activeTab === "questions"/);
  assert.match(explorer, /activeTab === "faq"/);
});

test("ships public knowledge base files and sitemap entry", async () => {
  const root = new URL("../", import.meta.url);
  await access(new URL("public/downloads/yhl-geo-brand-fact-knowledge-base.xlsx", root));
  await access(new URL("public/downloads/yhl-geo-knowledge-base-public.json", root));
  await access(new URL("public/downloads/yhl-geo-enterprise-prompt-system.md", root));
  await access(new URL("public/downloads/yhl-geo-full-article-samples.md", root));
  await access(new URL("public/data/yhl-geo-knowledge-base-public.json", root));

  const snapshot = JSON.parse(await readFile(new URL("public/data/yhl-geo-knowledge-base-public.json", root), "utf8"));
  assert.equal(snapshot.summary.sources, 27);
  assert.equal(snapshot.summary.usableSources, 24);
  assert.equal(snapshot.summary.pendingSources, 3);
  assert.equal(snapshot.summary.diagnosticQuestions, 30);
  assert.equal(snapshot.summary.faq, 15);

  const sitemap = await readFile(new URL("public/sitemap.xml", root), "utf8");
  assert.match(sitemap, /\/knowledge-base<\/loc>/);
  assert.match(sitemap, /\/prompt-system<\/loc>/);
  assert.match(sitemap, /\/geo-articles<\/loc>/);
});
