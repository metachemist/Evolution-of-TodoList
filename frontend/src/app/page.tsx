// Task: T016 | Root page — redirect based on access_token cookie presence
import { cookies } from 'next/headers'
import { redirect } from 'next/navigation'

export default async function RootPage() {
  const cookieStore = await cookies()
  const hasToken = cookieStore.has('access_token')
  redirect(hasToken ? '/dashboard' : '/login')
}
