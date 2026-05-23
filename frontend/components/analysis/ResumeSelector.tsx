"use client";

import type { ChangeEvent } from "react";
import type { ResumeDocument } from "@/types/resume";
import styles from "./ResumeSelector.module.scss";

interface ResumeSelectorProps {
  disabled?: boolean;
  onChange: (resumeId: string) => void;
  resumes: ResumeDocument[];
  value: string;
}

export function ResumeSelector({
  disabled = false,
  onChange,
  resumes,
  value,
}: ResumeSelectorProps) {
  function handleChange(event: ChangeEvent<HTMLSelectElement>) {
    onChange(event.target.value);
  }

  return (
    <label className={styles.field} htmlFor="resumeId">
      <span className={styles.label}>Parsed resume</span>
      <select
        className={styles.select}
        disabled={disabled}
        id="resumeId"
        onChange={handleChange}
        required
        value={value}
      >
        <option value="">Select a parsed resume</option>
        {resumes.map((resume) => (
          <option key={resume.id} value={resume.id}>
            {resume.fileName}
          </option>
        ))}
      </select>
    </label>
  );
}
