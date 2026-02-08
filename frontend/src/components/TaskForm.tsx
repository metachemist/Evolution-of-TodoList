'use client';

import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import Notification from './Notification';

type TaskFormProps = {
  task?: {
    id: number;
    title: string;
    description: string;
  } | null;
  onSubmit: (title: string, description: string) => Promise<void>;
  onCancel: () => void;
};

export function TaskForm({ task, onSubmit, onCancel }: TaskFormProps) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [errors, setErrors] = useState<{ title?: string; description?: string }>({});
  const [loading, setLoading] = useState(false);
  const [notification, setNotification] = useState<{message: string, type: 'success' | 'error' | 'info' | 'warning'} | null>(null);

  // Populate form with task data when editing
  useEffect(() => {
    if (task) {
      setTitle(task.title);
      setDescription(task.description);
    } else {
      setTitle('');
      setDescription('');
    }
  }, [task]);

  const validateForm = () => {
    const newErrors: { title?: string; description?: string } = {};

    if (!title.trim()) {
      newErrors.title = 'Title is required';
    } else if (title.length > 200) {
      newErrors.title = 'Title must be 200 characters or less';
    }

    if (description && description.length > 1000) {
      newErrors.description = 'Description must be 1000 characters or less';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validateForm()) return;

    setLoading(true);
    try {
      if (task) {
        // Update existing task
        await onSubmit(title, description);
        setNotification({ message: 'Task updated successfully!', type: 'success' });
      } else {
        // Create new task (ID will be assigned by backend)
        await onSubmit(title, description);
        setNotification({ message: 'Task created successfully!', type: 'success' });
      }
    } catch (error: any) {
      console.error('Error submitting task:', error);
      setNotification({ message: error.message || 'Error submitting task', type: 'error' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <form onSubmit={handleSubmit} className="mb-6 p-4 border rounded-lg bg-muted">
        <div className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="title">Title *</Label>
            <Input
              id="title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Task title"
              className={errors.title ? 'border-red-500' : ''}
            />
            {errors.title && <p className="text-sm text-red-500">{errors.title}</p>}
          </div>

          <div className="space-y-2">
            <Label htmlFor="description">Description</Label>
            <Textarea
              id="description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Task description (optional)"
              className={errors.description ? 'border-red-500' : ''}
            />
            {errors.description && <p className="text-sm text-red-500">{errors.description}</p>}
          </div>

          <div className="flex space-x-2 pt-2">
            <Button type="submit" disabled={loading}>
              {loading ? (task ? 'Updating...' : 'Creating...') : task ? 'Update Task' : 'Create Task'}
            </Button>
            <Button type="button" variant="outline" onClick={onCancel}>
              Cancel
            </Button>
          </div>
        </div>
      </form>
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