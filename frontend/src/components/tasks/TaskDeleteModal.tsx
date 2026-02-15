'use client'
// Task: T039 | TaskDeleteModal — confirmation dialog with destructive delete button

import { useDeleteTask } from '@/hooks/use-tasks'
import { Modal } from '@/components/ui/Modal'
import { Button } from '@/components/ui/Button'
import type { Task } from '@/types'

interface TaskDeleteModalProps {
  task: Task
  open: boolean
  onOpenChange: (open: boolean) => void
}

export function TaskDeleteModal({ task, open, onOpenChange }: TaskDeleteModalProps) {
  const deleteTask = useDeleteTask()

  async function handleDelete() {
    await deleteTask.mutateAsync(task.id)
    onOpenChange(false)
  }

  return (
    <Modal
      open={open}
      onOpenChange={onOpenChange}
      title="Delete Task"
      description="Are you sure you want to delete this task? This action cannot be undone."
    >
      <div className="flex justify-end gap-3">
        <Button
          type="button"
          variant="ghost"
          size="sm"
          onClick={() => onOpenChange(false)}
        >
          Cancel
        </Button>
        <Button
          type="button"
          variant="destructive"
          size="sm"
          loading={deleteTask.isPending}
          onClick={() => void handleDelete()}
        >
          Delete
        </Button>
      </div>
    </Modal>
  )
}
