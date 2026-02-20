'use client'
// Task: T026 | useTasks — TanStack Query hook for fetching tasks
// Task: T031 | useCreateTask — optimistic prepend
// Task: T034 | useUpdateTask — optimistic replacement
// Task: T037 | useToggleTask — optimistic completion flip
// Task: T038 | useDeleteTask — optimistic filter-out
// Task: T066 | Deep-work task hooks (overview + focus minutes)

import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { toast } from 'sonner'
import { apiClient, ApiError } from '@/lib/api-client'
import { useUser } from '@/providers/UserProvider'
import { CLIENT_ERROR_CODES } from '@/shared/error-codes'
import type {
  Task,
  TaskCreateRequest,
  TaskFocusRequest,
  TaskOverview,
  TaskUpdateRequest,
} from '@/types'

const TASK_PRIORITIES = new Set(['LOW', 'MEDIUM', 'HIGH'])
const TASK_STATUSES = new Set(['TODO', 'IN_PROGRESS', 'DONE'])

function useTasksQueryKey(userId: string) {
  return ['tasks', userId] as const
}

function useOverviewQueryKey(userId: string) {
  return ['tasks-overview', userId] as const
}

function isTask(value: unknown): value is Task {
  if (typeof value !== 'object' || value === null) return false
  const candidate = value as Record<string, unknown>
  return (
    typeof candidate.id === 'string' &&
    typeof candidate.title === 'string' &&
    (typeof candidate.description === 'string' || candidate.description === null) &&
    typeof candidate.is_completed === 'boolean' &&
    typeof candidate.priority === 'string' &&
    TASK_PRIORITIES.has(candidate.priority) &&
    (typeof candidate.due_date === 'string' || candidate.due_date === null) &&
    typeof candidate.focus_minutes === 'number' &&
    Number.isFinite(candidate.focus_minutes) &&
    typeof candidate.status === 'string' &&
    TASK_STATUSES.has(candidate.status) &&
    typeof candidate.created_at === 'string' &&
    typeof candidate.updated_at === 'string' &&
    typeof candidate.owner_id === 'string'
  )
}

function isTaskOverview(value: unknown): value is TaskOverview {
  if (typeof value !== 'object' || value === null) return false
  const candidate = value as Record<string, unknown>
  return (
    typeof candidate.total_tasks === 'number' &&
    typeof candidate.completed_tasks === 'number' &&
    typeof candidate.in_progress_tasks === 'number' &&
    typeof candidate.overdue_tasks === 'number' &&
    typeof candidate.total_focus_minutes === 'number' &&
    typeof candidate.completion_rate === 'number'
  )
}

function parseTaskArray(value: unknown): Task[] {
  if (!Array.isArray(value)) {
    throw new ApiError(CLIENT_ERROR_CODES.API_CONTRACT_ERROR, 'Task list response must be an array.')
  }
  if (!value.every((entry) => isTask(entry))) {
    throw new ApiError(CLIENT_ERROR_CODES.API_CONTRACT_ERROR, 'Task list contains invalid task payloads.')
  }
  return value
}

function parseTask(value: unknown): Task {
  if (!isTask(value)) {
    throw new ApiError(CLIENT_ERROR_CODES.API_CONTRACT_ERROR, 'Task response payload is invalid.')
  }
  return value
}

async function fetchTasks(userId: string): Promise<Task[]> {
  const data = await apiClient.get<unknown>(`/api/${userId}/tasks`)
  return parseTaskArray(data)
}

