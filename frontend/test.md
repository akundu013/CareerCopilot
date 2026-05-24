# Frontend Testing Guide

This frontend uses Vitest, React Testing Library, and Playwright.

Run commands from the `frontend/` folder.

## Install Dependencies

If dependencies are not installed yet:

```powershell
cd frontend
npm install
```

If Playwright browsers are missing:

```powershell
npx playwright install chromium
```

## Unit And Component Tests

Run all Vitest tests:

```powershell
npm run test
```

Run Vitest in watch mode:

```powershell
npm run test:watch
```

Run one test file:

```powershell
npx vitest run components\analysis\JobDescriptionInput.test.tsx
```

## E2E Tests

Run Playwright E2E tests:

```powershell
npm run test:e2e
```

The Playwright config starts the Next.js dev server automatically at:

```txt
http://127.0.0.1:3000
```

## Verification Commands

Use these commands before considering frontend changes ready:

```powershell
npm run lint
npx tsc --noEmit
npm run build
npm run test
npm run test:e2e
```

## Test Setup Files

`vitest.config.ts`

Configures Vitest for React component tests. It uses the `jsdom` browser-like environment, enables global test APIs, loads `test/setup.ts`, and excludes the `e2e/` folder so Playwright tests are not run by Vitest.

`test/setup.ts`

Loads `@testing-library/jest-dom/vitest` so tests can use matchers like `toBeRequired`, `toBeDisabled`, and `toBeInTheDocument`.

`playwright.config.ts`

Configures Playwright E2E tests. It points Playwright to the `e2e/` folder and starts the Next.js dev server before tests run.

## Test Files

`components/analysis/JobDescriptionInput.test.tsx`

Tests the job description textarea used by the analysis form. It verifies required field behavior, change handling, and disabled state behavior.

`components/analysis/ResumeSelector.test.tsx`

Tests resume selection for the analysis form. It verifies that parsed resumes are shown and that selecting a resume calls the parent change handler with the selected resume id.

`components/auth/DemoLoginButton.test.tsx`

Tests demo login behavior. It mocks `useAuth` and Next.js navigation, verifies missing demo credentials show a readable error, and verifies successful demo login redirects to `/dashboard`.

`e2e/landing.spec.ts`

Runs a browser smoke test against the landing page. It verifies the main Career Copilot page loads and exposes the primary dashboard and feature entry points.

## Notes

- Component tests should mock Firebase, auth hooks, router navigation, and API calls.
- E2E tests should cover high-value user paths, not implementation details.
- Keep form validation tests close to the component that owns the form state.
- Keep Playwright tests in `e2e/` so they stay separate from Vitest.
