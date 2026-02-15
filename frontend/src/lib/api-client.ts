// Task: T007 | Centralized API fetch wrapper with credentials and typed methods
// Task: T008 | Error code catalog mapping backend codes to user-facing messages

const BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000'

// User-facing error messages mapped from backend error codes
const ERROR_MESSAGES: Record<string, string> = {
  INVALID_CREDENTIALS: 'Invalid email or password.',
  EMAIL_ALREADY_EXISTS: 'An account with this email already exists.',
  UNAUTHORIZED_ACCESS: "You don't have permission to perform this action.",
  USER_NOT_FOUND: 'User not found.',
  TASK_NOT_FOUND: 'This task no longer exists.',
  INTERNAL_SERVER_ERROR: 'An unexpected server error occurred. Please try again.',
  REQUEST_TIMEOUT: 'The request is taking longer than expected. Please check your connection.',
  NETWORK_ERROR: 'Unable to connect to the server. Please check your connection and try again.',
  SESSION_EXPIRED: 'Your session has expired. Please log in again.',
}

export class ApiError extends Error {
  constructor(
    public readonly code: string,
    message: string,
    public readonly status?: number,
  ) {
    super(message)
    this.name = 'ApiError'
  }
}

function getUserMessage(code: string, fallback?: string): string {
  return ERROR_MESSAGES[code] ?? fallback ?? 'An unexpected error occurred.'
}

async function request<T>(method: string, path: string, body?: unknown): Promise<T> {
  let response: Response

  try {
    response = await fetch(`${BASE_URL}${path}`, {
      method,
      credentials: 'include',
      headers: body !== undefined ? { 'Content-Type': 'application/json' } : {},
      body: body !== undefined ? JSON.stringify(body) : undefined,
      signal: AbortSignal.timeout(15000),
    })
  } catch (err) {
    if (err instanceof DOMException && err.name === 'AbortError') {
      throw new ApiError('REQUEST_TIMEOUT', getUserMessage('REQUEST_TIMEOUT'))
    }
    if (err instanceof TypeError) {
      throw new ApiError('NETWORK_ERROR', getUserMessage('NETWORK_ERROR'))
    }
    throw err
  }

  if (!response.ok) {
    let code = String(response.status)
    let backendMessage: string | undefined

    try {
      const json = await response.json()
      if (json?.error?.code) code = json.error.code
      if (json?.error?.message) backendMessage = json.error.message
    } catch {
      // ignore parse errors
    }

    // Session expired (401)
    if (response.status === 401 && code !== 'INVALID_CREDENTIALS') {
      code = 'SESSION_EXPIRED'
    }

    throw new ApiError(code, getUserMessage(code, backendMessage), response.status)
  }

  // 204 No Content
  if (response.status === 204) {
    return undefined as T
  }

  return response.json() as Promise<T>
}

export const apiClient = {
  get: <T>(path: string) => request<T>('GET', path),
  post: <T>(path: string, body?: unknown) => request<T>('POST', path, body),
  put: <T>(path: string, body?: unknown) => request<T>('PUT', path, body),
  patch: <T>(path: string, body?: unknown) => request<T>('PATCH', path, body),
  delete: <T>(path: string) => request<T>('DELETE', path),
}
