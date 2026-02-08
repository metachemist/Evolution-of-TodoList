'use client';

import { SignInForm } from '@/components/SignInForm';
import { AuthGuard } from '@/components/AuthGuard';
import { useRouter } from 'next/navigation';

export default function SignInPage() {
  const router = useRouter();
  
  return (
    <AuthGuard requireAuth={false}>
      <div className="container mx-auto py-10 flex items-center justify-center">
        <SignInForm onSwitchToSignUp={() => router.push('/auth/signup')} />
      </div>
    </AuthGuard>
  );
}