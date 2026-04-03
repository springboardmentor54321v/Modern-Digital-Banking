import React, { useState, useEffect } from 'react';
import { AlertTriangle, Clock } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

/**
 * SessionTimeoutWarning Component
 * Displays a warning modal when user is about to be logged out due to inactivity
 */
export const SessionTimeoutWarning = ({ timeoutMinutes = 60, warningSeconds = 300 }) => {
  const [showWarning, setShowWarning] = useState(false);
  const [secondsRemaining, setSecondsRemaining] = useState(warningSeconds);
  const { isLoggedIn } = useAuth();

  useEffect(() => {
    if (!isLoggedIn) {
      setShowWarning(false);
      return;
    }

    let warningTimeout, countdownInterval;

    const setupWarning = () => {
      // Show warning after inactivity period minus warning time
      warningTimeout = setTimeout(() => {
        setShowWarning(true);
        setSecondsRemaining(warningSeconds);

        // Start countdown
        countdownInterval = setInterval(() => {
          setSecondsRemaining(prev => {
            if (prev <= 1) {
              clearInterval(countdownInterval);
              setShowWarning(false);
              return warningSeconds;
            }
            return prev - 1;
          });
        }, 1000);
      }, (timeoutMinutes * 60 * 1000) - (warningSeconds * 1000));
    };

    const handleActivity = () => {
      // Hide warning and reset timeout on activity
      setShowWarning(false);
      if (countdownInterval) clearInterval(countdownInterval);
      if (warningTimeout) clearTimeout(warningTimeout);
      setupWarning();
    };

    setupWarning();

    // Activity event listeners
    const activityEvents = ['mousedown', 'keydown', 'scroll', 'touchstart', 'click'];
    activityEvents.forEach(event => {
      document.addEventListener(event, handleActivity);
    });

    return () => {
      if (warningTimeout) clearTimeout(warningTimeout);
      if (countdownInterval) clearInterval(countdownInterval);
      activityEvents.forEach(event => {
        document.removeEventListener(event, handleActivity);
      });
    };
  }, [isLoggedIn, timeoutMinutes, warningSeconds]);

  if (!showWarning || !isLoggedIn) {
    return null;
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 pointer-events-auto">
      <div className="bg-white rounded-lg shadow-2xl p-6 max-w-md mx-4 transform transition-all">
        <div className="flex items-center justify-center mb-4">
          <div className="bg-yellow-100 p-3 rounded-full">
            <AlertTriangle className="w-8 h-8 text-yellow-600" />
          </div>
        </div>

        <h2 className="text-xl font-bold text-gray-800 text-center mb-2">
          Session Timeout Warning
        </h2>

        <p className="text-gray-600 text-center mb-4">
          Your session will expire due to inactivity in
        </p>

        <div className="flex items-center justify-center mb-6">
          <Clock className="w-5 h-5 text-red-500 mr-2" />
          <span className="text-3xl font-bold text-red-500">
            {secondsRemaining}s
          </span>
        </div>

        <p className="text-sm text-gray-500 text-center mb-4">
          Please make any activity to continue your session, or you will be automatically logged out.
        </p>

        <div className="flex gap-3">
          <button
            onClick={() => setShowWarning(false)}
            className="flex-1 px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg font-medium transition-colors"
          >
            Continue Session
          </button>
        </div>
      </div>
    </div>
  );
};

export default SessionTimeoutWarning;
