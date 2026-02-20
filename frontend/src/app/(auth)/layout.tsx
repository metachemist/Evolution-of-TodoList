// Task: T020 | (auth) route group layout — minimal centered card, redirects if already authenticated
import { cookies } from 'next/headers'
import { redirect } from 'next/navigation'
import { ApiError, parseApiEnvelope } from '@/lib/api-client'
import { BRAND_NAME } from '@/lib/brand'
import { CLIENT_ERROR_CODES } from '@/shared/error-codes'
import { AppBackdrop } from '@/components/ui/AppBackdrop'

const BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000'

function hasValidUserPayload(value: unknown): value is { id: string; email: string } {
  return (
    typeof value === 'object' &&
    value !== null &&
    'id' in value &&
    typeof value.id === 'string' &&
    'email' in value &&
    typeof value.email === 'string'
  )
}

async function hasValidSession(cookieHeader: string): Promise<boolean> {
  if (!cookieHeader) {
    return false
  }
  try {
    const res = await fetch(`${BASE_URL}/api/auth/me`, {
      headers: { Cookie: cookieHeader },
      cache: 'no-store',
    })
    let payload: unknown
    try {
      payload = (await res.json()) as unknown
    } catch {
      throw new ApiError(CLIENT_ERROR_CODES.API_CONTRACT_ERROR, 'Invalid JSON in /api/auth/me response.', res.status)
    }
    const envelope = parseApiEnvelope<unknown>(payload, res.status)
    if (!res.ok) return false
    return envelope.success && hasValidUserPayload(envelope.data)
  } catch (err) {
    if (err instanceof ApiError && err.code === CLIENT_ERROR_CODES.API_CONTRACT_ERROR) {
      throw err
    }
    return false
  }
}

export default async function AuthLayout({ children }: { children: React.ReactNode }) {
  const cookieStore = await cookies()
  const cookieHeader = cookieStore.toString()
  if (await hasValidSession(cookieHeader)) {
    redirect('/dashboard')
  }

  return (
    <main className="app-shell">
      <AppBackdrop />
      <div className="relative mx-auto flex min-h-screen w-full max-w-6xl items-center justify-center px-4 py-10">
        <section className="surface-panel w-full max-w-[460px] p-8 sm:p-10">
          <div className="mb-8">
            <p className="inline-flex items-center rounded-full border border-border-soft bg-muted/55 px-3 py-1 text-[11px] font-semibold tracking-[0.16em] text-muted-foreground uppercase">
              {BRAND_NAME}
            </p>
          </div>
          {children}
        </section>
      </div>
    </main>
  )
}
