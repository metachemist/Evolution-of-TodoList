// Task: T022 | Register page — renders RegisterForm
import { RegisterForm } from '@/components/auth/RegisterForm'
import { BRAND_TITLE } from '@/lib/brand'
import { FadeIn } from '@/components/ui/FadeIn'

export const metadata = { title: BRAND_TITLE }

export default function RegisterPage() {
  return (
    <FadeIn>
      <h1 className="text-heading text-foreground">Create your Focentra account</h1>
      <p className="mt-2 text-body">Designed for deep work.</p>
      <RegisterForm />
    </FadeIn>
  )
}
