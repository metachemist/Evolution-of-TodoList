'use client'
// Task: T028 | TaskItem — displays a single task row with toggle, edit, delete
// Task: T036 | Wire edit button to TaskEditModal
// Task: T040 | Wire completion checkbox to useToggleTask
// Task: T041 | Wire delete button to TaskDeleteModal

import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { AlarmClock, Check, CircleAlert, Pencil, Timer, Trash2 } from 'lucide-react'
import { useToggleTask } from '@/hooks/use-tasks'
import { TaskEditModal } from './TaskEditModal'
import { TaskDeleteModal } from './TaskDeleteModal'
import { TaskFocusModal } from './TaskFocusModal'
import type { Task } from '@/types'

interface TaskItemProps {
  task: Task
}

export function TaskItem({ task }: TaskItemProps) {
  const [editOpen, setEditOpen] = useState(false)
  const [deleteOpen, setDeleteOpen] = useState(false)
  const [focusOpen, setFocusOpen] = useState(false)
  const [currentTime, setCurrentTime] = useState(() => Date.now())
  const toggleTask = useToggleTask()
  const isDone = task.status === 'DONE' || task.is_completed

  useEffect(() => {
    const intervalId = window.setInterval(() => {
      setCurrentTime(Date.now())
    }, 60_000)
    return () => {
      window.clearInterval(intervalId)
    }
  }, [])

  const isOverdue =
    task.due_date !== null &&
    new Date(task.due_date).getTime() < currentTime &&
    !isDone

  function getPriorityClasses(): string {
    if (task.priority === 'HIGH') {
      return 'border-rose-500/40 bg-rose-500/12 text-rose-200'
    }
    if (task.priority === 'LOW') {
      return 'border-emerald-500/40 bg-emerald-500/12 text-emerald-200'
    }
    return 'border-amber-500/40 bg-amber-500/12 text-amber-200'
  }

  function getStatusClasses(): string {
    if (task.status === 'DONE') {
      return 'border-primary/45 bg-primary/15 text-primary'
    }
    if (task.status === 'IN_PROGRESS') {
      return 'border-sky-500/45 bg-sky-500/12 text-sky-200'
    }
    return 'border-border-soft bg-background/60 text-muted-foreground'
  }

  function formatDueDate(): string {
    if (!task.due_date) {
      return 'No due date'
    }
    const parsed = new Date(task.due_date)
    if (Number.isNaN(parsed.getTime())) {
      return 'Invalid due date'
    }
    return parsed.toLocaleString(undefined, {
      month: 'short',
      day: 'numeric',
      hour: 'numeric',
      minute: '2-digit',
    })
  }

  function formatFocusMinutes(minutes: number): string {
    const hours = Math.floor(minutes / 60)
    const remainder = minutes % 60
    if (hours === 0) {
      return `${remainder}m`
    }
    return `${hours}h ${remainder}m`
  }

  return (
    <motion.li
      className="surface-card surface-card-hover flex h-full flex-col gap-3 p-4"
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.24 }}
      whileHover={{ scale: 1.005 }}
    >
      <div className="flex items-start gap-3">
        <button
          type="button"
          onClick={() => toggleTask.mutate(task.id)}
          aria-label={`Mark "${task.title}" as ${isDone ? 'incomplete' : 'complete'}`}
          className={[
            'mt-0.5 inline-flex h-5 w-5 shrink-0 items-center justify-center rounded-md border transition',
            isDone
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
              isDone ? 'line-through text-muted-foreground' : '',
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
      </div>

      <div className="flex flex-wrap items-center gap-2">
        <span className={['rounded-full border px-2.5 py-1 text-[11px] font-semibold tracking-wide', getPriorityClasses()].join(' ')}>
          {task.priority}
        </span>
        <span className={['rounded-full border px-2.5 py-1 text-[11px] font-semibold tracking-wide', getStatusClasses()].join(' ')}>
          {task.status.replace('_', ' ')}
        </span>
        {isOverdue && (
          <span className="inline-flex items-center gap-1 rounded-full border border-rose-500/45 bg-rose-500/10 px-2.5 py-1 text-[11px] font-semibold tracking-wide text-rose-200">
            <CircleAlert className="h-3 w-3" />
            OVERDUE
          </span>
        )}
      </div>

      <div className="mt-auto flex flex-col gap-2 text-xs text-muted-foreground">
        <p className="inline-flex items-center gap-1.5">
          <AlarmClock className="h-3.5 w-3.5" />
          {formatDueDate()}
        </p>
        <p className="inline-flex items-center gap-1.5">
          <Timer className="h-3.5 w-3.5" />
          Focus time: {formatFocusMinutes(task.focus_minutes)}
        </p>
      </div>

      <div className="flex shrink-0 items-center gap-1.5 pt-1">
        <button
          onClick={() => setFocusOpen(true)}
          aria-label="Start focus mode"
          className="rounded-lg border border-border-soft bg-background/50 px-2.5 py-2 text-xs font-semibold text-muted-foreground transition hover:scale-[1.03] hover:border-border-strong hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
        >
          Start Focus
        </button>
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
      <TaskFocusModal
        task={task}
        open={focusOpen}
        onOpenChange={(open) => {
          setFocusOpen(open)
        }}
      />
    </motion.li>
  )
}
