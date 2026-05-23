import type {
  InterviewAnswer,
  InterviewQuestion,
  InterviewSession,
} from "@/types/interview";
import { DeleteInterviewButton } from "./DeleteInterviewButton";
import styles from "./InterviewHistoryCard.module.scss";

interface InterviewHistoryCardProps {
  isDeleteDisabled?: boolean;
  isDeleting?: boolean;
  isOpen?: boolean;
  onDelete: () => void;
  onToggleOpen: () => void;
  session: InterviewSession;
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

function getAnsweredCount(answers: InterviewAnswer[]): number {
  return answers.filter((answer) => answer.answer.trim()).length;
}

function getAnswerForQuestion(
  question: InterviewQuestion,
  answers: InterviewAnswer[],
): string {
  return (
    answers.find((answer) => answer.questionId === question.id)?.answer.trim() ||
    "No answer saved yet."
  );
}

export function InterviewHistoryCard({
  isDeleteDisabled = false,
  isDeleting = false,
  isOpen = false,
  onDelete,
  onToggleOpen,
  session,
}: InterviewHistoryCardProps) {
  return (
    <article className={styles.card}>
      <div className={styles.header}>
        <div className={styles.summary}>
          <span className={styles.eyebrow}>
            {formatDate(session.createdAt)}
          </span>
          <h2>{session.resumeFileName}</h2>
        </div>
        <strong className={styles.count}>
          {session.questions.length} questions
        </strong>
      </div>

      <dl className={styles.metaGrid}>
        <div>
          <dt>Answered</dt>
          <dd>{getAnsweredCount(session.answers)}</dd>
        </div>
        <div>
          <dt>Updated</dt>
          <dd>{formatDate(session.updatedAt)}</dd>
        </div>
      </dl>

      {isOpen ? (
        <div className={styles.review}>
          {session.questions.map((question) => (
            <section className={styles.reviewItem} key={question.id}>
              <span>{question.category}</span>
              <h3>{question.prompt}</h3>
              <p>{getAnswerForQuestion(question, session.answers)}</p>
            </section>
          ))}
        </div>
      ) : null}

      <div className={styles.actions}>
        <button
          className={styles.openButton}
          onClick={onToggleOpen}
          type="button"
        >
          {isOpen ? "Close session" : "Open session"}
        </button>
        <DeleteInterviewButton
          disabled={isDeleteDisabled}
          isDeleting={isDeleting}
          onClick={onDelete}
        />
      </div>
    </article>
  );
}
