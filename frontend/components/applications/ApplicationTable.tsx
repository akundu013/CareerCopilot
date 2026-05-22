"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import {
  ApplicationFilters,
  type ApplicationStatusFilter,
} from "@/components/applications/ApplicationFilters";
import { ApplicationRow } from "@/components/applications/ApplicationRow";
import { Button } from "@/components/ui/Button";
import { EmptyState } from "@/components/ui/EmptyState";
import { Spinner } from "@/components/ui/Spinner";
import { getApplications } from "@/services/application-api";
import type { JobApplication } from "@/types/application";
import styles from "./ApplicationTable.module.scss";

function getCreatedTime(application: JobApplication): number {
  const createdAt = new Date(application.createdAt).getTime();

  return Number.isNaN(createdAt) ? 0 : createdAt;
}

export function ApplicationTable() {
  const [applications, setApplications] = useState<JobApplication[]>([]);
  const [activeFilter, setActiveFilter] =
    useState<ApplicationStatusFilter>("all");
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const loadApplications = useCallback(async (showLoading = true) => {
    try {
      if (showLoading) {
        setIsLoading(true);
        setError(null);
      }

      setApplications(await getApplications());
      setError(null);
    } catch (loadError) {
      setError(
        loadError instanceof Error
          ? loadError.message
          : "Unable to load applications. Please try again.",
      );
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    const timerId = window.setTimeout(() => {
      void loadApplications(false);
    }, 0);

    return () => window.clearTimeout(timerId);
  }, [loadApplications]);

  const sortedApplications = useMemo(
    () =>
      [...applications].sort(
        (firstApplication, secondApplication) =>
          getCreatedTime(secondApplication) - getCreatedTime(firstApplication),
      ),
    [applications],
  );

  const filteredApplications = useMemo(() => {
    if (activeFilter === "all") {
      return sortedApplications;
    }

    return sortedApplications.filter(
      (application) => application.status === activeFilter,
    );
  }, [activeFilter, sortedApplications]);

  if (isLoading) {
    return (
      <section className={styles.statePanel} aria-live="polite">
        <Spinner label="Loading applications" />
        <p>Loading applications...</p>
      </section>
    );
  }

  if (error) {
    return (
      <section className={styles.statePanel} aria-live="polite">
        <h2>Unable to load applications</h2>
        <p>{error}</p>
        <Button onClick={() => void loadApplications()} variant="secondary">
          Try again
        </Button>
      </section>
    );
  }

  return (
    <section className={styles.tableSection}>
      <div className={styles.toolbar}>
        <ApplicationFilters
          activeFilter={activeFilter}
          onFilterChange={setActiveFilter}
        />
        <Button href="/dashboard/applications/new">Add application</Button>
      </div>

      {applications.length === 0 ? (
        <div className={styles.emptyWrap}>
          <EmptyState
            description="Create your first tracked application to start building a clear job-search pipeline."
            title="No applications yet"
          />
          <Button href="/dashboard/applications/new">Add application</Button>
        </div>
      ) : filteredApplications.length === 0 ? (
        <div className={styles.emptyWrap}>
          <EmptyState
            description="Try a different status filter or add another application."
            title="No applications match this filter"
          />
        </div>
      ) : (
        <div className={styles.tableWrap}>
          <table className={styles.table}>
            <thead>
              <tr>
                <th scope="col">Company</th>
                <th scope="col">Role</th>
                <th scope="col">Status</th>
                <th scope="col">Location</th>
                <th scope="col">Applied</th>
                <th scope="col">Updated</th>
              </tr>
            </thead>
            <tbody>
              {filteredApplications.map((application) => (
                <ApplicationRow
                  application={application}
                  key={application.id}
                />
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}
