'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { useAuth } from '@/context/AuthContext';
import Notification from './Notification';

type SignInFormProps = {
  onSwitchToSignUp: () => void;
};

export function SignInForm({ onSwitchToSignUp }: SignInFormProps) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errors, setErrors] = useState<{ email?: string; password?: string; general?: string }>({});
  const [loading, setLoading] = useState(false);
  const [notification, setNotification] = useState<{message: string, type: 'success' | 'error' | 'info' | 'warning'} | null>(null);
  const router = useRouter();
  const { login } = useAuth();

  const validateForm = () => {
    const newErrors: { email?: string; password?: string; general?: string } = {};

    // Email validation
    if (!email) {
      newErrors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(email)) {
      newErrors.email = 'Email address is invalid';
    }

    // Password validation
    if (!password) {
      newErrors.password = 'Password is required';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validateForm()) return;

    setLoading(true);
    try {
      await login(email, password);
      // Redirect to dashboard or home page after successful login
      router.push('/dashboard');
      setNotification({ message: 'Login successful!', type: 'success' });
    } catch (error: any) {
      console.error('Login error:', error);
      setErrors({ 
        ...errors, 
        general: error.message || 'Login failed. Please check your credentials.' 
      });
      setNotification({ message: error.message || 'Login failed. Please check your credentials.', type: 'error' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Card className="w-full max-w-md mx-auto">
        <CardHeader>
          <CardTitle>Sign In</CardTitle>
          <CardDescription>Welcome back! Please sign in to continue</CardDescription>
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
              <div className="rounded-md bg-destructive/15 p-4">
                <p className="text-sm text-destructive">{errors.general}</p>
              </div>
            )}
          </CardContent>
          <CardFooter className="flex flex-col">
            <Button type="submit" className="w-full" disabled={loading}>
              {loading ? 'Signing In...' : 'Sign In'}
            </Button>
            <p className="mt-4 text-sm text-muted-foreground">
              Don't have an account?{' '}
              <button
                type="button"
                onClick={onSwitchToSignUp}
                className="text-primary underline-offset-4 hover:underline"
              >
                Sign Up
              </button>
            </p>
          </CardFooter>
        </form>
      </Card>
      {notification && (
        <Notification 
          message={notification.message} 
          type={notification.type} 
          onClose={() => setNotification(null)} 
        />
      )}
    </>
  );
}