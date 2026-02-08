'use client';

import { SignUpForm } from '@/components/SignUpForm';
import { AuthGuard } from '@/components/AuthGuard';
import { useRouter } from 'next/navigation';

export default function SignUpPage() {
  const router = useRouter();
  
  return (
    <AuthGuard requireAuth={false}>
      <div className="container mx-auto py-10 flex items-center justify-center">
        <SignUpForm onSwitchToSignIn={() => router.push('/auth/signin')} />
      </div>
    </AuthGuard>
  );
}