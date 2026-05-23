import type { InterviewQuestion } from "@/types/interview";
import { AnswerEditor } from "./AnswerEditor";
import styles from "./QuestionCard.module.scss";

interface QuestionCardProps {
  answer: string;
  disabled?: boolean;
  number: number;
  onAnswerChange: (questionId: string, answer: string) => void;
  question: InterviewQuestion;
}

export function QuestionCard({
  answer,
  disabled = false,
  number,
  onAnswerChange,
  question,
}: QuestionCardProps) {
  return (
    <article className={styles.card}>
      <div className={styles.promptRow}>
        <span className={styles.number}>{number}</span>
        <p>{question.prompt}</p>
      </div>

      <AnswerEditor
        disabled={disabled}
        onChange={(value) => onAnswerChange(question.id, value)}
        questionId={question.id}
        value={answer}
      />
    </article>
  );
}
