import type { ReactNode } from "react";
import { DemoModeBanner } from "@/components/demo/DemoModeBanner";
import { Header } from "@/components/layout/Header";
import { Sidebar } from "@/components/layout/Sidebar";
import styles from "./AppShell.module.scss";

interface AppShellProps {
  children: ReactNode;
}

export function AppShell({ children }: AppShellProps) {
  return (
    <div className={styles.shell}>
      <Header />
      <div className={styles.body}>
        <Sidebar />
        <main className={styles.content}>
          <DemoModeBanner />
          {children}
        </main>
      </div>
    </div>
  );
}
