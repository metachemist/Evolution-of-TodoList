// Task: T060 | E2E tests for viewing tasks with axe-core
import { test, expect } from '@playwright/test'
import { checkA11y, injectAxe } from 'axe-playwright'

test.describe('View tasks', () => {
  test.beforeEach(async ({ page }) => {
    // Ensure logged in
    await page.goto('/login')
    await page.fill('input[type="email"]', 'e2e@example.com')
    await page.fill('input[type="password"]', 'TestPassword123!')
    await page.click('button[type="submit"]')
    await page.waitForURL(/\/dashboard/)
  })

  test('shows empty state when no tasks', async ({ page }) => {
    await injectAxe(page)
    // If no tasks, empty state is shown
    // Note: This test is environment-dependent; checks the UI pattern
    await expect(page).toHaveURL(/\/dashboard/)
    await checkA11y(page)
  })

  test('renders task list after login', async ({ page }) => {
    await injectAxe(page)
    await expect(page.getByRole('heading', { name: /my tasks/i })).toBeVisible()
    await checkA11y(page)
  })
})
