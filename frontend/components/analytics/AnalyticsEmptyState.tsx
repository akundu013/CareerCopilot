import { Button } from "@/components/ui/Button";
import styles from "./AnalyticsEmptyState.module.scss";

export function AnalyticsEmptyState() {
  return (
    <section className={styles.emptyState}>
      <div className={styles.content}>
        <span className={styles.eyebrow}>No analytics yet</span>
        <h2>Build your job-search signal</h2>
        <p>
          Add applications, parse resumes, create match analyses, and save
          interview answers to unlock dashboard insights.
        </p>
      </div>

      <div className={styles.actions}>
        <Button href="/dashboard/applications/new">Add application</Button>
        <Button href="/dashboard/resumes" variant="secondary">
          Manage resumes
        </Button>
        <Button href="/dashboard/analysis" variant="secondary">
          Create analysis
        </Button>
      </div>
    </section>
  );
}
