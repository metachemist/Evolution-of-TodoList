// Task: T005 | Zod validation schemas for forms
import { z } from 'zod'

// Login / Register
export const authSchema = z.object({
  email: z.string().email('Please enter a valid email address.'),
  password: z.string().min(8, 'Password must be at least 8 characters.'),
})

// Task Create
export const taskCreateSchema = z.object({
  title: z
    .string()
    .trim()
    .min(1, 'Title is required.')
    .max(255, 'Title must be 255 characters or less.'),
  description: z
    .string()
    .trim()
    .max(5000, 'Description must be 5000 characters or less.')
    .optional()
    .or(z.literal('')),
  priority: z.enum(['LOW', 'MEDIUM', 'HIGH']),
  status: z.enum(['TODO', 'IN_PROGRESS', 'DONE']),
  due_date: z
    .string()
    .optional()
    .or(z.literal(''))
    .refine(
      (value) => !value || !Number.isNaN(Date.parse(value)),
      'Please select a valid due date.',
    ),
})

// Task Update (same constraints)
export const taskUpdateSchema = taskCreateSchema

export type AuthFormData = z.infer<typeof authSchema>
export type TaskCreateFormData = z.infer<typeof taskCreateSchema>
export type TaskUpdateFormData = z.infer<typeof taskUpdateSchema>
