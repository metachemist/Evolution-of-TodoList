'use client'
// Task: T033 | NewTaskButton — owns modal open state, renders Create Task button + modal

import { useState } from 'react'
import { Button } from '@/components/ui/Button'
import { TaskCreateModal } from './TaskCreateModal'

export function NewTaskButton() {
  const [open, setOpen] = useState(false)

  return (
    <>
      <Button onClick={() => setOpen(true)} className="w-full sm:w-auto">
        + Create Task
      </Button>
      <TaskCreateModal open={open} onOpenChange={setOpen} />
    </>
  )
}
