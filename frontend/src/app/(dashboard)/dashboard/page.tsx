// Task: T030 | Dashboard page — Server Component shell rendering TaskList and NewTaskButton
import { TaskList } from '@/components/tasks/TaskList'
import { NewTaskButton } from '@/components/tasks/NewTaskButton'
import { TaskOverviewCards } from '@/components/tasks/TaskOverviewCards'
import { BRAND_TITLE } from '@/lib/brand'
import { FadeIn } from '@/components/ui/FadeIn'

export const metadata = { title: BRAND_TITLE }

export default function DashboardPage() {
  return (
    <FadeIn className="space-y-6">
      <TaskOverviewCards />

      <section className="surface-panel p-5 sm:p-7">
        <div className="mb-7 flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <p className="text-xs font-semibold tracking-[0.14em] text-muted-foreground uppercase">
              Workspace
            </p>
            <h1 className="mt-2 text-heading text-foreground">My Tasks</h1>
            <p className="mt-2 text-sm text-muted-foreground">
              Plan your day with clarity and keep progress in motion.
            </p>
          </div>
          <NewTaskButton />
        </div>
        <TaskList />
      </section>
    </FadeIn>
  )
}
