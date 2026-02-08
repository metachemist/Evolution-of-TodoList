'use client';

import { Checkbox } from '@/components/ui/checkbox';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';

type TaskItemProps = {
  task: {
    id: number;
    title: string;
    description: string;
    completed: boolean;
  };
  onEdit: (id: number) => void;
  onDelete: (id: number) => void;
  onToggleCompletion: (id: number) => void;
};

export function TaskItem({ task, onEdit, onDelete, onToggleCompletion }: TaskItemProps) {
  return (
    <div className="flex items-start space-x-2 p-3 border rounded hover:bg-gray-50 transition-colors">
      <Checkbox
        id={`task-${task.id}`}
        checked={task.completed}
        onCheckedChange={() => onToggleCompletion(task.id)}
        className="mt-0.5"
      />
      <div className="grow">
        <Label
          htmlFor={`task-${task.id}`}
          className={`${task.completed ? 'line-through text-gray-500' : ''} cursor-pointer block font-medium`}
        >
          {task.title}
        </Label>
        {task.description && (
          <p className={`text-sm mt-1 ${task.completed ? 'text-gray-400' : 'text-gray-600'}`}>
            {task.description}
          </p>
        )}
      </div>
      <div className="flex space-x-1">
        <Button
          variant="outline"
          size="sm"
          onClick={() => onEdit(task.id)}
        >
          Edit
        </Button>
        <Button
          variant="destructive"
          size="sm"
          onClick={() => onDelete(task.id)}
        >
          Delete
        </Button>
      </div>
    </div>
  );
}