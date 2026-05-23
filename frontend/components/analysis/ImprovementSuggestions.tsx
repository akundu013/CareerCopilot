import styles from "./ImprovementSuggestions.module.scss";

interface ImprovementSuggestionsProps {
  suggestions: string[];
}

export function ImprovementSuggestions({
  suggestions,
}: ImprovementSuggestionsProps) {
  return (
    <section className={styles.suggestions}>
      <h3>Improvement suggestions</h3>
      {suggestions.length ? (
        <ul className={styles.list}>
          {suggestions.map((suggestion) => (
            <li key={suggestion}>{suggestion}</li>
          ))}
        </ul>
      ) : (
        <p className={styles.empty}>No improvement suggestions returned.</p>
      )}
    </section>
  );
}
