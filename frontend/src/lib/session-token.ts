// Task: T024 | Client-side access token persistence for cross-domain auth flow

const ACCESS_TOKEN_COOKIE_NAME = 'access_token'
const ACCESS_TOKEN_STORAGE_KEY = 'focentra_access_token'
const ACCESS_TOKEN_MAX_AGE_SECONDS = 60 * 60 * 24

function isBrowser(): boolean {
  return typeof window !== 'undefined' && typeof document !== 'undefined'
}

function serializeCookie(name: string, value: string, maxAgeSeconds: number): string {
  const secure = typeof window !== 'undefined' && window.location.protocol === 'https:'
  const parts = [
    `${name}=${encodeURIComponent(value)}`,
    'Path=/',
    `Max-Age=${maxAgeSeconds}`,
    'SameSite=Lax',
  ]
  if (secure) {
    parts.push('Secure')
  }
  return parts.join('; ')
}

function findCookie(name: string): string | null {
  if (!isBrowser()) return null
  const key = `${name}=`
  const rawCookie = document.cookie
    .split(';')
    .map((part) => part.trim())
    .find((part) => part.startsWith(key))
  if (!rawCookie) return null
  return decodeURIComponent(rawCookie.slice(key.length))
}

export function persistAccessToken(token: string): void {
  if (!isBrowser()) return
  document.cookie = serializeCookie(
    ACCESS_TOKEN_COOKIE_NAME,
    token,
    ACCESS_TOKEN_MAX_AGE_SECONDS,
  )
  try {
    window.localStorage.setItem(ACCESS_TOKEN_STORAGE_KEY, token)
  } catch {
    // Ignore storage availability issues (private mode / blocked storage).
  }
}

export function clearPersistedAccessToken(): void {
  if (!isBrowser()) return
  document.cookie = serializeCookie(ACCESS_TOKEN_COOKIE_NAME, '', 0)
  try {
    window.localStorage.removeItem(ACCESS_TOKEN_STORAGE_KEY)
  } catch {
    // Ignore storage availability issues (private mode / blocked storage).
  }
}

export function getPersistedAccessToken(): string | null {
  if (!isBrowser()) return null
  const cookieToken = findCookie(ACCESS_TOKEN_COOKIE_NAME)
  if (cookieToken) return cookieToken
  try {
    return window.localStorage.getItem(ACCESS_TOKEN_STORAGE_KEY)
  } catch {
    return null
  }
}

