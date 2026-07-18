import { access, writeFile } from "node:fs/promises";
import { join } from "node:path";

const root = process.cwd();
const outDir = join(root, "out");
const defaultSiteUrl = "https://evelay.github.io/yhl-geo-portfolio";
const sitemapPaths = [
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
const lastmod = "2026-07-17";

function normalizeUrl(value) {
  return value.replace(/\/+$/, "");
}

function inferGitHubPagesUrl() {
  if (process.env.NEXT_PUBLIC_SITE_URL) {
    return normalizeUrl(process.env.NEXT_PUBLIC_SITE_URL);
  }

  const repository = process.env.GITHUB_REPOSITORY;
  if (!repository) return defaultSiteUrl;

  const [owner, repo] = repository.split("/");
  if (!owner || !repo) return defaultSiteUrl;

  if (repo === `${owner}.github.io`) {
    return `https://${owner}.github.io`;
  }

  return `https://${owner}.github.io/${repo}`;
}

async function writePreparedFile(fileName, siteUrl) {
  const filePath = join(outDir, fileName);

  try {
    await access(filePath);
  } catch {
    return;
  }

  const content = fileName === "robots.txt" ? renderRobots(siteUrl) : renderSitemap(siteUrl);
  await writeFile(filePath, content);
}

function renderRobots(siteUrl) {
  return `User-agent: *\nAllow: /\n\nSitemap: ${siteUrl}/sitemap.xml\n`;
}

function renderSitemap(siteUrl) {
  const entries = sitemapPaths
    .map((path) => {
      const loc = path === "/" ? `${siteUrl}/` : `${siteUrl}${path}`;
      return `  <url><loc>${loc}</loc><lastmod>${lastmod}</lastmod></url>`;
    })
    .join("\n");

  return `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${entries}\n</urlset>\n`;
}

async function main() {
  await access(outDir);

  const siteUrl = inferGitHubPagesUrl();
  await writePreparedFile("robots.txt", siteUrl);
  await writePreparedFile("sitemap.xml", siteUrl);
  await writeFile(join(outDir, ".nojekyll"), "");

  if (process.env.GITHUB_PAGES_CNAME) {
    await writeFile(join(outDir, "CNAME"), `${process.env.GITHUB_PAGES_CNAME.trim()}\n`);
  }

  console.log(`Prepared GitHub Pages static output for ${siteUrl}`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
