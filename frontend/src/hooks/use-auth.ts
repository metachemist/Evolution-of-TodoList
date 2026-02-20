'use client'
// Task: T017 | useAuth hook — login, register, logout with routing

import { useRouter } from 'next/navigation'
import { apiClient, ApiError } from '@/lib/api-client'
import { getQueryClient } from '@/lib/query-client'
import { clearPersistedAccessToken, persistAccessToken } from '@/lib/session-token'
import type { AuthRequest, TokenResponse } from '@/types'

export function useAuth() {
  const router = useRouter()

  async function login(data: AuthRequest): Promise<void> {
    const tokenData = await apiClient.post<TokenResponse>('/api/auth/login', data)
    persistAccessToken(tokenData.access_token)
    router.push('/dashboard')
    router.refresh()
  }

  async function register(data: AuthRequest): Promise<void> {
    const tokenData = await apiClient.post<TokenResponse>('/api/auth/register', data)
    persistAccessToken(tokenData.access_token)
    router.push('/dashboard')
    router.refresh()
  }

  async function logout(): Promise<void> {
    clearPersistedAccessToken()
    try {
      await apiClient.post('/api/auth/logout')
    } catch (err) {
      if (!(err instanceof ApiError)) throw err
      // Proceed with logout even if the server call fails
    }
    getQueryClient().clear()
    router.push('/')
    router.refresh()
  }

  return { login, register, logout }
}
