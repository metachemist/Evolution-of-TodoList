import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { SignInForm } from '../components/SignInForm';

// Mock the useAuth hook
vi.mock('../context/AuthContext', () => ({
  useAuth: () => ({
    login: vi.fn().mockResolvedValue(undefined),
    token: null,
    user: null
  })
}));

// Mock next/router
vi.mock('next/navigation', () => ({
  useRouter: () => ({
    push: vi.fn()
  })
}));

describe('SignInForm Component', () => {
  const mockOnSwitchToSignUp = vi.fn();

  beforeEach(() => {
    mockOnSwitchToSignUp.mockClear();
  });

  it('renders correctly', () => {
    render(<SignInForm onSwitchToSignUp={mockOnSwitchToSignUp} />);

    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /sign in/i })).toBeInTheDocument();
  });

  it('validates email format', async () => {
    render(<SignInForm onSwitchToSignUp={mockOnSwitchToSignUp} />);

    fireEvent.change(screen.getByLabelText(/email/i), { target: { value: 'invalid-email' } });
    fireEvent.change(screen.getByLabelText(/password/i), { target: { value: 'password123' } });
    fireEvent.click(screen.getByRole('button', { name: /sign in/i }));

    await waitFor(() => {
      expect(screen.getByText(/email address is invalid/i)).toBeInTheDocument();
    });
  });

  it('validates required fields', async () => {
    render(<SignInForm onSwitchToSignUp={mockOnSwitchToSignUp} />);

    fireEvent.click(screen.getByRole('button', { name: /sign in/i }));

    await waitFor(() => {
      expect(screen.getByText(/email is required/i)).toBeInTheDocument();
    });
  });

  it('calls onSwitchToSignUp when sign up link is clicked', () => {
    render(<SignInForm onSwitchToSignUp={mockOnSwitchToSignUp} />);

    fireEvent.click(screen.getByText(/sign up/i));
    expect(mockOnSwitchToSignUp).toHaveBeenCalled();
  });
});