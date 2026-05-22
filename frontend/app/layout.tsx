import type { Metadata } from "next";
import "../styles/globals.scss";

export const metadata: Metadata = {
  title: "AI Job Search Copilot",
  description:
    "A SaaS-style job search workspace for tracking applications, improving resumes, and preparing for interviews.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
