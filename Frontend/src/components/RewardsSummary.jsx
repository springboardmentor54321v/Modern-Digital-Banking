import React, { useEffect, useState } from "react";
import { Gift, Trophy, Star } from "lucide-react";
import { fetchRewards } from "../api/rewards";

const RewardsSummary = () => {
  const [rewards, setRewards] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadRewards();
  }, []);

  const loadRewards = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await fetchRewards();
      setRewards(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const totalPoints = rewards.reduce((sum, reward) => sum + Number(reward.points_balance || 0), 0);

  if (loading) {
    return (
      <div className="bg-white rounded-2xl p-8 shadow-lg border border-gray-200 mb-8">
        <div className="animate-pulse">
          <div className="h-6 bg-gray-200 rounded w-1/3 mb-4"></div>
          <div className="h-4 bg-gray-200 rounded w-1/2 mb-6"></div>
          <div className="grid md:grid-cols-3 gap-4">
            <div className="h-20 bg-gray-200 rounded"></div>
            <div className="h-20 bg-gray-200 rounded"></div>
            <div className="h-20 bg-gray-200 rounded"></div>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white rounded-2xl p-8 shadow-lg border border-gray-200 mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-3">
          <Gift className="w-7 h-7 text-blue-600" />
          Rewards Summary
        </h2>
        <p className="text-red-600">Failed to load rewards: {error}</p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-2xl p-8 shadow-lg border border-gray-200 mb-8">
      <h2 className="text-2xl font-bold text-gray-900 mb-8 flex items-center gap-3">
        <Gift className="w-7 h-7 text-blue-600" />
        Rewards Summary
      </h2>

      {rewards.length > 0 ? (
        <>
          {/* Summary Cards */}
          <div className="grid md:grid-cols-3 gap-6 mb-8">
            <div className="bg-gradient-to-br from-blue-50 to-blue-100 p-6 rounded-xl border border-blue-200">
              <div className="flex items-center gap-3 mb-3">
                <Trophy className="w-6 h-6 text-blue-600" />
                <span className="font-semibold text-gray-900">Total Points</span>
              </div>
              <p className="text-2xl font-bold text-blue-600">
                {totalPoints.toLocaleString()}
              </p>
            </div>

            <div className="bg-gradient-to-br from-green-50 to-green-100 p-6 rounded-xl border border-green-200">
              <div className="flex items-center gap-3 mb-3">
                <Star className="w-6 h-6 text-green-600" />
                <span className="font-semibold text-gray-900">Active Programs</span>
              </div>
              <p className="text-2xl font-bold text-green-600">
                {rewards.length}
              </p>
            </div>

            <div className="bg-gradient-to-br from-purple-50 to-purple-100 p-6 rounded-xl border border-purple-200">
              <div className="flex items-center gap-3 mb-3">
                <Gift className="w-6 h-6 text-purple-600" />
                <span className="font-semibold text-gray-900">Highest Balance</span>
              </div>
              <p className="text-2xl font-bold text-purple-600">
                {Math.max(...rewards.map(r => Number(r.points_balance || 0))).toLocaleString()}
              </p>
            </div>
          </div>

          {/* Individual Rewards */}
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
            {rewards.slice(0, 6).map(reward => (
              <div
                key={reward.id}
                className="bg-gradient-to-br from-gray-50 to-gray-100 p-4 rounded-xl border border-gray-200 hover:border-blue-300 hover:shadow-md transition-all"
              >
                <div className="flex items-center justify-between mb-2">
                  <h3 className="font-semibold text-gray-900 text-sm">
                    {reward.program_name}
                  </h3>
                  <span className="text-xs text-gray-500">
                    {new Date(reward.last_updated).toLocaleDateString('en-IN', {
                      month: 'short',
                      day: 'numeric'
                    })}
                  </span>
                </div>
                <p className="text-xl font-bold text-blue-600">
                  {Number(reward.points_balance).toLocaleString()}
                </p>
                <p className="text-xs text-gray-600">points</p>
              </div>
            ))}
          </div>
        </>
      ) : (
        <div className="text-center py-12">
          <Gift className="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 mb-2">No Rewards Yet</h3>
          <p className="text-gray-600">Start earning rewards with your transactions</p>
        </div>
      )}
    </div>
  );
};

export default RewardsSummary;