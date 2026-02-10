'use client';

import { useState, useEffect } from 'react';
import { TaskItem } from './TaskItem';
import { TaskForm } from './TaskForm';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { useAuth } from '@/context/AuthContext';
import { describe } from 'node:test';
// import Notification from './Notification'; // Uncomment if you have this component
// import ErrorBoundary from './ErrorBoundary'; // Uncomment if you have this component

// Define the Task type
type Task = {
  id: number;
  user_id: number;
  title: string;
  description: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
};

export function TaskList() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const { token, userId } = useAuth(); // Get userId from auth context

  // Helper to get the correct Backend URL
  const getApiUrl = (endpoint: string = '') => {
    if (!userId) return '';
    return `${process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000'}/api/${userId}${endpoint}`;
  };

  // Fetch tasks from the backend
  useEffect(() => {
    const fetchTasks = async () => {
      if (!token || !userId) return;

      try {
        setLoading(true);
        const response = await fetch(getApiUrl('/tasks'), {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });

        if (!response.ok) {
          throw new Error(`Error: ${response.status}`);
        }

        const data = await response.json();
        // Handle different response structures (list vs dict)
        setTasks(Array.isArray(data) ? data : data.data || []);
      } catch (err: any) {
        setError(err.message || 'Failed to fetch tasks');
        console.error('Error fetching tasks:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchTasks();
  }, [token, userId]);

  // Handle creating a new task
  const handleCreateTask = async (title: string, description: string) => {
    if (!token || !userId) return;
    
    const url = getApiUrl('/tasks');
    if (!url) return;

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ title, description }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to create task');
      }

      const newTask = await response.json();
      setTasks([newTask, ...tasks]); // Add new task to top
      setShowForm(false);
    } catch (err: any) {
      console.error('Error creating task:', err);
      alert(err.message);
    }
  };

  // Handle updating a task
  const handleUpdateTask = async (id: number, title: string, description: string) => {
    if (!token || !userId) return;

    const url = getApiUrl(`/tasks/${id}`);
    if (!url) return;

    try {
      const response = await fetch(url, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ title, description }),
      });

      if (!response.ok) {
        throw new Error('Failed to update task');
      }

      const updatedTask = await response.json();
      setTasks(tasks.map(task => task.id === id ? updatedTask : task));
      setEditingTask(null);
      setShowForm(false);
    } catch (err: any) {
      console.error('Error updating task:', err);
      alert(err.message);
    }
  };

  // Handle deleting a task
  const handleDeleteTask = async (id: number) => {
    if (!token || !userId) return;

    const url = getApiUrl(`/tasks/${id}`);
    if (!url) return;

    try {
      const response = await fetch(url, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error('Failed to delete task');
      }

      setTasks(tasks.filter(task => task.id !== id));
    } catch (err: any) {
      console.error('Error deleting task:', err);
      alert(err.message);
    }
  };

  // Handle toggling task completion
  const handleToggleCompletion = async (id: number) => {
    if (!token || !userId) return;
    const task = tasks.find(t => t.id === id);
    if (!task) return;

    const url = getApiUrl(`/tasks/${id}/complete`);
    if (!url) return;

    try {
      const response = await fetch(url, {
        method: 'PATCH', // Using PATCH as defined in backend
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ completed: !task.completed }),
      });

      if (!response.ok) {
        throw new Error('Failed to update task');
      }

      const updatedTask = await response.json();
      setTasks(tasks.map(t => t.id === id ? updatedTask : t));
    } catch (err: any) {
      console.error('Error toggling task:', err);
    }
  };

  if (loading) return <div className="p-4 text-center">Loading tasks...</div>;
  if (error) return <div className="p-4 text-red-500">Error: {error}</div>;

  return (
    <Card className="w-full max-w-2xl mx-auto mt-8">
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle>My Tasks</CardTitle>
        <Button onClick={() => { setShowForm(!showForm); setEditingTask(null); }}>
          {showForm ? 'Cancel' : 'Add Task'}
        </Button>
      </CardHeader>
      <CardContent>
        {showForm && (
          <div className="mb-6">
            <TaskForm 
              task={editingTask} 
              onSubmit={(title, description) => {
                  if (editingTask) {
                    // EDIT MODE: We inject the ID here manually
                    return handleUpdateTask(editingTask.id, title, description);
                  } else {
                    // CREATE MODE: Just pass the data
                    return handleCreateTask(title, description);
                  }
                }}
              onCancel={() => setShowForm(false)}
            />
          </div>
        )}
        <div className="space-y-2">
          {tasks.length === 0 ? (
            <p className="text-gray-500 text-center">No tasks found.</p>
          ) : (
            tasks.map(task => (
              <TaskItem 
                key={task.id} 
                task={task} 
                onEdit={() => { setEditingTask(task); setShowForm(true); }}
                onDelete={() => handleDeleteTask(task.id)}
                onToggleCompletion={() => handleToggleCompletion(task.id)}
              />
            ))
          )}
        </div>
      </CardContent>
    </Card>
  );
}