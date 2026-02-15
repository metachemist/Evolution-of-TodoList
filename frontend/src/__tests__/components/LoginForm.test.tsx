// Task: T055 | Component tests for LoginForm
import { describe, it, expect, vi } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { LoginForm } from '@/components/auth/LoginForm'
import { http, HttpResponse } from 'msw'
import { server } from '../mocks/server'
import React from 'react'

const mockPush = vi.fn()
const mockRefresh = vi.fn()
let mockSearchParams = new URLSearchParams()

vi.mock('next/navigation', () => ({
  useRouter: () => ({ push: mockPush, refresh: mockRefresh }),
  useSearchParams: () => mockSearchParams,
}))

function Wrapper({ children }: { children: React.ReactNode }) {
  const qc = new QueryClient({ defaultOptions: { queries: { retry: false } } })
  return React.createElement(QueryClientProvider, { client: qc }, children)
}

describe('LoginForm', () => {
  it('renders email and password fields', () => {
    mockSearchParams = new URLSearchParams()
    render(<LoginForm />, { wrapper: Wrapper })
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument()
  })

  it('disables submit button during loading', async () => {
    const user = userEvent.setup()
    mockSearchParams = new URLSearchParams()

    server.use(
      http.post('http://localhost:8000/api/auth/login', async () => {
        await new Promise((r) => setTimeout(r, 300))
        return HttpResponse.json({ access_token: 'tok', token_type: 'bearer' })
      }),
    )

    render(<LoginForm />, { wrapper: Wrapper })

    await user.type(screen.getByLabelText(/email/i), 'user@example.com')
    await user.type(screen.getByLabelText(/password/i), 'password123')

    const submitBtn = screen.getByRole('button', { name: /sign in/i })
    user.click(submitBtn) // Don't await — we want to check loading state
    await waitFor(() => expect(submitBtn).toBeDisabled())
  })

  it('shows error message on 401', async () => {
    const user = userEvent.setup()
    mockSearchParams = new URLSearchParams()

    server.use(
      http.post('http://localhost:8000/api/auth/login', () =>
        HttpResponse.json(
          { success: false, data: null, error: { code: 'INVALID_CREDENTIALS', message: 'bad' } },
          { status: 401 },
        ),
      ),
    )

    render(<LoginForm />, { wrapper: Wrapper })

    await user.type(screen.getByLabelText(/email/i), 'user@example.com')
    await user.type(screen.getByLabelText(/password/i), 'password123')
    await user.click(screen.getByRole('button', { name: /sign in/i }))

    await waitFor(() => {
      expect(screen.getByRole('alert')).toHaveTextContent(/Invalid email or password/i)
    })
  })

  it('shows session expired banner when reason=session_expired', () => {
    mockSearchParams = new URLSearchParams('reason=session_expired')
    render(<LoginForm />, { wrapper: Wrapper })
    expect(screen.getByRole('alert')).toHaveTextContent(/session has expired/i)
  })
})
