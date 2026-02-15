'use client'
// Task: T029 | TaskList — displays tasks with loading skeleton, error, and empty states

import { useTasks } from '@/hooks/use-tasks'
import { TaskItem } from './TaskItem'
import { EmptyState } from './EmptyState'
import { Button } from '@/components/ui/Button'

function LoadingSkeleton() {
  return (
    <ul className="flex flex-col gap-3" aria-label="Loading tasks">
      {[1, 2, 3].map((n) => (
        <li
          key={n}
          className="flex items-start gap-3 rounded-lg border border-border bg-background p-4 animate-pulse"
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
      <div className="flex flex-col items-center gap-4 py-16 text-center">
        <p className="text-foreground">Failed to load tasks.</p>
        <Button size="sm" onClick={() => void refetch()}>
          Try again
        </Button>
      </div>
    )
  }

  if (!tasks || tasks.length === 0) return <EmptyState />

  return (
    <ul role="list" className="flex flex-col gap-3">
      {tasks.map((task) => (
        <TaskItem key={task.id} task={task} />
      ))}
    </ul>
  )
}
