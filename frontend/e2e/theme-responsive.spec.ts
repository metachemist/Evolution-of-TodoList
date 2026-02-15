// Task: T064 | E2E tests for theme toggle and responsive layout with axe-core
import { test, expect } from '@playwright/test'
import { checkA11y, injectAxe } from 'axe-playwright'

test.describe('Theme and responsive layout', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/login')
    await page.fill('input[type="email"]', 'e2e@example.com')
    await page.fill('input[type="password"]', 'TestPassword123!')
    await page.click('button[type="submit"]')
    await page.waitForURL(/\/dashboard/)
  })

  test('theme toggle adds .dark class to <html>', async ({ page }) => {
    await injectAxe(page)

    // Toggle to dark
    await page.click('[aria-label="Switch to dark mode"]')
    await expect(page.locator('html')).toHaveClass(/dark/)
    await checkA11y(page)

    // Toggle back to light
    await page.click('[aria-label="Switch to light mode"]')
    await expect(page.locator('html')).not.toHaveClass(/dark/)
    await checkA11y(page)
  })

  test('layout is accessible at 375px viewport (mobile)', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 812 })
    await injectAxe(page)

    await expect(page.getByRole('heading', { name: /my tasks/i })).toBeVisible()
    await checkA11y(page)
  })
})
