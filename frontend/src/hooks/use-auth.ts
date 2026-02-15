'use client'
// Task: T017 | useAuth hook — login, register, logout with routing

import { useRouter } from 'next/navigation'
import { apiClient, ApiError } from '@/lib/api-client'
import { getQueryClient } from '@/lib/query-client'
import type { AuthRequest, TokenResponse } from '@/types'

export function useAuth() {
  const router = useRouter()

  async function login(data: AuthRequest): Promise<void> {
    await apiClient.post<TokenResponse>('/api/auth/login', data)
    router.push('/dashboard')
    router.refresh()
  }

  async function register(data: AuthRequest): Promise<void> {
    await apiClient.post<TokenResponse>('/api/auth/register', data)
    router.push('/dashboard')
    router.refresh()
  }

  async function logout(): Promise<void> {
    try {
      await apiClient.post('/api/auth/logout')
    } catch (err) {
      if (!(err instanceof ApiError)) throw err
      // Proceed with logout even if the server call fails
    }
    getQueryClient().clear()
    router.push('/login')
    router.refresh()
  }

  return { login, register, logout }
}
