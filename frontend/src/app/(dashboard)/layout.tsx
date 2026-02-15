// Task: T024 | Dashboard layout RSC — fetches /api/auth/me, wraps children in UserProvider
import { cookies } from 'next/headers'
import { redirect } from 'next/navigation'
import { UserProvider } from '@/providers/UserProvider'
import { NavBar } from '@/components/ui/NavBar'
import type { User } from '@/types'

const BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000'

async function getMe(cookieHeader: string): Promise<User | null> {
  try {
    const res = await fetch(`${BASE_URL}/api/auth/me`, {
      headers: { Cookie: cookieHeader },
      cache: 'no-store',
    })
    if (!res.ok) return null
    return res.json()
  } catch {
    return null
  }
}

export default async function DashboardLayout({ children }: { children: React.ReactNode }) {
  const cookieStore = await cookies()
  const cookieHeader = cookieStore.toString()
  const user = await getMe(cookieHeader)

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
