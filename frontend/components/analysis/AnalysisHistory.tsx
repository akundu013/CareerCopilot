"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { Button } from "@/components/ui/Button";
import { EmptyState } from "@/components/ui/EmptyState";
import { Spinner } from "@/components/ui/Spinner";
import { deleteAnalysis, getAnalyses } from "@/services/analysis-api";
import type { AnalysisSummary } from "@/types/analysis";
import { AnalysisHistoryCard } from "./AnalysisHistoryCard";
import styles from "./AnalysisHistory.module.scss";

function getCreatedTime(analysis: AnalysisSummary): number {
  const createdAt = new Date(analysis.createdAt).getTime();

  return Number.isNaN(createdAt) ? 0 : createdAt;
}

export function AnalysisHistory() {
  const [analyses, setAnalyses] = useState<AnalysisSummary[]>([]);
  const [analysisToDelete, setAnalysisToDelete] =
    useState<AnalysisSummary | null>(null);
  const [deleteError, setDeleteError] = useState<string | null>(null);
  const [deleteSuccessMessage, setDeleteSuccessMessage] = useState<
    string | null
  >(null);
  const [deletingAnalysisId, setDeletingAnalysisId] = useState<string | null>(
    null,
  );
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const loadAnalyses = useCallback(async (showLoading = true) => {
    try {
      if (showLoading) {
        setIsLoading(true);
      }

      setError(null);
      setAnalyses(await getAnalyses());
    } catch (loadError) {
      setError(
        loadError instanceof Error
          ? loadError.message
          : "Unable to load analysis history. Please try again.",
      );
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    const timerId = window.setTimeout(() => {
      void loadAnalyses();
    }, 0);

    return () => window.clearTimeout(timerId);
  }, [loadAnalyses]);

  const sortedAnalyses = useMemo(
    () =>
      [...analyses].sort(
        (firstAnalysis, secondAnalysis) =>
          getCreatedTime(secondAnalysis) - getCreatedTime(firstAnalysis),
      ),
    [analyses],
  );

  function handleRequestDelete(analysis: AnalysisSummary) {
    if (deletingAnalysisId) {
      return;
    }

    setDeleteError(null);
    setDeleteSuccessMessage(null);
    setAnalysisToDelete(analysis);
  }

  function handleCancelDelete() {
    if (deletingAnalysisId) {
      return;
    }

    setDeleteError(null);
    setAnalysisToDelete(null);
  }

  async function handleConfirmDelete() {
    if (!analysisToDelete) {
      return;
    }

    try {
      setDeleteError(null);
      setDeleteSuccessMessage(null);
      setDeletingAnalysisId(analysisToDelete.id);
      await deleteAnalysis(analysisToDelete.id);
      setAnalyses((currentAnalyses) =>
        currentAnalyses.filter(
          (analysis) => analysis.id !== analysisToDelete.id,
        ),
      );
      setDeleteSuccessMessage("Analysis deleted.");
      setAnalysisToDelete(null);
      await loadAnalyses(false);
    } catch (deleteFailure) {
      setDeleteError(
        deleteFailure instanceof Error
          ? deleteFailure.message
          : "Unable to delete analysis. Please try again.",
      );
    } finally {
      setDeletingAnalysisId(null);
    }
  }

  if (isLoading) {
    return (
      <section className={styles.statePanel} aria-live="polite">
        <Spinner label="Loading analysis history" />
        <p>Loading analysis history...</p>
      </section>
    );
  }

  if (error) {
    return (
      <section className={styles.statePanel} aria-live="polite">
        <h2>Unable to load analysis history</h2>
        <p>{error}</p>
        <Button onClick={() => void loadAnalyses()} variant="secondary">
          Try again
        </Button>
      </section>
    );
  }

  return (
    <>
      <section
        className={styles.historySection}
        aria-labelledby="analysis-history-title"
      >
        <div className={styles.header}>
          <div>
            <span className={styles.eyebrow}>History</span>
            <h2 id="analysis-history-title">Saved analyses</h2>
          </div>
          <Button href="/dashboard/analysis">New analysis</Button>
        </div>

        {deleteSuccessMessage ? (
          <p className={styles.successMessage} role="status">
            {deleteSuccessMessage}
          </p>
        ) : null}

        {sortedAnalyses.length === 0 ? (
          <div className={styles.emptyWrap}>
            <EmptyState
              description="Generate your first job match analysis to start building a comparison history."
              title="No analyses yet"
            />
          </div>
        ) : (
          <div className={styles.cardGrid}>
            {sortedAnalyses.map((analysis) => (
              <AnalysisHistoryCard
                analysis={analysis}
                isDeleteDisabled={Boolean(
                  deletingAnalysisId && deletingAnalysisId !== analysis.id,
                )}
                isDeleting={deletingAnalysisId === analysis.id}
                key={analysis.id}
                onDelete={() => handleRequestDelete(analysis)}
              />
            ))}
          </div>
        )}
      </section>

      {analysisToDelete ? (
        <div className={styles.dialogOverlay} role="presentation">
          <section
            aria-labelledby="delete-analysis-title"
            aria-modal="true"
            className={styles.dialog}
            role="dialog"
          >
            <div className={styles.dialogContent}>
              <span className={styles.dialogEyebrow}>Delete analysis</span>
              <h2 id="delete-analysis-title">Delete this analysis?</h2>
              <p>
                This will permanently remove the saved analysis for{" "}
                <strong>{analysisToDelete.resumeFileName}</strong>.
              </p>
            </div>

            {deleteError ? (
              <p className={styles.dialogError} role="alert">
                {deleteError}
              </p>
            ) : null}

            <div className={styles.dialogActions}>
              <Button
                disabled={deletingAnalysisId === analysisToDelete.id}
                onClick={handleCancelDelete}
                variant="secondary"
              >
                Cancel
              </Button>
              <button
                className={styles.dangerButton}
                disabled={deletingAnalysisId === analysisToDelete.id}
                onClick={() => void handleConfirmDelete()}
                type="button"
              >
                {deletingAnalysisId === analysisToDelete.id
                  ? "Deleting..."
                  : "Delete analysis"}
              </button>
            </div>
          </section>
        </div>
      ) : null}
    </>
  );
}
