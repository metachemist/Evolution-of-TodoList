This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

## E2E Environment (Playwright)

Run E2E tests from `frontend/`:

```bash
npm run test:e2e
```

Prerequisites:

- Backend dependencies are installed (`cd backend && poetry install`).
- Frontend dependencies are installed (`cd frontend && npm ci`).

Playwright now orchestrates the full stack automatically:

- Starts backend (`uvicorn`) on `http://127.0.0.1:38000` via `frontend/playwright.config.ts`.
- Resets an isolated SQLite DB at `backend/.tmp/playwright-e2e.db` before each E2E run.
- Starts frontend (`next dev`) on `http://localhost:3000` with `NEXT_PUBLIC_API_URL` pointed at the Playwright backend.
- Seeds the deterministic E2E user (`e2e@example.com`) in `frontend/e2e/global-setup.ts`.

No manually started backend is required for E2E execution.

This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.
