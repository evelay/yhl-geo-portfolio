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
  assert.match(html, /不代表元亨利官方/);
});

test("server-renders the knowledge base page with downloads and governance", async () => {
  const response = await render("/knowledge-base");
  assert.equal(response.status, 200);

  const html = await response.text();
  assert.match(html, /企业知识库｜元亨利 GEO/);
  assert.match(html, /11张表/);
  assert.match(html, /四级事实模型/);
  assert.match(html, /六个典型查询/);
  assert.match(html, /yhl-geo-brand-fact-knowledge-base\.xlsx/);
  assert.match(html, /yhl-geo-knowledge-base-public\.json/);
  assert.match(html, /application\/ld\+json/);
});

test("ships public knowledge base files and sitemap entry", async () => {
  const root = new URL("../", import.meta.url);
  await access(new URL("public/downloads/yhl-geo-brand-fact-knowledge-base.xlsx", root));
  await access(new URL("public/downloads/yhl-geo-knowledge-base-public.json", root));
  await access(new URL("public/data/yhl-geo-knowledge-base-public.json", root));

  const snapshot = JSON.parse(await readFile(new URL("public/data/yhl-geo-knowledge-base-public.json", root), "utf8"));
  assert.equal(snapshot.summary.sources, 27);
  assert.equal(snapshot.summary.usableSources, 24);
  assert.equal(snapshot.summary.pendingSources, 3);
  assert.equal(snapshot.summary.diagnosticQuestions, 30);
  assert.equal(snapshot.summary.faq, 15);

  const sitemap = await readFile(new URL("public/sitemap.xml", root), "utf8");
  assert.match(sitemap, /\/knowledge-base<\/loc>/);
});
