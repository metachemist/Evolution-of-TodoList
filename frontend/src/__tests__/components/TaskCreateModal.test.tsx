// Task: T065 | Component tests for TaskCreateModal and NewTaskButton
import { describe, it, expect, vi } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { UserProvider } from '@/providers/UserProvider'
import { TaskCreateModal } from '@/components/tasks/TaskCreateModal'
import { NewTaskButton } from '@/components/tasks/NewTaskButton'
import { http, HttpResponse } from 'msw'
import { server } from '../mocks/server'
import React from 'react'

const testUser = { id: 'user-123', email: 'test@example.com' }

function Wrapper({ children }: { children: React.ReactNode }) {
  const qc = new QueryClient({
    defaultOptions: { queries: { retry: false }, mutations: { retry: false } },
  })
  return (
    <QueryClientProvider client={qc}>
      <UserProvider user={testUser}>{children}</UserProvider>
    </QueryClientProvider>
  )
}

describe('TaskCreateModal', () => {
  it('submits a new task and closes modal', async () => {
    const user = userEvent.setup()
    const onOpenChange = vi.fn()

    server.use(
      http.post('http://localhost:8000/api/:userId/tasks', async ({ request }) => {
        const body = (await request.json()) as {
          title: string
          description?: string
          priority: 'LOW' | 'MEDIUM' | 'HIGH'
          due_date?: string
          status: 'TODO' | 'IN_PROGRESS' | 'DONE'
        }
        return HttpResponse.json(
          {
            success: true,
            data: {
              id: 'task-new',
              title: body.title,
              description: body.description ?? null,
              is_completed: body.status === 'DONE',
              priority: body.priority,
              due_date: body.due_date ?? null,
              focus_minutes: 0,
              status: body.status,
              created_at: new Date().toISOString(),
              updated_at: new Date().toISOString(),
              owner_id: 'user-123',
            },
            error: null,
          },
          { status: 201 },
        )
      }),
    )

    render(<TaskCreateModal open onOpenChange={onOpenChange} />, { wrapper: Wrapper })

    await user.type(screen.getByLabelText(/^title$/i), 'Task from modal test')
    await user.click(screen.getByRole('button', { name: /create task/i }))

    await waitFor(() => {
      expect(onOpenChange).toHaveBeenCalledWith(false)
    })
  })

  it('shows server error when creation fails', async () => {
    const user = userEvent.setup()
    const onOpenChange = vi.fn()

    server.use(
      http.post('http://localhost:8000/api/:userId/tasks', () =>
        HttpResponse.json(
          {
            success: false,
            data: null,
            error: { code: 'VALIDATION_ERROR', message: 'Validation failed.' },
          },
          { status: 422 },
        ),
      ),
    )

    render(<TaskCreateModal open onOpenChange={onOpenChange} />, { wrapper: Wrapper })

    await user.type(screen.getByLabelText(/^title$/i), 'Task should fail')
    await user.click(screen.getByRole('button', { name: /create task/i }))

    await waitFor(() => {
      expect(screen.getByRole('alert')).toHaveTextContent(/validation failed/i)
    })
    expect(onOpenChange).not.toHaveBeenCalledWith(false)
  })
})

describe('NewTaskButton', () => {
  it('opens create task modal when clicked', async () => {
    const user = userEvent.setup()
    render(<NewTaskButton />, { wrapper: Wrapper })

    await user.click(screen.getByRole('button', { name: /create task/i }))

    await waitFor(() => {
      expect(screen.getByRole('dialog')).toBeInTheDocument()
      expect(screen.getByRole('heading', { name: /^create task$/i })).toBeInTheDocument()
    })
  })
})
