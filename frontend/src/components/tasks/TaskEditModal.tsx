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
import type { Task } from '@/types'

interface TaskEditModalProps {
  task: Task
  open: boolean
  onOpenChange: (open: boolean) => void
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
    },
  })

  // Reset form values when task changes
  useEffect(() => {
    reset({ title: task.title, description: task.description ?? '' })
  }, [task, reset])

  async function onSubmit(data: TaskUpdateFormData) {
    setServerError(null)
    try {
      await updateTask.mutateAsync({ taskId: task.id, data })
      onOpenChange(false)
    } catch (err) {
      if (err instanceof ApiError && err.code === 'TASK_NOT_FOUND') {
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
          <Button size="sm" onClick={() => onOpenChange(false)}>Close</Button>
        </div>
      </Modal>
    )
  }

  return (
    <Modal open={open} onOpenChange={onOpenChange} title="Edit Task">
      <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-4" noValidate>
        {serverError && (
          <div role="alert" className="rounded-md border border-destructive px-4 py-3 text-sm text-destructive">
            {serverError}
          </div>
        )}

        <Input
          label="Title"
          registration={register('title')}
          error={errors.title?.message}
          autoFocus
        />
        <div className="flex flex-col gap-1">
          <label htmlFor={`edit-description-${task.id}`} className="text-sm font-medium text-foreground">
            Description <span className="text-muted-foreground">(optional)</span>
          </label>
          <textarea
            id={`edit-description-${task.id}`}
            {...register('description')}
            rows={3}
            className="w-full rounded-md border border-border bg-background px-3 py-2 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
          />
          {errors.description && (
            <p className="text-sm text-destructive" role="alert">{errors.description.message}</p>
          )}
        </div>

        <div className="flex justify-end gap-3">
          <Button type="button" variant="ghost" size="sm" onClick={() => onOpenChange(false)}>
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
