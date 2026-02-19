// Task: T065 | Component tests for RegisterForm
import { describe, it, expect, vi } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { RegisterForm } from '@/components/auth/RegisterForm'
import { http, HttpResponse } from 'msw'
import { server } from '../mocks/server'
import React from 'react'

const mockPush = vi.fn()
const mockRefresh = vi.fn()

vi.mock('next/navigation', () => ({
  useRouter: () => ({ push: mockPush, refresh: mockRefresh }),
}))

function Wrapper({ children }: { children: React.ReactNode }) {
  const qc = new QueryClient({ defaultOptions: { queries: { retry: false } } })
  return React.createElement(QueryClientProvider, { client: qc }, children)
}

describe('RegisterForm', () => {
  it('renders email and password fields', () => {
    render(<RegisterForm />, { wrapper: Wrapper })
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument()
  })

  it('submits successfully and redirects to dashboard', async () => {
    const user = userEvent.setup()

    server.use(
      http.post('http://localhost:8000/api/auth/register', () =>
        HttpResponse.json(
          {
            success: true,
            data: { access_token: 'tok', token_type: 'bearer' },
            error: null,
          },
          { status: 201 },
        ),
      ),
    )

    render(<RegisterForm />, { wrapper: Wrapper })

    await user.type(screen.getByLabelText(/email/i), 'new@example.com')
    await user.type(screen.getByLabelText(/password/i), 'Password123')
    await user.click(screen.getByRole('button', { name: /create account/i }))

    await waitFor(() => {
      expect(mockPush).toHaveBeenCalledWith('/dashboard')
      expect(mockRefresh).toHaveBeenCalled()
    })
  })

  it('shows backend validation error on failed registration', async () => {
    const user = userEvent.setup()

    server.use(
      http.post('http://localhost:8000/api/auth/register', () =>
        HttpResponse.json(
          {
            success: false,
            data: null,
            error: {
              code: 'EMAIL_ALREADY_EXISTS',
              message: 'An account with this email already exists.',
            },
          },
          { status: 409 },
        ),
      ),
    )

    render(<RegisterForm />, { wrapper: Wrapper })

    await user.type(screen.getByLabelText(/email/i), 'existing@example.com')
    await user.type(screen.getByLabelText(/password/i), 'Password123')
    await user.click(screen.getByRole('button', { name: /create account/i }))

    await waitFor(() => {
      expect(screen.getByRole('alert')).toHaveTextContent(/already exists/i)
    })
  })
})
