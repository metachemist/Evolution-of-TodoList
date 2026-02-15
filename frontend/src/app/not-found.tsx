// Task: T045 | 404 not-found page
import Link from 'next/link'

export default function NotFound() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-4 bg-background px-4 text-center">
      <h1 className="text-3xl font-bold text-foreground">Page not found</h1>
      <p className="text-muted-foreground">The page you requested doesn&apos;t exist.</p>
      <Link href="/dashboard" className="text-primary hover:underline">
        ← Back to dashboard
      </Link>
    </main>
  )
}
