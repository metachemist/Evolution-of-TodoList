// Task: T024 — F05 fix: server-side session validation with explicit cookie forwarding
// Spec: @specs/1-specify/phase-2/feature-03-auth-db-monorepo.md (FR-004, FR-011, US4)
// Note: Next.js Edge middleware runs server-side. `credentials: 'include'` does NOT
//       auto-forward client cookies in a server fetch. The access_token must be extracted
//       and forwarded explicitly via the Cookie header.
import { NextResponse } from 'next/server'

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000'

export default async function proxy(request: Request) {
  const url = new URL(request.url)
  const { pathname } = url
  // Parse access_token from the standard Cookie header (nodejs runtime, no NextRequest.cookies)
  const cookieHeader = request.headers.get('cookie') ?? ''
  const cookieValue = cookieHeader
    .split(';')
    .map(c => c.trim().split('='))
    .find(([k]) => k === 'access_token')
    ?.[1]

  // ── Dashboard routes: require a valid session ──────────────────────────────
  if (pathname.startsWith('/dashboard')) {
    if (!cookieValue) {
      // No cookie at all — skip the network call and redirect immediately
      const loginUrl = new URL('/login?reason=session_expired', request.url)
      return NextResponse.redirect(loginUrl)
    }

    // Validate the session by calling the backend's /me endpoint.
    // Explicitly forward the cookie so the server-side fetch carries it (F05 fix).
    try {
      const res = await fetch(`${API_URL}/api/auth/me`, {
        method: 'GET',
        headers: {
          Cookie: `access_token=${cookieValue}`,
        },
        cache: 'no-store',
      })

      if (!res.ok) {
        // 401 SESSION_EXPIRED or INVALID_TOKEN — redirect to login with reason
        const loginUrl = new URL('/login?reason=session_expired', request.url)
        return NextResponse.redirect(loginUrl)
      }
    } catch {
      // Network error fetching /me (backend down) — fail open to avoid lockout
      // The dashboard layout will handle the error state
    }

    return NextResponse.next()
  }

  // ── Auth pages: redirect authenticated users to dashboard ──────────────────
  if (pathname === '/login' || pathname === '/register') {
    if (cookieValue) {
      // Cookie present — attempt a quick validation before redirecting
      // (avoids redirect loops with an expired cookie on the auth page)
      try {
        const res = await fetch(`${API_URL}/api/auth/me`, {
          method: 'GET',
          headers: {
            Cookie: `access_token=${cookieValue}`,
          },
          cache: 'no-store',
        })
        if (res.ok) {
          const dashboardUrl = new URL('/dashboard', request.url)
          return NextResponse.redirect(dashboardUrl)
        }
        // Expired/invalid cookie — let the user stay on the auth page
      } catch {
        // Network error — let the user stay on the auth page
      }
    }
  }

  return NextResponse.next()
}

export const config = {
  matcher: ['/dashboard/:path*', '/login', '/register'],
}
