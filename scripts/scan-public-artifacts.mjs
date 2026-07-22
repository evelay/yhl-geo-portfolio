import { readdir, readFile, stat } from "node:fs/promises";
import { join, relative, sep } from "node:path";
import { fileURLToPath } from "node:url";

const textExtensions = new Set([".css", ".html", ".js", ".json", ".svg", ".txt", ".xml"]);
const restrictedDownloadPattern = new RegExp(
  `(?:\\/Users\\/[^"'\\s<>]*\\/)?${["internal", "review"].join("-")}\\/downloads\\/[^"'\\s<>]+`,
  "g",
);
const userHomePathPattern = new RegExp(["", "Users", ""].join("\\/"), "g");
const fileSchemePattern = new RegExp(["file", "://"].join(""), "g");

const forbiddenPatterns = [
  { id: "user home path", regex: userHomePathPattern },
  { id: "file scheme", regex: fileSchemePattern },
  { id: "New project", regex: /New project/g },
  { id: "yhl_geo_portfolio_delivery", regex: /yhl_geo_portfolio_delivery/g },
  { id: "chatgpt.site", regex: /chatgpt\.site/g },
  { id: "real internal review path", regex: restrictedDownloadPattern },
];

const localhostPattern = { id: "localhost", regex: /localhost/g };

function normalizePath(value) {
  return value.split(sep).join("/");
}

function extensionOf(filePath) {
  const dotIndex = filePath.lastIndexOf(".");
  return dotIndex === -1 ? "" : filePath.slice(dotIndex);
}

function isTextArtifact(filePath) {
  return textExtensions.has(extensionOf(filePath));
}

function isVendorChunk(relativePath) {
  return /^out\/_next\/static\/chunks\/[^/]+\.js$/.test(relativePath);
}

function sourceTypeFor(relativePath) {
  if (isVendorChunk(relativePath)) return "third-party-vendor";
  if (relativePath.startsWith("out/")) return "generated-business-artifact";
  if (relativePath.startsWith("public/")) return "project-data";
  return "unknown";
}

function contextFor(content, index) {
  const start = Math.max(0, index - 60);
  const end = Math.min(content.length, index + 80);
  return content.slice(start, end).replace(/\s+/g, " ").trim();
}

function collectPatternMatches(content, pattern, artifact, sourceType) {
  const matches = [];
  pattern.regex.lastIndex = 0;

  for (const match of content.matchAll(pattern.regex)) {
    matches.push({
      artifact,
      matched_pattern: pattern.id,
      match_context: contextFor(content, match.index ?? 0),
      source_type: sourceType,
      risk: "public local path or restricted provenance leak",
      action: "remove from public artifact or replace with logical source identifier",
      status: "manual-review",
      notes: "",
    });
  }

  return matches;
}

async function walk(rootDir, currentDir = rootDir) {
  let entries;
  try {
    entries = await readdir(currentDir, { withFileTypes: true });
  } catch (error) {
    if (error.code === "ENOENT") return [];
    throw error;
  }

  const files = [];
  for (const entry of entries) {
    const fullPath = join(currentDir, entry.name);
    if (entry.isDirectory()) {
      files.push(...(await walk(rootDir, fullPath)));
      continue;
    }
    if (entry.isFile() && isTextArtifact(entry.name)) files.push(fullPath);
  }
  return files;
}

export async function scanPublicArtifacts(rootDir = process.cwd()) {
  const scanRoots = [join(rootDir, "public"), join(rootDir, "out")];
  const files = [];

  for (const scanRoot of scanRoots) {
    try {
      const info = await stat(scanRoot);
      if (info.isDirectory()) files.push(...(await walk(rootDir, scanRoot)));
    } catch (error) {
      if (error.code !== "ENOENT") throw error;
    }
  }

  const matches = [];

  for (const filePath of files) {
    const artifact = normalizePath(relative(rootDir, filePath));
    const sourceType = sourceTypeFor(artifact);
    const content = await readFile(filePath, "utf8");

    for (const pattern of forbiddenPatterns) {
      matches.push(...collectPatternMatches(content, pattern, artifact, sourceType));
    }

    const localhostMatches = collectPatternMatches(content, localhostPattern, artifact, sourceType);
    for (const match of localhostMatches) {
      if (isVendorChunk(artifact)) {
        matches.push({
          ...match,
          risk: "low",
          action: "accepted only for generated Next vendor chunk",
          status: "accepted-third-party-literal",
          notes: "Exact allowlist: out/_next/static/chunks/*.js. Business artifacts still fail on localhost.",
        });
      } else {
        matches.push({
          ...match,
          risk: "business artifact points to local runtime literal",
          action: "remove localhost from public business artifact",
        });
      }
    }
  }

  const violations = matches.filter((match) => match.status !== "accepted-third-party-literal");
  return { checked_files: files.length, matches, violations };
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const result = await scanPublicArtifacts(process.cwd());
  console.log(JSON.stringify(result, null, 2));
  if (result.violations.length > 0) process.exitCode = 1;
}
