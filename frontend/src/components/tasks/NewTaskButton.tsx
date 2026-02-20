'use client'
// Task: T033 | NewTaskButton — owns modal open state, renders Create Task button + modal

import { useState } from 'react'
import { Plus } from 'lucide-react'
import { Button } from '@/components/ui/Button'
import { TaskCreateModal } from './TaskCreateModal'

export function NewTaskButton() {
  const [open, setOpen] = useState(false)

  return (
    <>
      <Button onClick={() => setOpen(true)} size="lg" className="w-full sm:w-auto">
        <Plus className="h-4 w-4" />
        Create Task
      </Button>
      <TaskCreateModal open={open} onOpenChange={setOpen} />
    </>
  )
}
