'use client'
// Task: T028 | TaskItem — displays a single task row with toggle, edit, delete
// Task: T036 | Wire edit button to TaskEditModal
// Task: T040 | Wire completion checkbox to useToggleTask
// Task: T041 | Wire delete button to TaskDeleteModal

import { useState } from 'react'
import { motion } from 'framer-motion'
import { Check, Pencil, Trash2 } from 'lucide-react'
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
    <motion.li
      className="surface-card surface-card-hover flex h-full items-start gap-3 p-4"
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.24 }}
      whileHover={{ scale: 1.005 }}
    >
      <button
        type="button"
        onClick={() => toggleTask.mutate(task.id)}
        aria-label={`Mark "${task.title}" as ${task.is_completed ? 'incomplete' : 'complete'}`}
        className={[
          'mt-0.5 inline-flex h-5 w-5 shrink-0 items-center justify-center rounded-md border transition',
          task.is_completed
            ? 'border-primary bg-primary text-primary-foreground'
            : 'border-border-soft bg-background/70 text-transparent hover:border-border-strong',
        ].join(' ')}
      >
        <Check className="h-3.5 w-3.5" />
      </button>

      <div className="min-w-0 flex-1">
        <p
          className={[
            'text-sm font-semibold leading-5 text-foreground transition',
            task.is_completed ? 'line-through text-muted-foreground' : '',
          ].join(' ')}
        >
          {task.title}
        </p>
        {task.description && (
          <p className="mt-1.5 line-clamp-2 text-sm leading-relaxed text-muted-foreground" title={task.description}>
            {task.description}
          </p>
        )}
      </div>

      <div className="flex shrink-0 items-center gap-1.5">
        <button
          onClick={() => setEditOpen(true)}
          aria-label="Edit task"
          className="rounded-lg border border-border-soft bg-background/50 p-2 text-muted-foreground transition hover:scale-[1.03] hover:border-border-strong hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
        >
          <Pencil className="h-3.5 w-3.5" />
        </button>

        <button
          onClick={() => setDeleteOpen(true)}
          aria-label="Delete task"
          className="rounded-lg border border-border-soft bg-background/50 p-2 text-muted-foreground transition hover:scale-[1.03] hover:border-destructive/45 hover:text-destructive focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
        >
          <Trash2 className="h-3.5 w-3.5" />
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
    </motion.li>
  )
}
