import type { ReactNode } from "react";
import styles from "./Badge.module.scss";

type BadgeTone = "neutral" | "success" | "accent";

interface BadgeProps {
  children: ReactNode;
  tone?: BadgeTone;
}

export function Badge({ children, tone = "neutral" }: BadgeProps) {
  return <span className={`${styles.badge} ${styles[tone]}`}>{children}</span>;
}
