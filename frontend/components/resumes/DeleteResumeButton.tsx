import { Button } from "@/components/ui/Button";
import styles from "./ResumeList.module.scss";

interface DeleteResumeButtonProps {
  disabled?: boolean;
  isDeleting?: boolean;
  onDelete: () => void;
}

export function DeleteResumeButton({
  disabled = false,
  isDeleting = false,
  onDelete,
}: DeleteResumeButtonProps) {
  return (
    <Button
      className={styles.deleteButton}
      disabled={disabled || isDeleting}
      onClick={onDelete}
      variant="secondary"
    >
      {isDeleting ? "Deleting..." : "Delete"}
    </Button>
  );
}
