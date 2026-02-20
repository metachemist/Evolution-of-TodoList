// Task: T065 | Component tests for ThemeToggle
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { ThemeToggle } from '@/components/ui/ThemeToggle'

const setTheme = vi.fn()
let currentTheme = 'light'

vi.mock('next-themes', () => ({
  useTheme: () => ({
    resolvedTheme: currentTheme,
    setTheme,
  }),
}))

describe('ThemeToggle', () => {
  beforeEach(() => {
    setTheme.mockReset()
    currentTheme = 'light'
  })

  it('switches from light to dark', async () => {
    const user = userEvent.setup()
    render(<ThemeToggle />)

    const button = await waitFor(() =>
      screen.getByRole('button', { name: /switch to dark mode/i }),
    )

    await user.click(button)
    expect(setTheme).toHaveBeenCalledWith('dark')
  })

  it('switches from dark to light', async () => {
    const user = userEvent.setup()
    currentTheme = 'dark'
    render(<ThemeToggle />)

    const button = await waitFor(() =>
      screen.getByRole('button', { name: /switch to light mode/i }),
    )

    await user.click(button)
    expect(setTheme).toHaveBeenCalledWith('light')
  })
})
