// Task: T027 | EmptyState — shown when no tasks exist
import { Sparkles } from 'lucide-react'

export function EmptyState() {
  return (
    <div className="surface-card flex flex-col items-center gap-4 py-16 text-center">
      <span className="inline-flex h-12 w-12 items-center justify-center rounded-xl border border-border-soft bg-primary/15 text-primary">
        <Sparkles className="h-6 w-6" />
      </span>
      <div className="max-w-md">
        <p className="text-subheading text-foreground">No tasks yet.</p>
        <p className="mt-1 text-sm text-muted-foreground">
          Create your first task to get started.
        </p>
      </div>
    </div>
  )
}