async function fetchTasksOverview(): Promise<TaskOverview> {
  const data = await apiClient.get<unknown>('/api/tasks/overview')
  if (!isTaskOverview(data)) {
    throw new ApiError(CLIENT_ERROR_CODES.API_CONTRACT_ERROR, 'Task overview response payload is invalid.')
  }
  return data
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

// T066: Overview metrics for authenticated user's dashboard
export function useTasksOverview() {
  const user = useUser()
  return useQuery({
    queryKey: useOverviewQueryKey(user.id),
    queryFn: () => fetchTasksOverview(),
    staleTime: 0,
  })
}

// T031: Create task with optimistic prepend
export function useCreateTask() {
  const user = useUser()
  const queryClient = useQueryClient()
  const tasksQueryKey = useTasksQueryKey(user.id)
  const overviewQueryKey = useOverviewQueryKey(user.id)

  return useMutation({
    mutationFn: async (data: TaskCreateRequest) => {
      const created = await apiClient.post<unknown>(`/api/${user.id}/tasks`, data)
      return parseTask(created)
    },

    onMutate: async (newTask) => {
      await queryClient.cancelQueries({ queryKey: tasksQueryKey })
      const snapshot = queryClient.getQueryData<Task[]>(tasksQueryKey)

      const optimistic: Task = {
        id: `optimistic-${Date.now()}`,
        title: newTask.title,
        description: newTask.description ?? null,
        is_completed: newTask.status === 'DONE',
        priority: newTask.priority,
        due_date: newTask.due_date ?? null,
        focus_minutes: 0,
        status: newTask.status,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        owner_id: user.id,
      }

      queryClient.setQueryData<Task[]>(tasksQueryKey, (old = []) => [optimistic, ...old])
      return { snapshot }
    },

    onError: (_err, _vars, ctx) => {
      if (ctx?.snapshot !== undefined) {
        queryClient.setQueryData(tasksQueryKey, ctx.snapshot)
      }
      toast.error('Failed to create task.', { duration: 5000 })
    },

    onSuccess: () => {
      toast.success('Task created.', { duration: 3000 })
    },

    onSettled: () => {
      void queryClient.invalidateQueries({ queryKey: tasksQueryKey })
      void queryClient.invalidateQueries({ queryKey: overviewQueryKey })
    },
  })
}

// T034: Update task with optimistic replacement
export function useUpdateTask() {
  const user = useUser()
  const queryClient = useQueryClient()
  const tasksQueryKey = useTasksQueryKey(user.id)
  const overviewQueryKey = useOverviewQueryKey(user.id)

  return useMutation({
    mutationFn: async ({ taskId, data }: { taskId: string; data: TaskUpdateRequest }) => {
      const updated = await apiClient.put<unknown>(`/api/${user.id}/tasks/${taskId}`, data)
      return parseTask(updated)
    },

    onMutate: async ({ taskId, data }) => {
      await queryClient.cancelQueries({ queryKey: tasksQueryKey })
      const snapshot = queryClient.getQueryData<Task[]>(tasksQueryKey)

      queryClient.setQueryData<Task[]>(tasksQueryKey, (old = []) =>
        old.map((task) => {
          if (task.id !== taskId) return task
          const nextStatus = data.status ?? task.status
          const nextIsCompleted = data.status !== undefined ? data.status === 'DONE' : task.is_completed
          return {
            ...task,
            title: data.title ?? task.title,
            description: data.description ?? task.description,
            priority: data.priority ?? task.priority,
            due_date: data.due_date ?? task.due_date,
            status: nextStatus,
            is_completed: nextIsCompleted,
            updated_at: new Date().toISOString(),
          }
        }),
      )
      return { snapshot }
    },

    onError: (err, _vars, ctx) => {
      if (ctx?.snapshot !== undefined) {
        queryClient.setQueryData(tasksQueryKey, ctx.snapshot)
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
      void queryClient.invalidateQueries({ queryKey: tasksQueryKey })
      void queryClient.invalidateQueries({ queryKey: overviewQueryKey })
    },
  })
}

// T037: Toggle task completion with optimistic flip
export function useToggleTask() {
  const user = useUser()
  const queryClient = useQueryClient()
  const tasksQueryKey = useTasksQueryKey(user.id)
  const overviewQueryKey = useOverviewQueryKey(user.id)

  return useMutation({
    mutationFn: async (taskId: string) => {
      const updated = await apiClient.patch<unknown>(`/api/${user.id}/tasks/${taskId}/complete`)
      return parseTask(updated)
    },

    onMutate: async (taskId) => {
      await queryClient.cancelQueries({ queryKey: tasksQueryKey })
      const snapshot = queryClient.getQueryData<Task[]>(tasksQueryKey)

      queryClient.setQueryData<Task[]>(tasksQueryKey, (old = []) =>
        old.map((task) => {
          if (task.id !== taskId) return task
          const toggledCompleted = !task.is_completed
          return {
            ...task,
            is_completed: toggledCompleted,
            status: toggledCompleted ? 'DONE' : 'TODO',
            updated_at: new Date().toISOString(),
          }
        }),
      )
      return { snapshot }
    },

    onError: (_err, _vars, ctx) => {
      if (ctx?.snapshot !== undefined) {
        queryClient.setQueryData(tasksQueryKey, ctx.snapshot)
      }
      toast.error('Failed to update task.', { duration: 5000 })
    },

    onSettled: () => {
      void queryClient.invalidateQueries({ queryKey: tasksQueryKey })
      void queryClient.invalidateQueries({ queryKey: overviewQueryKey })
    },
  })
}

// T038: Delete task with optimistic removal
export function useDeleteTask() {
  const user = useUser()
  const queryClient = useQueryClient()
  const tasksQueryKey = useTasksQueryKey(user.id)
  const overviewQueryKey = useOverviewQueryKey(user.id)

  return useMutation({
    mutationFn: (taskId: string) => apiClient.delete<void>(`/api/${user.id}/tasks/${taskId}`),

    onMutate: async (taskId) => {
      await queryClient.cancelQueries({ queryKey: tasksQueryKey })
      const snapshot = queryClient.getQueryData<Task[]>(tasksQueryKey)

      queryClient.setQueryData<Task[]>(tasksQueryKey, (old = []) =>
        old.filter((task) => task.id !== taskId),
      )
      return { snapshot }
    },

    onError: (_err, _vars, ctx) => {
      if (ctx?.snapshot !== undefined) {
        queryClient.setQueryData(tasksQueryKey, ctx.snapshot)
      }
      toast.error('Failed to delete task.', { duration: 5000 })
    },

    onSuccess: () => {
      toast.success('Task deleted.', { duration: 3000 })
    },

    onSettled: () => {
      void queryClient.invalidateQueries({ queryKey: tasksQueryKey })
      void queryClient.invalidateQueries({ queryKey: overviewQueryKey })
    },
  })
}

// T066: Add focused minutes with optimistic update
export function useAddTaskFocus() {
  const user = useUser()
  const queryClient = useQueryClient()
  const tasksQueryKey = useTasksQueryKey(user.id)
  const overviewQueryKey = useOverviewQueryKey(user.id)

  return useMutation({
    mutationFn: async ({ taskId, data }: { taskId: string; data: TaskFocusRequest }) => {
      const updated = await apiClient.post<unknown>(`/api/tasks/${taskId}/focus`, data)
      return parseTask(updated)
    },
    onMutate: async ({ taskId, data }) => {
      await queryClient.cancelQueries({ queryKey: tasksQueryKey })
      const snapshot = queryClient.getQueryData<Task[]>(tasksQueryKey)

      queryClient.setQueryData<Task[]>(tasksQueryKey, (old = []) =>
        old.map((task) => {
          if (task.id !== taskId) return task
          return {
            ...task,
            focus_minutes: task.focus_minutes + data.minutes,
            status: task.status === 'TODO' ? 'IN_PROGRESS' : task.status,
            updated_at: new Date().toISOString(),
          }
        }),
      )
      return { snapshot }
    },
    onError: (_err, _vars, ctx) => {
      if (ctx?.snapshot !== undefined) {
        queryClient.setQueryData(tasksQueryKey, ctx.snapshot)
      }
      toast.error('Failed to save focus session.', { duration: 5000 })
    },
    onSuccess: () => {
      toast.success('Focus session logged.', { duration: 3000 })
    },
    onSettled: () => {
      void queryClient.invalidateQueries({ queryKey: tasksQueryKey })
      void queryClient.invalidateQueries({ queryKey: overviewQueryKey })
    },
  })
}
