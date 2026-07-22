import type { NextConfig } from "next";

function normalizeBasePath(value: string | undefined) {
  if (!value) return "";
  const trimmed = value.trim().replace(/^\/+|\/+$/g, "");
  return trimmed ? `/${trimmed}` : "";
}

function inferGitHubPagesBasePath() {
  const explicit = process.env.NEXT_PUBLIC_BASE_PATH;
  if (explicit !== undefined) return normalizeBasePath(explicit);

  const repository = process.env.GITHUB_REPOSITORY;
  if (!repository) return "";

  const [owner, repo] = repository.split("/");
  if (!owner || !repo) return "";

  return repo === `${owner}.github.io` ? "" : normalizeBasePath(repo);
}

const isGitHubPagesBuild = process.env.GITHUB_PAGES === "true";
const githubPagesBasePath = isGitHubPagesBuild ? inferGitHubPagesBasePath() : "";

const nextConfig: NextConfig = {
  ...(isGitHubPagesBuild
    ? {
        output: "export" as const,
        trailingSlash: true,
        basePath: githubPagesBasePath || undefined,
        assetPrefix: githubPagesBasePath || undefined,
        images: {
          unoptimized: true,
        },
      }
    : {}),
};

export default nextConfig;
