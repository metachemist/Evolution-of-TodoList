// Task: T062 | E2E tests for editing tasks with axe-core
import { test, expect } from '@playwright/test'
import { checkA11y, injectAxe } from 'axe-playwright'

test.describe('Edit task', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/login')
    await page.fill('input[type="email"]', 'e2e@example.com')
    await page.fill('input[type="password"]', 'TestPassword123!')
    await page.click('button[type="submit"]')
    await page.waitForURL(/\/dashboard/)
  })

  test('edit modal opens pre-filled and can save changes', async ({ page }) => {
    await injectAxe(page)

    // Requires a task to exist — create one first
    await page.click('button:has-text("Create Task")')
    await page.fill('input[id="title"]', 'Task to Edit')
    await page.click('dialog button:has-text("Create Task")')
    await expect(page.getByText('Task to Edit')).toBeVisible()

    // Click edit button on the first task
    await page.click('[aria-label="Edit task"]', { timeout: 5000 })
    await expect(page.getByRole('dialog')).toBeVisible()
    await checkA11y(page)

    // Verify the modal is pre-filled
    const titleInput = page.locator('dialog input')
    await expect(titleInput).toHaveValue('Task to Edit')

    // Update the title
    await titleInput.fill('Updated Task Title')
    await page.click('dialog button:has-text("Save Changes")')

    await expect(page.getByText('Updated Task Title')).toBeVisible()
    await checkA11y(page)
  })
})
