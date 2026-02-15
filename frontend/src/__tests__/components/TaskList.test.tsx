// Task: T057 | Component tests for TaskList
import { describe, it, expect } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import { QueryClientProvider, QueryClient } from '@tanstack/react-query'
import { UserProvider } from '@/providers/UserProvider'
import { TaskList } from '@/components/tasks/TaskList'
import { http, HttpResponse } from 'msw'
import { server } from '../mocks/server'

const testUser = { id: 'user-123', email: 'test@example.com' }

function TestWrapper({ children }: { children: React.ReactNode }) {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  })
  return (
    <QueryClientProvider client={queryClient}>
      <UserProvider user={testUser}>{children}</UserProvider>
    </QueryClientProvider>
  )
}

describe('TaskList', () => {
  it('renders loading skeleton initially', () => {
    render(<TaskList />, { wrapper: TestWrapper })
    expect(screen.getByLabelText(/loading tasks/i)).toBeInTheDocument()
  })

  it('renders EmptyState when no tasks', async () => {
    server.use(
      http.get('http://localhost:8000/api/:userId/tasks', () => HttpResponse.json([])),
    )

    render(<TaskList />, { wrapper: TestWrapper })

    await waitFor(() => {
      expect(screen.getByText(/No tasks yet/i)).toBeInTheDocument()
    })
  })

  it('renders TaskItem for each task', async () => {
    render(<TaskList />, { wrapper: TestWrapper })

    await waitFor(() => {
      expect(screen.getByText('Test Task 1')).toBeInTheDocument()
    })
  })

  it('shows error state with retry button on fetch failure', async () => {
    server.use(
      http.get('http://localhost:8000/api/:userId/tasks', () =>
        HttpResponse.json({ error: { code: 'INTERNAL_SERVER_ERROR' } }, { status: 500 }),
      ),
    )

    render(<TaskList />, { wrapper: TestWrapper })

    await waitFor(() => {
      expect(screen.getByText(/Failed to load tasks/i)).toBeInTheDocument()
    })
    expect(screen.getByRole('button', { name: /try again/i })).toBeInTheDocument()
  })
})
