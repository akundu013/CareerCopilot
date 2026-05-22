"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState, type FormEvent } from "react";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { useAuth } from "@/hooks/useAuth";
import styles from "./page.module.scss";

export default function LoginPage() {
  const router = useRouter();
  const { isAuthenticated, loading, login } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    if (!loading && isAuthenticated) {
      router.replace("/dashboard");
    }
  }, [isAuthenticated, loading, router]);

  if (loading || isAuthenticated) {
    return (
      <main className={styles.statePage}>
        <section className={styles.stateCard} aria-live="polite">
          <h1>Checking session</h1>
          <p>Please wait while Career Copilot prepares your workspace.</p>
        </section>
      </main>
    );
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setIsSubmitting(true);

    try {
      await login(email, password);
      router.push("/dashboard");
    } catch (loginError) {
      setError(
        loginError instanceof Error
          ? loginError.message
          : "Unable to log in. Please try again.",
      );
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <main className={styles.page}>
      <section className={styles.brandPanel} aria-labelledby="login-heading">
        <Link className={styles.brand} href="/">
          <span className={styles.brandMark}>CC</span>
          <span>Career Copilot</span>
        </Link>

        <div className={styles.brandCopy}>
          <span className={styles.eyebrow}>Recruiter-ready job search</span>
          <h1 id="login-heading">Welcome back to your search command center.</h1>
          <p>
            Track opportunities, sharpen your resume, and prepare for interviews
            in one focused workspace.
          </p>
        </div>

        <div className={styles.valueList} aria-label="Product benefits">
          <span>Application pipeline clarity</span>
          <span>Resume-to-role preparation</span>
          <span>Interview momentum tracking</span>
        </div>
      </section>

      <section className={styles.formPanel} aria-label="Login form">
        <div className={styles.card}>
          <div className={styles.cardHeader}>
            <span>Sign in</span>
            <h2>Access Career Copilot</h2>
            <p>Use your email and password to continue to the dashboard.</p>
          </div>

          <form className={styles.form} onSubmit={handleSubmit}>
            <Input
              autoComplete="email"
              disabled={isSubmitting}
              id="email"
              label="Email"
              onChange={(event) => setEmail(event.target.value)}
              placeholder="you@example.com"
              required
              type="email"
              value={email}
            />

            <Input
              autoComplete="current-password"
              disabled={isSubmitting}
              id="password"
              label="Password"
              onChange={(event) => setPassword(event.target.value)}
              placeholder="Enter your password"
              required
              type="password"
              value={password}
            />

            {error ? (
              <p className={styles.error} role="alert">
                {error}
              </p>
            ) : null}

            <Button disabled={isSubmitting} type="submit">
              {isSubmitting ? "Signing in..." : "Sign in"}
            </Button>
          </form>

          <p className={styles.footerText}>
            New to Career Copilot? <Link href="/signup">Create an account</Link>
          </p>
        </div>
      </section>
    </main>
  );
}
