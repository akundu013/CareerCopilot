"use client";

import { useCallback, useEffect, useState } from "react";
import { ApplicationForm } from "@/components/applications/ApplicationForm";
import { Button } from "@/components/ui/Button";
import { Spinner } from "@/components/ui/Spinner";
import {
  getApplicationById,
  updateApplication,
} from "@/services/application-api";
import type { CreateApplicationInput, JobApplication } from "@/types/application";
import styles from "./ApplicationForm.module.scss";

interface EditApplicationPanelProps {
  applicationId: string;
}

export function EditApplicationPanel({
  applicationId,
}: EditApplicationPanelProps) {
  const [application, setApplication] = useState<JobApplication | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const loadApplication = useCallback(async (showLoading = true) => {
    try {
      if (showLoading) {
        setIsLoading(true);
        setError(null);
      }

      setApplication(await getApplicationById(applicationId));
      setError(null);
    } catch (loadError) {
      setError(
        loadError instanceof Error
          ? loadError.message
          : "Unable to load this application. Please try again.",
      );
    } finally {
      setIsLoading(false);
    }
  }, [applicationId]);

  useEffect(() => {
    const timerId = window.setTimeout(() => {
      void loadApplication(false);
    }, 0);

    return () => window.clearTimeout(timerId);
  }, [loadApplication]);

  async function handleUpdate(input: CreateApplicationInput) {
    await updateApplication(applicationId, input);
  }

  if (isLoading) {
    return (
      <section className={styles.statePanel} aria-live="polite">
        <Spinner label="Loading application" />
        <p>Loading application...</p>
      </section>
    );
  }

  if (error) {
    return (
      <section className={styles.statePanel} aria-live="polite">
        <h2>Unable to load application</h2>
        <p>{error}</p>
        <div className={styles.stateActions}>
          <Button href="/dashboard/applications" variant="secondary">
            Back to applications
          </Button>
          <Button onClick={() => void loadApplication()}>Try again</Button>
        </div>
      </section>
    );
  }

  if (!application) {
    return (
      <section className={styles.statePanel} aria-live="polite">
        <h2>Application not found</h2>
        <p>This application may have been removed or is unavailable.</p>
        <Button href="/dashboard/applications" variant="secondary">
          Back to applications
        </Button>
      </section>
    );
  }

  return (
    <ApplicationForm
      cancelHref="/dashboard/applications"
      initialApplication={application}
      onSubmit={handleUpdate}
      submitLabel="Update application"
      submittingLabel="Updating..."
    />
  );
}
