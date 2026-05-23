import { Button } from "@/components/ui/Button";
import type { Analysis } from "@/types/analysis";
import { ImprovementSuggestions } from "./ImprovementSuggestions";
import { MatchedRequirementsList } from "./MatchedRequirementsList";
import { MatchScoreCard } from "./MatchScoreCard";
import { MissingRequirementsList } from "./MissingRequirementsList";
import styles from "./AnalysisResult.module.scss";

interface AnalysisResultProps {
  analysis: Analysis;
}

export function AnalysisResult({ analysis }: AnalysisResultProps) {
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
    </section>
  );
}
