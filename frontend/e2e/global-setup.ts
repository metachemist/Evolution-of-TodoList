// Task: T050 | Playwright global setup for self-contained E2E environment
const BACKEND_URL = process.env.PLAYWRIGHT_BACKEND_URL ?? 'http://127.0.0.1:38000'
const PROBE_TIMEOUT_MS = 5000
const MAX_ATTEMPTS = 60
const DELAY_MS = 500

async function fetchWithTimeout(
  input: string,
  init: RequestInit = {},
  timeoutMs: number = PROBE_TIMEOUT_MS,
): Promise<Response> {
  const controller = new AbortController()
  const timeout = setTimeout(() => controller.abort(), timeoutMs)
  try {
    return await fetch(input, { ...init, signal: controller.signal })
  } finally {
    clearTimeout(timeout)
  }
}

async function waitForHealthReady(): Promise<void> {
  const healthUrl = `${BACKEND_URL}/health`

  for (let attempt = 1; attempt <= MAX_ATTEMPTS; attempt += 1) {
    try {
      const response = await fetchWithTimeout(healthUrl)
      if (!response.ok) {
        await new Promise((resolve) => setTimeout(resolve, DELAY_MS))
        continue
      }

      const payload = (await response.json()) as {
        success?: boolean
        data?: { status?: string }
      }
      if (payload.success && payload.data?.status === 'healthy') {
        return
      }
    } catch {
      // Ignore transient connection errors while webServer is starting.
    }
    await new Promise((resolve) => setTimeout(resolve, DELAY_MS))
  }

  throw new Error(`Backend did not become ready at ${healthUrl}.`)
}

async function waitForAuthRouteReady(): Promise<void> {
  const meUrl = `${BACKEND_URL}/api/auth/me`

  for (let attempt = 1; attempt <= MAX_ATTEMPTS; attempt += 1) {
    try {
      const response = await fetchWithTimeout(meUrl)
      if (response.status === 401) {
        return
      }
    } catch {
      // Ignore transient errors while backend starts.
    }
    await new Promise((resolve) => setTimeout(resolve, DELAY_MS))
  }

  throw new Error(`Backend auth-route probe failed at ${meUrl}.`)
}

export default async function globalSetup(): Promise<void> {
  await waitForHealthReady()
  await waitForAuthRouteReady()
}
