"use client";

import { useRouter } from "next/navigation";
import { useEffect, type ReactNode } from "react";
import { useAuth } from "@/hooks/useAuth";
import styles from "./ProtectedRoute.module.scss";

interface ProtectedRouteProps {
  children: ReactNode;
}

export function ProtectedRoute({ children }: ProtectedRouteProps) {
  const router = useRouter();
  const { loading, isAuthenticated } = useAuth();

  useEffect(() => {
    if (!loading && !isAuthenticated) {
      router.replace("/login");
    }
  }, [isAuthenticated, loading, router]);

  if (loading || !isAuthenticated) {
    return (
      <main className={styles.state}>
        <section className={styles.panel} aria-live="polite">
          <h1>Checking access</h1>
          <p>Please wait while Career Copilot verifies your session.</p>
        </section>
      </main>
    );
  }

  return children;
}
