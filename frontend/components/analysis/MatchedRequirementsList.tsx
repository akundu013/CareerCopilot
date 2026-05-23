import styles from "./MatchedRequirementsList.module.scss";

interface MatchedRequirementsListProps {
  requirements: string[];
}

export function MatchedRequirementsList({
  requirements,
}: MatchedRequirementsListProps) {
  return (
    <section className={styles.listPanel}>
      <h3>Matched requirements</h3>
      {requirements.length ? (
        <ul className={styles.list}>
          {requirements.map((requirement) => (
            <li key={requirement}>{requirement}</li>
          ))}
        </ul>
      ) : (
        <p className={styles.empty}>No matched requirements found.</p>
      )}
    </section>
  );
}
