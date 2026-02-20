// Task: T004 | Shared TypeScript types — mirrors backend response shapes

export interface User {
  id: string    // UUID
  email: string
}

export type TaskPriority = 'LOW' | 'MEDIUM' | 'HIGH'
export type TaskStatus = 'TODO' | 'IN_PROGRESS' | 'DONE'

export interface Task {
  id: string
  title: string
  description: string | null
  is_completed: boolean
  priority: TaskPriority
  due_date: string | null
  focus_minutes: number
  status: TaskStatus
  created_at: string   // ISO 8601
  updated_at: string   // ISO 8601
  owner_id: string     // UUID, matches authenticated user
}

export interface TaskCreateRequest {
  title: string
  description?: string
  priority: TaskPriority
  due_date?: string
  status: TaskStatus
}

export interface TaskUpdateRequest {
  title?: string
  description?: string
  priority?: TaskPriority
  due_date?: string
  status?: TaskStatus
}

export interface TaskOverview {
  total_tasks: number
  completed_tasks: number
  in_progress_tasks: number
  overdue_tasks: number
  total_focus_minutes: number
  completion_rate: number
}

export interface TaskFocusRequest {
  minutes: number
}

export interface AuthRequest {
  email: string
  password: string
}

export interface TokenResponse {
  access_token: string
  token_type: 'bearer'
}

export interface ApiErrorResponse {
  success: false
  data: null
  error: {
    code: string
    message: string
  }
}
