"use client";

import { useState } from "react";
import { ProtectedRoute } from "@/components/auth/ProtectedRoute";
import { AppShell } from "@/components/layout/AppShell";
import { PageContainer } from "@/components/layout/PageContainer";
import { ResumeList } from "@/components/resumes/ResumeList";
import { ResumeUploader } from "@/components/resumes/ResumeUploader";

export default function ResumesPage() {
  const [resumeRefreshKey, setResumeRefreshKey] = useState(0);

  function refreshResumes() {
    setResumeRefreshKey((currentKey) => currentKey + 1);
  }

  return (
    <ProtectedRoute>
      <AppShell>
        <PageContainer
          description="Upload resume files so Career Copilot can store the original document and prepare it for parsing."
          eyebrow="Resumes"
          title="Resume library"
        >
          <ResumeUploader onUploadComplete={refreshResumes} />
          <ResumeList refreshKey={resumeRefreshKey} />
        </PageContainer>
      </AppShell>
    </ProtectedRoute>
  );
}
