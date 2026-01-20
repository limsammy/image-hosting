import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { BrowserRouter } from 'react-router-dom';
import Register from '../../src/pages/Register';
import { AuthProvider } from '../../src/contexts/AuthContext';

// Mock the auth API
vi.mock('../../src/api/auth', () => ({
  authApi: {
    register: vi.fn(),
    login: vi.fn(),
    getCurrentUser: vi.fn(),
  },
}));

const renderRegister = () => {
  return render(
    <BrowserRouter>
      <AuthProvider>
        <Register />
      </AuthProvider>
    </BrowserRouter>
  );
};

describe('Register Page', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders registration form', () => {
    renderRegister();

    expect(screen.getByRole('heading', { name: /create your account/i })).toBeInTheDocument();
    expect(screen.getByLabelText(/username/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/^email$/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/^password$/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/confirm password/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /create account/i })).toBeInTheDocument();
  });

  it('validates required fields', async () => {
    const user = userEvent.setup();
    renderRegister();

    const submitButton = screen.getByRole('button', { name: /create account/i });
    await user.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/username is required/i)).toBeInTheDocument();
      expect(screen.getByText(/email is required/i)).toBeInTheDocument();
      expect(screen.getByText(/^password is required/i)).toBeInTheDocument();
    });
  });

  it('validates username length', async () => {
    const user = userEvent.setup();
    renderRegister();

    const usernameInput = screen.getByLabelText(/username/i);
    await user.type(usernameInput, 'ab');
    await user.click(screen.getByRole('button', { name: /create account/i }));

    await waitFor(() => {
      expect(screen.getByText(/username must be at least 3 characters/i)).toBeInTheDocument();
    });
  });

  it('validates email format', async () => {
    const user = userEvent.setup();
    renderRegister();

    const usernameInput = screen.getByLabelText(/username/i);
    const emailInput = screen.getByLabelText(/^email$/i);

    // Fill username and invalid email, then submit
    await user.type(usernameInput, 'testuser');
    await user.type(emailInput, 'notanemail');

    // Submit without filling password fields
    await user.click(screen.getByRole('button', { name: /create account/i }));

    // Should show email validation error
    await waitFor(() => {
      expect(screen.getByText(/please enter a valid email address/i)).toBeInTheDocument();
    });
  });

  it('validates password length', async () => {
    const user = userEvent.setup();
    renderRegister();

    const passwordInput = screen.getByLabelText(/^password$/i);
    await user.type(passwordInput, 'short');
    await user.click(screen.getByRole('button', { name: /create account/i }));

    await waitFor(() => {
      expect(screen.getByText(/password must be at least 8 characters/i)).toBeInTheDocument();
    });
  });

  it('validates password confirmation match', async () => {
    const user = userEvent.setup();
    renderRegister();

    const passwordInput = screen.getByLabelText(/^password$/i);
    const confirmPasswordInput = screen.getByLabelText(/confirm password/i);

    await user.type(passwordInput, 'password123');
    await user.type(confirmPasswordInput, 'password456');
    await user.click(screen.getByRole('button', { name: /create account/i }));

    await waitFor(() => {
      expect(screen.getByText(/passwords do not match/i)).toBeInTheDocument();
    });
  });

  it('clears field error when user starts typing', async () => {
    const user = userEvent.setup();
    renderRegister();

    // Trigger validation
    await user.click(screen.getByRole('button', { name: /create account/i }));

    await waitFor(() => {
      expect(screen.getByText(/username is required/i)).toBeInTheDocument();
    });

    // Start typing in username field
    const usernameInput = screen.getByLabelText(/username/i);
    await user.type(usernameInput, 'test');

    // Error should be cleared
    expect(screen.queryByText(/username is required/i)).not.toBeInTheDocument();
  });

  it('disables form during submission', async () => {
    const user = userEvent.setup();
    const { authApi } = await import('../../src/api/auth');

    // Mock register to return a promise that we control
    (authApi.register as any).mockImplementation(
      () => new Promise((resolve) => setTimeout(() => resolve({ access_token: 'test-token' }), 100))
    );
    (authApi.getCurrentUser as any).mockResolvedValue({ id: 1, username: 'testuser', email: 'test@example.com' });

    renderRegister();

    const usernameInput = screen.getByLabelText(/username/i);
    const submitButton = screen.getByRole('button', { name: /create account/i });

    await user.type(usernameInput, 'testuser');
    await user.type(screen.getByLabelText(/^email$/i), 'test@example.com');
    await user.type(screen.getByLabelText(/^password$/i), 'password123');
    await user.type(screen.getByLabelText(/confirm password/i), 'password123');

    await user.click(submitButton);

    // Button text should change and inputs should be disabled
    await waitFor(() => {
      expect(screen.getByText(/creating account.../i)).toBeInTheDocument();
    });
    expect(usernameInput).toBeDisabled();
  });

  it('has link to login page', () => {
    renderRegister();

    const loginLinks = screen.getAllByRole('link', { name: /sign in/i });
    expect(loginLinks.length).toBeGreaterThan(0);
    // Both links should point to /login
    loginLinks.forEach((link) => {
      expect(link).toHaveAttribute('href', '/login');
    });
  });
});
