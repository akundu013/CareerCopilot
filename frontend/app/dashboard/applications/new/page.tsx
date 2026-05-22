import { ApplicationForm } from "@/components/applications/ApplicationForm";
import { ProtectedRoute } from "@/components/auth/ProtectedRoute";
import { AppShell } from "@/components/layout/AppShell";
import { PageContainer } from "@/components/layout/PageContainer";

export default function NewApplicationPage() {
  return (
    <ProtectedRoute>
      <AppShell>
        <PageContainer
          description="Record a job opportunity so Career Copilot can help track the next step in your search."
          eyebrow="Applications"
          title="Add application"
        >
          <ApplicationForm />
        </PageContainer>
      </AppShell>
    </ProtectedRoute>
  );
}
