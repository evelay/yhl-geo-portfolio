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
  title: { default: "元亨利红木家具 GEO 诊断与内容优化项目", template: "%s｜元亨利 GEO" },
  description: "基于公开资料完成的元亨利红木家具 GEO 诊断与内容优化项目，覆盖五平台测试、内容策略和研究方法。",
  alternates: { canonical: canonicalUrl },
  openGraph: {
    title: "元亨利红木家具 GEO 诊断与内容优化项目",
    description: "五平台回答测试、事实与来源治理、结构化内容与网站技术优化。",
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
