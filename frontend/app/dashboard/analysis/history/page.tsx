import { AnalysisHistory } from "@/components/analysis/AnalysisHistory";
import { ProtectedRoute } from "@/components/auth/ProtectedRoute";
import { AppShell } from "@/components/layout/AppShell";
import { PageContainer } from "@/components/layout/PageContainer";

export default function AnalysisHistoryPage() {
  return (
    <ProtectedRoute>
      <AppShell>
        <PageContainer
          description="Review saved job match analyses and remove results you no longer need."
          eyebrow="Analysis"
          title="Analysis history"
        >
          <AnalysisHistory />
        </PageContainer>
      </AppShell>
    </ProtectedRoute>
  );
}
