"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { useAuth } from "@/hooks/useAuth";
import styles from "./Header.module.scss";

export function Header() {
  const router = useRouter();
  const { logout } = useAuth();
  const [isLoggingOut, setIsLoggingOut] = useState(false);

  async function handleLogout() {
    setIsLoggingOut(true);

    try {
      await logout();
      router.replace("/login");
    } finally {
      setIsLoggingOut(false);
    }
  }

  return (
    <header className={styles.header}>
      <Link className={styles.brand} href="/">
        <span className={styles.brandMark}>CC</span>
        <span>Career Copilot</span>
      </Link>

      <nav className={styles.nav} aria-label="Primary navigation">
        <Link href="/">Home</Link>
        <Link href="/dashboard">Dashboard</Link>
        <button
          className={styles.logoutButton}
          disabled={isLoggingOut}
          onClick={handleLogout}
          type="button"
        >
          {isLoggingOut ? "Signing out..." : "Logout"}
        </button>
      </nav>
    </header>
  );
}
