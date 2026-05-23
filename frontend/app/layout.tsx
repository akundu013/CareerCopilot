import type { Metadata } from "next";
import { AuthProvider } from "@/components/auth/AuthProvider";
import "../styles/globals.scss";

export const metadata: Metadata = {
  title: "Career Copilot",
  description:
    "A SaaS-style job search workspace for tracking applications, improving resumes, and preparing for interviews.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html data-scroll-behavior="smooth" lang="en">
      <body>
        <AuthProvider>{children}</AuthProvider>
      </body>
    </html>
  );
}
