'use client'
// Task: T035 | TaskEditModal — pre-filled form + optimistic update

import { useEffect, useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { Modal } from '@/components/ui/Modal'
import { Input } from '@/components/ui/Input'
import { Button } from '@/components/ui/Button'
import { useUpdateTask } from '@/hooks/use-tasks'
import { taskUpdateSchema, type TaskUpdateFormData } from '@/lib/validations'
import { ApiError } from '@/lib/api-client'
import { BACKEND_ERROR_CODES } from '@/shared/error-codes'
import type { Task } from '@/types'

interface TaskEditModalProps {
  task: Task
  open: boolean
  onOpenChange: (open: boolean) => void
}

function toDateTimeLocal(value: string | null): string {
  if (!value) {
    return ''
  }
  const parsed = new Date(value)
  if (Number.isNaN(parsed.getTime())) {
    return ''
  }
  const local = new Date(parsed.getTime() - parsed.getTimezoneOffset() * 60000)
  return local.toISOString().slice(0, 16)
}

export function TaskEditModal({ task, open, onOpenChange }: TaskEditModalProps) {
  const updateTask = useUpdateTask()
  const [serverError, setServerError] = useState<string | null>(null)
  const [notFound, setNotFound] = useState(false)

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<TaskUpdateFormData>({
    resolver: zodResolver(taskUpdateSchema),
    defaultValues: {
      title: task.title,
      description: task.description ?? '',
      priority: task.priority,
      status: task.status,
      due_date: toDateTimeLocal(task.due_date),
    },
  })

  // Reset form values when task changes
  useEffect(() => {
    reset({
      title: task.title,
      description: task.description ?? '',
      priority: task.priority,
      status: task.status,
      due_date: toDateTimeLocal(task.due_date),
    })
  }, [task, reset])

  async function onSubmit(data: TaskUpdateFormData) {
    setServerError(null)
    try {
      await updateTask.mutateAsync({
        taskId: task.id,
        data: {
          title: data.title,
          description: data.description ? data.description : undefined,
          priority: data.priority,
          status: data.status,
          due_date: data.due_date ? new Date(data.due_date).toISOString() : undefined,
        },
      })
      onOpenChange(false)
    } catch (err) {
      if (err instanceof ApiError && err.code === BACKEND_ERROR_CODES.TASK_NOT_FOUND) {
        setNotFound(true)
      } else if (err instanceof ApiError) {
        setServerError(err.message)
      } else {
        setServerError('An unexpected error occurred.')
      }
    }
  }

  if (notFound) {
    return (
      <Modal open={open} onOpenChange={onOpenChange} title="Task Not Found">
        <p className="text-sm text-muted-foreground">This task no longer exists.</p>
        <div className="mt-4 flex justify-end">
          <Button size="sm" variant="secondary" onClick={() => onOpenChange(false)}>Close</Button>
        </div>
      </Modal>
    )
  }

  return (
    <Modal open={open} onOpenChange={onOpenChange} title="Edit Task">
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
            <label htmlFor={`edit-priority-${task.id}`} className="text-sm font-medium text-foreground">
              Priority
            </label>
            <select
              id={`edit-priority-${task.id}`}
              {...register('priority')}
              className="input-premium"
            >
              <option value="LOW">LOW</option>
              <option value="MEDIUM">MEDIUM</option>
              <option value="HIGH">HIGH</option>
            </select>
            {errors.priority && (
              <p className="text-sm text-destructive" role="alert">{errors.priority.message}</p>
            )}
          </div>
          <div className="flex flex-col gap-1">
            <label htmlFor={`edit-status-${task.id}`} className="text-sm font-medium text-foreground">
              Status
            </label>
            <select
              id={`edit-status-${task.id}`}
              {...register('status')}
              className="input-premium"
            >
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
          <label htmlFor={`edit-due-date-${task.id}`} className="text-sm font-medium text-foreground">
            Due Date <span className="text-muted-foreground">(optional)</span>
          </label>
          <input
            id={`edit-due-date-${task.id}`}
            type="datetime-local"
            {...register('due_date')}
            className="input-premium"
          />
          {errors.due_date && (
            <p className="text-sm text-destructive" role="alert">{errors.due_date.message}</p>
          )}
        </div>
        <div className="flex flex-col gap-1">
          <label htmlFor={`edit-description-${task.id}`} className="text-sm font-medium text-foreground">
            Description <span className="text-muted-foreground">(optional)</span>
          </label>
          <textarea
            id={`edit-description-${task.id}`}
            {...register('description')}
            rows={3}
            className="input-premium min-h-[96px] resize-y"
          />
          {errors.description && (
            <p className="text-sm text-destructive" role="alert">{errors.description.message}</p>
          )}
        </div>

        <div className="flex justify-end gap-3">
          <Button type="button" variant="secondary" size="sm" onClick={() => onOpenChange(false)}>
            Cancel
          </Button>
          <Button type="submit" size="sm" loading={isSubmitting}>
            Save Changes
          </Button>
        </div>
      </form>
    </Modal>
  )
}
