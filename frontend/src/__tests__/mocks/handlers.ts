// Task: T049 | MSW request handlers for test mocking
import { http, HttpResponse } from 'msw'

const BASE_URL = 'http://localhost:8000'

export const handlers = [
  // Auth endpoints
  http.post(`${BASE_URL}/api/auth/login`, () =>
    HttpResponse.json({ access_token: 'test-token', token_type: 'bearer' }),
  ),
  http.post(`${BASE_URL}/api/auth/register`, () =>
    HttpResponse.json({ access_token: 'test-token', token_type: 'bearer' }),
  ),
  http.post(`${BASE_URL}/api/auth/logout`, () =>
    HttpResponse.json({ success: true }),
  ),
  http.get(`${BASE_URL}/api/auth/me`, () =>
    HttpResponse.json({ id: 'user-123', email: 'test@example.com' }),
  ),

  // Task endpoints
  http.get(`${BASE_URL}/api/:userId/tasks`, () =>
    HttpResponse.json([
      {
        id: 'task-1',
        title: 'Test Task 1',
        description: 'A test task',
        is_completed: false,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        owner_id: 'user-123',
      },
    ]),
  ),
  http.post(`${BASE_URL}/api/:userId/tasks`, async ({ request }) => {
    const body = await request.json() as { title: string; description?: string }
    return HttpResponse.json({
      id: 'task-new',
      title: body.title,
      description: body.description ?? null,
      is_completed: false,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      owner_id: 'user-123',
    })
  }),
  http.put(`${BASE_URL}/api/:userId/tasks/:taskId`, async ({ request }) => {
    const body = await request.json() as { title?: string; description?: string }
    return HttpResponse.json({
      id: 'task-1',
      title: body.title ?? 'Test Task 1',
      description: body.description ?? null,
      is_completed: false,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      owner_id: 'user-123',
    })
  }),
  http.patch(`${BASE_URL}/api/:userId/tasks/:taskId/complete`, () =>
    HttpResponse.json({ id: 'task-1', is_completed: true }),
  ),
  http.delete(`${BASE_URL}/api/:userId/tasks/:taskId`, () =>
    new HttpResponse(null, { status: 204 }),
  ),
]
