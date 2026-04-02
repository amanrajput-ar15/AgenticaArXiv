import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./global.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "AgenticArXiv",
  description: "Autonomous Research Orchestration powered by Gemini",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      {/* suppressHydrationWarning ignores Chrome extension injections */}
      <body className={inter.className} suppressHydrationWarning>
        {children}
      </body>
    </html>
  );
}