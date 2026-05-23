import { Button } from "@/components/ui/Button";
import type { ResumeDocument } from "@/types/resume";
import { ResumeStatusBadge } from "./ResumeStatusBadge";
import styles from "./ResumeList.module.scss";

interface ResumeCardProps {
  isParsing?: boolean;
  onParse: () => void;
  resume: ResumeDocument;
}

function formatDate(value: string): string {
  const date = new Date(value);

  if (Number.isNaN(date.getTime())) {
    return "Unknown";
  }

  return new Intl.DateTimeFormat("en", {
    day: "numeric",
    month: "short",
    year: "numeric",
  }).format(date);
}

function formatFileSize(sizeBytes: number): string {
  if (sizeBytes < 1024 * 1024) {
    return `${Math.max(1, Math.round(sizeBytes / 1024))} KB`;
  }

  return `${(sizeBytes / 1024 / 1024).toFixed(2)} MB`;
}

function getParseStatusText(resume: ResumeDocument): string {
  if (resume.status === "parsed") {
    return "Text extracted and ready for matching.";
  }

  if (resume.status === "parse_failed") {
    return "Parsing failed. You can try parsing again.";
  }

  return "Waiting for parsing.";
}

export function ResumeCard({
  isParsing = false,
  onParse,
  resume,
}: ResumeCardProps) {
  const isParsed = resume.status === "parsed";

  return (
    <article className={styles.card}>
      <div className={styles.cardHeader}>
        <div className={styles.fileSummary}>
          <h3>{resume.fileName}</h3>
          <p>{getParseStatusText(resume)}</p>
        </div>
        <ResumeStatusBadge status={resume.status} />
      </div>

      <dl className={styles.metaGrid}>
        <div>
          <dt>Uploaded</dt>
          <dd>{formatDate(resume.createdAt)}</dd>
        </div>
        <div>
          <dt>Updated</dt>
          <dd>{formatDate(resume.updatedAt)}</dd>
        </div>
        <div>
          <dt>Size</dt>
          <dd>{formatFileSize(resume.sizeBytes)}</dd>
        </div>
        <div>
          <dt>Type</dt>
          <dd>{resume.contentType || "Unknown"}</dd>
        </div>
      </dl>

      <div className={styles.cardActions}>
        <a
          className={styles.fileLink}
          href={resume.fileUrl}
          rel="noreferrer"
          target="_blank"
        >
          Open file
        </a>
        <Button
          className={styles.parseButton}
          disabled={isParsing}
          onClick={onParse}
          variant={isParsed ? "secondary" : "primary"}
        >
          {isParsing
            ? "Parsing..."
            : isParsed
              ? "Parse again"
              : "Parse resume"}
        </Button>
      </div>
    </article>
  );
}
