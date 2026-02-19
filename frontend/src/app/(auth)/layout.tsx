// Task: T020 | (auth) route group layout — minimal centered card, redirects if already authenticated
import { cookies } from 'next/headers'
import { redirect } from 'next/navigation'
import { ApiError, parseApiEnvelope } from '@/lib/api-client'
import { CLIENT_ERROR_CODES } from '@/shared/error-codes'

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
    <main className="flex min-h-screen items-center justify-center bg-background px-4">
      <div className="w-full max-w-[400px] rounded-lg border border-border bg-muted p-8 shadow-sm">
        {children}
      </div>
    </main>
  )
}
