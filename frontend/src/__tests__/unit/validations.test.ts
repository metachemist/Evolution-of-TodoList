// Task: T052 | Unit tests for Zod validation schemas
import { describe, it, expect } from 'vitest'
import { authSchema, taskCreateSchema, taskUpdateSchema } from '@/lib/validations'

describe('authSchema', () => {
  it('accepts valid email and password', () => {
    const result = authSchema.safeParse({ email: 'user@example.com', password: 'password123' })
    expect(result.success).toBe(true)
  })

  it('rejects invalid email with correct message', () => {
    const result = authSchema.safeParse({ email: 'not-an-email', password: 'password123' })
    expect(result.success).toBe(false)
    if (!result.success) {
      expect(result.error.issues[0].message).toBe('Please enter a valid email address.')
    }
  })

  it('rejects password shorter than 8 chars with correct message', () => {
    const result = authSchema.safeParse({ email: 'user@example.com', password: 'short' })
    expect(result.success).toBe(false)
    if (!result.success) {
      expect(result.error.issues[0].message).toBe('Password must be at least 8 characters.')
    }
  })
})

describe('taskCreateSchema', () => {
  it('accepts valid title only', () => {
    const result = taskCreateSchema.safeParse({ title: 'My task', priority: 'MEDIUM', status: 'TODO' })
    expect(result.success).toBe(true)
  })

  it('accepts title with description', () => {
    const result = taskCreateSchema.safeParse({
      title: 'My task',
      description: 'Details here',
      priority: 'HIGH',
      status: 'IN_PROGRESS',
    })
    expect(result.success).toBe(true)
  })

  it('accepts empty string for description', () => {
    const result = taskCreateSchema.safeParse({ title: 'My task', description: '', priority: 'LOW', status: 'TODO' })
    expect(result.success).toBe(true)
  })

  it('rejects empty title with correct message', () => {
    const result = taskCreateSchema.safeParse({ title: '', priority: 'MEDIUM', status: 'TODO' })
    expect(result.success).toBe(false)
    if (!result.success) {
      expect(result.error.issues[0].message).toBe('Title is required.')
    }
  })

  it('rejects title exceeding 255 chars', () => {
    const result = taskCreateSchema.safeParse({ title: 'a'.repeat(256), priority: 'MEDIUM', status: 'TODO' })
    expect(result.success).toBe(false)
    if (!result.success) {
      expect(result.error.issues[0].message).toBe('Title must be 255 characters or less.')
    }
  })

  it('rejects description exceeding 5000 chars', () => {
    const result = taskCreateSchema.safeParse({
      title: 'Task',
      description: 'a'.repeat(5001),
      priority: 'MEDIUM',
      status: 'TODO',
    })
    expect(result.success).toBe(false)
    if (!result.success) {
      expect(result.error.issues[0].message).toBe('Description must be 5000 characters or less.')
    }
  })
})

describe('taskUpdateSchema', () => {
  it('is the same schema as taskCreateSchema', () => {
    // Both accept the same inputs
    const createResult = taskUpdateSchema.safeParse({ title: 'Updated title', priority: 'MEDIUM', status: 'TODO' })
    expect(createResult.success).toBe(true)
  })

  it('rejects empty title with correct message', () => {
    const result = taskUpdateSchema.safeParse({ title: '', priority: 'MEDIUM', status: 'TODO' })
    expect(result.success).toBe(false)
    if (!result.success) {
      expect(result.error.issues[0].message).toBe('Title is required.')
    }
  })
})
