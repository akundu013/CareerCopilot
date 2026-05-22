import Link from "next/link";
import styles from "./Header.module.scss";

export function Header() {
  return (
    <header className={styles.header}>
      <Link className={styles.brand} href="/">
        <span className={styles.brandMark}>AI</span>
        <span>Career Copilot</span>
      </Link>

      <nav className={styles.nav} aria-label="Primary navigation">
        <Link href="/">Home</Link>
        <Link href="/dashboard">Dashboard</Link>
      </nav>
    </header>
  );
}
