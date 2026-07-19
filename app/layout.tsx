import type { Metadata } from "next";
import "./globals.css";

const defaultSiteUrl = "https://evelay.github.io/yhl-geo-portfolio";

function normalizeUrl(value: string) {
  return value.replace(/\/+$/, "");
}

function inferSiteUrl() {
  if (process.env.NEXT_PUBLIC_SITE_URL) {
    return normalizeUrl(process.env.NEXT_PUBLIC_SITE_URL);
  }

  if (process.env.GITHUB_PAGES === "true" && process.env.GITHUB_REPOSITORY) {
    const [owner, repo] = process.env.GITHUB_REPOSITORY.split("/");
    if (owner && repo) {
      return repo === `${owner}.github.io`
        ? `https://${owner}.github.io`
        : `https://${owner}.github.io/${repo}`;
    }
  }

  return defaultSiteUrl;
}

const siteUrl = inferSiteUrl();
const canonicalUrl = `${siteUrl}/`;
const faviconUrl = `${siteUrl}/favicon.svg`;

export const metadata: Metadata = {
  metadataBase: new URL(canonicalUrl),
  title: { default: "元亨利红木家具 GEO 公开研究案例", template: "%s｜元亨利 GEO" },
  description: "基于公开资料与225条AI回答的独立GEO研究作品集，未受元亨利委托，不代表品牌官方立场。",
  alternates: { canonical: canonicalUrl },
  openGraph: {
    title: "元亨利红木家具 GEO 公开研究案例",
    description: "公开资料研究、6项核心诊断、5个内容页面、13条公开FAQ与安全知识库快照；不代表品牌官方立场。",
    images: [{ url: `${siteUrl}/og-preview.png`, width: 1200, height: 630 }],
    type: "website",
  },
  icons: {
    icon: faviconUrl,
    shortcut: faviconUrl,
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="zh-CN">
      <body>{children}</body>
    </html>
  );
}
