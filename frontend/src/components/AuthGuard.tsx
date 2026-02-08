'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/context/AuthContext';

type AuthGuardProps = {
  children: React.ReactNode;
  requireAuth?: boolean; // If true, requires authentication; if false, redirects away if authenticated
};

export function AuthGuard({ children, requireAuth = true }: AuthGuardProps) {
  const { loading, token } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading) {
      // If authentication is required but user is not authenticated
      if (requireAuth && !token) {
        router.push('/auth/signin');
      }
      // If authentication is NOT required but user IS authenticated (e.g., for login/signup pages)
      else if (!requireAuth && token) {
        router.push('/dashboard');
      }
    }
  }, [token, loading, requireAuth, router]);

  // Show loading state while checking auth status
  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900"></div>
      </div>
    );
  }

  // If the user is authenticated and auth is required OR user is not authenticated and auth is not required
  if ((requireAuth && token) || (!requireAuth && !token)) {
    return <>{children}</>;
  }

  // Otherwise, don't render anything while redirecting
  return null;
}