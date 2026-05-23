import type { AnalysisSummary } from "@/types/analysis";
import { DeleteAnalysisButton } from "./DeleteAnalysisButton";
import styles from "./AnalysisHistoryCard.module.scss";

interface AnalysisHistoryCardProps {
  analysis: AnalysisSummary;
  isDeleteDisabled?: boolean;
  isDeleting?: boolean;
  onDelete: () => void;
}

function formatDate(value: string): string {
  const date = new Date(value);

  if (Number.isNaN(date.getTime())) {
    return "Date unavailable";
  }

  return date.toLocaleDateString(undefined, {
    day: "numeric",
    month: "short",
    year: "numeric",
  });
}

export function AnalysisHistoryCard({
  analysis,
  isDeleteDisabled = false,
  isDeleting = false,
  onDelete,
}: AnalysisHistoryCardProps) {
  return (
    <article className={styles.card}>
      <div className={styles.header}>
        <div className={styles.summary}>
          <span className={styles.eyebrow}>
            {formatDate(analysis.createdAt)}
          </span>
          <h2>{analysis.resumeFileName}</h2>
        </div>
        <strong className={styles.score}>{Math.round(analysis.matchScore)}%</strong>
      </div>

      <dl className={styles.metaGrid}>
        <div>
          <dt>Matched</dt>
          <dd>{analysis.matchedRequirements.length}</dd>
        </div>
        <div>
          <dt>Missing</dt>
          <dd>{analysis.missingRequirements.length}</dd>
        </div>
      </dl>

      <div className={styles.previewGrid}>
        <section>
          <h3>Matched requirements</h3>
          {analysis.matchedRequirements.length ? (
            <p>{analysis.matchedRequirements.slice(0, 3).join(", ")}</p>
          ) : (
            <p>No matched requirements.</p>
          )}
        </section>
        <section>
          <h3>Missing requirements</h3>
          {analysis.missingRequirements.length ? (
            <p>{analysis.missingRequirements.slice(0, 3).join(", ")}</p>
          ) : (
            <p>No missing requirements.</p>
          )}
        </section>
      </div>

      <div className={styles.actions}>
        <DeleteAnalysisButton
          disabled={isDeleteDisabled}
          isDeleting={isDeleting}
          onClick={onDelete}
        />
      </div>
    </article>
  );
}
