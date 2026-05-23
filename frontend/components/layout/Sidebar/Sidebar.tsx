"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import styles from "./Sidebar.module.scss";

const navigationItems = [
  { label: "Dashboard", href: "/dashboard" },
  { label: "Applications", href: "/dashboard/applications" },
  { label: "Resumes", href: "/dashboard/resumes" },
  { label: "Analysis", href: "/dashboard/analysis" },
  { label: "Analysis History", href: "/dashboard/analysis/history" },
  { label: "Interview Prep", href: "/dashboard/interview" },
  { label: "Interview History", href: "/dashboard/interview/history" },
  { label: "Analytics", href: "/dashboard" },
  { label: "Settings", href: "/dashboard" },
];

function isActiveRoute(pathname: string, href: string): boolean {
  if (href === "/dashboard") {
    return pathname === href;
  }

  if (href === "/dashboard/analysis") {
    return pathname === href;
  }

  if (href === "/dashboard/interview") {
    return pathname === href;
  }

  return pathname === href || pathname.startsWith(`${href}/`);
}

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className={styles.sidebar} aria-label="Dashboard navigation">
      <span className={styles.label}>Workspace</span>
      <nav className={styles.nav}>
        {navigationItems.map((item) => {
          const isActive = isActiveRoute(pathname, item.href);

          return (
            <Link
              aria-current={isActive ? "page" : undefined}
              className={`${styles.link} ${isActive ? styles.active : ""}`}
              href={item.href}
              key={item.label}
            >
              {item.label}
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
