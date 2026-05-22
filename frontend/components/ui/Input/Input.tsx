"use client";

import type { InputHTMLAttributes } from "react";
import styles from "./Input.module.scss";

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  helperText?: string;
  id: string;
  label: string;
}

export function Input({ helperText, id, label, ...props }: InputProps) {
  return (
    <div className={styles.field}>
      <label className={styles.label} htmlFor={id}>
        {label}
      </label>
      <input className={styles.input} id={id} {...props} />
      {helperText ? <p className={styles.helper}>{helperText}</p> : null}
    </div>
  );
}
