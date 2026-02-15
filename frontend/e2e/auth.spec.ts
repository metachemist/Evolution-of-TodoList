// Task: T059 | E2E tests for auth flow with axe-core accessibility checks
import { test, expect } from '@playwright/test'
import { checkA11y, injectAxe } from 'axe-playwright'

const testEmail = `e2e-${Date.now()}@example.com`
const testPassword = 'TestPassword123!'

test.describe('Authentication flow', () => {
  test('register a new account', async ({ page }) => {
    await page.goto('/register')
    await injectAxe(page)

    await page.fill('input[type="email"]', testEmail)
    await page.fill('input[type="password"]', testPassword)
    await page.click('button[type="submit"]')

    await expect(page).toHaveURL(/\/dashboard/)
    await checkA11y(page)
  })

  test('logout from dashboard', async ({ page }) => {
    // Login first
    await page.goto('/login')
    await page.fill('input[type="email"]', testEmail)
    await page.fill('input[type="password"]', testPassword)
    await page.click('button[type="submit"]')
    await expect(page).toHaveURL(/\/dashboard/)

    // Logout
    await page.click('button:has-text("Sign out")')
    await expect(page).toHaveURL(/\/login/)
  })

  test('login with existing account', async ({ page }) => {
    await page.goto('/login')
    await injectAxe(page)

    await page.fill('input[type="email"]', testEmail)
    await page.fill('input[type="password"]', testPassword)
    await page.click('button[type="submit"]')

    await expect(page).toHaveURL(/\/dashboard/)
    await checkA11y(page)
  })

  test('authenticated user redirected from /login to /dashboard', async ({ page }) => {
    // Login first to set cookie
    await page.goto('/login')
    await page.fill('input[type="email"]', testEmail)
    await page.fill('input[type="password"]', testPassword)
    await page.click('button[type="submit"]')
    await expect(page).toHaveURL(/\/dashboard/)

    // Try to navigate to login again
    await page.goto('/login')
    await expect(page).toHaveURL(/\/dashboard/)
  })

  test('shows session expired banner on ?reason=session_expired', async ({ page }) => {
    await page.goto('/login?reason=session_expired')
    await injectAxe(page)

    await expect(page.getByText(/session has expired/i)).toBeVisible()
    await checkA11y(page)
  })
})
