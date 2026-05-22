"use client";

import { useParams } from "next/navigation";
import { EditApplicationPanel } from "@/components/applications/EditApplicationPanel";
import { ProtectedRoute } from "@/components/auth/ProtectedRoute";
import { AppShell } from "@/components/layout/AppShell";
import { PageContainer } from "@/components/layout/PageContainer";

function getApplicationId(id: string | string[] | undefined): string {
  if (Array.isArray(id)) {
    return id[0] ?? "";
  }

  return id ?? "";
}

export default function EditApplicationPage() {
  const params = useParams<{ id?: string | string[] }>();
  const applicationId = getApplicationId(params.id);

  return (
    <ProtectedRoute>
      <AppShell>
        <PageContainer
          description="Update the details, status, and notes for this tracked role."
          eyebrow="Applications"
          title="Edit application"
        >
          <EditApplicationPanel applicationId={applicationId} />
        </PageContainer>
      </AppShell>
    </ProtectedRoute>
  );
}
