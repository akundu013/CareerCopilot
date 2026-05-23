import { ProtectedRoute } from "@/components/auth/ProtectedRoute";
import { InterviewHistory } from "@/components/interview/InterviewHistory";
import { AppShell } from "@/components/layout/AppShell";
import { PageContainer } from "@/components/layout/PageContainer";

export default function InterviewHistoryPage() {
  return (
    <ProtectedRoute>
      <AppShell>
        <PageContainer
          description="Review saved interview practice sessions, revisit answers, and remove sessions you no longer need."
          eyebrow="Interview"
          title="Interview history"
        >
          <InterviewHistory />
        </PageContainer>
      </AppShell>
    </ProtectedRoute>
  );
}
