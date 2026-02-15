// Task: T012 | TanStack Query client with global error handler for 401 and 403
import { QueryCache, QueryClient } from '@tanstack/react-query'
import { toast } from 'sonner'
import { ApiError } from './api-client'

function createQueryClient() {
  return new QueryClient({
    queryCache: new QueryCache({
      onError: (error) => {
        if (error instanceof ApiError) {
          if (error.status === 401 || error.code === 'SESSION_EXPIRED') {
            // Session expired — redirect to login with reason
            if (typeof window !== 'undefined') {
              window.location.href = '/login?reason=session_expired'
            }
          } else if (error.status === 403) {
            toast.error("You don't have permission to perform this action.", { duration: 5000 })
            if (typeof window !== 'undefined') {
              window.location.href = '/dashboard'
            }
          }
        }
      },
    }),
    defaultOptions: {
      queries: {
        staleTime: 0,
        retry: false,
      },
    },
  })
}

// Singleton for client-side; fresh instance for server
let clientQueryClient: QueryClient | undefined

export function getQueryClient() {
  if (typeof window === 'undefined') {
    return createQueryClient()
  }
  if (!clientQueryClient) {
    clientQueryClient = createQueryClient()
  }
  return clientQueryClient
}
