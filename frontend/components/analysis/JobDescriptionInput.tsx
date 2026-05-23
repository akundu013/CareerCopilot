"use client";

import type { ChangeEvent } from "react";
import styles from "./JobDescriptionInput.module.scss";

interface JobDescriptionInputProps {
  disabled?: boolean;
  onChange: (value: string) => void;
  value: string;
}

export function JobDescriptionInput({
  disabled = false,
  onChange,
  value,
}: JobDescriptionInputProps) {
  function handleChange(event: ChangeEvent<HTMLTextAreaElement>) {
    onChange(event.target.value);
  }

  return (
    <label className={styles.field} htmlFor="jobDescription">
      <span className={styles.label}>Job description</span>
      <textarea
        className={styles.textarea}
        disabled={disabled}
        id="jobDescription"
        onChange={handleChange}
        placeholder="Paste the full job description here, including responsibilities, qualifications, and requirements."
        required
        value={value}
      />
    </label>
  );
}
