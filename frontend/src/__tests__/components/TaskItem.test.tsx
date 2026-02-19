// Task: T058 | Component tests for TaskItem
import { describe, it, expect } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { QueryClientProvider, QueryClient } from '@tanstack/react-query'
import { UserProvider } from '@/providers/UserProvider'
import { TaskItem } from '@/components/tasks/TaskItem'
import type { Task } from '@/types'

const testUser = { id: 'user-123', email: 'test@example.com' }

const sampleTask: Task = {
  id: 'task-1',
  title: 'Test Task',
  description: 'A description for the task',
  is_completed: false,
  created_at: new Date().toISOString(),
  updated_at: new Date().toISOString(),
  owner_id: 'user-123',
}

function TestWrapper({ children }: { children: React.ReactNode }) {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false }, mutations: { retry: false } },
  })
  return (
    <QueryClientProvider client={queryClient}>
      <UserProvider user={testUser}>{children}</UserProvider>
    </QueryClientProvider>
  )
}

describe('TaskItem', () => {
  it('renders task title', () => {
    render(<TaskItem task={sampleTask} />, { wrapper: TestWrapper })
    expect(screen.getByText('Test Task')).toBeInTheDocument()
  })

  it('renders description with line-clamp-2', () => {
    render(<TaskItem task={sampleTask} />, { wrapper: TestWrapper })
    const desc = screen.getByText('A description for the task')
    expect(desc).toHaveClass('line-clamp-2')
  })

  it('applies line-through when task is completed', () => {
    const completedTask = { ...sampleTask, is_completed: true }
    render(<TaskItem task={completedTask} />, { wrapper: TestWrapper })
    const title = screen.getByText('Test Task')
    expect(title).toHaveClass('line-through')
  })

  it('renders Edit and Delete buttons with aria-labels', () => {
    render(<TaskItem task={sampleTask} />, { wrapper: TestWrapper })
    expect(screen.getByRole('button', { name: /edit task/i })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /delete task/i })).toBeInTheDocument()
  })

  it('opens edit modal when Edit button is clicked', async () => {
    const user = userEvent.setup()
    render(<TaskItem task={sampleTask} />, { wrapper: TestWrapper })
    await user.click(screen.getByRole('button', { name: /edit task/i }))
    await waitFor(() => {
      expect(screen.getByRole('dialog')).toBeInTheDocument()
    })
  })

  it('opens delete modal when Delete button is clicked', async () => {
    const user = userEvent.setup()
    render(<TaskItem task={sampleTask} />, { wrapper: TestWrapper })
    await user.click(screen.getByRole('button', { name: /delete task/i }))
    await waitFor(() => {
      expect(screen.getByText(/cannot be undone/i)).toBeInTheDocument()
    })
  })
})
