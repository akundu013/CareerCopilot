import { expect, test } from "@playwright/test";

test("landing page exposes the main product workflow", async ({ page }) => {
  await page.goto("/");

  await expect(
    page.getByRole("heading", { level: 1, name: "Career Copilot" }),
  ).toBeVisible();
  await expect(
    page.getByRole("link", { name: "View dashboard" }),
  ).toHaveAttribute("href", "/dashboard");
  await expect(page.getByText("Application Tracking")).toBeVisible();
  await expect(page.getByText("Resume Analysis")).toBeVisible();
  await expect(page.getByText("Interview Preparation")).toBeVisible();
});
