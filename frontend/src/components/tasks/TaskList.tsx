'use client'
// Task: T029 | TaskList — displays tasks with loading skeleton, error, and empty states

import { useMemo, useState } from 'react'
import { motion } from 'framer-motion'
import { useTasks } from '@/hooks/use-tasks'
import { TaskItem } from './TaskItem'
import { EmptyState } from './EmptyState'
import { Button } from '@/components/ui/Button'
import type { TaskPriority, TaskStatus } from '@/types'

function LoadingSkeleton() {
  return (
    <ul
      className="grid grid-cols-1 gap-6 overflow-x-hidden sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 auto-rows-fr"
      aria-label="Loading tasks"
    >
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
  const [statusFilter, setStatusFilter] = useState<TaskStatus | 'ALL'>('ALL')
  const [priorityFilter, setPriorityFilter] = useState<TaskPriority | 'ALL'>('ALL')
  const [search, setSearch] = useState('')

  const filteredTasks = useMemo(() => {
    const normalizedSearch = search.trim().toLowerCase()
    return (tasks ?? []).filter((task) => {
      if (statusFilter !== 'ALL' && task.status !== statusFilter) {
        return false
      }
      if (priorityFilter !== 'ALL' && task.priority !== priorityFilter) {
        return false
      }
      if (!normalizedSearch) {
        return true
      }
      const haystack = `${task.title} ${task.description ?? ''}`.toLowerCase()
      return haystack.includes(normalizedSearch)
    })
  }, [tasks, statusFilter, priorityFilter, search])

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
    <div className="space-y-5">
      <section className="surface-card grid grid-cols-1 gap-3 p-4 sm:grid-cols-2 lg:grid-cols-3">
        <div className="flex flex-col gap-1">
          <label htmlFor="status-filter" className="text-xs font-semibold tracking-wide text-muted-foreground uppercase">
            Status
          </label>
          <select
            id="status-filter"
            className="input-premium"
            value={statusFilter}
            onChange={(event) => setStatusFilter(event.target.value as TaskStatus | 'ALL')}
          >
            <option value="ALL">All statuses</option>
            <option value="TODO">TODO</option>
            <option value="IN_PROGRESS">IN PROGRESS</option>
            <option value="DONE">DONE</option>
          </select>
        </div>
        <div className="flex flex-col gap-1">
          <label htmlFor="priority-filter" className="text-xs font-semibold tracking-wide text-muted-foreground uppercase">
            Priority
          </label>
          <select
            id="priority-filter"
            className="input-premium"
            value={priorityFilter}
            onChange={(event) => setPriorityFilter(event.target.value as TaskPriority | 'ALL')}
          >
            <option value="ALL">All priorities</option>
            <option value="LOW">LOW</option>
            <option value="MEDIUM">MEDIUM</option>
            <option value="HIGH">HIGH</option>
          </select>
        </div>
        <div className="flex flex-col gap-1">
          <label htmlFor="task-search" className="text-xs font-semibold tracking-wide text-muted-foreground uppercase">
            Search
          </label>
          <input
            id="task-search"
            className="input-premium"
            placeholder="Search tasks..."
            value={search}
            onChange={(event) => setSearch(event.target.value)}
          />
        </div>
      </section>

      {filteredTasks.length === 0 ? (
        <div className="surface-card py-12 text-center text-sm text-muted-foreground">
          No tasks match your current filters.
        </div>
      ) : (
        <motion.ul
          role="list"
          className="grid grid-cols-1 gap-6 overflow-x-hidden sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 auto-rows-fr"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.25 }}
        >
          {filteredTasks.map((task) => (
            <TaskItem key={task.id} task={task} />
          ))}
        </motion.ul>
      )}
    </div>
  )
}
