import { Button } from "@/components/ui/Button";
import type { JobApplication } from "@/types/application";
import styles from "./ApplicationTable.module.scss";

interface DeleteApplicationDialogProps {
  application: JobApplication;
  error: string | null;
  isDeleting: boolean;
  onCancel: () => void;
  onConfirm: () => void;
}

export function DeleteApplicationDialog({
  application,
  error,
  isDeleting,
  onCancel,
  onConfirm,
}: DeleteApplicationDialogProps) {
  return (
    <div className={styles.dialogOverlay} role="presentation">
      <section
        aria-labelledby="delete-application-title"
        aria-modal="true"
        className={styles.dialog}
        role="dialog"
      >
        <div className={styles.dialogContent}>
          <span className={styles.dialogEyebrow}>Confirm deletion</span>
          <h2 id="delete-application-title">Delete this application?</h2>
          <p>
            This will remove the tracked application for{" "}
            <strong>{application.role}</strong> at{" "}
            <strong>{application.company}</strong>.
          </p>
          {error ? (
            <p className={styles.dialogError} role="alert">
              {error}
            </p>
          ) : null}
        </div>
        <div className={styles.dialogActions}>
          <Button disabled={isDeleting} onClick={onCancel} variant="secondary">
            Cancel
          </Button>
          <button
            className={styles.dangerButton}
            disabled={isDeleting}
            onClick={onConfirm}
            type="button"
          >
            {isDeleting ? "Deleting..." : "Delete application"}
          </button>
        </div>
      </section>
    </div>
  );
}
