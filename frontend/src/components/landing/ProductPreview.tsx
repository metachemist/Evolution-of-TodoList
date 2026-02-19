'use client'
// Task: T016 | Landing product preview mock for root page
// Spec: @specs/1-specify/phase-2/feature-02-nextjs-todo-frontend.md (FR-001, FR-003)

import { motion } from 'framer-motion'
import { CheckCircle2, Circle, Clock3 } from 'lucide-react'

type PreviewTask = {
  id: string
  title: string
  isCompleted: boolean
  status: 'Done' | 'In Progress' | 'Today'
}

const previewTasks: PreviewTask[] = [
  { id: '1', title: 'Finalize sprint priorities', isCompleted: true, status: 'Done' },
  { id: '2', title: 'Ship task filtering improvements', isCompleted: false, status: 'In Progress' },
  { id: '3', title: 'Review launch checklist', isCompleted: false, status: 'Today' },
]

function statusClasses(status: PreviewTask['status']): string {
  if (status === 'Done') {
    return 'bg-emerald-500/15 text-emerald-300 border border-emerald-400/30'
  }
  if (status === 'In Progress') {
    return 'bg-amber-500/15 text-amber-300 border border-amber-400/30'
  }
  return 'bg-sky-500/15 text-sky-300 border border-sky-400/30'
}

export function ProductPreview() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.2 }}
      className="relative mx-auto w-full max-w-xl"
    >
      <motion.div
        animate={{ y: [0, -8, 0] }}
        transition={{ duration: 6, repeat: Infinity, ease: 'easeInOut' }}
        className="relative overflow-hidden rounded-2xl border border-border/80 bg-background/80 p-5 shadow-[0_24px_70px_-36px_rgba(56,189,248,0.55)] backdrop-blur-xl"
      >
        <div
          aria-hidden="true"
          className="pointer-events-none absolute -right-20 -top-20 h-44 w-44 rounded-full bg-primary/20 blur-3xl"
        />

        <div className="relative">
          <header className="mb-4 flex items-center justify-between border-b border-border/70 pb-3">
            <div>
              <p className="text-xs uppercase tracking-[0.14em] text-muted-foreground">Dashboard</p>
              <h3 className="text-lg font-semibold text-foreground">Today&apos;s Focus</h3>
            </div>
            <div className="inline-flex items-center gap-2 rounded-full border border-border/70 bg-muted/70 px-3 py-1 text-xs text-muted-foreground">
              <Clock3 className="h-3.5 w-3.5" />
              Live
            </div>
          </header>

          <div className="space-y-3">
            {previewTasks.map((task) => (
              <div
                key={task.id}
                className="flex items-center justify-between rounded-lg border border-border/70 bg-muted/40 px-3 py-2.5"
              >
                <div className="flex items-center gap-2.5">
                  {task.isCompleted ? (
                    <CheckCircle2 className="h-4.5 w-4.5 text-emerald-400" />
                  ) : (
                    <Circle className="h-4.5 w-4.5 text-muted-foreground" />
                  )}
                  <span
                    className={[
                      'text-sm',
                      task.isCompleted ? 'text-muted-foreground line-through' : 'text-foreground',
                    ].join(' ')}
                  >
                    {task.title}
                  </span>
                </div>
                <span className={['rounded-full px-2.5 py-1 text-xs font-medium', statusClasses(task.status)].join(' ')}>
                  {task.status}
                </span>
              </div>
            ))}
          </div>
        </div>
      </motion.div>
    </motion.div>
  )
}
