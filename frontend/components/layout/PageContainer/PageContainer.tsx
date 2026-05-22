import type { ReactNode } from "react";
import styles from "./PageContainer.module.scss";

interface PageContainerProps {
  children: ReactNode;
  description?: string;
  eyebrow?: string;
  title: string;
}

export function PageContainer({
  children,
  description,
  eyebrow,
  title,
}: PageContainerProps) {
  return (
    <section className={styles.container}>
      <header className={styles.header}>
        {eyebrow ? <span className={styles.eyebrow}>{eyebrow}</span> : null}
        <h1 className={styles.title}>{title}</h1>
        {description ? (
          <p className={styles.description}>{description}</p>
        ) : null}
      </header>
      {children}
    </section>
  );
}
