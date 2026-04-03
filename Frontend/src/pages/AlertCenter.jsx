import React, { useState, useEffect } from 'react';
import { Bell, Check, AlertTriangle, AlertCircle, Clock, CreditCard } from 'lucide-react';
import { getAlerts, markAlertRead } from '../api/alerts';

const AlertCenter = () => {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchAlerts = async () => {
    try {
      setLoading(true);
      const data = await getAlerts();
      setAlerts(data.items || data || []);
    } catch (err) {
      setError(err.message || 'Failed to fetch alerts');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAlerts();

    // Set up polling every 60 seconds
    const interval = setInterval(fetchAlerts, 60000);

    return () => clearInterval(interval);
  }, []);

  const handleMarkAsRead = async (alertId) => {
    try {
      // For dynamic bill alerts, just update local state since they can't be marked as read in DB
      if (typeof alertId === 'string' && (alertId.startsWith('overdue_') || alertId.startsWith('upcoming_'))) {
        setAlerts(alerts.map(alert =>
          alert.id === alertId ? { ...alert, is_read: true } : alert
        ));
        return;
      }

      // For regular alerts, call the API
      await markAlertRead(alertId);
      // Update local state
      setAlerts(alerts.map(alert =>
        alert.id === alertId ? { ...alert, is_read: true } : alert
      ));
    } catch (err) {
      console.error('Failed to mark alert as read:', err);
    }
  };

  const getAlertIcon = (alertType) => {
    switch (alertType) {
      case 'budget_exceeded':
        return <AlertTriangle className="w-5 h-5 text-red-500" />;
      case 'low_balance':
        return <AlertCircle className="w-5 h-5 text-yellow-500" />;
      case 'overdue_bill':
        return <AlertTriangle className="w-5 h-5 text-red-600" />;
      case 'upcoming_bill':
        return <Clock className="w-5 h-5 text-orange-500" />;
      default:
        return <Bell className="w-5 h-5 text-blue-500" />;
    }
  };

  const getAlertColor = (alertType) => {
    switch (alertType) {
      case 'budget_exceeded':
        return 'border-red-200 bg-red-50';
      case 'low_balance':
        return 'border-yellow-200 bg-yellow-50';
      case 'overdue_bill':
        return 'border-red-200 bg-red-50';
      case 'upcoming_bill':
        return 'border-orange-200 bg-orange-50';
      default:
        return 'border-blue-200 bg-blue-50';
    }
  };

  if (loading && alerts.length === 0) {
    return (
      <div className="p-6">
        <div className="flex items-center justify-center h-32">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6">
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-600">Error: {error}</p>
          <button
            onClick={fetchAlerts}
            className="mt-2 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">Alert Center</h1>
        <p className="text-gray-600">Stay updated with your account notifications</p>
      </div>

      {alerts.length === 0 ? (
        <div className="text-center py-12">
          <Bell className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-500 text-lg">No alerts at the moment</p>
          <p className="text-gray-400 text-sm">You're all caught up!</p>
        </div>
      ) : (
        <div className="space-y-4">
          {(Array.isArray(alerts) ? alerts : []).map((alert) => (
            <div
              key={alert.id}
              className={`p-4 rounded-lg border ${getAlertColor(alert.alert_type)} ${!alert.is_read ? 'ring-2 ring-blue-200' : ''
                }`}
            >
              <div className="flex items-start justify-between">
                <div className="flex items-start gap-3">
                  {getAlertIcon(alert.alert_type)}
                  <div className="flex-1">
                    <p className={`text-sm ${alert.is_read ? 'text-gray-600' : 'text-gray-900 font-medium'}`}>
                      {alert.message}
                    </p>
                    <p className="text-xs text-gray-500 mt-1">
                      {new Date(alert.created_at).toLocaleString()}
                    </p>
                  </div>
                </div>
                {!alert.is_read && (
                  <button
                    onClick={() => handleMarkAsRead(alert.id)}
                    className="flex items-center gap-1 px-3 py-1 text-xs bg-white rounded-md border border-gray-300 hover:bg-gray-50 transition"
                  >
                    <Check className="w-3 h-3" />
                    Mark as Read
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      <div className="mt-6 text-xs text-gray-500 text-center">
        Auto-refreshing every 60 seconds
      </div>
    </div>
  );
};

export default AlertCenter;