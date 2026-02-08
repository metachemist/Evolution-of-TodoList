import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { TaskItem } from '../components/TaskItem';

describe('TaskItem Component', () => {
  const mockTask = {
    id: 1,
    title: 'Test Task',
    description: 'Test Description',
    completed: false,
  };

  const mockOnEdit = vi.fn();
  const mockOnDelete = vi.fn();
  const mockOnToggleCompletion = vi.fn();

  beforeEach(() => {
    mockOnEdit.mockClear();
    mockOnDelete.mockClear();
    mockOnToggleCompletion.mockClear();
  });

  it('renders task details correctly', () => {
    render(
      <TaskItem
        task={mockTask}
        onEdit={mockOnEdit}
        onDelete={mockOnDelete}
        onToggleCompletion={mockOnToggleCompletion}
      />
    );

    expect(screen.getByText('Test Task')).toBeInTheDocument();
    expect(screen.getByText('Test Description')).toBeInTheDocument();
    expect(screen.getByRole('checkbox')).toBeInTheDocument();
  });

  it('calls onToggleCompletion when checkbox is clicked', () => {
    render(
      <TaskItem
        task={mockTask}
        onEdit={mockOnEdit}
        onDelete={mockOnDelete}
        onToggleCompletion={mockOnToggleCompletion}
      />
    );

    fireEvent.click(screen.getByRole('checkbox'));
    expect(mockOnToggleCompletion).toHaveBeenCalledWith(1);
  });

  it('calls onEdit when edit button is clicked', () => {
    render(
      <TaskItem
        task={mockTask}
        onEdit={mockOnEdit}
        onDelete={mockOnDelete}
        onToggleCompletion={mockOnToggleCompletion}
      />
    );

    fireEvent.click(screen.getByRole('button', { name: /edit/i }));
    expect(mockOnEdit).toHaveBeenCalledWith(1);
  });

  it('calls onDelete when delete button is clicked', () => {
    render(
      <TaskItem
        task={mockTask}
        onEdit={mockOnEdit}
        onDelete={mockOnDelete}
        onToggleCompletion={mockOnToggleCompletion}
      />
    );

    fireEvent.click(screen.getByRole('button', { name: /delete/i }));
    expect(mockOnDelete).toHaveBeenCalledWith(1);
  });

  it('displays strikethrough for completed tasks', () => {
    const completedTask = { ...mockTask, completed: true };
    
    render(
      <TaskItem
        task={completedTask}
        onEdit={mockOnEdit}
        onDelete={mockOnDelete}
        onToggleCompletion={mockOnToggleCompletion}
      />
    );

    expect(screen.getByText('Test Task')).toHaveClass('line-through');
  });
});