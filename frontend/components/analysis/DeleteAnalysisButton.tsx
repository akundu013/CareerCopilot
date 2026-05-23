"use client";

import styles from "./DeleteAnalysisButton.module.scss";

interface DeleteAnalysisButtonProps {
  disabled?: boolean;
  isDeleting?: boolean;
  onClick: () => void;
}

export function DeleteAnalysisButton({
  disabled = false,
  isDeleting = false,
  onClick,
}: DeleteAnalysisButtonProps) {
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
