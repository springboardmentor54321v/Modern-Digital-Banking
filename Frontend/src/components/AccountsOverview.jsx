import React from "react";
import { TrendingUp, ArrowUpRight, ArrowDownRight, Wallet } from "lucide-react";

const AccountsOverview = ({ accounts, transactions }) => {
  const totalBalance = accounts.reduce(
    (sum, acc) => sum + Number(acc.balance || 0),
    0
  );

  const totalIncome = transactions
    .filter((t) => t.txn_type === "credit")
    .reduce((s, t) => s + Number(t.amount), 0);

  const totalExpense = transactions
    .filter((t) => t.txn_type === "debit")
    .reduce((s, t) => s + Number(t.amount), 0);

  return (
    <div className="grid md:grid-cols-3 gap-6 mb-8">
      <div className="relative group">
        <div className="absolute inset-0 bg-gradient-to-r from-blue-100 to-blue-50 rounded-2xl blur opacity-0 group-hover:opacity-100 transition duration-300"></div>
        <div className="relative bg-gradient-to-br from-blue-50 to-blue-100 text-gray-900 p-8 rounded-2xl shadow-md hover:shadow-lg overflow-hidden border border-blue-200">
          <div className="absolute top-0 right-0 opacity-5">
            <Wallet className="w-32 h-32" />
          </div>
          <div className="relative z-10">
            <p className="text-sm opacity-70 font-medium text-gray-700">Total Balance</p>
            <p className="text-xl font-bold mt-4 text-gray-900">₹{totalBalance.toFixed(2)}</p>
            <div className="flex items-center gap-2 mt-4 text-sm opacity-80 text-gray-700">
              <TrendingUp className="w-4 h-4" />
              <span>{accounts.length} account{accounts.length !== 1 ? 's' : ''}</span>
            </div>
          </div>
        </div>
      </div>

      <div className="relative group">
        <div className="absolute inset-0 bg-gradient-to-r from-green-100 to-emerald-50 rounded-2xl blur opacity-0 group-hover:opacity-100 transition duration-300"></div>
        <div className="relative bg-gradient-to-br from-green-50 to-emerald-100 text-gray-900 p-8 rounded-2xl shadow-md hover:shadow-lg overflow-hidden border border-green-200">
          <div className="absolute top-0 right-0 opacity-5">
            <ArrowUpRight className="w-32 h-32" />
          </div>
          <div className="relative z-10">
            <p className="text-sm opacity-70 font-medium text-gray-700">Total Income</p>
            <p className="text-xl font-bold mt-4 text-green-600">₹{totalIncome.toFixed(2)}</p>
            <div className="flex items-center gap-2 text-sm mt-4 opacity-80 text-gray-700">
              <ArrowUpRight className="w-4 h-4" />
              <span>{transactions.filter((t) => t.txn_type === "credit").length} transactions</span>
            </div>
          </div>
        </div>
      </div>

      <div className="relative group">
        <div className="absolute inset-0 bg-gradient-to-r from-red-100 to-pink-50 rounded-2xl blur opacity-0 group-hover:opacity-100 transition duration-300"></div>
        <div className="relative bg-gradient-to-br from-red-50 to-pink-100 text-gray-900 p-8 rounded-2xl shadow-md hover:shadow-lg overflow-hidden border border-red-200">
          <div className="absolute top-0 right-0 opacity-5">
            <ArrowDownRight className="w-32 h-32" />
          </div>
          <div className="relative z-10">
            <p className="text-sm opacity-70 font-medium text-gray-700">Total Expenses</p>
            <p className="text-xl font-bold mt-4 text-red-600">₹{totalExpense.toFixed(2)}</p>
            <div className="flex items-center gap-2 text-sm mt-4 opacity-80 text-gray-700">
              <ArrowDownRight className="w-4 h-4" />
              <span>{transactions.filter((t) => t.txn_type === "debit").length} transactions</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AccountsOverview;