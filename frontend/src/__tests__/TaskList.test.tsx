import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { TaskList } from '../components/TaskList';

// Mock the useAuth hook
vi.mock('../context/AuthContext', () => ({
  useAuth: () => ({
    token: 'mock-token',
    userId: '1',
    loading: false
  })
}));

// Mock fetch
const mockFetch = vi.fn();
global.fetch = mockFetch;

describe('TaskList Component', () => {
  beforeEach(() => {
    mockFetch.mockClear();
  });

  it('renders loading state initially', async () => {
    // Mock a delayed response to see the loading state
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ data: { tasks: [] } })
    });

    render(<TaskList />);
    
    expect(screen.getByText(/loading/i)).toBeInTheDocument();
  });

  it('fetches and displays tasks', async () => {
    const mockTasks = [
      {
        id: 1,
        user_id: 1,
        title: 'Test Task',
        description: 'Test Description',
        completed: false,
        created_at: '2023-01-01T00:00:00Z',
        updated_at: '2023-01-01T00:00:00Z'
      }
    ];

    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ data: { tasks: mockTasks } })
    });

    render(<TaskList />);

    await waitFor(() => {
      expect(screen.getByText('Test Task')).toBeInTheDocument();
    });
  });

  it('shows error message when fetch fails', async () => {
    mockFetch.mockRejectedValueOnce(new Error('Failed to fetch'));

    render(<TaskList />);

    await waitFor(() => {
      expect(screen.getByText(/error/i)).toBeInTheDocument();
    });
  });
});