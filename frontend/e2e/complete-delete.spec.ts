// Task: T063 | E2E tests for completing and deleting tasks with axe-core
import { test, expect } from '@playwright/test'
import { checkA11y, injectAxe } from 'axe-playwright'

test.describe('Complete and delete tasks', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/login')
    await page.fill('input[type="email"]', 'e2e@example.com')
    await page.fill('input[type="password"]', 'TestPassword123!')
    await page.click('button[type="submit"]')
    await page.waitForURL(/\/dashboard/)

    // Create a task to work with
    await page.click('button:has-text("Create Task")')
    await page.fill('input[id="title"]', 'Task to Complete/Delete')
    await page.click('dialog button:has-text("Create Task")')
    await expect(page.getByText('Task to Complete/Delete')).toBeVisible()
  })

  test('toggle task completion — title gets line-through', async ({ page }) => {
    await injectAxe(page)

    const checkbox = page.locator('input[type="checkbox"]').first()
    await checkbox.click()

    // Title should have line-through styling
    const title = page.getByText('Task to Complete/Delete')
    await expect(title).toHaveClass(/line-through/)
    await checkA11y(page)
  })

  test('delete task via confirmation modal', async ({ page }) => {
    await injectAxe(page)

    await page.click('[aria-label="Delete task"]')
    await expect(page.getByText(/cannot be undone/i)).toBeVisible()
    await checkA11y(page)

    await page.click('dialog button:has-text("Delete")')
    await expect(page.getByText('Task to Complete/Delete')).not.toBeVisible()
    await checkA11y(page)
  })
})
