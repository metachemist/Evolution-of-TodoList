// Task: T024 | Dashboard layout RSC — fetches /api/auth/me, wraps children in UserProvider
import { cookies } from 'next/headers'
import { redirect } from 'next/navigation'
import { UserProvider } from '@/providers/UserProvider'
import { NavBar } from '@/components/ui/NavBar'
import type { User } from '@/types'
import { ApiError, parseApiEnvelope } from '@/lib/api-client'
import { BACKEND_ERROR_CODES, CLIENT_ERROR_CODES, isAuthFailureCode } from '@/shared/error-codes'

const BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000'

function isUserPayload(value: unknown): value is User {
  return (
    typeof value === 'object' &&
    value !== null &&
    'id' in value &&
    typeof value.id === 'string' &&
    'email' in value &&
    typeof value.email === 'string'
  )
}

async function getMe(cookieHeader: string): Promise<User | null> {
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
  if (!res.ok) {
    const code = envelope.error?.code
    if (res.status === 401 || isAuthFailureCode(code)) {
      return null
    }
    throw new ApiError(code ?? BACKEND_ERROR_CODES.HTTP_ERROR, envelope.error?.message ?? 'Request failed.', res.status)
  }

  if (!envelope.success || !isUserPayload(envelope.data)) {
    throw new ApiError(CLIENT_ERROR_CODES.API_CONTRACT_ERROR, 'Invalid /api/auth/me success payload.', res.status)
  }

  return envelope.data
}

export default async function DashboardLayout({ children }: { children: React.ReactNode }) {
  const cookieStore = await cookies()
  const cookieHeader = cookieStore.toString()
  let user: User | null = null
  try {
    user = await getMe(cookieHeader)
  } catch (err) {
    if (err instanceof ApiError && err.code === CLIENT_ERROR_CODES.API_CONTRACT_ERROR) {
      throw err
    }
    user = null
  }

  if (!user) {
    redirect('/login')
  }

  return (
    <UserProvider user={user}>
      <div className="min-h-screen bg-background">
        <NavBar email={user.email} />
        <main className="mx-auto max-w-3xl px-4 py-8">{children}</main>
      </div>
    </UserProvider>
  )
}
