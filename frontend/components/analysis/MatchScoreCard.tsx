import type { MatchScore } from "@/types/analysis";
import styles from "./MatchScoreCard.module.scss";

interface MatchScoreCardProps {
  score: MatchScore;
}

export function MatchScoreCard({ score }: MatchScoreCardProps) {
  const roundedScore = Math.round(score);

  return (
    <section className={styles.scoreCard} aria-label="Match score">
      <span className={styles.label}>Match score</span>
      <strong className={styles.score}>{roundedScore}%</strong>
    </section>
  );
}
