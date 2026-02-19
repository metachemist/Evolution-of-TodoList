// Task: T050 | Playwright config — Chromium + Firefox + WebKit, base URL, webServer
import { defineConfig, devices } from '@playwright/test'

const FRONTEND_PORT = process.env.PLAYWRIGHT_FRONTEND_PORT ?? '3000'
const FRONTEND_URL = `http://localhost:${FRONTEND_PORT}`
const BACKEND_PORT = process.env.PLAYWRIGHT_BACKEND_PORT ?? '38001'
const BACKEND_URL = `http://127.0.0.1:${BACKEND_PORT}`
const E2E_DATABASE_URL = 'sqlite+aiosqlite:///./.tmp/playwright-e2e.db'
const E2E_USER_EMAIL = 'e2e@example.com'
const E2E_USER_PASSWORD = 'TestPassword123!'

process.env.PLAYWRIGHT_BACKEND_URL = BACKEND_URL
process.env.E2E_USER_EMAIL = E2E_USER_EMAIL
process.env.E2E_USER_PASSWORD = E2E_USER_PASSWORD

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  globalSetup: require.resolve('./e2e/global-setup'),
  use: {
    baseURL: FRONTEND_URL,
    trace: 'on-first-retry',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
  ],
  webServer: [
    {
      command:
        `bash -lc "set -euo pipefail; poetry run python -u scripts/prepare_e2e_db.py; exec poetry run uvicorn src.main:app --host 127.0.0.1 --port ${BACKEND_PORT} --log-level info"`,
      cwd: '../backend',
      url: `${BACKEND_URL}/health`,
      reuseExistingServer: false,
      timeout: 180000,
      stdout: 'pipe',
      stderr: 'pipe',
      env: {
        ...process.env,
        DATABASE_URL: E2E_DATABASE_URL,
        SECRET_KEY: 'e2e-test-secret-key-change-me-1234567890',
        CORS_ORIGIN: FRONTEND_URL,
        ALLOWED_ORIGINS: FRONTEND_URL,
        COOKIE_SECURE: 'false',
        ENVIRONMENT: 'test',
        PYTHONPATH: '.',
        E2E_USER_EMAIL,
        E2E_USER_PASSWORD,
      },
    },
    {
      command: 'npm run dev',
      cwd: '.',
      url: FRONTEND_URL,
      reuseExistingServer: false,
      timeout: 120000,
      stdout: 'pipe',
      stderr: 'pipe',
      env: {
        ...process.env,
        NEXT_PUBLIC_API_URL: BACKEND_URL,
        PORT: FRONTEND_PORT,
      },
    },
  ],
})
