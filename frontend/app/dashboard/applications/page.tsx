import { ApplicationTable } from "@/components/applications/ApplicationTable";
import { ProtectedRoute } from "@/components/auth/ProtectedRoute";
import { AppShell } from "@/components/layout/AppShell";
import { PageContainer } from "@/components/layout/PageContainer";

export default function ApplicationsPage() {
  return (
    <ProtectedRoute>
      <AppShell>
        <PageContainer
          description="Track every role, company, and next step from one focused workspace."
          eyebrow="Applications"
          title="Application tracker"
        >
          <ApplicationTable />
        </PageContainer>
      </AppShell>
    </ProtectedRoute>
  );
}
