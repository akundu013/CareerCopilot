import { AnalysisForm } from "@/components/analysis/AnalysisForm";
import { ProtectedRoute } from "@/components/auth/ProtectedRoute";
import { AppShell } from "@/components/layout/AppShell";
import { PageContainer } from "@/components/layout/PageContainer";

export default function AnalysisPage() {
  return (
    <ProtectedRoute>
      <AppShell>
        <PageContainer
          description="Compare a parsed resume against a job description and save the generated match analysis."
          eyebrow="Analysis"
          title="Job match analysis"
        >
          <AnalysisForm />
        </PageContainer>
      </AppShell>
    </ProtectedRoute>
  );
}
