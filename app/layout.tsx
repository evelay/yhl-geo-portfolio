import type { Metadata } from "next";
import "./globals.css";

const siteUrl = process.env.NEXT_PUBLIC_SITE_URL || "https://yhl-geo-portfolio-2026.layiiii.chatgpt.site";

export const metadata: Metadata = {
  metadataBase: new URL(siteUrl),
  title: { default: "元亨利红木家具 GEO 公开研究案例", template: "%s｜元亨利 GEO" },
  description: "基于225条AI回答、四维评分、信源审计、内容优化与90天执行方案的红木家具GEO求职作品集。",
  alternates: { canonical: "/" },
  openGraph: {
    title: "元亨利红木家具 GEO 公开研究案例",
    description: "225条AI回答、6项核心诊断、5个内容页面、15条FAQ与独立品牌内容优化方案。",
    images: [{ url: "/og-preview.png", width: 1200, height: 630 }],
    type: "website",
  },
  icons: {
    icon: "/favicon.svg",
    shortcut: "/favicon.svg",
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
