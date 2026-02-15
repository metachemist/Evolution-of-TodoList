'use client'
// Task: T023 | UserProvider — exposes authenticated user via React Context

import { createContext, useContext } from 'react'
import type { User } from '@/types'

const UserContext = createContext<User | null>(null)

export function UserProvider({
  user,
  children,
}: {
  user: User
  children: React.ReactNode
}) {
  return <UserContext.Provider value={user}>{children}</UserContext.Provider>
}

export function useUser(): User {
  const ctx = useContext(UserContext)
  if (!ctx) throw new Error('useUser must be used inside UserProvider')
  return ctx
}
