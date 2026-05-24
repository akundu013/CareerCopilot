"use client";

import {
  BarChart3,
  BriefcaseBusiness,
  FileSearch,
  FileText,
  History,
  LayoutDashboard,
  MessageSquareText,
  PanelLeftClose,
  PanelLeftOpen,
} from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import styles from "./Sidebar.module.scss";

const navigationItems = [
  { icon: LayoutDashboard, label: "Dashboard", href: "/dashboard" },
  {
    icon: BriefcaseBusiness,
    label: "Applications",
    href: "/dashboard/applications",
  },
  { icon: FileText, label: "Resumes", href: "/dashboard/resumes" },
  { icon: FileSearch, label: "Analysis", href: "/dashboard/analysis" },
  {
    icon: History,
    label: "Analysis History",
    href: "/dashboard/analysis/history",
  },
  {
    icon: MessageSquareText,
    label: "Interview Prep",
    href: "/dashboard/interview",
  },
  {
    icon: History,
    label: "Interview History",
    href: "/dashboard/interview/history",
  },
  { icon: BarChart3, label: "Analytics", href: "/dashboard/analytics" },
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

  if (href === "/dashboard/analytics") {
    return pathname === href;
  }

  return pathname === href || pathname.startsWith(`${href}/`);
}

export function Sidebar() {
  const pathname = usePathname();
  const [isCollapsed, setIsCollapsed] = useState(false);

  useEffect(() => {
    document.documentElement.style.setProperty(
      "--sidebar-width",
      isCollapsed ? "88px" : "264px",
    );

    return () => {
      document.documentElement.style.setProperty("--sidebar-width", "264px");
    };
  }, [isCollapsed]);

  return (
    <aside
      className={`${styles.sidebar} ${isCollapsed ? styles.collapsed : ""}`}
      aria-label="Dashboard navigation"
    >
      <div className={styles.header}>
        {/* <span className={styles.label}>Workspace</span> */}
        <button
          aria-label={isCollapsed ? "Expand sidebar" : "Collapse sidebar"}
          className={styles.toggle}
          onClick={() => setIsCollapsed((currentValue) => !currentValue)}
          title={isCollapsed ? "Expand sidebar" : "Collapse sidebar"}
          type="button"
        >
          {isCollapsed ? (
            <PanelLeftOpen aria-hidden="true" size={18} />
          ) : (
            <PanelLeftClose aria-hidden="true" size={18} />
          )}
        </button>
      </div>
      <nav className={styles.nav}>
        {navigationItems.map((item) => {
          const isActive = isActiveRoute(pathname, item.href);
          const Icon = item.icon;

          return (
            <Link
              aria-label={isCollapsed ? item.label : undefined}
              aria-current={isActive ? "page" : undefined}
              className={`${styles.link} ${isActive ? styles.active : ""}`}
              href={item.href}
              key={item.label}
              title={isCollapsed ? item.label : undefined}
            >
              <Icon aria-hidden="true" className={styles.icon} size={20} />
              <span className={styles.linkText}>{item.label}</span>
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
