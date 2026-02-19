'use client'
// Task: T032 | TaskCreateModal — form + optimistic insert

import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { Modal } from '@/components/ui/Modal'
import { Input } from '@/components/ui/Input'
import { Button } from '@/components/ui/Button'
import { useCreateTask } from '@/hooks/use-tasks'
import { taskCreateSchema, type TaskCreateFormData } from '@/lib/validations'
import { ApiError } from '@/lib/api-client'

interface TaskCreateModalProps {
  open: boolean
  onOpenChange: (open: boolean) => void
}

export function TaskCreateModal({ open, onOpenChange }: TaskCreateModalProps) {
  const createTask = useCreateTask()
  const [serverError, setServerError] = useState<string | null>(null)

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<TaskCreateFormData>({
    resolver: zodResolver(taskCreateSchema),
    defaultValues: {
      priority: 'MEDIUM',
      status: 'TODO',
      due_date: '',
    },
  })

  async function onSubmit(data: TaskCreateFormData) {
    setServerError(null)
    try {
      await createTask.mutateAsync({
        title: data.title,
        description: data.description || undefined,
        priority: data.priority,
        status: data.status,
        due_date: data.due_date ? new Date(data.due_date).toISOString() : undefined,
      })
      reset()
      onOpenChange(false)
    } catch (err) {
      if (err instanceof ApiError) {
        setServerError(err.message)
      } else {
        setServerError('An unexpected error occurred.')
      }
    }
  }

  function handleOpenChange(open: boolean) {
    if (!open) reset()
    setServerError(null)
    onOpenChange(open)
  }

  return (
    <Modal open={open} onOpenChange={handleOpenChange} title="Create Task">
      <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-4" noValidate>
        {serverError && (
          <div role="alert" className="rounded-xl border border-destructive/55 bg-destructive/10 px-4 py-3 text-sm text-destructive">
            {serverError}
          </div>
        )}

        <Input
          label="Title"
          registration={register('title')}
          error={errors.title?.message}
          autoFocus
        />
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <div className="flex flex-col gap-1">
            <label htmlFor="priority" className="text-sm font-medium text-foreground">
              Priority
            </label>
            <select id="priority" {...register('priority')} className="input-premium">
              <option value="LOW">LOW</option>
              <option value="MEDIUM">MEDIUM</option>
              <option value="HIGH">HIGH</option>
            </select>
            {errors.priority && (
              <p className="text-sm text-destructive" role="alert">{errors.priority.message}</p>
            )}
          </div>
          <div className="flex flex-col gap-1">
            <label htmlFor="status" className="text-sm font-medium text-foreground">
              Status
            </label>
            <select id="status" {...register('status')} className="input-premium">
              <option value="TODO">TODO</option>
              <option value="IN_PROGRESS">IN PROGRESS</option>
              <option value="DONE">DONE</option>
            </select>
            {errors.status && (
              <p className="text-sm text-destructive" role="alert">{errors.status.message}</p>
            )}
          </div>
        </div>
        <div className="flex flex-col gap-1">
          <label htmlFor="due_date" className="text-sm font-medium text-foreground">
            Due Date <span className="text-muted-foreground">(optional)</span>
          </label>
          <input
            id="due_date"
            type="datetime-local"
            {...register('due_date')}
            className="input-premium"
          />
          {errors.due_date && (
            <p className="text-sm text-destructive" role="alert">{errors.due_date.message}</p>
          )}
        </div>
        <div className="flex flex-col gap-1">
          <label htmlFor="description" className="text-sm font-medium text-foreground">
            Description <span className="text-muted-foreground">(optional)</span>
          </label>
          <textarea
            id="description"
            {...register('description')}
            rows={3}
            className="input-premium min-h-[96px] resize-y"
            placeholder="Add a description..."
          />
          {errors.description && (
            <p className="text-sm text-destructive" role="alert">{errors.description.message}</p>
          )}
        </div>

        <div className="flex justify-end gap-3">
          <Button type="button" variant="secondary" size="sm" onClick={() => handleOpenChange(false)}>
            Cancel
          </Button>
          <Button type="submit" size="sm" loading={isSubmitting}>
            Create Task
          </Button>
        </div>
      </form>
    </Modal>
  )
}
