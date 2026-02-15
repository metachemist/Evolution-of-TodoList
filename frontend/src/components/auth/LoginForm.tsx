'use client'
// Task: T018 | LoginForm — react-hook-form + Zod, session expiry banner, error display

import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { useSearchParams } from 'next/navigation'
import { Input } from '@/components/ui/Input'
import { Button } from '@/components/ui/Button'
import { useAuth } from '@/hooks/use-auth'
import { authSchema, type AuthFormData } from '@/lib/validations'
import { ApiError } from '@/lib/api-client'
import Link from 'next/link'

export function LoginForm() {
  const { login } = useAuth()
  const searchParams = useSearchParams()
  const reason = searchParams.get('reason')
  const [serverError, setServerError] = useState<string | null>(null)

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<AuthFormData>({
    resolver: zodResolver(authSchema),
  })

  async function onSubmit(data: AuthFormData) {
    setServerError(null)
    try {
      await login(data)
    } catch (err) {
      if (err instanceof ApiError) {
        setServerError(err.message)
      } else {
        setServerError('An unexpected error occurred. Please try again.')
      }
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-4" noValidate>
      {reason === 'session_expired' && (
        <div
          role="alert"
          className="rounded-md border border-border bg-muted px-4 py-3 text-sm text-muted-foreground"
        >
          Your session has expired. Please log in again.
        </div>
      )}

      {serverError && (
        <div role="alert" className="rounded-md border border-destructive px-4 py-3 text-sm text-destructive">
          {serverError}
        </div>
      )}

      <Input
        label="Email"
        type="email"
        autoComplete="email"
        registration={register('email')}
        error={errors.email?.message}
      />
      <Input
        label="Password"
        type="password"
        autoComplete="current-password"
        registration={register('password')}
        error={errors.password?.message}
      />

      <Button type="submit" loading={isSubmitting} className="w-full">
        Sign in
      </Button>

      <p className="text-center text-sm text-muted-foreground">
        Don&apos;t have an account?{' '}
        <Link href="/register" className="font-medium text-primary hover:underline">
          Register
        </Link>
      </p>
    </form>
  )
}
