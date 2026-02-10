'use client';
import { useRouter } from 'next/navigation';
import { SignInForm } from '@/components/SignInForm'; // Check your import path
import { AuthGuard }from '@/components/AuthGuard'; // Check your import path

export default function SignInPage() {
  const router = useRouter();

  return (
    // Only the background color and centering logic remains here.
    <div className="min-h-screen w-full flex items-center justify-center bg-stone-100">
      <AuthGuard requireAuth={false}>
        <SignInForm onSwitchToSignUp={() => router.push('/auth/signup')} />
      </AuthGuard>
    </div>
  );
}