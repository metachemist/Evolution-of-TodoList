// Task: T049 | MSW request handlers for test mocking
import { http, HttpResponse } from 'msw'

const BASE_URL = 'http://localhost:8000'

function ok<T>(data: T, status = 200) {
  return HttpResponse.json({ success: true, data, error: null }, { status })
}

const baseTask = {
  id: 'task-1',
  title: 'Test Task 1',
  description: 'A test task',
  is_completed: false,
  priority: 'MEDIUM',
  due_date: null,
  focus_minutes: 0,
  status: 'TODO',
  created_at: new Date().toISOString(),
  updated_at: new Date().toISOString(),
  owner_id: 'user-123',
} as const

export const handlers = [
  // Auth endpoints
  http.post(`${BASE_URL}/api/auth/login`, () => ok({ access_token: 'test-token', token_type: 'bearer' })),
  http.post(`${BASE_URL}/api/auth/register`, () => ok({ access_token: 'test-token', token_type: 'bearer' }, 201)),
  http.post(`${BASE_URL}/api/auth/logout`, () => ok({ logged_out: true })),
  http.get(`${BASE_URL}/api/auth/me`, () => ok({ id: 'user-123', email: 'test@example.com' })),

  // Task endpoints
  http.get(`${BASE_URL}/api/tasks/overview`, () =>
    ok({
      total_tasks: 1,
      completed_tasks: 0,
      in_progress_tasks: 0,
      overdue_tasks: 0,
      total_focus_minutes: 0,
      completion_rate: 0,
    })),
  http.get(`${BASE_URL}/api/:userId/tasks`, () => ok([baseTask])),
  http.post(`${BASE_URL}/api/:userId/tasks`, async ({ request }) => {
    const body = await request.json() as {
      title: string
      description?: string
      priority: 'LOW' | 'MEDIUM' | 'HIGH'
      due_date?: string
      status: 'TODO' | 'IN_PROGRESS' | 'DONE'
    }
    return ok({
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
    }, 201)
  }),
  http.put(`${BASE_URL}/api/:userId/tasks/:taskId`, async ({ request }) => {
    const body = await request.json() as {
      title?: string
      description?: string
      priority?: 'LOW' | 'MEDIUM' | 'HIGH'
      due_date?: string
      status?: 'TODO' | 'IN_PROGRESS' | 'DONE'
    }
    return ok({
      ...baseTask,
      id: 'task-1',
      title: body.title ?? baseTask.title,
      description: body.description ?? null,
      is_completed: body.status ? body.status === 'DONE' : baseTask.is_completed,
      priority: body.priority ?? baseTask.priority,
      due_date: body.due_date ?? null,
      focus_minutes: baseTask.focus_minutes,
      status: body.status ?? baseTask.status,
      updated_at: new Date().toISOString(),
    })
  }),
  http.patch(`${BASE_URL}/api/:userId/tasks/:taskId/complete`, () =>
    ok({
      ...baseTask,
      is_completed: true,
      status: 'DONE',
      updated_at: new Date().toISOString(),
    }),
  ),
  http.post(`${BASE_URL}/api/tasks/:taskId/focus`, async ({ request }) => {
    const body = await request.json() as { minutes: number }
    return ok({
      ...baseTask,
      focus_minutes: baseTask.focus_minutes + body.minutes,
      status: 'IN_PROGRESS',
      updated_at: new Date().toISOString(),
    })
  },
  ),
  http.delete(`${BASE_URL}/api/:userId/tasks/:taskId`, () =>
    new HttpResponse(null, { status: 204 }),
  ),
]
