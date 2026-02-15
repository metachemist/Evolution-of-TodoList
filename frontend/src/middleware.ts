// Task: T015 | Route-level auth guard — cookie presence check only (not validation)
// Real auth validation happens in (dashboard)/layout.tsx via GET /api/auth/me
// Note: proxy.ts is the Next.js 16 renamed middleware.ts (per ADR-003)
import { NextRequest, NextResponse } from 'next/server'

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl
  const hasToken = request.cookies.has('access_token')

  // Redirect unauthenticated users away from dashboard
  if (pathname.startsWith('/dashboard') && !hasToken) {
    const loginUrl = new URL('/login', request.url)
    return NextResponse.redirect(loginUrl)
  }

  // Redirect authenticated users away from auth pages
  if ((pathname === '/login' || pathname === '/register') && hasToken) {
    const dashboardUrl = new URL('/dashboard', request.url)
    return NextResponse.redirect(dashboardUrl)
  }

  return NextResponse.next()
}

export const config = {
  matcher: ['/dashboard/:path*', '/login', '/register'],
}
