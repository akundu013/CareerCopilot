"use client";

import { useEffect, useMemo, useState } from "react";
import { Button } from "@/components/ui/Button";
import { Spinner } from "@/components/ui/Spinner";
import { getAnalyticsSummary } from "@/services/analytics-api";
import type { AnalyticsSummary } from "@/types/analytics";
import { AnalyticsEmptyState } from "./AnalyticsEmptyState";
import { ApplicationsByStatusChart } from "./ApplicationsByStatusChart";
import { RequirementsChart } from "./RequirementsChart";
import { SummaryCard } from "./SummaryCard";
import { WeeklyActivityChart } from "./WeeklyActivityChart";
import styles from "./AnalyticsDashboard.module.scss";

function isEmptySummary(summary: AnalyticsSummary): boolean {
  return (
    summary.totalApplications === 0 &&
    summary.totalResumes === 0 &&
    summary.totalAnalyses === 0 &&
    summary.totalInterviewSessions === 0
  );
}

function formatPercent(value: number): string {
  return `${Math.round(value)}%`;
}

export function AnalyticsDashboard() {
  const [summary, setSummary] = useState<AnalyticsSummary | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const parsedResumeLabel = useMemo(() => {
    if (!summary) {
      return "0";
    }

    return `${summary.parsedResumes}/${summary.totalResumes}`;
  }, [summary]);

  useEffect(() => {
    let isMounted = true;

    async function loadAnalytics() {
      try {
        setIsLoading(true);
        setError(null);
        const analyticsSummary = await getAnalyticsSummary();

        if (isMounted) {
          setSummary(analyticsSummary);
        }
      } catch (loadError) {
        if (!isMounted) {
          return;
        }

        setError(
          loadError instanceof Error
            ? loadError.message
            : "Unable to load analytics. Please try again.",
        );
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    }

    loadAnalytics();

    return () => {
      isMounted = false;
    };
  }, []);

  if (isLoading) {
    return (
      <section className={styles.statePanel} aria-live="polite">
        <Spinner label="Loading analytics" />
        <p>Loading analytics...</p>
      </section>
    );
  }

  if (error) {
    return (
      <section className={styles.statePanel} aria-live="polite">
        <h2>Unable to load analytics</h2>
        <p>{error}</p>
        <Button onClick={() => window.location.reload()} variant="secondary">
          Try again
        </Button>
      </section>
    );
  }

  if (!summary || isEmptySummary(summary)) {
    return <AnalyticsEmptyState />;
  }

  return (
    <div className={styles.dashboard}>
      <section className={styles.summaryGrid} aria-label="Analytics summary">
        <SummaryCard
          description="Roles currently tracked in your application pipeline."
          label="Total Applications"
          value={summary.totalApplications}
        />
        <SummaryCard
          description="Applications with a meaningful employer response."
          label="Response Rate"
          value={formatPercent(summary.responseRate)}
        />
        <SummaryCard
          description="Average score from saved job match analyses."
          label="Average Match Score"
          value={formatPercent(summary.averageMatchScore)}
        />
        <SummaryCard
          description="Parsed resumes available for job matching."
          label="Parsed Resumes"
          value={parsedResumeLabel}
        />
        <SummaryCard
          description="Generated interview preparation sessions."
          label="Interview Sessions"
          value={summary.totalInterviewSessions}
        />
        <SummaryCard
          description="Saved practice answers across interview sessions."
          label="Saved Interview Answers"
          value={summary.savedInterviewAnswers}
        />
      </section>

      <div className={styles.chartGrid}>
        <ApplicationsByStatusChart data={summary.applicationsByStatus} />
        <WeeklyActivityChart data={summary.weeklyApplicationActivity} />
        <RequirementsChart
          data={summary.topMissingRequirements}
          description="The most common gaps found across saved analyses."
          emptyMessage="No missing requirements yet."
          title="Top Missing Requirements"
        />
        <RequirementsChart
          data={summary.topMatchedRequirements}
          description="The strengths most often matched against job descriptions."
          emptyMessage="No matched requirements yet."
          title="Top Matched Requirements"
        />
      </div>
    </div>
  );
}
