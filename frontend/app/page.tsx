import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import styles from "./page.module.scss";

const features = [
  {
    description:
      "Organize roles, companies, statuses, and follow-up timing in one workspace.",
    title: "Application Tracking",
  },
  {
    description:
      "Compare resume content against job descriptions before applications go out.",
    title: "Resume Analysis",
  },
  {
    description:
      "Prepare focused practice prompts for behavioral and technical interviews.",
    title: "Interview Preparation",
  },
  {
    description:
      "Review search activity, response patterns, and progress over time.",
    title: "Analytics",
  },
];

const stackItems = ["Next.js", "React", "FastAPI", "Firebase"];

export default function Home() {
  return (
    <main className={styles.page}>
      <section className={styles.hero}>
        <div className={styles.heroContent}>
          <Badge tone="success">SaaS job search workspace</Badge>
          <h1>Career Copilot</h1>
          <p>
            Tracking applications,
            improving resumes, preparing for interviews, and understanding job
            search momentum.
          </p>
          <div className={styles.actions}>
            <Button href="/login">Sign in</Button>
            <Button href="/signup" variant="secondary">
              Create account
            </Button>
            <Button href="#features" variant="ghost">
              Explore features
            </Button>
          </div>
        </div>

        <aside className={styles.preview} aria-label="Product preview">
          <div className={styles.previewHeader}>
            <span />
            <span />
            <span />
          </div>
          <div className={styles.previewBody}>
            <div>
              <span>Application pipeline</span>
              <strong>24 roles</strong>
            </div>
            <div>
              <span>Resume match</span>
              <strong>82%</strong>
            </div>
            <div>
              <span>Interview prep</span>
              <strong>6 sessions</strong>
            </div>
          </div>
        </aside>
      </section>

      <section className={styles.section} id="features">
        <div className={styles.sectionHeader}>
          <span>Core workflow</span>
          <h2>Everything needed to manage a serious job search</h2>
        </div>
        <div className={styles.featureGrid}>
          {features.map((feature) => (
            <Card key={feature.title} title={feature.title}>
              <p>{feature.description}</p>
            </Card>
          ))}
        </div>
      </section>

      <section className={styles.stackSection}>
        <div className={styles.sectionHeader}>
          <span>Technology stack</span>
          <h2>Built with a modern full-stack architecture</h2>
        </div>
        <div className={styles.stackList}>
          {stackItems.map((item) => (
            <Badge key={item} tone="neutral">
              {item}
            </Badge>
          ))}
        </div>
      </section>
    </main>
  );
}
