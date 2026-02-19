'use client'
// Task: T046 | Dashboard error boundary — shown when an unexpected error occurs

import { Button } from '@/components/ui/Button'

interface ErrorProps {
  error: Error & { digest?: string }
  reset: () => void
}

export default function DashboardError({ reset }: ErrorProps) {
  return (
    <main className="surface-panel flex min-h-[50vh] flex-col items-center justify-center gap-4 p-8 text-center">
      <h2 className="text-heading text-foreground">Something went wrong</h2>
      <p className="text-body max-w-md">
        An unexpected error occurred. Please try refreshing the page.
      </p>
      <Button onClick={() => reset()}>
        Refresh page
      </Button>
    </main>
  )
}
