import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { SignUpForm } from '../components/SignUpForm';

// Mock the useAuth hook
vi.mock('../context/AuthContext', () => ({
  useAuth: () => ({
    register: vi.fn().mockResolvedValue(undefined),
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

describe('SignUpForm Component', () => {
  const mockOnSwitchToSignIn = vi.fn();

  beforeEach(() => {
    mockOnSwitchToSignIn.mockClear();
  });

  it('renders correctly', () => {
    render(<SignUpForm onSwitchToSignIn={mockOnSwitchToSignIn} />);

    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/confirm password/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /sign up/i })).toBeInTheDocument();
  });

  it('validates email format', async () => {
    render(<SignUpForm onSwitchToSignIn={mockOnSwitchToSignIn} />);

    fireEvent.change(screen.getByLabelText(/email/i), { target: { value: 'invalid-email' } });
    fireEvent.change(screen.getByLabelText(/password/i), { target: { value: 'ValidPass1!' } });
    fireEvent.change(screen.getByLabelText(/confirm password/i), { target: { value: 'ValidPass1!' } });
    fireEvent.click(screen.getByRole('button', { name: /sign up/i }));

    await waitFor(() => {
      expect(screen.getByText(/email address is invalid/i)).toBeInTheDocument();
    });
  });

  it('validates password requirements', async () => {
    render(<SignUpForm onSwitchToSignIn={mockOnSwitchToSignIn} />);

    fireEvent.change(screen.getByLabelText(/email/i), { target: { value: 'test@example.com' } });
    fireEvent.change(screen.getByLabelText(/password/i), { target: { value: 'weak' } }); // Doesn't meet requirements
    fireEvent.change(screen.getByLabelText(/confirm password/i), { target: { value: 'weak' } });
    fireEvent.click(screen.getByRole('button', { name: /sign up/i }));

    await waitFor(() => {
      expect(screen.getByText(/password must be at least 8 characters/i)).toBeInTheDocument();
    });
  });

  it('validates password match', async () => {
    render(<SignUpForm onSwitchToSignIn={mockOnSwitchToSignIn} />);

    fireEvent.change(screen.getByLabelText(/email/i), { target: { value: 'test@example.com' } });
    fireEvent.change(screen.getByLabelText(/password/i), { target: { value: 'ValidPass1!' } });
    fireEvent.change(screen.getByLabelText(/confirm password/i), { target: { value: 'differentPass1!' } });
    fireEvent.click(screen.getByRole('button', { name: /sign up/i }));

    await waitFor(() => {
      expect(screen.getByText(/passwords do not match/i)).toBeInTheDocument();
    });
  });

  it('calls onSwitchToSignIn when sign in link is clicked', () => {
    render(<SignUpForm onSwitchToSignIn={mockOnSwitchToSignIn} />);

    fireEvent.click(screen.getByText(/sign in/i));
    expect(mockOnSwitchToSignIn).toHaveBeenCalled();
  });
});