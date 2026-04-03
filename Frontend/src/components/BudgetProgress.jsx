import React from "react";
import { Target, Calendar } from "lucide-react";

const BudgetProgress = ({ budgets }) => {
  const getMonthName = (month) => {
    const months = [
      "January", "February", "March", "April", "May", "June",
      "July", "August", "September", "October", "November", "December"
    ];
    return months[month - 1] || "Unknown";
  };

  return (
    <div className="bg-white rounded-2xl p-8 shadow-lg border border-gray-200 mb-8">
      <h2 className="text-2xl font-bold text-gray-900 mb-8 flex items-center gap-3">
        <Target className="w-7 h-7 text-blue-600" />
        Budget Progress
      </h2>

      {budgets.length ? (
        <div className="grid md:grid-cols-2 gap-6">
          {budgets.map((b) => {
            const spent = Number(b.spent_amount || 0);
            const limit = Number(b.limit_amount || 0);
            const percent = limit ? Math.min((spent / limit) * 100, 100) : 0;
            const remaining = limit - spent;

            return (
              <div
                key={b.id}
                className="group bg-gradient-to-br from-gray-50 to-gray-100 rounded-xl p-6 border border-gray-200 hover:border-gray-300 hover:shadow-md transition duration-300"
              >
                <div className="flex justify-between items-start mb-4">
                  <div className="flex-1">
                    <h3 className="font-semibold text-gray-900 text-lg">{b.category}</h3>
                    <div className="flex items-center gap-1 mt-1 text-gray-600 text-sm">
                      <Calendar className="w-4 h-4" />
                      <span>{getMonthName(b.month)} {b.year}</span>
                    </div>
                  </div>
                  <span
                    className={`text-sm font-bold px-3 py-1 rounded-full ${
                      percent >= 100
                        ? "bg-red-100 text-red-700"
                        : percent >= 80
                        ? "bg-yellow-100 text-yellow-700"
                        : "bg-green-100 text-green-700"
                    }`}
                  >
                    {percent.toFixed(0)}%
                  </span>
                </div>

                <div className="mb-4">
                  <div className="w-full bg-gray-300 h-3 rounded-full overflow-hidden">
                    <div
                      className={`h-3 rounded-full transition-all duration-500 ${
                        percent >= 100
                          ? "bg-red-500"
                          : percent >= 80
                          ? "bg-yellow-500"
                          : "bg-green-500"
                      }`}
                      style={{ width: `${percent}%` }}
                    />
                  </div>
                </div>

                <div className="space-y-3 text-sm">
                  <div className="flex justify-between text-gray-700">
                    <span>Spent</span>
                    <span className="font-semibold text-gray-900">₹{spent.toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between text-gray-700">
                    <span>Limit</span>
                    <span className="font-semibold text-gray-900">₹{limit.toFixed(2)}</span>
                  </div>
                  <div className="pt-3 border-t border-gray-300 flex justify-between">
                    <span className="text-gray-600">Remaining</span>
                    <span
                      className={`font-semibold ${
                        remaining >= 0 ? "text-green-600" : "text-red-600"
                      }`}
                    >
                      {remaining >= 0 ? `₹${remaining.toFixed(2)}` : `-₹${Math.abs(remaining).toFixed(2)}`}
                    </span>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        <p className="text-gray-500 text-center py-12">No budgets are created for now.</p>
      )}
    </div>
  );
};

export default BudgetProgress;