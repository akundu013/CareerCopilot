import styles from "./EmptyState.module.scss";

interface EmptyStateProps {
  description: string;
  title: string;
}

export function EmptyState({ description, title }: EmptyStateProps) {
  return (
    <section className={styles.emptyState}>
      <span className={styles.icon} aria-hidden="true">
        0
      </span>
      <h2 className={styles.title}>{title}</h2>
      <p className={styles.description}>{description}</p>
    </section>
  );
}
