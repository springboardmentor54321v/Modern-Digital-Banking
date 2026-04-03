import React from "react";
import { ArrowUpRight, ArrowDownRight, RefreshCcw } from "lucide-react";

const RecentTransactions = ({ transactions }) => {
  const recentTransactions = transactions.slice(0, 5); // Show last 5 transactions

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-IN', {
      day: 'numeric',
      month: 'short',
      year: 'numeric'
    });
  };

  return (
    <div className="bg-white rounded-2xl p-8 shadow-lg border border-gray-200 mb-8">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-gray-900 flex items-center gap-3">
          <RefreshCcw className="w-7 h-7 text-blue-600" />
          Recent Transactions
        </h2>
        <span className="text-sm text-gray-500">
          Last {recentTransactions.length} transactions
        </span>
      </div>

      {recentTransactions.length > 0 ? (
        <div className="space-y-4">
          {recentTransactions.map((transaction) => (
            <div
              key={transaction.id}
              className="flex items-center justify-between p-4 bg-gray-50 rounded-xl hover:bg-gray-100 transition-colors"
            >
              <div className="flex items-center gap-4">
                <div className={`w-10 h-10 rounded-full flex items-center justify-center ${
                  transaction.txn_type === 'credit'
                    ? 'bg-green-100 text-green-600'
                    : 'bg-red-100 text-red-600'
                }`}>
                  {transaction.txn_type === 'credit' ? (
                    <ArrowUpRight className="w-5 h-5" />
                  ) : (
                    <ArrowDownRight className="w-5 h-5" />
                  )}
                </div>
                <div>
                  <p className="font-semibold text-gray-900">
                    {transaction.description || 'Transaction'}
                  </p>
                  <p className="text-sm text-gray-600">
                    {transaction.category} • {formatDate(transaction.txn_date)}
                  </p>
                  {transaction.merchant && (
                    <p className="text-xs text-gray-500">{transaction.merchant}</p>
                  )}
                </div>
              </div>
              <div className="text-right">
                <p className={`font-bold ${
                  transaction.txn_type === 'credit' ? 'text-green-600' : 'text-red-600'
                }`}>
                  {transaction.txn_type === 'credit' ? '+' : '-'}₹{Number(transaction.amount).toFixed(2)}
                </p>
                <p className="text-xs text-gray-500">{transaction.currency}</p>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="text-center py-12">
          <RefreshCcw className="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 mb-2">No Transactions Yet</h3>
          <p className="text-gray-600">Your recent transactions will appear here</p>
        </div>
      )}
    </div>
  );
};

export default RecentTransactions;