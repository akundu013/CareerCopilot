import { ProtectedRoute } from "@/components/auth/ProtectedRoute";
import { InterviewPage } from "@/components/interview/InterviewPage";
import { AppShell } from "@/components/layout/AppShell";
import { PageContainer } from "@/components/layout/PageContainer";

export default function InterviewPracticePage() {
  return (
    <ProtectedRoute>
      <AppShell>
        <PageContainer
          description="Generate deterministic interview questions from a saved job match analysis and draft practice answers."
          eyebrow="Interview"
          title="Interview preparation"
        >
          <InterviewPage />
        </PageContainer>
      </AppShell>
    </ProtectedRoute>
  );
}
