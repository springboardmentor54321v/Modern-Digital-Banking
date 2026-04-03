import React, { useState, useEffect } from 'react';
import { AlertTriangle, Calendar, Clock, IndianRupee } from 'lucide-react';
import { getUpcomingBills } from '../api/bills.js';
import Load from '../components/Loader.jsx';

/**
 * UpcomingBills Component
 * Displays bills due within the next 3 days with warning styling
 */
const UpcomingBills = () => {
  const [upcomingBills, setUpcomingBills] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchUpcomingBills();
  }, []);

  const fetchUpcomingBills = async () => {
    try {
      setLoading(true);
      setError(null);

      const bills = await getUpcomingBills();
      // Bills are already filtered by backend - just sort by due date
      const sortedBills = bills.sort((a, b) => new Date(a.due_date) - new Date(b.due_date));

      setUpcomingBills(sortedBills);
    } catch (err) {
      setError(err.message || 'Failed to load upcoming bills');
    } finally {
      setLoading(false);
    }
  };

  const getDaysUntilDue = (dueDate) => {
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const due = new Date(dueDate);
    due.setHours(0, 0, 0, 0);

    const diffTime = due - today;
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays === 0) return 'Due today';
    if (diffDays === 1) return 'Due tomorrow';
    return `Due in ${diffDays} days`;
  };

  const getUrgencyColor = (dueDate) => {
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const due = new Date(dueDate);
    due.setHours(0, 0, 0, 0);

    const diffTime = due - today;
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays === 0) return 'bg-red-100 border-red-300 text-red-800'; // Due today - red
    if (diffDays === 1) return 'bg-orange-100 border-orange-300 text-orange-800'; // Due tomorrow - orange
    return 'bg-yellow-100 border-yellow-300 text-yellow-800'; // Due in 2-3 days - yellow
  };

  const getUrgencyIcon = (dueDate) => {
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const due = new Date(dueDate);
    due.setHours(0, 0, 0, 0);

    const diffTime = due - today;
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays === 0) return <AlertTriangle className="w-5 h-5 text-red-600" />;
    if (diffDays === 1) return <Clock className="w-5 h-5 text-orange-600" />;
    return <Calendar className="w-5 h-5 text-yellow-600" />;
  };

  if (loading) {
    return (
      <div className="bg-white rounded-2xl p-6 shadow-lg border border-gray-200">
        <div className="flex items-center gap-3 mb-4">
          <AlertTriangle className="w-6 h-6 text-yellow-600" />
          <h2 className="text-xl font-bold text-gray-900">Upcoming Bills</h2>
        </div>
        <Load />
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white rounded-2xl p-6 shadow-lg border border-gray-200">
        <div className="flex items-center gap-3 mb-4">
          <AlertTriangle className="w-6 h-6 text-yellow-600" />
          <h2 className="text-xl font-bold text-gray-900">Upcoming Bills</h2>
        </div>
        <p className="text-red-600 text-sm">{error}</p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-2xl p-6 shadow-lg border border-gray-200">
      <div className="flex items-center gap-3 mb-6">
        <AlertTriangle className="w-6 h-6 text-yellow-600" />
        <h2 className="text-xl font-bold text-gray-900">Upcoming Bills</h2>
        {upcomingBills.length > 0 && (
          <span className="bg-yellow-100 text-yellow-800 text-xs font-semibold px-2 py-1 rounded-full">
            {upcomingBills.length}
          </span>
        )}
      </div>

      {upcomingBills.length === 0 ? (
        <div className="text-center py-8">
          <Calendar className="w-12 h-12 text-gray-300 mx-auto mb-3" />
          <p className="text-gray-500 text-sm">No upcoming bills in the next 3 days</p>
          <p className="text-gray-400 text-xs mt-1">All caught up! 🎉</p>
        </div>
      ) : (
        <div className="space-y-3">
          {upcomingBills.map((bill) => (
            <div
              key={bill.id}
              className={`flex items-center justify-between p-4 rounded-lg border-2 transition-all hover:shadow-md ${getUrgencyColor(bill.due_date)}`}
            >
              <div className="flex items-center gap-3">
                {getUrgencyIcon(bill.due_date)}
                <div>
                  <h3 className="font-semibold text-gray-900 text-sm">
                    {bill.biller_name}
                  </h3>
                  <p className="text-xs opacity-75">
                    {getDaysUntilDue(bill.due_date)}
                  </p>
                </div>
              </div>

              <div className="text-right">
                <div className="flex items-center gap-1 font-bold text-gray-900">
                  <IndianRupee className="w-4 h-4" />
                  <span className="text-sm">{Number(bill.amount_due).toFixed(2)}</span>
                </div>
                <p className="text-xs opacity-75">
                  {new Date(bill.due_date).toLocaleDateString('en-IN', {
                    day: 'numeric',
                    month: 'short'
                  })}
                </p>
              </div>
            </div>
          ))}
        </div>
      )}

      {upcomingBills.length > 0 && (
        <div className="mt-4 pt-4 border-t border-gray-200">
          <p className="text-xs text-gray-500 text-center">
            💡 Pay bills on time to avoid late fees and maintain good credit
          </p>
        </div>
      )}
    </div>
  );
};

export default UpcomingBills;