'use client'
// Task: T010 | Input primitive with label, error, and accessibility attributes

import React from 'react'
import type { UseFormRegisterReturn } from 'react-hook-form'

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label: string
  error?: string
  registration?: UseFormRegisterReturn
}

export function Input({ label, error, registration, id, className = '', ...props }: InputProps) {
  const inputId = id ?? registration?.name
  const errorId = error ? `${inputId}-error` : undefined

  return (
    <div className="flex flex-col gap-1">
      <label htmlFor={inputId} className="text-sm font-medium text-foreground">
        {label}
      </label>
      <input
        id={inputId}
        {...registration}
        {...props}
        aria-describedby={errorId}
        aria-invalid={error ? true : undefined}
        className={[
          'input-premium',
          error ? 'border-destructive' : '',
          className,
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
