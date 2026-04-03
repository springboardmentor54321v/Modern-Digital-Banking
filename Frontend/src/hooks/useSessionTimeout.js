import { useEffect, useRef, useCallback } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

/**
 * Custom hook to handle automatic session timeout
 * Logs out user after 1 hour of inactivity
 * Resets timer on user activity (mouse, keyboard, clicks)
 */
export const useSessionTimeout = (timeoutMinutes = 60) => {
  const { logoutUser, isLoggedIn } = useAuth();
  const navigate = useNavigate();
  const timeoutRef = useRef(null);
  const warningTimeoutRef = useRef(null);
  const isCleaningUp = useRef(false);

  // Convert minutes to milliseconds
  const INACTIVITY_TIMEOUT = 60 * 60 * 1000;
  const WARNING_TIME = 5 * 60 * 1000; // Show warning 5 minutes before logout

  const resetTimeout = useCallback(() => {
    // Clear existing timeouts
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }
    if (warningTimeoutRef.current) {
      clearTimeout(warningTimeoutRef.current);
    }

    // Only set new timeout if user is logged in
    if (!isLoggedIn) {
      return;
    }

    // Set warning timeout (30 seconds before logout)
    warningTimeoutRef.current = setTimeout(() => {
      if (isLoggedIn) {
        // You can dispatch a showWarning action here if you want UI feedback
        console.warn('Session will expire soon due to inactivity');
      }
    }, INACTIVITY_TIMEOUT - WARNING_TIME);

    // Set actual logout timeout
    timeoutRef.current = setTimeout(() => {
      if (isCleaningUp.current) return; // Prevent double execution
      isCleaningUp.current = true;

      console.log('Session expired due to inactivity');
      logoutUser();
      navigate('/login', {
        state: { message: 'Your session has expired due to inactivity. Please login again.' }
      });

      isCleaningUp.current = false;
    }, INACTIVITY_TIMEOUT);
  }, [isLoggedIn, logoutUser, navigate, INACTIVITY_TIMEOUT, WARNING_TIME]);

  // Set up activity listeners
  useEffect(() => {
    if (!isLoggedIn) {
      // Clean up timeouts if not logged in
      if (timeoutRef.current) clearTimeout(timeoutRef.current);
      if (warningTimeoutRef.current) clearTimeout(warningTimeoutRef.current);
      return;
    }

    // Initial timeout setup
    resetTimeout();

    // Activity event listeners
    const activityEvents = [
      'mousedown',
      'keydown',
      'scroll',
      'touchstart',
      'click',
      'mousemove'
    ];

    const handleActivity = () => {
      resetTimeout();
    };

    // Add event listeners
    activityEvents.forEach(event => {
      document.addEventListener(event, handleActivity);
    });

    // Cleanup function
    return () => {
      // Remove event listeners
      activityEvents.forEach(event => {
        document.removeEventListener(event, handleActivity);
      });

      // Clear timeouts
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
      if (warningTimeoutRef.current) {
        clearTimeout(warningTimeoutRef.current);
      }
    };
  }, [isLoggedIn, resetTimeout]);
};

export default useSessionTimeout;
