import styles from "./SummaryCard.module.scss";

interface SummaryCardProps {
  description: string;
  label: string;
  value: number | string;
}

export function SummaryCard({ description, label, value }: SummaryCardProps) {
  return (
    <article className={styles.card}>
      <span className={styles.label}>{label}</span>
      <strong className={styles.value}>{value}</strong>
      <p>{description}</p>
    </article>
  );
}
