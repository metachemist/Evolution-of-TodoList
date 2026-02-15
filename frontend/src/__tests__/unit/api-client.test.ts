// Task: T051 | Unit tests for API client
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { apiClient, ApiError } from '@/lib/api-client'

describe('apiClient', () => {
  beforeEach(() => {
    vi.restoreAllMocks()
  })

  it('includes credentials: include on every request', async () => {
    const fetchSpy = vi.spyOn(globalThis, 'fetch').mockResolvedValueOnce(
      new Response(JSON.stringify({ data: 'ok' }), { status: 200 }),
    )

    await apiClient.get('/api/test')

    expect(fetchSpy).toHaveBeenCalledWith(
      expect.any(String),
      expect.objectContaining({ credentials: 'include' }),
    )
  })

  it('maps TypeError to NETWORK_ERROR', async () => {
    vi.spyOn(globalThis, 'fetch').mockRejectedValueOnce(new TypeError('Failed to fetch'))

    await expect(apiClient.get('/api/test')).rejects.toMatchObject({
      code: 'NETWORK_ERROR',
      message: expect.stringContaining('Unable to connect'),
    })
  })

  it('maps AbortError to REQUEST_TIMEOUT', async () => {
    const abortError = new DOMException('The operation was aborted.', 'AbortError')
    vi.spyOn(globalThis, 'fetch').mockRejectedValueOnce(abortError)

    await expect(apiClient.get('/api/test')).rejects.toMatchObject({
      code: 'REQUEST_TIMEOUT',
      message: expect.stringContaining('taking longer than expected'),
    })
  })

  it('maps INVALID_CREDENTIALS backend code to user-friendly message', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValueOnce(
      new Response(
        JSON.stringify({ success: false, data: null, error: { code: 'INVALID_CREDENTIALS', message: 'bad creds' } }),
        { status: 401 },
      ),
    )

    await expect(apiClient.post('/api/auth/login', {})).rejects.toMatchObject({
      code: 'INVALID_CREDENTIALS',
      message: 'Invalid email or password.',
    })
  })

  it('maps EMAIL_ALREADY_EXISTS to user-friendly message', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValueOnce(
      new Response(
        JSON.stringify({ success: false, data: null, error: { code: 'EMAIL_ALREADY_EXISTS', message: 'exists' } }),
        { status: 409 },
      ),
    )

    await expect(apiClient.post('/api/auth/register', {})).rejects.toMatchObject({
      code: 'EMAIL_ALREADY_EXISTS',
      message: expect.stringContaining('already exists'),
    })
  })

  it('maps TASK_NOT_FOUND to user-friendly message', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValueOnce(
      new Response(
        JSON.stringify({ success: false, data: null, error: { code: 'TASK_NOT_FOUND', message: 'not found' } }),
        { status: 404 },
      ),
    )

    await expect(apiClient.get('/api/user/tasks/xyz')).rejects.toMatchObject({
      code: 'TASK_NOT_FOUND',
      message: expect.stringContaining('no longer exists'),
    })
  })

  it('raises ApiError for non-ok responses', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValueOnce(
      new Response(JSON.stringify({ error: { code: 'INTERNAL_SERVER_ERROR' } }), { status: 500 }),
    )

    const err = await apiClient.get('/api/test').catch((e: unknown) => e)
    expect(err).toBeInstanceOf(ApiError)
    expect((err as ApiError).status).toBe(500)
  })
})
