// Task: T021 | Login page — renders LoginForm with session expiry message support
import { Suspense } from 'react'
import { LoginForm } from '@/components/auth/LoginForm'

export const metadata = { title: 'Sign In — Todo App' }

export default function LoginPage() {
  return (
    <>
      <h1 className="mb-6 text-2xl font-bold text-foreground">Sign in to your account</h1>
      <Suspense>
        <LoginForm />
      </Suspense>
    </>
  )
}
