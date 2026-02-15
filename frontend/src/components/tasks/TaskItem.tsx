'use client'
// Task: T028 | TaskItem — displays a single task row with toggle, edit, delete
// Task: T036 | Wire edit button to TaskEditModal
// Task: T040 | Wire completion checkbox to useToggleTask
// Task: T041 | Wire delete button to TaskDeleteModal

import { useState } from 'react'
import { useToggleTask } from '@/hooks/use-tasks'
import { TaskEditModal } from './TaskEditModal'
import { TaskDeleteModal } from './TaskDeleteModal'
import type { Task } from '@/types'

interface TaskItemProps {
  task: Task
}

export function TaskItem({ task }: TaskItemProps) {
  const [editOpen, setEditOpen] = useState(false)
  const [deleteOpen, setDeleteOpen] = useState(false)
  const toggleTask = useToggleTask()

  return (
    <li className="flex items-start gap-3 rounded-lg border border-border bg-background p-4">
      {/* Completion checkbox */}
      <input
        type="checkbox"
        checked={task.is_completed}
        onChange={() => toggleTask.mutate(task.id)}
        aria-label={`Mark "${task.title}" as ${task.is_completed ? 'incomplete' : 'complete'}`}
        className="mt-1 h-4 w-4 shrink-0 cursor-pointer accent-primary"
      />

      {/* Title + description */}
      <div className="min-w-0 flex-1">
        <p
          className={[
            'text-sm font-medium text-foreground',
            task.is_completed ? 'line-through opacity-60' : '',
          ].join(' ')}
        >
          {task.title}
        </p>
        {task.description && (
          <p
            className="mt-1 line-clamp-2 text-xs text-muted-foreground"
            title={task.description}
          >
            {task.description}
          </p>
        )}
      </div>

      {/* Action buttons */}
      <div className="flex shrink-0 items-center gap-1">
        <button
          onClick={() => setEditOpen(true)}
          aria-label="Edit task"
          className="rounded p-1.5 text-muted-foreground hover:bg-muted hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
        >
          <svg className="h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" aria-hidden="true">
            <path strokeLinecap="round" strokeLinejoin="round" d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L10.582 16.07a4.5 4.5 0 01-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 011.13-1.897l8.932-8.931zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0115.75 21H5.25A2.25 2.25 0 013 18.75V8.25A2.25 2.25 0 015.25 6H10" />
          </svg>
        </button>

        <button
          onClick={() => setDeleteOpen(true)}
          aria-label="Delete task"
          className="rounded p-1.5 text-muted-foreground hover:bg-muted hover:text-destructive focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
        >
          <svg className="h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" aria-hidden="true">
            <path strokeLinecap="round" strokeLinejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
          </svg>
        </button>
      </div>

      <TaskEditModal
        task={task}
        open={editOpen}
        onOpenChange={(open) => {
          setEditOpen(open)
        }}
      />

      <TaskDeleteModal
        task={task}
        open={deleteOpen}
        onOpenChange={(open) => {
          setDeleteOpen(open)
        }}
      />
    </li>
  )
}
