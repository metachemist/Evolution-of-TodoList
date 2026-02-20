// Task: T025 — Session expiry banner on login page
// Spec: @specs/1-specify/phase-2/feature-03-auth-db-monorepo.md (US4, FR-015, SESS-001)
import { Suspense } from 'react'
import { LoginForm } from '@/components/auth/LoginForm'
import { BRAND_TITLE } from '@/lib/brand'
import { FadeIn } from '@/components/ui/FadeIn'

export const metadata = { title: BRAND_TITLE }

interface LoginPageProps {
  searchParams: Promise<{ reason?: string }>
}

export default async function LoginPage({ searchParams }: LoginPageProps) {
  const params = await searchParams
  const showExpiredBanner = params.reason === 'session_expired'

  return (
    <FadeIn>
      {showExpiredBanner && (
        <div
          role="alert"
          aria-live="polite"
          className="mb-5 rounded-xl border border-amber-300/45 bg-amber-500/10 px-4 py-3 text-sm text-amber-200"
        >
          Your session has expired. Please log in again.
        </div>
      )}
      <h1 className="text-heading text-foreground">Welcome back to Focentra</h1>
      <p className="mt-2 text-body">Sign in to continue your focused workflow.</p>
      <Suspense>
        <LoginForm />
      </Suspense>
    </FadeIn>
  )
}
