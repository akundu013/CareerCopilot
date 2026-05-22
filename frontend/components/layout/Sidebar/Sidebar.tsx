import Link from "next/link";
import styles from "./Sidebar.module.scss";

const navigationItems = [
  { label: "Dashboard", href: "/dashboard", active: true },
  { label: "Applications", href: "/dashboard" },
  { label: "Resumes", href: "/dashboard" },
  { label: "Interview Prep", href: "/dashboard" },
  { label: "Analytics", href: "/dashboard" },
  { label: "Settings", href: "/dashboard" },
];

export function Sidebar() {
  return (
    <aside className={styles.sidebar} aria-label="Dashboard navigation">
      <span className={styles.label}>Workspace</span>
      <nav className={styles.nav}>
        {navigationItems.map((item) => (
          <Link
            aria-current={item.active ? "page" : undefined}
            className={`${styles.link} ${item.active ? styles.active : ""}`}
            href={item.href}
            key={item.label}
          >
            {item.label}
          </Link>
        ))}
      </nav>
    </aside>
  );
}
