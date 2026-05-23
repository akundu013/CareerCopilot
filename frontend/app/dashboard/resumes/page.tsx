import { ProtectedRoute } from "@/components/auth/ProtectedRoute";
import { AppShell } from "@/components/layout/AppShell";
import { PageContainer } from "@/components/layout/PageContainer";
import { ResumeUploader } from "@/components/resumes/ResumeUploader";

export default function ResumesPage() {
  return (
    <ProtectedRoute>
      <AppShell>
        <PageContainer
          description="Upload resume files so Career Copilot can store the original document and prepare it for parsing."
          eyebrow="Resumes"
          title="Resume library"
        >
          <ResumeUploader />
        </PageContainer>
      </AppShell>
    </ProtectedRoute>
  );
}
