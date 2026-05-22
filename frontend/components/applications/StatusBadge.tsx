import type { ApplicationStatus } from "@/types/application";
import styles from "./ApplicationTable.module.scss";

const STATUS_LABELS: Record<ApplicationStatus, string> = {
  applied: "Applied",
  interviewing: "Interviewing",
  offer: "Offer",
  rejected: "Rejected",
  withdrawn: "Withdrawn",
};

interface StatusBadgeProps {
  status: ApplicationStatus;
}

export function StatusBadge({ status }: StatusBadgeProps) {
  return (
    <span className={`${styles.statusBadge} ${styles[status]}`}>
      {STATUS_LABELS[status]}
    </span>
  );
}
