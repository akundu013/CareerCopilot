import { AnalyticsDashboard } from "@/components/analytics/AnalyticsDashboard";
import { ProtectedRoute } from "@/components/auth/ProtectedRoute";
import { AppShell } from "@/components/layout/AppShell";
import { PageContainer } from "@/components/layout/PageContainer";

export default function AnalyticsPage() {
  return (
    <ProtectedRoute>
      <AppShell>
        <PageContainer
          description="Track job-search momentum, match quality, resume readiness, and interview preparation progress from your saved data."
          eyebrow="Analytics"
          title="Analytics dashboard"
        >
          <AnalyticsDashboard />
        </PageContainer>
      </AppShell>
    </ProtectedRoute>
  );
}
