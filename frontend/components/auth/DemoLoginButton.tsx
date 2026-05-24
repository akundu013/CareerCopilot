"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/hooks/useAuth";
import styles from "./DemoLoginButton.module.scss";

interface DemoLoginButtonProps {
  disabled?: boolean;
  onError: (message: string) => void;
  onLoadingChange: (isLoading: boolean) => void;
}

export function DemoLoginButton({
  disabled = false,
  onError,
  onLoadingChange,
}: DemoLoginButtonProps) {
  const router = useRouter();
  const { login } = useAuth();
  const [isDemoLoading, setIsDemoLoading] = useState(false);

  async function handleDemoLogin() {
    const demoEmail = process.env.NEXT_PUBLIC_DEMO_EMAIL;
    const demoPassword = process.env.NEXT_PUBLIC_DEMO_PASSWORD;

    onError("");

    if (!demoEmail || !demoPassword) {
      onError(
        "Demo login is not configured. Add demo credentials to your environment variables.",
      );
      return;
    }

    setIsDemoLoading(true);
    onLoadingChange(true);

    try {
      await login(demoEmail, demoPassword);
      router.push("/dashboard");
    } catch (demoLoginError) {
      onError(
        demoLoginError instanceof Error
          ? demoLoginError.message
          : "Unable to log in with the demo account. Please try again.",
      );
    } finally {
      setIsDemoLoading(false);
      onLoadingChange(false);
    }
  }

  return (
    <div className={styles.demoPanel}>
      <button
        className={styles.button}
        disabled={disabled || isDemoLoading}
        onClick={handleDemoLogin}
        type="button"
      >
        {isDemoLoading ? "Preparing demo..." : "Try Demo Account"}
      </button>
      <p className={styles.helperText}>
        Explore Career Copilot with sample applications, resumes, analyses, and
        interview prep.
      </p>
    </div>
  );
}
