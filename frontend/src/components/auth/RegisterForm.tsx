'use client'
// Task: T019 | RegisterForm — react-hook-form + Zod, loading state, error display

import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { Input } from '@/components/ui/Input'
import { Button } from '@/components/ui/Button'
import { useAuth } from '@/hooks/use-auth'
import { authSchema, type AuthFormData } from '@/lib/validations'
import { ApiError } from '@/lib/api-client'
import Link from 'next/link'

export function RegisterForm() {
  const { register: registerUser } = useAuth()
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
      await registerUser(data)
    } catch (err) {
      if (err instanceof ApiError) {
        setServerError(err.message)
      } else {
        setServerError('An unexpected error occurred. Please try again.')
      }
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="mt-7 flex flex-col gap-4" noValidate>
      {serverError && (
        <div role="alert" className="rounded-xl border border-destructive/55 bg-destructive/10 px-4 py-3 text-sm text-destructive">
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
        autoComplete="new-password"
        registration={register('password')}
        error={errors.password?.message}
      />

      <Button type="submit" size="lg" loading={isSubmitting} className="mt-1 w-full">
        Create account
      </Button>

      <p className="text-center text-sm text-muted-foreground">
        Already have an account?{' '}
        <Link href="/login" className="font-semibold text-primary transition hover:opacity-90">
          Sign in
        </Link>
      </p>
    </form>
  )
}
