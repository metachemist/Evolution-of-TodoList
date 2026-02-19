'use client'
// Task: T029 | TaskList — displays tasks with loading skeleton, error, and empty states

import { motion } from 'framer-motion'
import { useTasks } from '@/hooks/use-tasks'
import { TaskItem } from './TaskItem'
import { EmptyState } from './EmptyState'
import { Button } from '@/components/ui/Button'

function LoadingSkeleton() {
  return (
    <ul className="grid grid-cols-1 gap-6 overflow-x-hidden md:grid-cols-2 auto-rows-fr" aria-label="Loading tasks">
      {[1, 2, 3].map((n) => (
        <li
          key={n}
          className="surface-card flex h-full items-start gap-3 p-4 animate-pulse"
        >
          <div className="mt-1 h-4 w-4 shrink-0 rounded-full bg-muted" />
          <div className="flex-1 space-y-2">
            <div className="h-3 w-3/5 rounded bg-muted" />
            <div className="h-3 w-2/5 rounded bg-muted" />
          </div>
        </li>
      ))}
    </ul>
  )
}

export function TaskList() {
  const { data: tasks, isLoading, isError, refetch } = useTasks()

  if (isLoading) return <LoadingSkeleton />

  if (isError) {
    return (
      <div className="surface-card flex flex-col items-center gap-4 py-16 text-center">
        <p className="text-subheading text-foreground">Failed to load tasks.</p>
        <Button size="sm" variant="secondary" onClick={() => void refetch()}>
          Try again
        </Button>
      </div>
    )
  }

  if (!tasks || tasks.length === 0) return <EmptyState />

  return (
    <motion.ul
      role="list"
      className="grid grid-cols-1 gap-6 overflow-x-hidden md:grid-cols-2 auto-rows-fr"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.25 }}
    >
      {tasks.map((task) => (
        <TaskItem key={task.id} task={task} />
      ))}
    </motion.ul>
  )
}
