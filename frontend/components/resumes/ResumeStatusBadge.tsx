import type { ResumeStatus } from "@/types/resume";
import styles from "./ResumeList.module.scss";

const STATUS_LABELS: Record<ResumeStatus, string> = {
  uploaded: "Uploaded",
  parsed: "Parsed",
  parse_failed: "Parse failed",
};

const STATUS_CLASS_NAMES: Record<ResumeStatus, string> = {
  uploaded: styles.uploaded,
  parsed: styles.parsed,
  parse_failed: styles.parseFailed,
};

interface ResumeStatusBadgeProps {
  status: ResumeStatus;
}

export function ResumeStatusBadge({ status }: ResumeStatusBadgeProps) {
  return (
    <span className={`${styles.statusBadge} ${STATUS_CLASS_NAMES[status]}`}>
      {STATUS_LABELS[status]}
    </span>
  );
}
