// Task: T051 | Unit tests for API client
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { apiClient, ApiError } from '@/lib/api-client'
import { BACKEND_ERROR_CODES, CLIENT_ERROR_CODES } from '@/shared/error-codes'

describe('apiClient', () => {
  beforeEach(() => {
    vi.restoreAllMocks()
  })

  it('includes credentials: include on every request', async () => {
    const fetchSpy = vi.spyOn(globalThis, 'fetch').mockResolvedValueOnce(
      new Response(JSON.stringify({ success: true, data: 'ok', error: null }), { status: 200 }),
    )

    await expect(apiClient.get('/api/test')).resolves.toBe('ok')

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
      code: BACKEND_ERROR_CODES.INVALID_CREDENTIALS,
      message: 'Invalid email or password. Please try again.',
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
      code: BACKEND_ERROR_CODES.EMAIL_ALREADY_EXISTS,
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
      code: BACKEND_ERROR_CODES.TASK_NOT_FOUND,
      message: expect.stringContaining('could not be found'),
    })
  })

  it('raises ApiError for non-ok responses', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValueOnce(
      new Response(
        JSON.stringify({ success: false, data: null, error: { code: 'INTERNAL_SERVER_ERROR', message: 'boom' } }),
        { status: 500 },
      ),
    )

    const err = await apiClient.get('/api/test').catch((e: unknown) => e)
    expect(err).toBeInstanceOf(ApiError)
    expect((err as ApiError).status).toBe(500)
  })

  it('throws API_CONTRACT_ERROR when successful response is missing data', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValueOnce(
      new Response(JSON.stringify({ success: true, error: null }), { status: 200 }),
    )

    await expect(apiClient.get('/api/test')).rejects.toMatchObject({
      code: CLIENT_ERROR_CODES.API_CONTRACT_ERROR,
    })
  })

  it('throws API_CONTRACT_ERROR when response is not envelope-shaped', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValueOnce(
      new Response(JSON.stringify({ id: 'raw-response' }), { status: 200 }),
    )

    await expect(apiClient.get('/api/test')).rejects.toMatchObject({
      code: CLIENT_ERROR_CODES.API_CONTRACT_ERROR,
    })
  })

  it('throws API_CONTRACT_ERROR when error response omits error object', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValueOnce(
      new Response(JSON.stringify({ success: false, data: null }), { status: 400 }),
    )

    await expect(apiClient.get('/api/test')).rejects.toMatchObject({
      code: CLIENT_ERROR_CODES.API_CONTRACT_ERROR,
    })
  })
})
