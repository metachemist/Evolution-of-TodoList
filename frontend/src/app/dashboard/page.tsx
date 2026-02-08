'use client';

import { useAuth } from '@/context/AuthContext';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { TaskList } from '@/components/TaskList';
import { AuthGuard } from '@/components/AuthGuard';

export default function DashboardPage() {
  const { user, logout } = useAuth();

  const handleLogout = () => {
    logout();
  };

  return (
    <AuthGuard requireAuth={true}>
      <div className="container min-h-screen bg-slate-50 flex flex-col">
        <div className="flex justify-between items-center mb-6">
          <div>
            <h1 className="text-3xl font-bold">Dashboard</h1>
            <p className="text-muted-foreground">Welcome back, {user?.email || 'User'}!</p>
          </div>
          <Button onClick={handleLogout} variant="outline">
            Logout
          </Button>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Your Tasks</CardTitle>
            <CardDescription>Manage your tasks efficiently</CardDescription>
          </CardHeader>
          <CardContent>
            <TaskList />
          </CardContent>
        </Card>
      </div>
    </AuthGuard>
  );
}