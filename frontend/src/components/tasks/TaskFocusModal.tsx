'use client'
// Task: T066 | TaskFocusModal — 25-minute countdown and focus-minute logging

import { useCallback, useEffect, useMemo, useState } from 'react'
import { Modal } from '@/components/ui/Modal'
import { Button } from '@/components/ui/Button'
import { useAddTaskFocus } from '@/hooks/use-tasks'
import type { Task } from '@/types'

interface TaskFocusModalProps {
  task: Task
  open: boolean
  onOpenChange: (open: boolean) => void
}

const FOCUS_SESSION_MINUTES = 25
const FOCUS_SESSION_SECONDS = FOCUS_SESSION_MINUTES * 60

function formatRemaining(seconds: number): string {
  const minutes = Math.floor(seconds / 60)
  const remainder = seconds % 60
  return `${String(minutes).padStart(2, '0')}:${String(remainder).padStart(2, '0')}`
}

export function TaskFocusModal({ task, open, onOpenChange }: TaskFocusModalProps) {
  const addFocus = useAddTaskFocus()
  const [remainingSeconds, setRemainingSeconds] = useState(FOCUS_SESSION_SECONDS)
  const [isRunning, setIsRunning] = useState(false)
  const [serverError, setServerError] = useState<string | null>(null)
  const [isLogging, setIsLogging] = useState(false)
  const [isLogged, setIsLogged] = useState(false)

  useEffect(() => {
    if (!open) {
      setRemainingSeconds(FOCUS_SESSION_SECONDS)
      setIsRunning(false)
      setServerError(null)
      setIsLogging(false)
      setIsLogged(false)
      return
    }
    setRemainingSeconds(FOCUS_SESSION_SECONDS)
    setIsRunning(true)
    setServerError(null)
    setIsLogging(false)
    setIsLogged(false)
  }, [open])

  useEffect(() => {
    if (!open || !isRunning || remainingSeconds <= 0 || isLogged) {
      return
    }
    const intervalId = window.setInterval(() => {
      setRemainingSeconds((prev) => Math.max(prev - 1, 0))
    }, 1000)
    return () => {
      window.clearInterval(intervalId)
    }
  }, [open, isRunning, remainingSeconds, isLogged])

  const logFocusSession = useCallback(async (): Promise<void> => {
    setServerError(null)
    setIsLogging(true)
    try {
      await addFocus.mutateAsync({
        taskId: task.id,
        data: { minutes: FOCUS_SESSION_MINUTES },
      })
      setIsLogged(true)
      onOpenChange(false)
    } catch (error) {
      if (error instanceof Error) {
        setServerError(error.message)
      } else {
        setServerError('Failed to record focus session.')
      }
      setIsRunning(false)
    } finally {
      setIsLogging(false)
    }
  }, [addFocus, onOpenChange, task.id])

  useEffect(() => {
    if (!open || remainingSeconds > 0 || isLogged || isLogging) {
      return
    }
    setIsRunning(false)
    void logFocusSession()
  }, [open, remainingSeconds, isLogged, isLogging, logFocusSession])

  const formattedRemaining = useMemo(() => formatRemaining(remainingSeconds), [remainingSeconds])

  return (
    <Modal
      open={open}
      onOpenChange={onOpenChange}
      title="Focus Mode"
      description={`Deep work session for "${task.title}"`}
    >
      <div className="flex flex-col gap-5">
        {serverError && (
          <div
            role="alert"
            className="rounded-xl border border-destructive/55 bg-destructive/10 px-4 py-3 text-sm text-destructive"
          >
            {serverError}
          </div>
        )}

        <div className="surface-card flex flex-col items-center gap-2 px-4 py-6 text-center">
          <p className="text-sm text-muted-foreground">Session length: {FOCUS_SESSION_MINUTES} minutes</p>
          <p className="text-4xl font-bold tracking-tight text-foreground">{formattedRemaining}</p>
          <p className="text-xs text-muted-foreground">
            {remainingSeconds > 0 ? 'Stay focused until the timer ends.' : 'Logging your focus session...'}
          </p>
        </div>

        <div className="flex justify-end gap-3">
          <Button
            type="button"
            variant="secondary"
            size="sm"
            onClick={() => onOpenChange(false)}
            disabled={isLogging}
          >
            Close
          </Button>
          <Button
            type="button"
            variant="ghost"
            size="sm"
            onClick={() => setIsRunning((prev) => !prev)}
            disabled={remainingSeconds === 0 || isLogging}
          >
            {isRunning ? 'Pause' : 'Resume'}
          </Button>
          <Button
            type="button"
            size="sm"
            onClick={() => void logFocusSession()}
            loading={isLogging}
          >
            Complete Now
          </Button>
        </div>
      </div>
    </Modal>
  )
}
