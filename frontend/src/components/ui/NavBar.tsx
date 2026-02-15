'use client'
// Task: T025 | NavBar — user email display + logout button + ThemeToggle (client component)
// Task: T043 | Add ThemeToggle to NavBar

import { useAuth } from '@/hooks/use-auth'
import { Button } from './Button'
import { ThemeToggle } from './ThemeToggle'

interface NavBarProps {
  email: string
}

export function NavBar({ email }: NavBarProps) {
  const { logout } = useAuth()

  return (
    <nav className="border-b border-border bg-background px-4 py-3">
      <div className="mx-auto flex max-w-3xl items-center justify-between">
        <span className="font-semibold text-foreground">Todo App</span>
        <div className="flex items-center gap-2">
          <span className="hidden text-sm text-muted-foreground sm:block">{email}</span>
          <ThemeToggle />
          <Button variant="ghost" size="sm" onClick={() => void logout()}>
            Sign out
          </Button>
        </div>
      </div>
    </nav>
  )
}
