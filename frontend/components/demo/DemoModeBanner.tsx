"use client";

import { useAuth } from "@/hooks/useAuth";
import styles from "./DemoModeBanner.module.scss";

const FALLBACK_DEMO_EMAIL = "demo@careercopilot.dev";

function getConfiguredDemoEmail(): string {
  return (
    process.env.NEXT_PUBLIC_DEMO_EMAIL?.trim().toLowerCase() ||
    FALLBACK_DEMO_EMAIL
  );
}

export function DemoModeBanner() {
  const { user } = useAuth();
  const userEmail = user?.email?.trim().toLowerCase();

  if (!userEmail || userEmail !== getConfiguredDemoEmail()) {
    return null;
  }

  return (
    <aside className={styles.banner} aria-label="Demo mode notice">
      <span className={styles.label}>Demo Mode</span>
      <p>
        You are exploring sample data. Seeded demo records are protected, but
        you can try limited uploads, analyses, and interview prep.
      </p>
    </aside>
  );
}
