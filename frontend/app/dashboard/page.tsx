import { ProtectedRoute } from "@/components/auth/ProtectedRoute";
import { AppShell } from "@/components/layout/AppShell";
import { PageContainer } from "@/components/layout/PageContainer";
import { Badge } from "@/components/ui/Badge";
import { Card } from "@/components/ui/Card";
import { EmptyState } from "@/components/ui/EmptyState";
import styles from "./page.module.scss";

const metrics = [
  {
    helper: "Manage tracked roles in the application workspace",
    label: "Applications",
    value: "0",
  },
  {
    helper: "Upload, list, and parse resumes from the resume library",
    label: "Resumes",
    value: "0",
  },
  {
    helper: "Interview prep arrives in a later milestone",
    label: "Interviews",
    value: "0",
  },
];

export default function DashboardPage() {
  return (
    <ProtectedRoute>
      <AppShell>
        <PageContainer
          description="A focused workspace for tracking applications, managing resumes, and preparing future job-search intelligence."
          eyebrow="Dashboard"
          title="Welcome to Career Copilot"
        >
          <div className={styles.statusRow}>
            <Badge tone="success">Milestone 6</Badge>
            <Badge tone="neutral">Resume management</Badge>
          </div>

          <div className={styles.summaryGrid}>
            {metrics.map((metric) => (
              <Card key={metric.label}>
                <div className={styles.metric}>
                  <span className={styles.metricLabel}>{metric.label}</span>
                  <strong className={styles.metricValue}>
                    {metric.value}
                  </strong>
                  <p>{metric.helper}</p>
                </div>
              </Card>
            ))}
          </div>

          <EmptyState
            description="Use the sidebar to manage applications and resumes. Match analysis and interview preparation arrive in future milestones."
            title="Workspace ready"
          />
        </PageContainer>
      </AppShell>
    </ProtectedRoute>
  );
}
