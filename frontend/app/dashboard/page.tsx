import Link from "next/link";
import { ProtectedRoute } from "@/components/auth/ProtectedRoute";
import { AppShell } from "@/components/layout/AppShell";
import { PageContainer } from "@/components/layout/PageContainer";
import { Badge } from "@/components/ui/Badge";
import { Card } from "@/components/ui/Card";
import styles from "./page.module.scss";

const workspaceAreas = [
  {
    description: "Track companies, roles, statuses, notes, and edit history.",
    href: "/dashboard/applications",
    label: "Applications",
    status: "Ready",
  },
  {
    description: "Upload resumes, store metadata, parse text, and manage files.",
    href: "/dashboard/resumes",
    label: "Resumes",
    status: "Ready",
  },
  {
    description: "Compare parsed resumes with job descriptions and review gaps.",
    href: "/dashboard/analysis",
    label: "Match Analysis",
    status: "Ready",
  },
  {
    description: "Generate interview questions and save practice answers.",
    href: "/dashboard/interview",
    label: "Interview Prep",
    status: "Ready",
  },
  {
    description: "Review application, resume, analysis, and interview trends.",
    href: "/dashboard/analytics",
    label: "Analytics",
    status: "Ready",
  },
  {
    description: "Use controlled sample data without risking real user records.",
    href: "/login",
    label: "Demo Mode",
    status: "Configured",
  },
];

export default function DashboardPage() {
  return (
    <ProtectedRoute>
      <AppShell>
        <PageContainer
          description="A working job-search command center for applications, resumes, match analysis, interview preparation, analytics, demo access, and AI-assisted feedback."
          eyebrow="Dashboard"
          title="Welcome to Career Copilot"
        >

          <div className={styles.quickActions}>
            <Link href="/dashboard/applications/new">Add application</Link>
            <Link href="/dashboard/resumes">Upload resume</Link>
            <Link href="/dashboard/analysis">Analyze job match</Link>
          </div>

          <div className={styles.workspaceGrid}>
            {workspaceAreas.map((area) => (
              <Link className={styles.areaLink} href={area.href} key={area.label}>
                <Card>
                  <div className={styles.area}>
                    <span className={styles.areaStatus}>{area.status}</span>
                    <h2>{area.label}</h2>
                    <p>{area.description}</p>
                  </div>
                </Card>
              </Link>
            ))}
          </div>
        </PageContainer>
      </AppShell>
    </ProtectedRoute>
  );
}
