import type { ChangeEvent } from "react";
import styles from "./AnswerEditor.module.scss";

interface AnswerEditorProps {
  disabled?: boolean;
  onChange: (value: string) => void;
  questionId: string;
  value: string;
}

export function AnswerEditor({
  disabled = false,
  onChange,
  questionId,
  value,
}: AnswerEditorProps) {
  function handleChange(event: ChangeEvent<HTMLTextAreaElement>) {
    onChange(event.target.value);
  }

  return (
    <label className={styles.field} htmlFor={`answer-${questionId}`}>
      <span className={styles.label}>Practice answer</span>
      <textarea
        className={styles.textarea}
        disabled={disabled}
        id={`answer-${questionId}`}
        onChange={handleChange}
        placeholder="Draft your answer here..."
        rows={5}
        value={value}
      />
    </label>
  );
}
