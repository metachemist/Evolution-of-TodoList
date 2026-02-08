'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';

// Define the shape of our authentication context
interface AuthContextType {
  user: any | null;
  token: string | null;
  userId: string | number | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  register: (email: string, password: string) => Promise<void>;
}

// Create the authentication context
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Custom hook to use the auth context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

// Define props for the AuthProvider component
interface AuthProviderProps {
  children: ReactNode;
}

// AuthProvider component
export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<any | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [userId, setUserId] = useState<string | number | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  // Check for existing token on initial load
  useEffect(() => {
    const storedToken = localStorage.getItem('token');
    if (storedToken) {
      setToken(storedToken);
      // In a real app, you would decode the token or make an API call to validate it
      // For now, we'll just set a dummy user object
      try {
        const decodedToken = JSON.parse(atob(storedToken.split('.')[1]));
        setUser(decodedToken);
        // Extract user ID from token
        const extractedUserId = decodedToken.user_id || decodedToken.sub || null;
        setUserId(extractedUserId);
      } catch (error) {
        console.error('Error decoding token:', error);
        localStorage.removeItem('token');
      }
    }
    setLoading(false);
  }, []);

  // Login function
  const login = async (email: string, password: string) => {
    setLoading(true);
    try {
      // Call the backend login API
      let response;
      try {
        response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000'}/api/v1/auth/login`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ email, password }),
        });
      } catch (networkError) {
        console.error('Network error during login:', networkError);
        throw new Error('Network error: Could not connect to the server. Please make sure the backend is running.');
      }

      const data = await response.json();
      
      if (!response.ok) {
        // Handle error response - could be in different formats
        let errorMessage = 'Login failed';
        
        if (data.detail) {
          errorMessage = data.detail;
        } else if (data.message) {
          errorMessage = data.message;
        } else if (typeof data === 'string') {
          errorMessage = data;
        }
        
        throw new Error(errorMessage);
      }
      
      // Check if the response has the expected structure
      if (!data.data || !data.data.token) {
        throw new Error('Invalid response format from server');
      }

      // Store the token in localStorage
      const jwtToken = data.data.token;
      localStorage.setItem('token', jwtToken);
      setToken(jwtToken);

      // Set user data (with fallback to prevent errors)
      const userData = data.data.user || {};
      setUser(userData);

      // Extract and store user ID from the token
      try {
        const tokenParts = jwtToken.split('.');
        const payload = JSON.parse(atob(tokenParts[1]));
        const extractedUserId = payload.user_id || payload.sub || userData.id || null;
        setUserId(extractedUserId);
      } catch (decodeError) {
        console.error('Error decoding token to extract user ID:', decodeError);
        // Fallback to user ID from response if token decode fails
        setUserId(userData.id || null);
      }
    } catch (error: any) {
      console.error('Login error:', error);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  // Logout function
  const logout = () => {
    // Remove token from localStorage
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);
  };


  // Register function
  const register = async (email: string, password: string) => {
    setLoading(true);
    try {
      // Call the backend register API
      let response;
      try {
        response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000'}/api/v1/auth/register`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ email, password }),
        });
      } catch (networkError) {
        console.error('Network error during registration:', networkError);
        throw new Error('Network error: Could not connect to the server. Please make sure the backend is running.');
      }

      const data = await response.json();
      
      if (!response.ok) {
        // Handle error response - could be in different formats
        let errorMessage = 'Registration failed';
        
        if (data.detail) {
          errorMessage = data.detail;
        } else if (data.message) {
          errorMessage = data.message;
        } else if (typeof data === 'string') {
          errorMessage = data;
        }
        
        throw new Error(errorMessage);
      }
      
      // Check if the response has the expected structure
      if (!data.data || !data.data.token) {
        throw new Error('Invalid response format from server');
      }

      // Store the token in localStorage
      const jwtToken = data.data.token;
      localStorage.setItem('token', jwtToken);
      setToken(jwtToken);

      // Set user data (with fallback to prevent errors)
      const userData = data.data.user || {};
      setUser(userData);

      // Extract and store user ID from the token
      try {
        const tokenParts = jwtToken.split('.');
        const payload = JSON.parse(atob(tokenParts[1]));
        const extractedUserId = payload.user_id || payload.sub || userData.id || null;
        setUserId(extractedUserId);
      } catch (decodeError) {
        console.error('Error decoding token to extract user ID:', decodeError);
        // Fallback to user ID from response if token decode fails
        setUserId(userData.id || null);
      }
    } catch (error: any) {
      console.error('Registration error:', error);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  // Value to provide to consumers
  const value = {
    user,
    token,
    userId,
    loading,
    login,
    logout,
    register,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};