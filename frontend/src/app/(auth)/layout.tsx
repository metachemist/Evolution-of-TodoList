// Task: T020 | (auth) route group layout — minimal centered card, redirects if already authenticated
import { cookies } from 'next/headers'
import { redirect } from 'next/navigation'

export default async function AuthLayout({ children }: { children: React.ReactNode }) {
  const cookieStore = await cookies()
  if (cookieStore.has('access_token')) {
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
