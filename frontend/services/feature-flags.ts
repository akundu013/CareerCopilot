const enabledValues = new Set(["1", "true", "yes", "on"]);

export function isSignupEnabled(): boolean {
  const rawValue = process.env.NEXT_PUBLIC_SIGNUP_ENABLED;

  if (!rawValue) {
    return true;
  }

  return enabledValues.has(rawValue.trim().toLowerCase());
}