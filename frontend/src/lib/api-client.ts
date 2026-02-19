// Task: T007 | Centralized API fetch wrapper with credentials and typed methods
// Task: T008 | Error code catalog mapping backend codes to user-facing messages

import {
  CLIENT_ERROR_CODES,
  DEFAULT_ERROR_MESSAGE,
  ERROR_MESSAGES,
  isBackendErrorCode,
} from '@/shared/error-codes'

const BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000'

const API_CONTRACT_ERROR = CLIENT_ERROR_CODES.API_CONTRACT_ERROR
const ENVELOPE_KEYS = new Set(['success', 'data', 'error'])

export interface ApiEnvelopeError {
  code: string
  message: string
}

export interface ApiEnvelope<T> {
  success: boolean
  data?: T
  error?: ApiEnvelopeError | null
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
  return ERROR_MESSAGES[code as keyof typeof ERROR_MESSAGES] ?? fallback ?? DEFAULT_ERROR_MESSAGE
}

function hasOwn(obj: Record<string, unknown>, key: string): boolean {
  return Object.prototype.hasOwnProperty.call(obj, key)
}

function isObject(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value)
}

function asContractError(reason: string, status?: number): ApiError {
  return new ApiError(API_CONTRACT_ERROR, `${getUserMessage(API_CONTRACT_ERROR)} ${reason}`, status)
}

function parseEnvelopeError(value: unknown, status?: number): ApiEnvelopeError | null | undefined {
  if (value === undefined || value === null) return value
  if (!isObject(value)) {
    throw asContractError('"error" must be null or an object.', status)
  }
  if (typeof value.code !== 'string' || typeof value.message !== 'string') {
    throw asContractError('"error.code" and "error.message" must be strings.', status)
  }
  if (!isBackendErrorCode(value.code)) {
    throw asContractError(`Unknown backend error code "${value.code}".`, status)
  }
  return { code: value.code, message: value.message }
}

export function parseApiEnvelope<T>(value: unknown, status?: number): ApiEnvelope<T> {
  if (!isObject(value)) {
    throw asContractError('Response body must be a JSON object.', status)
  }

  for (const key of Object.keys(value)) {
    if (!ENVELOPE_KEYS.has(key)) {
      throw asContractError(`Unexpected key "${key}" in API response.`, status)
    }
  }

  if (!hasOwn(value, 'success') || typeof value.success !== 'boolean') {
    throw asContractError('Missing or invalid "success" boolean.', status)
  }

  const hasData = hasOwn(value, 'data')
  const hasError = hasOwn(value, 'error')
  const parsedError = parseEnvelopeError(value.error, status)

  if (value.success) {
    if (!hasData) {
      throw asContractError('Successful responses must include "data".', status)
    }
    if (parsedError !== undefined && parsedError !== null) {
      throw asContractError('Successful responses must not include error details.', status)
    }
  } else {
    if (!hasError || parsedError === undefined || parsedError === null) {
      throw asContractError('Failed responses must include an error object.', status)
    }
  }

  return {
    success: value.success,
    data: value.data as T,
    error: parsedError,
  }
}

async function parseResponseEnvelope<T>(response: Response): Promise<ApiEnvelope<T>> {
  let payload: unknown
  try {
    payload = (await response.json()) as unknown
  } catch {
    throw asContractError('Response body is not valid JSON.', response.status)
  }
  return parseApiEnvelope<T>(payload, response.status)
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
      throw new ApiError(CLIENT_ERROR_CODES.REQUEST_TIMEOUT, getUserMessage(CLIENT_ERROR_CODES.REQUEST_TIMEOUT))
    }
    if (err instanceof TypeError) {
      throw new ApiError(CLIENT_ERROR_CODES.NETWORK_ERROR, getUserMessage(CLIENT_ERROR_CODES.NETWORK_ERROR))
    }
    throw err
  }

  // 204 No Content
  if (response.status === 204) {
    return undefined as T
  }

  const envelope = await parseResponseEnvelope<T>(response)

  if (!response.ok) {
    const error = envelope.error
    if (!error) {
      throw asContractError('Failed response is missing error details.', response.status)
    }
    throw new ApiError(error.code, getUserMessage(error.code, error.message), response.status)
  }

  if (!envelope.success) {
    throw asContractError('2xx response must have success=true.', response.status)
  }

  return envelope.data as T
}

export const apiClient = {
  get: <T>(path: string) => request<T>('GET', path),
  post: <T>(path: string, body?: unknown) => request<T>('POST', path, body),
  put: <T>(path: string, body?: unknown) => request<T>('PUT', path, body),
  patch: <T>(path: string, body?: unknown) => request<T>('PATCH', path, body),
  delete: <T>(path: string) => request<T>('DELETE', path),
}
