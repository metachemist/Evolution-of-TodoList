// Task: T008 | Shared backend/frontend error code catalog to prevent drift
// Source of truth: backend/src/utils/error_mapper.py + backend/src/main.py HTTP code_map

export const BACKEND_ERROR_CODES = {
  EMAIL_ALREADY_EXISTS: 'EMAIL_ALREADY_EXISTS',
  INVALID_CREDENTIALS: 'INVALID_CREDENTIALS',
  VALIDATION_ERROR: 'VALIDATION_ERROR',
  SESSION_EXPIRED: 'SESSION_EXPIRED',
  INVALID_TOKEN: 'INVALID_TOKEN',
  UNAUTHORIZED: 'UNAUTHORIZED',
  FORBIDDEN: 'FORBIDDEN',
  TASK_NOT_FOUND: 'TASK_NOT_FOUND',
  RATE_LIMITED: 'RATE_LIMITED',
  INTERNAL_ERROR: 'INTERNAL_ERROR',
  SERVICE_UNAVAILABLE: 'SERVICE_UNAVAILABLE',
  NOT_FOUND: 'NOT_FOUND',
  HTTP_ERROR: 'HTTP_ERROR',
} as const

export type BackendErrorCode = typeof BACKEND_ERROR_CODES[keyof typeof BACKEND_ERROR_CODES]

export const BACKEND_ERROR_MESSAGES: Record<BackendErrorCode, string> = {
  EMAIL_ALREADY_EXISTS: 'An account with this email already exists. Please log in instead.',
  INVALID_CREDENTIALS: 'Invalid email or password. Please try again.',
  VALIDATION_ERROR: 'Validation failed.',
  SESSION_EXPIRED: 'Your session has expired. Please log in again.',
  INVALID_TOKEN: 'Your session has expired. Please log in again.',
  UNAUTHORIZED: 'Please log in to continue.',
  FORBIDDEN: 'You do not have permission to perform this action.',
  TASK_NOT_FOUND: 'This task could not be found.',
  RATE_LIMITED: 'Too many requests. Please wait a moment and try again.',
  INTERNAL_ERROR: 'Something went wrong on our end. Please try again later.',
  SERVICE_UNAVAILABLE: 'Something went wrong on our end. Please try again later.',
  NOT_FOUND: 'This resource could not be found.',
  HTTP_ERROR: 'Request failed.',
}

export const CLIENT_ERROR_CODES = {
  API_CONTRACT_ERROR: 'API_CONTRACT_ERROR',
  REQUEST_TIMEOUT: 'REQUEST_TIMEOUT',
  NETWORK_ERROR: 'NETWORK_ERROR',
} as const

export type ClientErrorCode = typeof CLIENT_ERROR_CODES[keyof typeof CLIENT_ERROR_CODES]
export type KnownErrorCode = BackendErrorCode | ClientErrorCode

export const CLIENT_ERROR_MESSAGES: Record<ClientErrorCode, string> = {
  API_CONTRACT_ERROR: 'Server response did not match the expected contract.',
  REQUEST_TIMEOUT: 'The request is taking longer than expected. Please check your connection.',
  NETWORK_ERROR: 'Unable to connect to the server. Please check your connection and try again.',
}

export const ERROR_MESSAGES: Record<KnownErrorCode, string> = {
  ...BACKEND_ERROR_MESSAGES,
  ...CLIENT_ERROR_MESSAGES,
}

export const DEFAULT_ERROR_MESSAGE = 'An unexpected error occurred.'

const BACKEND_CODE_SET = new Set<string>(Object.values(BACKEND_ERROR_CODES))
const AUTH_FAILURE_CODE_SET = new Set<string>([
  BACKEND_ERROR_CODES.UNAUTHORIZED,
  BACKEND_ERROR_CODES.INVALID_TOKEN,
  BACKEND_ERROR_CODES.SESSION_EXPIRED,
])

export function isBackendErrorCode(code: string): code is BackendErrorCode {
  return BACKEND_CODE_SET.has(code)
}

export function isAuthFailureCode(code: string | undefined): boolean {
  return typeof code === 'string' && AUTH_FAILURE_CODE_SET.has(code)
}
