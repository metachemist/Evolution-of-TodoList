'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { useAuth } from '@/context/AuthContext';
// import Notification from './Notification'; // Uncomment if you are using this

type SignInFormProps = {
  onSwitchToSignUp: () => void;
};

export function SignInForm({ onSwitchToSignUp }: SignInFormProps) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errors, setErrors] = useState<{ email?: string; password?: string; general?: string }>({});
  const [loading, setLoading] = useState(false);
  const router = useRouter();
  const { login } = useAuth();

  const validateForm = () => {
    const newErrors: { email?: string; password?: string; general?: string } = {};
    if (!email) newErrors.email = 'Email is required';
    if (!password) newErrors.password = 'Password is required';
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validateForm()) return;

    setLoading(true); // START LOADING: This triggers the spinner view
    try {
      await login(email, password);
      router.push('/dashboard');
    } catch (error: any) {
      console.error('Login error:', error);
      setErrors({ ...errors, general: error.message || 'Login failed.' });
      setLoading(false); // Stop loading on error so they can try again
    }
  };

  // 1. LOADING STATE: If loading, show ONLY the spinner (No text, no form)
  if (loading) {
    return (
      <div className="flex justify-center items-center h-100 w-full max-w-md mx-auto bg-white rounded-lg shadow-lg">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    );
  }

  // 2. NORMAL STATE: Show Text + Form
  return (
    <div className="w-full max-w-md mx-auto">
        
      {/* MOVED TEXT HERE: This is now part of the component */}
      <div className="flex flex-col gap-2 mb-6 text-center">
        <span className="text-2xl font-bold">Welcome to Todo App</span>
        <span className="text-sm text-muted-foreground">Please sign in to continue</span>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Sign In</CardTitle>
          <CardDescription>Enter your credentials below</CardDescription>
        </CardHeader>
        <form onSubmit={handleSubmit}>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                placeholder="name@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className={errors.email ? 'border-red-500' : ''}
              />
              {errors.email && <p className="text-sm text-red-500">{errors.email}</p>}
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="password">Password</Label>
              <Input
                id="password"
                type="password"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className={errors.password ? 'border-red-500' : ''}
              />
              {errors.password && <p className="text-sm text-red-500">{errors.password}</p>}
            </div>
            
            {errors.general && (
              <div className="p-3 text-sm text-red-500 bg-red-50 rounded-md">
                {errors.general}
              </div>
            )}
          </CardContent>
          <CardFooter className="flex flex-col gap-4">
            <Button type="submit" className="w-full">
              Sign In
            </Button>
            <p className="text-sm text-center text-muted-foreground">
              Don't have an account?{' '}
              <button
                type="button"
                onClick={onSwitchToSignUp}
                className="text-primary hover:underline font-medium"
              >
                Sign Up
              </button>
            </p>
          </CardFooter>
        </form>
      </Card>
    </div>
  );
}