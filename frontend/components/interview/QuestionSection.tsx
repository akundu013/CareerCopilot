import type {
  InterviewQuestion,
  InterviewQuestionCategory,
} from "@/types/interview";
import { QuestionCard } from "./QuestionCard";
import styles from "./QuestionSection.module.scss";

interface QuestionSectionProps {
  answerMap: Record<string, string>;
  category: InterviewQuestionCategory;
  disabled?: boolean;
  onAnswerChange: (questionId: string, answer: string) => void;
  questions: InterviewQuestion[];
}

const CATEGORY_LABELS: Record<InterviewQuestionCategory, string> = {
  general: "General questions",
  behavioral: "Behavioral questions",
  technical: "Technical questions",
};

export function QuestionSection({
  answerMap,
  category,
  disabled = false,
  onAnswerChange,
  questions,
}: QuestionSectionProps) {
  return (
    <section className={styles.section} aria-labelledby={`${category}-title`}>
      <div className={styles.header}>
        <span className={styles.count}>{questions.length}</span>
        <h3 id={`${category}-title`}>{CATEGORY_LABELS[category]}</h3>
      </div>

      <div className={styles.cards}>
        {questions.map((question, index) => (
          <QuestionCard
            answer={answerMap[question.id] ?? ""}
            disabled={disabled}
            key={question.id}
            number={index + 1}
            onAnswerChange={onAnswerChange}
            question={question}
          />
        ))}
      </div>
    </section>
  );
}
