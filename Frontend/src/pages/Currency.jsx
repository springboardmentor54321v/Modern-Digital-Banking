import React, { useEffect, useState } from "react";
import { Globe, RefreshCcw, TrendingUp, TrendingDown } from "lucide-react";
import { getExchangeRates } from "../api/currency";

export default function Currency() {
  const [rates, setRates] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);

  const loadRates = async () => {
    try {
      setError(null);
      const data = await getExchangeRates();
      setRates(data.rates || {});
      setLastUpdated(new Date());
    } catch (err) {
      console.error("Failed to load exchange rates", err);
      setError(err.toString());
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadRates();
    const interval = setInterval(loadRates, 5 * 60 * 1000); // refresh every 5 minutes
    return () => clearInterval(interval);
  }, []);

  // Major currencies to display
  const majorCurrencies = ['USD', 'EUR', 'GBP', 'JPY', 'CAD', 'AUD', 'CHF', 'CNY'];

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-6xl mx-auto p-6">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2 flex items-center gap-3">
            <Globe className="w-8 h-8 text-blue-600" />
            Currency Exchange Rates
          </h1>
          <p className="text-gray-600">Real-time exchange rates against Indian Rupee (INR)</p>
        </div>

        {/* Main Currency Display */}
        <div className="bg-white rounded-2xl shadow-lg border border-gray-200 p-8 mb-8">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-semibold text-gray-900">Live Rates</h2>
            <div className="flex items-center gap-4">
              {lastUpdated && (
                <span className="text-sm text-gray-500">
                  Last updated: {lastUpdated.toLocaleTimeString()}
                </span>
              )}
              <button
                onClick={loadRates}
                className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
              >
                <RefreshCcw className="w-4 h-4" />
                Refresh
              </button>
            </div>
          </div>

          {loading ? (
            <div className="text-center py-12">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
              <p className="text-gray-600">Loading exchange rates...</p>
            </div>
          ) : error ? (
            <div className="text-center py-12">
              <p className="text-red-600 text-lg mb-2">Failed to load rates</p>
              <p className="text-gray-600">Currency data unavailable</p>
            </div>
          ) : (
            <div className="space-y-6">
              {/* Compact Display */}
              <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl p-6 border border-blue-200">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Major Currencies</h3>
                <div className="font-mono text-lg leading-relaxed">
                  {majorCurrencies
                    .filter(currency => rates[currency])
                    .map((currency, index) => (
                      <span key={currency} className="inline-block mr-6 mb-3">
                        <span className="font-bold text-gray-900">{currency}</span>
                        <span className="text-gray-500 mx-2">→</span>
                        <span className="text-green-600 font-bold">₹{Number(rates[currency]).toFixed(2)}</span>
                        {index < majorCurrencies.filter(c => rates[c]).length - 1 && (
                          <span className="text-gray-300 ml-4">|</span>
                        )}
                      </span>
                    ))}
                </div>
              </div>

              {/* Detailed Table */}
              <div className="bg-white border border-gray-200 rounded-xl overflow-hidden">
                <div className="px-6 py-4 bg-gray-50 border-b border-gray-200">
                  <h3 className="text-lg font-semibold text-gray-900">All Available Rates</h3>
                </div>
                <div className="divide-y divide-gray-200">
                  {Object.entries(rates)
                    .sort(([a], [b]) => a.localeCompare(b))
                    .map(([currency, rate]) => (
                      <div key={currency} className="px-6 py-4 flex items-center justify-between hover:bg-gray-50">
                        <div className="flex items-center gap-3">
                          <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                            <span className="text-sm font-bold text-blue-600">{currency.slice(0, 2)}</span>
                          </div>
                          <span className="font-medium text-gray-900">{currency}</span>
                        </div>
                        <div className="text-right">
                          <span className="text-xl font-bold text-green-600">₹{Number(rate).toFixed(2)}</span>
                          <div className="text-sm text-gray-500">1 {currency} = ₹{Number(rate).toFixed(4)}</div>
                        </div>
                      </div>
                    ))}
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Info Section */}
        <div className="bg-blue-50 rounded-xl p-6 border border-blue-200">
          <div className="flex items-start gap-3">
            <div className="w-6 h-6 bg-blue-600 rounded-full flex items-center justify-center mt-0.5">
              <span className="text-white text-sm">ℹ</span>
            </div>
            <div>
              <h3 className="font-semibold text-blue-900 mb-2">About Exchange Rates</h3>
              <p className="text-blue-800 text-sm leading-relaxed">
                These rates are updated in real-time from reliable financial data providers.
                All rates are shown against the Indian Rupee (INR) and are for informational purposes only.
                For actual transactions, please check with your financial institution for current rates.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}