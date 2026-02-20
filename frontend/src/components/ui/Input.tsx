'use client'
// Task: T010 | Input primitive with label, error, and accessibility attributes

import React from 'react'
import type { UseFormRegisterReturn } from 'react-hook-form'

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label: string
  labelHint?: string
  error?: string
  registration?: UseFormRegisterReturn
}

export function Input({ label, labelHint, error, registration, id, className = '', ...props }: InputProps) {
  const inputId = id ?? registration?.name
  const errorId = error ? `${inputId}-error` : undefined

  return (
    <div className="flex w-full flex-col gap-1">
      <label htmlFor={inputId} className="flex items-baseline gap-2 text-sm font-medium text-foreground">
        <span>{label}</span>
        {labelHint && <span className="text-xs font-normal text-muted-foreground">{labelHint}</span>}
      </label>
      <input
        id={inputId}
        {...registration}
        {...props}
        aria-describedby={errorId}
        aria-invalid={error ? true : undefined}
        className={[
          'input-premium',
          className,
          error ? 'border-destructive' : '',
          'w-full',
        ].join(' ')}
      />
      {error && (
        <p id={errorId} className="text-sm text-destructive" role="alert">
          {error}
        </p>
      )}
    </div>
  )
}
