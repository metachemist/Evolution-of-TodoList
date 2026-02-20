'use client'
// Task: T025 | NavBar — user email display + logout button + ThemeToggle (client component)
// Task: T043 | Add ThemeToggle to NavBar

import { useAuth } from '@/hooks/use-auth'
import { BRAND_NAME, BRAND_TAGLINE } from '@/lib/brand'
import { Button } from './Button'
import { ThemeToggle } from './ThemeToggle'

interface NavBarProps {
  email: string
}

export function NavBar({ email }: NavBarProps) {
  const { logout } = useAuth()

  return (
    <nav className="relative border-b border-border-soft bg-surface-panel/70 px-4 py-3 backdrop-blur-xl">
      <div className="mx-auto flex w-full max-w-5xl items-center justify-between">
        <div className="flex items-center gap-3">
          <span className="inline-flex h-8 w-8 items-center justify-center rounded-lg border border-border-soft bg-primary/20 text-sm font-bold text-primary">
            F
          </span>
          <div>
            <p className="text-sm font-semibold tracking-tight text-foreground">{BRAND_NAME}</p>
            <p className="text-xs text-muted-foreground">{BRAND_TAGLINE}</p>
          </div>
        </div>

        <div className="flex items-center gap-2.5">
          <span className="hidden rounded-lg border border-border-soft bg-surface-card/60 px-3 py-1.5 text-xs text-muted-foreground sm:block">
            {email}
          </span>
          <ThemeToggle />
          <Button variant="ghost" size="sm" onClick={() => void logout()}>
            Sign out
          </Button>
        </div>
      </div>
    </nav>
  )
}
