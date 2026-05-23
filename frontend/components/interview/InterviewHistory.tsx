"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { Button } from "@/components/ui/Button";
import { EmptyState } from "@/components/ui/EmptyState";
import { Spinner } from "@/components/ui/Spinner";
import {
  deleteInterviewSession,
  getInterviewSessions,
} from "@/services/interview-api";
import type { InterviewSession } from "@/types/interview";
import { InterviewHistoryCard } from "./InterviewHistoryCard";
import styles from "./InterviewHistory.module.scss";

function getCreatedTime(session: InterviewSession): number {
  const createdAt = new Date(session.createdAt).getTime();

  return Number.isNaN(createdAt) ? 0 : createdAt;
}

export function InterviewHistory() {
  const [sessions, setSessions] = useState<InterviewSession[]>([]);
  const [openSessionId, setOpenSessionId] = useState<string | null>(null);
  const [sessionToDelete, setSessionToDelete] =
    useState<InterviewSession | null>(null);
  const [deleteError, setDeleteError] = useState<string | null>(null);
  const [deleteSuccessMessage, setDeleteSuccessMessage] = useState<
    string | null
  >(null);
  const [deletingSessionId, setDeletingSessionId] = useState<string | null>(
    null,
  );
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const loadSessions = useCallback(async (showLoading = true) => {
    try {
      if (showLoading) {
        setIsLoading(true);
      }

      setError(null);
      setSessions(await getInterviewSessions());
    } catch (loadError) {
      setError(
        loadError instanceof Error
          ? loadError.message
          : "Unable to load interview history. Please try again.",
      );
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    const timerId = window.setTimeout(() => {
      void loadSessions();
    }, 0);

    return () => window.clearTimeout(timerId);
  }, [loadSessions]);

  const sortedSessions = useMemo(
    () =>
      [...sessions].sort(
        (firstSession, secondSession) =>
          getCreatedTime(secondSession) - getCreatedTime(firstSession),
      ),
    [sessions],
  );

  function handleToggleOpen(sessionId: string) {
    setOpenSessionId((currentSessionId) =>
      currentSessionId === sessionId ? null : sessionId,
    );
  }

  function handleRequestDelete(session: InterviewSession) {
    if (deletingSessionId) {
      return;
    }

    setDeleteError(null);
    setDeleteSuccessMessage(null);
    setSessionToDelete(session);
  }

  function handleCancelDelete() {
    if (deletingSessionId) {
      return;
    }

    setDeleteError(null);
    setSessionToDelete(null);
  }

  async function handleConfirmDelete() {
    if (!sessionToDelete) {
      return;
    }

    try {
      setDeleteError(null);
      setDeleteSuccessMessage(null);
      setDeletingSessionId(sessionToDelete.id);
      await deleteInterviewSession(sessionToDelete.id);
      setSessions((currentSessions) =>
        currentSessions.filter((session) => session.id !== sessionToDelete.id),
      );

      if (openSessionId === sessionToDelete.id) {
        setOpenSessionId(null);
      }

      setDeleteSuccessMessage("Interview session deleted.");
      setSessionToDelete(null);
      await loadSessions(false);
    } catch (deleteFailure) {
      setDeleteError(
        deleteFailure instanceof Error
          ? deleteFailure.message
          : "Unable to delete interview session. Please try again.",
      );
    } finally {
      setDeletingSessionId(null);
    }
  }

  if (isLoading) {
    return (
      <section className={styles.statePanel} aria-live="polite">
        <Spinner label="Loading interview history" />
        <p>Loading interview history...</p>
      </section>
    );
  }

  if (error) {
    return (
      <section className={styles.statePanel} aria-live="polite">
        <h2>Unable to load interview history</h2>
        <p>{error}</p>
        <Button onClick={() => void loadSessions()} variant="secondary">
          Try again
        </Button>
      </section>
    );
  }

  return (
    <>
      <section
        className={styles.historySection}
        aria-labelledby="interview-history-title"
      >
        <div className={styles.header}>
          <div>
            <span className={styles.eyebrow}>History</span>
            <h2 id="interview-history-title">Saved sessions</h2>
          </div>
          <Button href="/dashboard/interview">New session</Button>
        </div>

        {deleteSuccessMessage ? (
          <p className={styles.successMessage} role="status">
            {deleteSuccessMessage}
          </p>
        ) : null}

        {sortedSessions.length === 0 ? (
          <div className={styles.emptyWrap}>
            <EmptyState
              description="Generate an interview practice session to review saved questions and answers here."
              title="No interview sessions yet"
            />
          </div>
        ) : (
          <div className={styles.cardGrid}>
            {sortedSessions.map((session) => (
              <InterviewHistoryCard
                isDeleteDisabled={Boolean(
                  deletingSessionId && deletingSessionId !== session.id,
                )}
                isDeleting={deletingSessionId === session.id}
                isOpen={openSessionId === session.id}
                key={session.id}
                onDelete={() => handleRequestDelete(session)}
                onToggleOpen={() => handleToggleOpen(session.id)}
                session={session}
              />
            ))}
          </div>
        )}
      </section>

      {sessionToDelete ? (
        <div className={styles.dialogOverlay} role="presentation">
          <section
            aria-labelledby="delete-interview-title"
            aria-modal="true"
            className={styles.dialog}
            role="dialog"
          >
            <div className={styles.dialogContent}>
              <span className={styles.dialogEyebrow}>Delete session</span>
              <h2 id="delete-interview-title">
                Delete this interview session?
              </h2>
              <p>
                This will permanently remove the saved interview session for{" "}
                <strong>{sessionToDelete.resumeFileName}</strong>.
              </p>
            </div>

            {deleteError ? (
              <p className={styles.dialogError} role="alert">
                {deleteError}
              </p>
            ) : null}

            <div className={styles.dialogActions}>
              <Button
                disabled={deletingSessionId === sessionToDelete.id}
                onClick={handleCancelDelete}
                variant="secondary"
              >
                Cancel
              </Button>
              <button
                className={styles.dangerButton}
                disabled={deletingSessionId === sessionToDelete.id}
                onClick={() => void handleConfirmDelete()}
                type="button"
              >
                {deletingSessionId === sessionToDelete.id
                  ? "Deleting..."
                  : "Delete session"}
              </button>
            </div>
          </section>
        </div>
      ) : null}
    </>
  );
}
