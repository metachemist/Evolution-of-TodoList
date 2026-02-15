// Task: T030 | Dashboard page — Server Component shell rendering TaskList and NewTaskButton
import { TaskList } from '@/components/tasks/TaskList'
import { NewTaskButton } from '@/components/tasks/NewTaskButton'

export const metadata = { title: 'Dashboard — Todo App' }

export default function DashboardPage() {
  return (
    <div>
      <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <h1 className="text-2xl font-bold text-foreground">My Tasks</h1>
        <NewTaskButton />
      </div>
      <TaskList />
    </div>
  )
}
