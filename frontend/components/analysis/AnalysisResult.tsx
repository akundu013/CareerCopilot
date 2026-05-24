"use client";

import { useState } from "react";
import { Button } from "@/components/ui/Button";
import { generateAIFeedback } from "@/services/analysis-api";
import type { AIFeedback, Analysis } from "@/types/analysis";
import { ImprovementSuggestions } from "./ImprovementSuggestions";
import { MatchedRequirementsList } from "./MatchedRequirementsList";
import { MatchScoreCard } from "./MatchScoreCard";
import { MissingRequirementsList } from "./MissingRequirementsList";
import styles from "./AnalysisResult.module.scss";

interface AnalysisResultProps {
  analysis: Analysis;
}

export function AnalysisResult({ analysis }: AnalysisResultProps) {
  const [aiFeedback, setAiFeedback] = useState<AIFeedback | null>(
    analysis.aiFeedback ?? null,
  );
  const [aiFeedbackError, setAiFeedbackError] = useState<string | null>(null);
  const [isGeneratingFeedback, setIsGeneratingFeedback] = useState(false);

  async function handleGenerateAIFeedback() {
    try {
      setIsGeneratingFeedback(true);
      setAiFeedbackError(null);
      setAiFeedback(await generateAIFeedback(analysis.id));
    } catch (feedbackError) {
      setAiFeedbackError(
        feedbackError instanceof Error
          ? feedbackError.message
          : "Unable to generate AI feedback. Please try again.",
      );
    } finally {
      setIsGeneratingFeedback(false);
    }
  }

  return (
    <section className={styles.result} aria-labelledby="analysis-result-title">
      <div className={styles.header}>
        <div>
          <span className={styles.eyebrow}>Generated analysis</span>
          <h2 id="analysis-result-title">{analysis.resumeFileName}</h2>
        </div>
        <Button href="/dashboard/analysis/history" variant="secondary">
          View history
        </Button>
      </div>

      <div className={styles.summaryGrid}>
        <MatchScoreCard score={analysis.matchScore} />
        <section className={styles.requirementSummary}>
          <span>{analysis.extractedRequirements.length}</span>
          <p>requirements detected from the job description</p>
        </section>
      </div>

      <div className={styles.listGrid}>
        <MatchedRequirementsList
          requirements={analysis.matchedRequirements}
        />
        <MissingRequirementsList
          requirements={analysis.missingRequirements}
        />
      </div>

      <ImprovementSuggestions
        suggestions={analysis.improvementSuggestions}
      />

      <section className={styles.aiFeedbackPanel}>
        <div className={styles.aiFeedbackHeader}>
          <div>
            <span className={styles.eyebrow}>Optional AI feedback</span>
            <h3>Short match feedback</h3>
          </div>
          <Button
            disabled={isGeneratingFeedback}
            onClick={() => void handleGenerateAIFeedback()}
            variant="secondary"
          >
            {isGeneratingFeedback ? "Generating..." : "Generate AI Feedback"}
          </Button>
        </div>

        {aiFeedbackError ? (
          <p className={styles.aiError} role="alert">
            {aiFeedbackError}
          </p>
        ) : null}

        {aiFeedback ? (
          <div className={styles.aiFeedbackContent}>
            <p>{aiFeedback.summary}</p>
            {aiFeedback.tips.length ? (
              <ul>
                {aiFeedback.tips.map((tip) => (
                  <li key={tip}>{tip}</li>
                ))}
              </ul>
            ) : null}
          </div>
        ) : (
          <p className={styles.aiHelpText}>
            Generate a concise AI summary from the saved match score and
            requirement lists. Full resume text is not sent.
          </p>
        )}
      </section>
    </section>
  );
}
