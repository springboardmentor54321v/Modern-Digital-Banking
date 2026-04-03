import React, { useEffect, useState } from 'react';
import { fetchRewards, fetchRewardsBalance } from '../api/rewards';
import { Gift } from 'lucide-react';
import toast from 'react-hot-toast';
import Load from '../components/Loader';

export default function Gifts() {
  const [rewards, setRewards] = useState([]);
  const [balance, setBalance] = useState(null);
  const [currentReward, setCurrentReward] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadRewards();
  }, []);

  async function loadRewards() {
    setLoading(true);
    try {
      const [data, balData] = await Promise.all([
        fetchRewards(),
        fetchRewardsBalance().catch(() => null)
      ]);
      setRewards(data || []);
      if (balData) setBalance(balData);
    } catch (err) {
      toast.error(err.message || 'Failed to load rewards');
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return <Load />
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-teal-50">
      <div className="mx-auto max-w-6xl">
        <div className="mb-10">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Rewards</h1>
          <p className="text-gray-600">Track your reward points</p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {rewards.map(reward => (
            <div
              key={reward.id}
              className="group relative bg-white rounded-2xl shadow-md hover:shadow-xl transition-all duration-300 overflow-hidden border border-gray-200 hover:border-blue-300"
            >
              <div className="absolute top-0 left-0 w-1 h-24 bg-gradient-to-b from-blue-500 to-blue-300"></div>

              <div className="p-8">
                <div className="w-14 h-14 bg-gradient-to-br from-blue-100 to-indigo-100 rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300">
                  <Gift className="w-7 h-7 text-blue-600" />
                </div>

                <h3 className="text-xl font-bold text-gray-900 mb-2 group-hover:text-blue-600 transition-colors">
                  {reward.program_name}
                </h3>

                <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl p-4 mb-4 border border-blue-100">
                  <p className="text-sm text-gray-600 mb-1">Points Balance</p>
                  <p className="text-3xl font-bold text-blue-600">
                    {reward.points_balance.toLocaleString()}
                  </p>
                </div>

                <div className="text-xs text-gray-500">
                  <p>Last updated: {new Date(reward.last_updated).toLocaleDateString('en-IN', {
                    day: 'numeric',
                    month: 'short',
                    year: 'numeric'
                  })}</p>
                </div>
              </div>
            </div>
          ))}
        </div>

        {rewards.length === 0 && (
          <div className="text-center py-16">
            <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Gift className="w-8 h-8 text-gray-400" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">No reward programs found.</h3>
          </div>
        )}
      </div>
    </div>
  );
}
