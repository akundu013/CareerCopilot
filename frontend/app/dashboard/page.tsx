import { AppShell } from "@/components/layout/AppShell";
import { PageContainer } from "@/components/layout/PageContainer";
import { Badge } from "@/components/ui/Badge";
import { Card } from "@/components/ui/Card";
import { EmptyState } from "@/components/ui/EmptyState";
import styles from "./page.module.scss";

const metrics = [
  { helper: "Application tracker arrives later", label: "Applications", value: "0" },
  { helper: "Resume storage arrives later", label: "Resumes", value: "0" },
  { helper: "Interview prep arrives later", label: "Interviews", value: "0" },
];

export default function DashboardPage() {
  return (
    <AppShell>
      <PageContainer
        description="This page establishes the first authenticated-style SaaS experience before Firebase, real data, or business features are introduced."
        eyebrow="Dashboard"
        title="Welcome to Career Copilot"
      >
        <div className={styles.statusRow}>
          <Badge tone="success">Milestone 2A</Badge>
          <Badge tone="neutral">Frontend shell</Badge>
        </div>

        <div className={styles.summaryGrid}>
          {metrics.map((metric) => (
            <Card key={metric.label}>
              <div className={styles.metric}>
                <span className={styles.metricLabel}>{metric.label}</span>
                <strong className={styles.metricValue}>{metric.value}</strong>
                <p>{metric.helper}</p>
              </div>
            </Card>
          ))}
        </div>

        <EmptyState
          description="Firebase, authentication, and real job search data will be added in future milestones."
          title="No workspace data yet"
        />
      </PageContainer>
    </AppShell>
  );
}
