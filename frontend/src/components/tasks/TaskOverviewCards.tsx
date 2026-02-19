'use client'
// Task: T066 | TaskOverviewCards — dashboard deep-work metrics section

import { Activity, CheckCircle2, Clock3, Hourglass, Timer } from 'lucide-react'
import { useTasksOverview } from '@/hooks/use-tasks'
import type { ReactNode } from 'react'

function OverviewSkeleton() {
  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-5">
      {[1, 2, 3, 4, 5].map((key) => (
        <div key={key} className="surface-card h-24 animate-pulse bg-muted/35" />
      ))}
    </div>
  )
}

function StatCard({
  title,
  value,
  icon,
}: {
  title: string
  value: string
  icon: ReactNode
}) {
  return (
    <article className="surface-card flex h-full items-start justify-between gap-3 p-4">
      <div>
        <p className="text-xs font-semibold tracking-wide text-muted-foreground uppercase">{title}</p>
        <p className="mt-2 text-2xl font-bold text-foreground">{value}</p>
      </div>
      <span className="inline-flex h-8 w-8 items-center justify-center rounded-lg border border-border-soft bg-background/65 text-primary">
        {icon}
      </span>
    </article>
  )
}

export function TaskOverviewCards() {
  const { data, isLoading, isError } = useTasksOverview()

  if (isLoading) {
    return <OverviewSkeleton />
  }

  if (isError || !data) {
    return (
      <div className="surface-card py-6 text-center text-sm text-muted-foreground">
        Could not load progress overview.
      </div>
    )
  }

  const focusHours = (data.total_focus_minutes / 60).toFixed(1)

  return (
    <section className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-5">
      <StatCard title="Completed" value={String(data.completed_tasks)} icon={<CheckCircle2 className="h-4 w-4" />} />
      <StatCard title="In Progress" value={String(data.in_progress_tasks)} icon={<Activity className="h-4 w-4" />} />
      <StatCard title="Overdue" value={String(data.overdue_tasks)} icon={<Hourglass className="h-4 w-4" />} />
      <StatCard title="Focus Time" value={`${focusHours}h`} icon={<Timer className="h-4 w-4" />} />
      <StatCard title="Completion Rate" value={`${data.completion_rate.toFixed(1)}%`} icon={<Clock3 className="h-4 w-4" />} />
    </section>
  )
}
