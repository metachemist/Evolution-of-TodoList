// Task: T004 | Shared TypeScript types — mirrors backend response shapes

export interface User {
  id: string    // UUID
  email: string
}

export interface Task {
  id: string
  title: string
  description: string | null
  is_completed: boolean
  created_at: string   // ISO 8601
  updated_at: string   // ISO 8601
  owner_id: string     // UUID, matches authenticated user
}

export interface TaskCreateRequest {
  title: string
  description?: string
}

export interface TaskUpdateRequest {
  title?: string
  description?: string
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
