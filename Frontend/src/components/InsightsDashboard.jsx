import React, { useState, useEffect } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer
} from "recharts";
import { TrendingUp, PieChart as PieChartIcon, Store, Target } from "lucide-react";
import {
  getCashFlow,
  getCategorySpend,
  getTopMerchants,
  getBudgetBurnRate
} from "../api/insights";

const InsightsDashboard = () => {
  const [cashFlowData, setCashFlowData] = useState([]);
  const [categorySpendData, setCategorySpendData] = useState([]);
  const [topMerchantsData, setTopMerchantsData] = useState([]);
  const [budgetBurnRate, setBudgetBurnRate] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [cashFlow, categorySpend, topMerchants, burnRate] = await Promise.all([
          getCashFlow(),
          getCategorySpend(),
          getTopMerchants(),
          getBudgetBurnRate()
        ]);

        setCashFlowData(cashFlow);
        setCategorySpendData(
          Array.isArray(categorySpend)
            ? categorySpend.map((row) => ({
              name: row.category,
              value: Number(row.total_spent || 0),
            }))
            : []
        );
        setTopMerchantsData(Array.isArray(topMerchants) ? topMerchants : []);
        setBudgetBurnRate({
          spent: Number(burnRate?.budget_used || 0),
          total: Number(burnRate?.total_budget || 0),
          percentage: Math.round((Number(burnRate?.burn_rate || 0) * 100) * 10) / 10,
        });
      } catch (err) {
        setError(err.message || "Failed to fetch insights data");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];

  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-6 p-6">
        {[...Array(4)].map((_, i) => (
          <div key={i} className="bg-white rounded-lg shadow-md p-6 animate-pulse">
            <div className="h-4 bg-gray-200 rounded w-3/4 mb-4"></div>
            <div className="h-32 bg-gray-200 rounded"></div>
          </div>
        ))}
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6">
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-600">Error: {error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Insights Dashboard</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-6">
        {/* Cash Flow Bar Chart */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center gap-2 mb-4">
            <TrendingUp className="w-5 h-5 text-blue-600" />
            <h2 className="text-lg font-semibold text-gray-900">Cash Flow</h2>
          </div>
          {cashFlowData.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={cashFlowData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="income" fill="#10B981" name="Income" />
                <Bar dataKey="expense" fill="#EF4444" name="Expense" />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <div className="flex items-center justify-center h-32 text-gray-500">
              No Data Available
            </div>
          )}
        </div>

        {/* Category-wise Spending Pie Chart */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center gap-2 mb-4">
            <PieChartIcon className="w-5 h-5 text-green-600" />
            <h2 className="text-lg font-semibold text-gray-900">Category Spending</h2>
          </div>
          {categorySpendData.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={categorySpendData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {categorySpendData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          ) : (
            <div className="flex items-center justify-center h-32 text-gray-500">
              No Data Available
            </div>
          )}
        </div>

        {/* Top Merchants Table */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center gap-2 mb-4">
            <Store className="w-5 h-5 text-purple-600" />
            <h2 className="text-lg font-semibold text-gray-900">Top Merchants</h2>
          </div>
          {topMerchantsData.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="min-w-full">
                <thead>
                  <tr className="border-b">
                    <th className="text-left py-2 px-2 text-sm font-medium text-gray-700">Merchant</th>
                    <th className="text-right py-2 px-2 text-sm font-medium text-gray-700">Amount</th>
                  </tr>
                </thead>
                <tbody>
                  {topMerchantsData.slice(0, 5).map((merchant, index) => (
                    <tr key={index} className="border-b border-gray-100">
                      <td className="py-2 px-2 text-sm text-gray-900">{merchant.merchant}</td>
                      <td className="py-2 px-2 text-sm text-gray-900 text-right">₹{Number(merchant.total_spent || 0).toFixed(2)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="flex items-center justify-center h-32 text-gray-500">
              No Data Available
            </div>
          )}
        </div>

        {/* Budget Burn Rate Progress Bar */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center gap-2 mb-4">
            <Target className="w-5 h-5 text-orange-600" />
            <h2 className="text-lg font-semibold text-gray-900">Budget Burn Rate</h2>
          </div>
          <div className="space-y-4">
            <div>
              <div className="flex justify-between text-sm text-gray-600 mb-1">
                <span>Monthly Budget</span>
                <span>{budgetBurnRate.percentage || 0}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-orange-500 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${Math.min(budgetBurnRate.percentage || 0, 100)}%` }}
                ></div>
              </div>
              <div className="flex justify-between text-xs text-gray-500 mt-1">
                <span>₹{budgetBurnRate.spent || 0} spent</span>
                <span>₹{budgetBurnRate.total || 0} total</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default InsightsDashboard;