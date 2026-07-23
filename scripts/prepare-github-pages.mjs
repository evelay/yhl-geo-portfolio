import { access, readFile, writeFile } from "node:fs/promises";
import { join } from "node:path";

const root = process.cwd();
const outDir = join(root, "out");
const defaultRepository = "evelay/yhl-geo-portfolio";
const defaultSiteUrl = "https://evelay.github.io/yhl-geo-portfolio";

function normalizeBasePath(value) {
  if (!value) return "";
  const trimmed = value.trim().replace(/^\/+|\/+$/g, "");
  return trimmed ? `/${trimmed}` : "";
}

function normalizeUrl(value) {
  return value.replace(/\/+$/, "");
}

function repositoryParts() {
  const repository = process.env.GITHUB_REPOSITORY || defaultRepository;
  const [owner, repo] = repository.split("/");
  return { owner, repo };
}

function inferBasePath() {
  if (process.env.NEXT_PUBLIC_BASE_PATH !== undefined) {
    return normalizeBasePath(process.env.NEXT_PUBLIC_BASE_PATH);
  }

  const { owner, repo } = repositoryParts();
  if (!owner || !repo || repo === `${owner}.github.io`) return "";
  return normalizeBasePath(repo);
}

function inferSiteUrl() {
  if (process.env.NEXT_PUBLIC_SITE_URL) {
    return normalizeUrl(process.env.NEXT_PUBLIC_SITE_URL);
  }

  const { owner, repo } = repositoryParts();
  if (!owner || !repo) return defaultSiteUrl;
  if (repo === `${owner}.github.io`) return `https://${owner}.github.io`;
  return `https://${owner}.github.io/${repo}`;
}

async function exists(filePath) {
  try {
    await access(filePath);
    return true;
  } catch {
    return false;
  }
}

function routePathFromLoc(loc, basePath) {
  const url = new URL(loc);
  let pathname = url.pathname || "/";

  if (basePath && (pathname === basePath || pathname.startsWith(`${basePath}/`))) {
    pathname = pathname.slice(basePath.length) || "/";
  }

  if (!pathname.startsWith("/")) pathname = `/${pathname}`;
  return pathname === "/" ? "/" : pathname.replace(/\/?$/, "/");
}

function renderLoc(siteUrl, routePath) {
  return routePath === "/" ? `${siteUrl}/` : `${siteUrl}${routePath}`;
}

function rewriteSitemap(sitemap, siteUrl, basePath) {
  return sitemap.replace(/<loc>([^<]+)<\/loc>/g, (_, loc) => {
    try {
      const routePath = routePathFromLoc(loc, basePath);
      return `<loc>${renderLoc(siteUrl, routePath)}</loc>`;
    } catch {
      return `<loc>${loc}</loc>`;
    }
  });
}

function renderRobots(siteUrl) {
  return `User-agent: *\nAllow: /\n\nSitemap: ${siteUrl}/sitemap.xml\n`;
}

async function prepareRobots(siteUrl) {
  const robotsPath = join(outDir, "robots.txt");
  await writeFile(robotsPath, renderRobots(siteUrl));
}

async function prepareSitemap(siteUrl, basePath) {
  const outSitemapPath = join(outDir, "sitemap.xml");
  const publicSitemapPath = join(root, "public", "sitemap.xml");
  const sourcePath = (await exists(outSitemapPath)) ? outSitemapPath : publicSitemapPath;
  const sitemap = await readFile(sourcePath, "utf8");
  await writeFile(outSitemapPath, rewriteSitemap(sitemap, siteUrl, basePath));
}

async function main() {
  await access(outDir);

  const siteUrl = inferSiteUrl();
  const basePath = inferBasePath();

  await prepareRobots(siteUrl);
  await prepareSitemap(siteUrl, basePath);
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
