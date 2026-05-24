import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, vi } from "vitest";
import { DemoLoginButton } from "./DemoLoginButton";

const push = vi.fn();
const login = vi.fn();

vi.mock("next/navigation", () => ({
  useRouter: () => ({
    push,
  }),
}));

vi.mock("@/hooks/useAuth", () => ({
  useAuth: () => ({
    login,
  }),
}));

describe("DemoLoginButton", () => {
  afterEach(() => {
    vi.clearAllMocks();
    delete process.env.NEXT_PUBLIC_DEMO_EMAIL;
    delete process.env.NEXT_PUBLIC_DEMO_PASSWORD;
  });

  it("shows a helpful error when demo credentials are missing", async () => {
    const user = userEvent.setup();
    const onError = vi.fn();

    render(
      <DemoLoginButton
        onError={onError}
        onLoadingChange={vi.fn()}
      />,
    );

    await user.click(screen.getByRole("button", { name: "Try Demo Account" }));

    expect(onError).toHaveBeenLastCalledWith(
      "Demo login is not configured. Add demo credentials to your environment variables.",
    );
    expect(login).not.toHaveBeenCalled();
  });

  it("logs in with configured demo credentials and routes to dashboard", async () => {
    const user = userEvent.setup();
    const onLoadingChange = vi.fn();

    process.env.NEXT_PUBLIC_DEMO_EMAIL = "demo@example.com";
    process.env.NEXT_PUBLIC_DEMO_PASSWORD = "demo-password";
    login.mockResolvedValueOnce({});

    render(
      <DemoLoginButton
        onError={vi.fn()}
        onLoadingChange={onLoadingChange}
      />,
    );

    await user.click(screen.getByRole("button", { name: "Try Demo Account" }));

    await waitFor(() => {
      expect(push).toHaveBeenCalledWith("/dashboard");
    });
    expect(login).toHaveBeenCalledWith("demo@example.com", "demo-password");
    expect(onLoadingChange).toHaveBeenNthCalledWith(1, true);
    expect(onLoadingChange).toHaveBeenLastCalledWith(false);
  });
});
