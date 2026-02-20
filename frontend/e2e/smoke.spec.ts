// Task: T050 | Minimal E2E smoke test for boot/readiness verification
import { test, expect } from '@playwright/test'

test('login page renders after backend/frontend boot', async ({ page }) => {
  await page.goto('/login')
  await expect(page.getByRole('button', { name: /(log in|login|sign in)/i })).toBeVisible()
})
