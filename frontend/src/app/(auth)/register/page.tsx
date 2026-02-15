// Task: T022 | Register page — renders RegisterForm
import { RegisterForm } from '@/components/auth/RegisterForm'

export const metadata = { title: 'Create Account — Todo App' }

export default function RegisterPage() {
  return (
    <>
      <h1 className="mb-6 text-2xl font-bold text-foreground">Create an account</h1>
      <RegisterForm />
    </>
  )
}
