"use client";

import styles from "./DeleteInterviewButton.module.scss";

interface DeleteInterviewButtonProps {
  disabled?: boolean;
  isDeleting?: boolean;
  onClick: () => void;
}

export function DeleteInterviewButton({
  disabled = false,
  isDeleting = false,
  onClick,
}: DeleteInterviewButtonProps) {
  return (
    <button
      className={styles.button}
      disabled={disabled || isDeleting}
      onClick={onClick}
      type="button"
    >
      {isDeleting ? "Deleting..." : "Delete"}
    </button>
  );
}
