'use client'
// Task: T026 | useTasks — TanStack Query hook for fetching tasks
// Task: T031 | useCreateTask — optimistic prepend
// Task: T034 | useUpdateTask — optimistic replacement
// Task: T037 | useToggleTask — optimistic completion flip
// Task: T038 | useDeleteTask — optimistic filter-out

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { toast } from 'sonner'
import { apiClient, ApiError } from '@/lib/api-client'
import { useUser } from '@/providers/UserProvider'
import { CLIENT_ERROR_CODES } from '@/shared/error-codes'
import type { Task, TaskCreateRequest, TaskUpdateRequest } from '@/types'

function useTasksQueryKey(userId: string) {
  return ['tasks', userId] as const
}

async function fetchTasks(userId: string): Promise<Task[]> {
  // Strict API client contract checks envelope shape; hook validates expected payload shape.
  const data = await apiClient.get<unknown>(`/api/${userId}/tasks`)
  if (!Array.isArray(data)) {
    throw new ApiError(CLIENT_ERROR_CODES.API_CONTRACT_ERROR, 'Task list response must be an array.')
  }
  return data as Task[]
}

// T026: Fetch all tasks for authenticated user
export function useTasks() {
  const user = useUser()
  return useQuery({
    queryKey: useTasksQueryKey(user.id),
    queryFn: () => fetchTasks(user.id),
    staleTime: 0,
  })
}

// T031: Create task with optimistic prepend
export function useCreateTask() {
  const user = useUser()
  const queryClient = useQueryClient()
  const queryKey = useTasksQueryKey(user.id)

  return useMutation({
    mutationFn: (data: TaskCreateRequest) =>
      apiClient.post<Task>(`/api/${user.id}/tasks`, data),

    onMutate: async (newTask) => {
      await queryClient.cancelQueries({ queryKey })
      const snapshot = queryClient.getQueryData<Task[]>(queryKey)

      const optimistic: Task = {
        id: `optimistic-${Date.now()}`,
        title: newTask.title,
        description: newTask.description ?? null,
        is_completed: false,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        owner_id: user.id,
      }

      queryClient.setQueryData<Task[]>(queryKey, (old = []) => [optimistic, ...old])
      return { snapshot }
    },

    onError: (_err, _vars, ctx) => {
      if (ctx?.snapshot !== undefined) {
        queryClient.setQueryData(queryKey, ctx.snapshot)
      }
      toast.error('Failed to create task.', { duration: 5000 })
    },

    onSuccess: () => {
      toast.success('Task created.', { duration: 3000 })
    },

    onSettled: () => {
      void queryClient.invalidateQueries({ queryKey })
    },
  })
}

// T034: Update task with optimistic replacement
export function useUpdateTask() {
  const user = useUser()
  const queryClient = useQueryClient()
  const queryKey = useTasksQueryKey(user.id)

  return useMutation({
    mutationFn: ({ taskId, data }: { taskId: string; data: TaskUpdateRequest }) =>
      apiClient.put<Task>(`/api/${user.id}/tasks/${taskId}`, data),

    onMutate: async ({ taskId, data }) => {
      await queryClient.cancelQueries({ queryKey })
      const snapshot = queryClient.getQueryData<Task[]>(queryKey)

      queryClient.setQueryData<Task[]>(queryKey, (old = []) =>
        old.map((t) =>
          t.id === taskId ? { ...t, ...data, updated_at: new Date().toISOString() } : t,
        ),
      )
      return { snapshot }
    },

    onError: (err, _vars, ctx) => {
      if (ctx?.snapshot !== undefined) {
        queryClient.setQueryData(queryKey, ctx.snapshot)
      }
      const msg =
        err instanceof Error && err.message.includes('no longer exists')
          ? 'This task no longer exists.'
          : 'Failed to update task.'
      toast.error(msg, { duration: 5000 })
    },

    onSuccess: () => {
      toast.success('Task updated.', { duration: 3000 })
    },

    onSettled: () => {
      void queryClient.invalidateQueries({ queryKey })
    },
  })
}

// T037: Toggle task completion with optimistic flip
export function useToggleTask() {
  const user = useUser()
  const queryClient = useQueryClient()
  const queryKey = useTasksQueryKey(user.id)

  return useMutation({
    mutationFn: (taskId: string) =>
      apiClient.patch<Task>(`/api/${user.id}/tasks/${taskId}/complete`),

    onMutate: async (taskId) => {
      await queryClient.cancelQueries({ queryKey })
      const snapshot = queryClient.getQueryData<Task[]>(queryKey)

      queryClient.setQueryData<Task[]>(queryKey, (old = []) =>
        old.map((t) =>
          t.id === taskId ? { ...t, is_completed: !t.is_completed } : t,
        ),
      )
      return { snapshot }
    },

    onError: (_err, _vars, ctx) => {
      if (ctx?.snapshot !== undefined) {
        queryClient.setQueryData(queryKey, ctx.snapshot)
      }
      toast.error('Failed to update task.', { duration: 5000 })
    },

    onSettled: () => {
      void queryClient.invalidateQueries({ queryKey })
    },
  })
}

// T038: Delete task with optimistic removal
export function useDeleteTask() {
  const user = useUser()
  const queryClient = useQueryClient()
  const queryKey = useTasksQueryKey(user.id)

  return useMutation({
    mutationFn: (taskId: string) => apiClient.delete<void>(`/api/${user.id}/tasks/${taskId}`),

    onMutate: async (taskId) => {
      await queryClient.cancelQueries({ queryKey })
      const snapshot = queryClient.getQueryData<Task[]>(queryKey)

      queryClient.setQueryData<Task[]>(queryKey, (old = []) =>
        old.filter((t) => t.id !== taskId),
      )
      return { snapshot }
    },

    onError: (_err, _vars, ctx) => {
      if (ctx?.snapshot !== undefined) {
        queryClient.setQueryData(queryKey, ctx.snapshot)
      }
      toast.error('Failed to delete task.', { duration: 5000 })
    },

    onSuccess: () => {
      toast.success('Task deleted.', { duration: 3000 })
    },

    onSettled: () => {
      void queryClient.invalidateQueries({ queryKey })
    },
  })
}
