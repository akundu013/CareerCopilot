"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState, type FormEvent } from "react";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { useAuth } from "@/hooks/useAuth";
import styles from "./page.module.scss";

export default function SignupPage() {
  const router = useRouter();
  const { signup } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  function validateForm() {
    if (!email.trim()) {
      return "Email is required.";
    }

    if (!password) {
      return "Password is required.";
    }

    if (password.length < 6) {
      return "Password must be at least 6 characters.";
    }

    if (password !== confirmPassword) {
      return "Passwords must match.";
    }

    return "";
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");

    const validationError = validateForm();

    if (validationError) {
      setError(validationError);
      return;
    }

    setIsSubmitting(true);

    try {
      await signup(email, password);
      router.push("/dashboard");
    } catch (signupError) {
      setError(
        signupError instanceof Error
          ? signupError.message
          : "Unable to create your account. Please try again.",
      );
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <main className={styles.page}>
      <section className={styles.brandPanel} aria-labelledby="signup-heading">
        <Link className={styles.brand} href="/">
          <span className={styles.brandMark}>CC</span>
          <span>Career Copilot</span>
        </Link>

        <div className={styles.brandCopy}>
          <span className={styles.eyebrow}>Build your search system</span>
          <h1 id="signup-heading">Start organizing every career move.</h1>
          <p>
            Create a focused workspace for applications, resumes, interviews,
            and search momentum before the next opportunity arrives.
          </p>
        </div>

        <div className={styles.valueList} aria-label="Signup benefits">
          <span>Structured application tracking</span>
          <span>Resume improvement workflows</span>
          <span>Interview preparation planning</span>
        </div>
      </section>

      <section className={styles.formPanel} aria-label="Signup form">
        <div className={styles.card}>
          <div className={styles.cardHeader}>
            <span>Create account</span>
            <h2>Join Career Copilot</h2>
            <p>Use an email and password to create your workspace.</p>
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
              autoComplete="new-password"
              disabled={isSubmitting}
              helperText="Use at least 6 characters."
              id="password"
              label="Password"
              minLength={6}
              onChange={(event) => setPassword(event.target.value)}
              placeholder="Create a password"
              required
              type="password"
              value={password}
            />

            <Input
              autoComplete="new-password"
              disabled={isSubmitting}
              id="confirm-password"
              label="Confirm password"
              minLength={6}
              onChange={(event) => setConfirmPassword(event.target.value)}
              placeholder="Confirm your password"
              required
              type="password"
              value={confirmPassword}
            />

            {error ? (
              <p className={styles.error} role="alert">
                {error}
              </p>
            ) : null}

            <Button disabled={isSubmitting} type="submit">
              {isSubmitting ? "Creating account..." : "Create account"}
            </Button>
          </form>

          <p className={styles.footerText}>
            Already have an account? <Link href="/login">Sign in</Link>
          </p>
        </div>
      </section>
    </main>
  );
}
