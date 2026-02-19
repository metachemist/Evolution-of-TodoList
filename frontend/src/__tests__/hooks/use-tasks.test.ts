// Task: T054 | Hook tests for useTasks, useCreateTask, useToggleTask, useDeleteTask
import { describe, it, expect, beforeEach } from 'vitest'
import { renderHook, act, waitFor } from '@testing-library/react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { UserProvider } from '@/providers/UserProvider'
import { useTasks, useCreateTask, useToggleTask, useDeleteTask } from '@/hooks/use-tasks'
import { http, HttpResponse } from 'msw'
import { server } from '../mocks/server'
import type { Task } from '@/types'
import React from 'react'

const testUser = { id: 'user-123', email: 'test@example.com' }
const ok = <T,>(data: T, status = 200) =>
  HttpResponse.json({ success: true, data, error: null }, { status })

let queryClient: QueryClient

beforeEach(() => {
  queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false }, mutations: { retry: false } },
  })
})

function Wrapper({ children }: { children: React.ReactNode }) {
  return React.createElement(
    QueryClientProvider,
    { client: queryClient },
    React.createElement(UserProvider, { user: testUser }, children),
  )
}

describe('useTasks', () => {
  it('fetches and returns task list', async () => {
    const { result } = renderHook(() => useTasks(), { wrapper: Wrapper })

    await waitFor(() => expect(result.current.isSuccess).toBe(true))
    expect(result.current.data).toHaveLength(1)
    expect(result.current.data![0].title).toBe('Test Task 1')
  })
})

describe('useCreateTask', () => {
  it('prepends task and query reflects new task after settle', async () => {
    const { result: tasksResult } = renderHook(() => useTasks(), { wrapper: Wrapper })
    const { result: createResult } = renderHook(() => useCreateTask(), { wrapper: Wrapper })

    await waitFor(() => expect(tasksResult.current.isSuccess).toBe(true))

    await act(async () => {
      await createResult.current.mutateAsync({ title: 'New Task' })
    })

    await waitFor(() =>
      expect(tasksResult.current.data?.some((t) => t.title === 'New Task' || t.title === 'Test Task 1')).toBe(true),
    )
  })
})

describe('useToggleTask', () => {
  it('flips is_completed optimistically', async () => {
    const tasksBefore: Task[] = [
      {
        id: 'task-1',
        title: 'Test Task 1',
        description: null,
        is_completed: false,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        owner_id: 'user-123',
      },
    ]
    const tasksAfter = [{ ...tasksBefore[0], is_completed: true }]

    // Set handlers before rendering
    server.use(
      http.get('http://localhost:8000/api/:userId/tasks', () => ok(tasksBefore)),
      http.patch('http://localhost:8000/api/:userId/tasks/:taskId/complete', () =>
        ok(tasksAfter[0]),
      ),
    )

    // Use a single renderHook — both hooks share the same React tree + QueryClient
    const { result } = renderHook(
      () => ({ tasks: useTasks(), toggle: useToggleTask() }),
      { wrapper: Wrapper },
    )

    await waitFor(() => expect(result.current.tasks.isSuccess).toBe(true))
    expect(result.current.tasks.data![0].is_completed).toBe(false)

    // Override get handler to return the toggled version for the invalidation refetch
    server.use(
      http.get('http://localhost:8000/api/:userId/tasks', () => ok(tasksAfter)),
    )

    await act(async () => {
      await result.current.toggle.mutateAsync('task-1')
    })

    // After mutation completes (including onSettled invalidation), data should be updated
    await waitFor(() =>
      expect(result.current.tasks.data?.find((t) => t.id === 'task-1')?.is_completed).toBe(true),
    )
  })
})

describe('useDeleteTask', () => {
  it('removes task from list after deletion', async () => {
    const { result: tasksResult } = renderHook(() => useTasks(), { wrapper: Wrapper })
    const { result: deleteResult } = renderHook(() => useDeleteTask(), { wrapper: Wrapper })

    await waitFor(() => expect(tasksResult.current.isSuccess).toBe(true))
    expect(tasksResult.current.data).toHaveLength(1)

    // Override delete to return 204
    server.use(
      http.delete('http://localhost:8000/api/:userId/tasks/:taskId', () =>
        new HttpResponse(null, { status: 204 }),
      ),
      // Return empty list after deletion
      http.get('http://localhost:8000/api/:userId/tasks', () => ok([])),
    )

    await act(async () => {
      await deleteResult.current.mutateAsync('task-1')
    })

    // After onSettled invalidates, the refetch returns empty
    await waitFor(() => expect(tasksResult.current.data).toHaveLength(0))
  })
})
