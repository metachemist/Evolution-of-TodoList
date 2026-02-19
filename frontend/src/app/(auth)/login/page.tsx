// Task: T025 — Session expiry banner on login page
// Spec: @specs/1-specify/phase-2/feature-03-auth-db-monorepo.md (US4, FR-015, SESS-001)
import { Suspense } from 'react'
import { LoginForm } from '@/components/auth/LoginForm'

export const metadata = { title: 'Sign In — Todo App' }

interface LoginPageProps {
  searchParams: Promise<{ reason?: string }>
}

export default async function LoginPage({ searchParams }: LoginPageProps) {
  const params = await searchParams
  const showExpiredBanner = params.reason === 'session_expired'

  return (
    <>
      {showExpiredBanner && (
        // WCAG: role="alert" announces to screen readers; aria-live="polite" queues the announcement
        <div
          role="alert"
          aria-live="polite"
          className="mb-4 rounded-md border border-amber-300 bg-amber-50 px-4 py-3 text-sm text-amber-800 dark:border-amber-700 dark:bg-amber-950 dark:text-amber-200"
        >
          Your session has expired. Please log in again.
        </div>
      )}
      <h1 className="mb-6 text-2xl font-bold text-foreground">Sign in to your account</h1>
      <Suspense>
        <LoginForm />
      </Suspense>
    </>
  )
}
