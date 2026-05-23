import styles from "./MissingRequirementsList.module.scss";

interface MissingRequirementsListProps {
  requirements: string[];
}

export function MissingRequirementsList({
  requirements,
}: MissingRequirementsListProps) {
  return (
    <section className={styles.listPanel}>
      <h3>Missing requirements</h3>
      {requirements.length ? (
        <ul className={styles.list}>
          {requirements.map((requirement) => (
            <li key={requirement}>{requirement}</li>
          ))}
        </ul>
      ) : (
        <p className={styles.empty}>No missing requirements found.</p>
      )}
    </section>
  );
}
