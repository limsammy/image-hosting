import { createContext, useContext, useState, useEffect, type ReactNode } from 'react';
import { authApi, type User, type LoginRequest, type RegisterRequest } from '../api/auth';

interface AuthContextType {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (credentials: LoginRequest) => Promise<void>;
  register: (data: RegisterRequest) => Promise<void>;
  logout: () => void;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Initialize auth state from localStorage
  useEffect(() => {
    const initAuth = async () => {
      const storedToken = localStorage.getItem('auth_token');
      const storedUser = localStorage.getItem('auth_user');

      if (storedToken && storedUser) {
        setToken(storedToken);
        try {
          // Verify token is still valid by fetching current user
          const currentUser = await authApi.getCurrentUser();
          setUser(currentUser);
          // Update stored user in case data changed
          localStorage.setItem('auth_user', JSON.stringify(currentUser));
        } catch (error) {
          // Token invalid or expired, clear storage
          console.error('Token validation failed:', error);
          localStorage.removeItem('auth_token');
          localStorage.removeItem('auth_user');
          setToken(null);
          setUser(null);
        }
      }

      setIsLoading(false);
    };

    initAuth();
  }, []);

  const login = async (credentials: LoginRequest) => {
    try {
      const response = await authApi.login(credentials);
      const authToken = response.access_token;

      // Store token
      localStorage.setItem('auth_token', authToken);
      setToken(authToken);

      // Fetch user profile
      const currentUser = await authApi.getCurrentUser();
      setUser(currentUser);
      localStorage.setItem('auth_user', JSON.stringify(currentUser));
    } catch (error) {
      console.error('Login failed:', error);
      throw error;
    }
  };

  const register = async (data: RegisterRequest) => {
    try {
      const response = await authApi.register(data);
      const authToken = response.access_token;

      // Store token
      localStorage.setItem('auth_token', authToken);
      setToken(authToken);

      // Fetch user profile
      const currentUser = await authApi.getCurrentUser();
      setUser(currentUser);
      localStorage.setItem('auth_user', JSON.stringify(currentUser));
    } catch (error) {
      console.error('Registration failed:', error);
      throw error;
    }
  };

  const logout = () => {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('auth_user');
    setToken(null);
    setUser(null);
  };

  const refreshUser = async () => {
    if (!token) return;

    try {
      const currentUser = await authApi.getCurrentUser();
      setUser(currentUser);
      localStorage.setItem('auth_user', JSON.stringify(currentUser));
    } catch (error) {
      console.error('Failed to refresh user:', error);
      // If refresh fails, user might need to re-login
      logout();
    }
  };

  const value: AuthContextType = {
    user,
    token,
    isAuthenticated: !!token && !!user,
    isLoading,
    login,
    register,
    logout,
    refreshUser,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

// Custom hook to use auth context
export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
