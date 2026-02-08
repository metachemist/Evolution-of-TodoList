'use client';

import { redirect } from 'next/navigation';

export default function AuthPage() {
  // Redirect to sign in page
  redirect('/auth/signin');
}