"use client";

import { useEffect, useMemo, useState, type ChangeEvent } from "react";
import { Button } from "@/components/ui/Button";
import { EmptyState } from "@/components/ui/EmptyState";
import { Spinner } from "@/components/ui/Spinner";
import { getAnalyses } from "@/services/analysis-api";
import {
  createInterviewSession,
  saveInterviewAnswers,
} from "@/services/interview-api";
import type { AnalysisSummary } from "@/types/analysis";
import type {
  InterviewAnswer,
  InterviewQuestionCategory,
  InterviewSession,
} from "@/types/interview";
import { QuestionSection } from "./QuestionSection";
import styles from "./InterviewPage.module.scss";

const QUESTION_CATEGORY_ORDER: InterviewQuestionCategory[] = [
  "general",
  "behavioral",
  "technical",
];

function getCreatedTime(analysis: AnalysisSummary): number {
  const createdAt = new Date(analysis.createdAt).getTime();

  return Number.isNaN(createdAt) ? 0 : createdAt;
}

function getInitialAnswerMap(
  answers: InterviewAnswer[],
): Record<string, string> {
  return answers.reduce<Record<string, string>>((answerMap, answer) => {
    answerMap[answer.questionId] = answer.answer;

    return answerMap;
  }, {});
}

export function InterviewPage() {
  const [analyses, setAnalyses] = useState<AnalysisSummary[]>([]);
  const [selectedAnalysisId, setSelectedAnalysisId] = useState("");
  const [activeSession, setActiveSession] = useState<InterviewSession | null>(
    null,
  );
  const [answerMap, setAnswerMap] = useState<Record<string, string>>({});
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [isLoadingAnalyses, setIsLoadingAnalyses] = useState(true);
  const [isGenerating, setIsGenerating] = useState(false);
  const [isSaving, setIsSaving] = useState(false);

  const sortedAnalyses = useMemo(
    () =>
      [...analyses].sort(
        (firstAnalysis, secondAnalysis) =>
          getCreatedTime(secondAnalysis) - getCreatedTime(firstAnalysis),
      ),
    [analyses],
  );

  useEffect(() => {
    let isMounted = true;

    async function loadAnalyses() {
      try {
        setIsLoadingAnalyses(true);
        setError(null);
        const analysisList = await getAnalyses();

        if (!isMounted) {
          return;
        }

        setAnalyses(analysisList);
        setSelectedAnalysisId((currentAnalysisId) => {
          if (currentAnalysisId) {
            return currentAnalysisId;
          }

          return analysisList[0]?.id ?? "";
        });
      } catch (loadError) {
        if (!isMounted) {
          return;
        }

        setError(
          loadError instanceof Error
            ? loadError.message
            : "Unable to load analyses. Please try again.",
        );
      } finally {
        if (isMounted) {
          setIsLoadingAnalyses(false);
        }
      }
    }

    loadAnalyses();

    return () => {
      isMounted = false;
    };
  }, []);

  function handleAnalysisChange(event: ChangeEvent<HTMLSelectElement>) {
    setSelectedAnalysisId(event.target.value);
    setActiveSession(null);
    setAnswerMap({});
    setError(null);
    setSuccessMessage(null);
  }

  async function handleGenerateSession() {
    if (!selectedAnalysisId) {
      setError("Select a saved analysis before generating interview questions.");
      return;
    }

    try {
      setIsGenerating(true);
      setError(null);
      setSuccessMessage(null);
      const session = await createInterviewSession({
        analysisId: selectedAnalysisId,
      });
      setActiveSession(session);
      setAnswerMap(getInitialAnswerMap(session.answers));
      setSuccessMessage("Interview session generated.");
    } catch (generateError) {
      setError(
        generateError instanceof Error
          ? generateError.message
          : "Unable to generate interview questions. Please try again.",
      );
    } finally {
      setIsGenerating(false);
    }
  }

  function handleAnswerChange(questionId: string, answer: string) {
    setAnswerMap((currentAnswerMap) => ({
      ...currentAnswerMap,
      [questionId]: answer,
    }));
    setSuccessMessage(null);
  }

  async function handleSaveAnswers() {
    if (!activeSession) {
      return;
    }

    const answers = activeSession.questions.map((question) => ({
      questionId: question.id,
      answer: answerMap[question.id] ?? "",
    }));

    try {
      setIsSaving(true);
      setError(null);
      setSuccessMessage(null);
      const updatedSession = await saveInterviewAnswers(activeSession.id, {
        answers,
      });
      setActiveSession(updatedSession);
      setAnswerMap(getInitialAnswerMap(updatedSession.answers));
      setSuccessMessage("Answers saved.");
    } catch (saveError) {
      setError(
        saveError instanceof Error
          ? saveError.message
          : "Unable to save answers. Please try again.",
      );
    } finally {
      setIsSaving(false);
    }
  }

  if (isLoadingAnalyses) {
    return (
      <section className={styles.statePanel} aria-live="polite">
        <Spinner label="Loading analyses" />
        <p>Loading saved analyses...</p>
      </section>
    );
  }

  if (!sortedAnalyses.length) {
    return (
      <div className={styles.emptyWrap}>
        <EmptyState
          description="Create a job match analysis first, then generate interview practice questions from it."
          title="No analyses yet"
        />
        <Button href="/dashboard/analysis">Create analysis</Button>
      </div>
    );
  }

  return (
    <div className={styles.stack}>
      <section className={styles.panel} aria-labelledby="interview-form-title">
        <div className={styles.header}>
          <div>
            <span className={styles.eyebrow}>Practice setup</span>
            <h2 id="interview-form-title">Select an analysis</h2>
          </div>
          <div className={styles.headerActions}>
            <Button href="/dashboard/analysis/history" variant="secondary">
              Analysis history
            </Button>
            <Button href="/dashboard/interview/history" variant="secondary">
              Interview history
            </Button>
          </div>
        </div>

        <label className={styles.field} htmlFor="analysisId">
          <span className={styles.label}>Saved analysis</span>
          <select
            className={styles.select}
            disabled={isGenerating}
            id="analysisId"
            onChange={handleAnalysisChange}
            required
            value={selectedAnalysisId}
          >
            <option value="">Select an analysis</option>
            {sortedAnalyses.map((analysis) => (
              <option key={analysis.id} value={analysis.id}>
                {analysis.resumeFileName} - {analysis.matchScore}% match
              </option>
            ))}
          </select>
        </label>

        {error ? (
          <p className={styles.error} role="alert">
            {error}
          </p>
        ) : null}

        {successMessage ? (
          <p className={styles.success} role="status">
            {successMessage}
          </p>
        ) : null}

        <div className={styles.actions}>
          <Button
            disabled={isGenerating || !selectedAnalysisId}
            onClick={() => void handleGenerateSession()}
          >
            {isGenerating ? "Generating..." : "Generate session"}
          </Button>
        </div>
      </section>

      {activeSession ? (
        <section
          className={styles.practice}
          aria-labelledby="interview-questions-title"
        >
          <div className={styles.header}>
            <div>
              <span className={styles.eyebrow}>Practice session</span>
              <h2 id="interview-questions-title">
                {activeSession.resumeFileName}
              </h2>
            </div>
            <Button
              disabled={isSaving}
              onClick={() => void handleSaveAnswers()}
            >
              {isSaving ? "Saving..." : "Save answers"}
            </Button>
          </div>

          <div className={styles.sections}>
            {QUESTION_CATEGORY_ORDER.map((category) => (
              <QuestionSection
                answerMap={answerMap}
                category={category}
                disabled={isSaving}
                key={category}
                onAnswerChange={handleAnswerChange}
                questions={activeSession.questions.filter(
                  (question) => question.category === category,
                )}
              />
            ))}
          </div>
        </section>
      ) : null}
    </div>
  );
}
