import { access, readFile, writeFile } from "node:fs/promises";
import { join } from "node:path";

const root = process.cwd();
const outDir = join(root, "out");
const previousSiteUrl = "https://yhl-geo-portfolio-2026.layiiii.chatgpt.site";

function normalizeUrl(value) {
  return value.replace(/\/+$/, "");
}

function inferGitHubPagesUrl() {
  if (process.env.NEXT_PUBLIC_SITE_URL) {
    return normalizeUrl(process.env.NEXT_PUBLIC_SITE_URL);
  }

  const repository = process.env.GITHUB_REPOSITORY;
  if (!repository) return previousSiteUrl;

  const [owner, repo] = repository.split("/");
  if (!owner || !repo) return previousSiteUrl;

  if (repo === `${owner}.github.io`) {
    return `https://${owner}.github.io`;
  }

  return `https://${owner}.github.io/${repo}`;
}

async function replaceSiteUrl(fileName, siteUrl) {
  const filePath = join(outDir, fileName);

  try {
    await access(filePath);
  } catch {
    return;
  }

  const content = await readFile(filePath, "utf8");
  await writeFile(filePath, content.replaceAll(previousSiteUrl, siteUrl));
}

async function main() {
  await access(outDir);

  const siteUrl = inferGitHubPagesUrl();
  await replaceSiteUrl("robots.txt", siteUrl);
  await replaceSiteUrl("sitemap.xml", siteUrl);
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
