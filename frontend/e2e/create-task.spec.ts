// Task: T061 | E2E tests for creating tasks with axe-core
import { test, expect } from '@playwright/test'
import { checkA11y, injectAxe } from 'axe-playwright'

test.describe('Create task', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/login')
    await page.fill('input[type="email"]', 'e2e@example.com')
    await page.fill('input[type="password"]', 'TestPassword123!')
    await page.click('button[type="submit"]')
    await page.waitForURL(/\/dashboard/)
  })

  test('create a task via modal', async ({ page }) => {
    await injectAxe(page)

    await page.click('button:has-text("Create Task")')
    await expect(page.getByRole('dialog')).toBeVisible()

    await checkA11y(page)

    await page.fill('input[id="title"]', 'E2E Test Task')
    await page.click('button:has-text("Create Task")', { timeout: 5000 })

    // Task should appear at top of list after creation
    await expect(page.getByText('E2E Test Task')).toBeVisible()
    await checkA11y(page)
  })
})
