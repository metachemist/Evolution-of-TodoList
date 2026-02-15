// Task: T053 | Hook tests for useAuth
import { describe, it, expect, vi } from 'vitest'
import { renderHook, act, waitFor } from '@testing-library/react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { useAuth } from '@/hooks/use-auth'
import { http, HttpResponse } from 'msw'
import { server } from '../mocks/server'
import React from 'react'

const mockPush = vi.fn()
const mockRefresh = vi.fn()

vi.mock('next/navigation', () => ({
  useRouter: () => ({ push: mockPush, refresh: mockRefresh }),
}))

function createWrapper() {
  const qc = new QueryClient({
    defaultOptions: { queries: { retry: false }, mutations: { retry: false } },
  })
  return function Wrapper({ children }: { children: React.ReactNode }) {
    return React.createElement(QueryClientProvider, { client: qc }, children)
  }
}

describe('useAuth', () => {
  it('login success — calls router.push("/dashboard")', async () => {
    mockPush.mockClear()
    const { result } = renderHook(() => useAuth(), { wrapper: createWrapper() })

    await act(async () => {
      await result.current.login({ email: 'user@example.com', password: 'password123' })
    })

    expect(mockPush).toHaveBeenCalledWith('/dashboard')
  })

  it('login 401 — throws ApiError with INVALID_CREDENTIALS code', async () => {
    server.use(
      http.post('http://localhost:8000/api/auth/login', () =>
        HttpResponse.json(
          { success: false, data: null, error: { code: 'INVALID_CREDENTIALS', message: 'bad' } },
          { status: 401 },
        ),
      ),
    )

    const { result } = renderHook(() => useAuth(), { wrapper: createWrapper() })

    let caughtError: unknown
    await act(async () => {
      try {
        await result.current.login({ email: 'user@example.com', password: 'wrongpass' })
      } catch (err) {
        caughtError = err
      }
    })

    expect(caughtError).toMatchObject({ code: 'INVALID_CREDENTIALS' })
  })

  it('logout — calls router.push("/login")', async () => {
    mockPush.mockClear()
    const { result } = renderHook(() => useAuth(), { wrapper: createWrapper() })

    await waitFor(() => expect(result.current).toBeDefined())

    await act(async () => {
      await result.current.logout()
    })

    expect(mockPush).toHaveBeenCalledWith('/login')
  })
})
