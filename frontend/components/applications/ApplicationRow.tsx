import Link from "next/link";
import type { JobApplication } from "@/types/application";
import { StatusBadge } from "./StatusBadge";
import styles from "./ApplicationTable.module.scss";

interface ApplicationRowProps {
  application: JobApplication;
  isDeleting: boolean;
  onRequestDelete: (application: JobApplication) => void;
}

function formatDate(value?: string): string {
  if (!value) {
    return "Not set";
  }

  const date = new Date(value);

  if (Number.isNaN(date.getTime())) {
    return value;
  }

  return new Intl.DateTimeFormat("en", {
    day: "numeric",
    month: "short",
    year: "numeric",
  }).format(date);
}

function isSeededDemoApplication(application: JobApplication): boolean {
  return Boolean(
    application.isSeededDemoData || application.createdByDemoSeed,
  );
}

export function ApplicationRow({
  application,
  isDeleting,
  onRequestDelete,
}: ApplicationRowProps) {
  const isProtectedDemoRecord = isSeededDemoApplication(application);

  return (
    <tr className={styles.row}>
      <td data-label="Company">
        <div className={styles.primaryCell}>
          <strong>{application.company}</strong>
          {application.jobUrl ? (
            <a
              href={application.jobUrl}
              rel="noreferrer"
              target="_blank"
            >
              Job post
            </a>
          ) : null}
        </div>
      </td>
      <td data-label="Role">{application.role}</td>
      <td data-label="Status">
        <StatusBadge status={application.status} />
      </td>
      <td data-label="Location">{application.location || "Not set"}</td>
      <td data-label="Applied">{formatDate(application.dateApplied)}</td>
      <td data-label="Updated">{formatDate(application.updatedAt)}</td>
      <td data-label="Actions">
        <div className={styles.actionGroup}>
          {isProtectedDemoRecord ? (
            <span className={styles.protectedLabel}>Protected demo data</span>
          ) : (
            <>
              <Link
                className={styles.actionLink}
                href={`/dashboard/applications/${encodeURIComponent(
                  application.id,
                )}/edit`}
              >
                Edit
              </Link>
              <button
                className={styles.deleteButton}
                disabled={isDeleting}
                onClick={() => onRequestDelete(application)}
                type="button"
              >
                Delete
              </button>
            </>
          )}
        </div>
      </td>
    </tr>
  );
}
