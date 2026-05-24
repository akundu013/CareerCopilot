"use client";

import { useEffect, useState } from "react";
import styles from "./ThemeToggle.module.scss";

type ThemeMode = "light" | "dark";

const STORAGE_KEY = "career-copilot-theme";

function getSystemTheme(): ThemeMode {
  if (typeof window === "undefined") {
    return "light";
  }

  return window.matchMedia("(prefers-color-scheme: dark)").matches
    ? "dark"
    : "light";
}

export function ThemeToggle() {
  const [theme, setTheme] = useState<ThemeMode>("light");
  const [isMounted, setIsMounted] = useState(false);
  const isDark = theme === "dark";

  useEffect(() => {
    const savedTheme = window.localStorage.getItem(STORAGE_KEY);
    const initialTheme: ThemeMode =
      savedTheme === "light" || savedTheme === "dark"
        ? savedTheme
        : getSystemTheme();

    document.documentElement.setAttribute("data-theme", initialTheme);
    setTheme(initialTheme);
    setIsMounted(true);
  }, []);

  function handleToggle() {
    const nextTheme: ThemeMode = theme === "dark" ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", nextTheme);
    window.localStorage.setItem(STORAGE_KEY, nextTheme);
    setTheme(nextTheme);
  }

  if (!isMounted) {
    return null;
  }

  return (
    <button
      aria-label={`Switch to ${isDark ? "light" : "dark"} mode`}
      aria-pressed={isDark}
      className={`${styles.toggle} ${isDark ? styles.dark : styles.light}`}
      onClick={handleToggle}
      type="button"
    >
      <span className={styles.icon} aria-hidden="true">
        <svg viewBox="0 0 24 24" focusable="false">
          <path d="M12 4a1 1 0 0 1 1 1v1a1 1 0 1 1-2 0V5a1 1 0 0 1 1-1Zm0 13a1 1 0 0 1 1 1v1a1 1 0 1 1-2 0v-1a1 1 0 0 1 1-1Zm8-6a1 1 0 0 1 0 2h-1a1 1 0 1 1 0-2h1ZM6 12a1 1 0 0 1-1 1H4a1 1 0 1 1 0-2h1a1 1 0 0 1 1 1Zm11.66-5.66a1 1 0 0 1 0 1.41l-.71.71a1 1 0 1 1-1.41-1.41l.71-.71a1 1 0 0 1 1.41 0ZM8.46 15.54a1 1 0 0 1 0 1.41l-.71.71a1 1 0 1 1-1.41-1.41l.71-.71a1 1 0 0 1 1.41 0Zm9.2 2.12a1 1 0 0 1-1.41 0l-.71-.71a1 1 0 0 1 1.41-1.41l.71.71a1 1 0 0 1 0 1.41ZM8.46 8.46a1 1 0 0 1-1.41 0l-.71-.71a1 1 0 1 1 1.41-1.41l.71.71a1 1 0 0 1 0 1.41ZM12 8a4 4 0 1 1 0 8a4 4 0 0 1 0-8Z" />
        </svg>
      </span>
      <span className={styles.icon} aria-hidden="true">
        <svg viewBox="0 0 24 24" focusable="false">
          <path d="M14.5 3.5a1 1 0 0 1 .82 1.57A7.5 7.5 0 1 0 18.93 15a1 1 0 0 1 1.48 1.3A9.5 9.5 0 1 1 13.2 3.28a1 1 0 0 1 1.3.22Z" />
        </svg>
      </span>
      <span className={styles.thumb} aria-hidden="true" />
    </button>
  );
}