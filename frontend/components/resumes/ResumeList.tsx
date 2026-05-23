"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { ResumeCard } from "@/components/resumes/ResumeCard";
import { Button } from "@/components/ui/Button";
import { EmptyState } from "@/components/ui/EmptyState";
import { Spinner } from "@/components/ui/Spinner";
import {
  deleteResume,
  getResumes,
  parseResume,
} from "@/services/resume-api";
import type { ResumeDocument } from "@/types/resume";
import styles from "./ResumeList.module.scss";

interface ResumeListProps {
  refreshKey?: number;
}

function getCreatedTime(resume: ResumeDocument): number {
  const createdAt = new Date(resume.createdAt).getTime();

  return Number.isNaN(createdAt) ? 0 : createdAt;
}

export function ResumeList({ refreshKey = 0 }: ResumeListProps) {
  const [resumes, setResumes] = useState<ResumeDocument[]>([]);
  const [deleteError, setDeleteError] = useState<string | null>(null);
  const [deleteSuccessMessage, setDeleteSuccessMessage] = useState<
    string | null
  >(null);
  const [deletingResumeId, setDeletingResumeId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [parseError, setParseError] = useState<string | null>(null);
  const [parsingResumeId, setParsingResumeId] = useState<string | null>(null);
  const [resumeToDelete, setResumeToDelete] =
    useState<ResumeDocument | null>(null);

  const loadResumes = useCallback(async (showLoading = true) => {
    try {
      if (showLoading) {
        setIsLoading(true);
      }

      setError(null);
      setResumes(await getResumes());
    } catch (loadError) {
      setError(
        loadError instanceof Error
          ? loadError.message
          : "Unable to load resumes. Please try again.",
      );
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    const timerId = window.setTimeout(() => {
      void loadResumes(refreshKey === 0);
    }, 0);

    return () => window.clearTimeout(timerId);
  }, [loadResumes, refreshKey]);

  const sortedResumes = useMemo(
    () =>
      [...resumes].sort(
        (firstResume, secondResume) =>
          getCreatedTime(secondResume) - getCreatedTime(firstResume),
      ),
    [resumes],
  );

  async function handleParseResume(resume: ResumeDocument) {
    if (parsingResumeId || deletingResumeId) {
      return;
    }

    try {
      setDeleteSuccessMessage(null);
      setParseError(null);
      setParsingResumeId(resume.id);

      const parsedResume = await parseResume(resume.id);

      setResumes((currentResumes) =>
        currentResumes.map((currentResume) =>
          currentResume.id === parsedResume.id ? parsedResume : currentResume,
        ),
      );

      await loadResumes(false);
    } catch (parseFailure) {
      setParseError(
        parseFailure instanceof Error
          ? parseFailure.message
          : "Unable to parse resume. Please try again.",
      );
    } finally {
      setParsingResumeId(null);
    }
  }

  function handleRequestDelete(resume: ResumeDocument) {
    if (deletingResumeId || parsingResumeId) {
      return;
    }

    setDeleteError(null);
    setDeleteSuccessMessage(null);
    setResumeToDelete(resume);
  }

  function handleCancelDelete() {
    if (deletingResumeId) {
      return;
    }

    setDeleteError(null);
    setResumeToDelete(null);
  }

  async function handleConfirmDelete() {
    if (!resumeToDelete) {
      return;
    }

    try {
      setDeleteError(null);
      setDeleteSuccessMessage(null);
      setDeletingResumeId(resumeToDelete.id);
      await deleteResume(resumeToDelete.id);
      setResumes((currentResumes) =>
        currentResumes.filter((resume) => resume.id !== resumeToDelete.id),
      );
      setDeleteSuccessMessage("Resume deleted.");
      setResumeToDelete(null);
      await loadResumes(false);
    } catch (deleteFailure) {
      setDeleteError(
        deleteFailure instanceof Error
          ? deleteFailure.message
          : "Unable to delete resume. Please try again.",
      );
    } finally {
      setDeletingResumeId(null);
    }
  }

  if (isLoading) {
    return (
      <section className={styles.statePanel} aria-live="polite">
        <Spinner label="Loading resumes" />
        <p>Loading resumes...</p>
      </section>
    );
  }

  if (error) {
    return (
      <section className={styles.statePanel} aria-live="polite">
        <h2>Unable to load resumes</h2>
        <p>{error}</p>
        <Button onClick={() => void loadResumes()} variant="secondary">
          Try again
        </Button>
      </section>
    );
  }

  return (
    <>
      <section
        className={styles.listSection}
        aria-labelledby="resume-list-title"
      >
        <div className={styles.header}>
          <div>
            <span className={styles.eyebrow}>Library</span>
            <h2 id="resume-list-title">Uploaded resumes</h2>
          </div>
          <span className={styles.count}>
            {sortedResumes.length}{" "}
            {sortedResumes.length === 1 ? "resume" : "resumes"}
          </span>
        </div>

        {deleteSuccessMessage ? (
          <p className={styles.successMessage} role="status">
            {deleteSuccessMessage}
          </p>
        ) : null}

        {sortedResumes.length === 0 ? (
          <div className={styles.emptyWrap}>
            <EmptyState
              description="Upload your first resume to start building a reusable library for parsing and future job matching."
              title="No resumes yet"
            />
          </div>
        ) : (
          <>
            {parseError ? (
              <p className={styles.parseError} role="alert">
                {parseError}
              </p>
            ) : null}

            <div className={styles.cardGrid}>
              {sortedResumes.map((resume) => (
                <ResumeCard
                  isDeleteDisabled={
                    Boolean(deletingResumeId) ||
                    Boolean(parsingResumeId && parsingResumeId !== resume.id)
                  }
                  isDeleting={deletingResumeId === resume.id}
                  isParseDisabled={
                    Boolean(parsingResumeId) ||
                    Boolean(deletingResumeId && deletingResumeId !== resume.id)
                  }
                  isParsing={parsingResumeId === resume.id}
                  key={resume.id}
                  onDelete={() => handleRequestDelete(resume)}
                  onParse={() => void handleParseResume(resume)}
                  resume={resume}
                />
              ))}
            </div>
          </>
        )}
      </section>

      {resumeToDelete ? (
        <div className={styles.dialogOverlay} role="presentation">
          <section
            aria-labelledby="delete-resume-title"
            aria-modal="true"
            className={styles.dialog}
            role="dialog"
          >
            <div className={styles.dialogContent}>
              <span className={styles.dialogEyebrow}>Delete resume</span>
              <h2 id="delete-resume-title">Delete this resume?</h2>
              <p>
                This will permanently remove{" "}
                <strong>{resumeToDelete.fileName}</strong> from Career Copilot
                and Firebase Storage.
              </p>
            </div>

            {deleteError ? (
              <p className={styles.dialogError} role="alert">
                {deleteError}
              </p>
            ) : null}

            <div className={styles.dialogActions}>
              <Button
                disabled={deletingResumeId === resumeToDelete.id}
                onClick={handleCancelDelete}
                variant="secondary"
              >
                Cancel
              </Button>
              <button
                className={styles.dangerButton}
                disabled={deletingResumeId === resumeToDelete.id}
                onClick={() => void handleConfirmDelete()}
                type="button"
              >
                {deletingResumeId === resumeToDelete.id
                  ? "Deleting..."
                  : "Delete resume"}
              </button>
            </div>
          </section>
        </div>
      ) : null}
    </>
  );
}
