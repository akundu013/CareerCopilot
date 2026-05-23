"use client";

import { useEffect, useMemo, useState, type FormEvent } from "react";
import { Button } from "@/components/ui/Button";
import { createAnalysis } from "@/services/analysis-api";
import { getResumes } from "@/services/resume-api";
import type { Analysis } from "@/types/analysis";
import type { ResumeDocument } from "@/types/resume";
import { AnalysisResult } from "./AnalysisResult";
import { JobDescriptionInput } from "./JobDescriptionInput";
import { ResumeSelector } from "./ResumeSelector";
import styles from "./AnalysisForm.module.scss";

export function AnalysisForm() {
  const [resumes, setResumes] = useState<ResumeDocument[]>([]);
  const [selectedResumeId, setSelectedResumeId] = useState("");
  const [jobDescription, setJobDescription] = useState("");
  const [createdAnalysis, setCreatedAnalysis] = useState<Analysis | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoadingResumes, setIsLoadingResumes] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const parsedResumes = useMemo(
    () => resumes.filter((resume) => resume.status === "parsed"),
    [resumes],
  );

  useEffect(() => {
    let isMounted = true;

    async function loadResumes() {
      try {
        setIsLoadingResumes(true);
        const resumeList = await getResumes();

        if (!isMounted) {
          return;
        }

        setResumes(resumeList);
        setSelectedResumeId((currentResumeId) => {
          if (currentResumeId) {
            return currentResumeId;
          }

          return (
            resumeList.find((resume) => resume.status === "parsed")?.id ?? ""
          );
        });
      } catch (loadError) {
        if (!isMounted) {
          return;
        }

        setError(
          loadError instanceof Error
            ? loadError.message
            : "Unable to load resumes. Please try again.",
        );
      } finally {
        if (isMounted) {
          setIsLoadingResumes(false);
        }
      }
    }

    loadResumes();

    return () => {
      isMounted = false;
    };
  }, []);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    setCreatedAnalysis(null);

    const trimmedJobDescription = jobDescription.trim();

    if (!selectedResumeId) {
      setError("Select a parsed resume before generating an analysis.");
      return;
    }

    if (!trimmedJobDescription) {
      setError("Paste a job description before generating an analysis.");
      return;
    }

    try {
      setIsSubmitting(true);
      const analysis = await createAnalysis({
        resumeId: selectedResumeId,
        jobDescription: trimmedJobDescription,
      });
      setCreatedAnalysis(analysis);
    } catch (submitError) {
      setError(
        submitError instanceof Error
          ? submitError.message
          : "Unable to generate analysis. Please try again.",
      );
    } finally {
      setIsSubmitting(false);
    }
  }

  if (isLoadingResumes) {
    return (
      <section className={styles.statePanel} aria-live="polite">
        <h2>Loading resumes</h2>
        <p>Checking your resume library for parsed resumes.</p>
      </section>
    );
  }

  if (!parsedResumes.length) {
    return (
      <section className={styles.statePanel}>
        <h2>No parsed resumes yet</h2>
        <p>
          Upload and parse a resume before running a job match analysis.
        </p>
        <div className={styles.stateActions}>
          <Button href="/dashboard/resumes">Go to resumes</Button>
        </div>
      </section>
    );
  }

  return (
    <div className={styles.stack}>
      <form className={styles.form} onSubmit={handleSubmit}>
        <div className={styles.header}>
          <h2>Generate a match analysis</h2>
          <p>
            Select a parsed resume and paste a job description to create a
            saved analysis.
          </p>
        </div>

        <ResumeSelector
          disabled={isSubmitting}
          onChange={setSelectedResumeId}
          resumes={parsedResumes}
          value={selectedResumeId}
        />

        <JobDescriptionInput
          disabled={isSubmitting}
          onChange={setJobDescription}
          value={jobDescription}
        />

        {error ? (
          <p className={styles.error} role="alert">
            {error}
          </p>
        ) : null}

        <div className={styles.actions}>
          <Button href="/dashboard/analysis/history" variant="secondary">
            View history
          </Button>
          <Button disabled={isSubmitting} type="submit">
            {isSubmitting ? "Generating..." : "Generate analysis"}
          </Button>
        </div>
      </form>

      {createdAnalysis ? <AnalysisResult analysis={createdAnalysis} /> : null}
    </div>
  );
}
