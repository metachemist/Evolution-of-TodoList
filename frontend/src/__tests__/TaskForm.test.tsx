import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { TaskForm } from '../components/TaskForm';

describe('TaskForm Component', () => {
  const mockOnSubmit = vi.fn();
  const mockOnCancel = vi.fn();

  beforeEach(() => {
    mockOnSubmit.mockClear();
    mockOnCancel.mockClear();
  });

  it('renders correctly in create mode', () => {
    render(
      <TaskForm 
        onSubmit={mockOnSubmit} 
        onCancel={mockOnCancel} 
      />
    );

    expect(screen.getByLabelText(/title \*/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/description/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /create task/i })).toBeInTheDocument();
  });

  it('renders correctly in edit mode', () => {
    const mockTask = {
      id: 1,
      title: 'Test Task',
      description: 'Test Description'
    };

    render(
      <TaskForm 
        task={mockTask}
        onSubmit={mockOnSubmit} 
        onCancel={mockOnCancel} 
      />
    );

    expect(screen.getByDisplayValue('Test Task')).toBeInTheDocument();
    expect(screen.getByDisplayValue('Test Description')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /update task/i })).toBeInTheDocument();
  });

  it('validates required fields', async () => {
    render(
      <TaskForm 
        onSubmit={mockOnSubmit} 
        onCancel={mockOnCancel} 
      />
    );

    fireEvent.click(screen.getByRole('button', { name: /create task/i }));

    await waitFor(() => {
      expect(screen.getByText(/title is required/i)).toBeInTheDocument();
    });
  });

  it('calls onSubmit with correct values when form is valid', async () => {
    render(
      <TaskForm 
        onSubmit={mockOnSubmit} 
        onCancel={mockOnCancel} 
      />
    );

    fireEvent.change(screen.getByLabelText(/title \*/i), { target: { value: 'New Task' } });
    fireEvent.change(screen.getByLabelText(/description/i), { target: { value: 'New Description' } });
    fireEvent.click(screen.getByRole('button', { name: /create task/i }));

    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalledWith(0, 'New Task', 'New Description');
    });
  });

  it('calls onCancel when cancel button is clicked', () => {
    render(
      <TaskForm 
        onSubmit={mockOnSubmit} 
        onCancel={mockOnCancel} 
      />
    );

    fireEvent.click(screen.getByRole('button', { name: /cancel/i }));
    expect(mockOnCancel).toHaveBeenCalled();
  });
});