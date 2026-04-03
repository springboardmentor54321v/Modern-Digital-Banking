import React, { useEffect, useState } from "react";
import Load from "../components/Loader";
import AccountsOverview from "../components/AccountsOverview";
import RecentTransactions from "../components/RecentTransactions";
import BudgetProgress from "../components/BudgetProgress";
import UpcomingBills from "../components/UpcomingBills";
import RewardsSummary from "../components/RewardsSummary";
import CurrencySummary from "../components/CurrencySummary";
import { getAccounts } from "../api/accounts";
import { getTransactions } from "../api/transactions";
import { getBudgets } from "../api/budgets";
import { useAuth } from "../context/AuthContext";
import { getUserIdFromAuth } from "../utils/authUser";

const Stats = () => {
  const { user } = useAuth();
  const [accounts, setAccounts] = useState([]);
  const [transactions, setTransactions] = useState([]);
  const [budgets, setBudgets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    setLoading(true);
    setError(null);

    try {
      const accountsData = await getAccounts();
      setAccounts(accountsData);

      if (accountsData.length > 0) {
        try {
          const txData = await getTransactions(accountsData[0].id);
          localStorage.setItem("selected_account_id", accountsData[0].id);
          setTransactions(txData);
        } catch (txErr) {
          console.error("Failed to fetch transactions:", txErr);
          setTransactions([]);
        }
      }
    } catch (accErr) {
      console.error("Failed to fetch accounts:", accErr);
      setAccounts([]);
    }

    try {
      const budgetData = await getBudgets();
      setBudgets(budgetData.slice(0, 4));
    } catch (budgetErr) {
      console.error("Failed to fetch budgets:", budgetErr);
      setBudgets([]);
    }

    setLoading(false);
  };

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center h-screen gap-4 bg-gradient-to-br from-blue-50 to-indigo-100">
        <p className="text-red-600 font-semibold text-lg">{error}</p>
        <button
          onClick={fetchDashboardData}
          className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition font-medium"
        >
          Retry
        </button>
      </div>
    );
  }

  if (loading) {
    return <Load />
  }

  return (
    <div className="min-h-screen">
      {/* 1. Financial Dashboard Header */}
      <div className="mb-10">
        <h1 className="text-4xl font-bold text-gray-900 mb-2">Financial Dashboard</h1>
        <p className="text-gray-600 text-lg">Manage your finances with real-time insights</p>
      </div>

      {/* 2. Accounts Overview */}
      <AccountsOverview accounts={accounts} transactions={transactions} />

      {/* 3. Transactions */}
      <RecentTransactions transactions={transactions} />

      {/* 4. Budget Progress */}
      <BudgetProgress budgets={budgets} />

      {/* 5. Bills */}
      <UpcomingBills />

      {/* 6. Rewards Summary */}
      <RewardsSummary />

      {/* 7. Currency Rates */}
      <CurrencySummary />
      {/* 8. Export Section */}
      <div className="bg-white rounded-lg shadow-md p-6 mt-8">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Export Data</h2>
        <p className="text-gray-600 mb-6">Download your transaction data in CSV or PDF format</p>
        <div className="flex gap-4 flex-wrap">
          <button
            onClick={async () => {
              const userId = user?.id ?? getUserIdFromAuth();
              const url = `${import.meta.env.VITE_API_BASE_URL}/export/transactions?format=csv&user_id=${userId}`;
              const res = await fetch(url, { headers: { Authorization: `Bearer ${localStorage.getItem("access_token")}` } });
              const blob = await res.blob();
              const a = document.createElement("a");
              a.href = window.URL.createObjectURL(blob);
              a.download = "transactions.csv";
              a.click();
            }}
            className="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition font-medium flex items-center gap-2"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Export CSV
          </button>
          <button
            onClick={async () => {
              const userId = user?.id ?? getUserIdFromAuth();
              const url = `${import.meta.env.VITE_API_BASE_URL}/export/insights?format=pdf&user_id=${userId}`;
              const res = await fetch(url, { headers: { Authorization: `Bearer ${localStorage.getItem("access_token")}` } });
              const blob = await res.blob();
              const a = document.createElement("a");
              a.href = window.URL.createObjectURL(blob);
              a.download = "insights.pdf";
              a.click();
            }}
            className="px-6 py-3 bg-red-600 text-white rounded-lg hover:bg-red-700 transition font-medium flex items-center gap-2"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3M3 17V7a2 2 0 012-2h6l2 2h6a2 2 0 012 2v10a2 2 0 01-2 2H5a2 2 0 01-2-2z" />
            </svg>
            Download PDF Report
          </button>
        </div>
      </div>
    </div>
  );
};

export default Stats;