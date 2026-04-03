import React, { useEffect, useState } from "react";
import { Globe, RefreshCcw } from "lucide-react";
import { getExchangeRates } from "../api/currency";

export default function CurrencySummary() {
  const [rates, setRates] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadRates = async () => {
    try {
      setError(null);
      const data = await getExchangeRates();
      setRates(data.rates || {});
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

  return (
    <div className="bg-white rounded-2xl p-6 shadow-md border border-gray-200 mb-8">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-semibold text-gray-900 flex items-center gap-2">
          <Globe className="w-5 h-5" /> Currency Rates
        </h2>
        <button
          onClick={loadRates}
          className="text-gray-500 hover:text-gray-700 transition"
        >
          <RefreshCcw className="w-4 h-4" />
        </button>
      </div>
      {loading ? (
        <p className="text-gray-600">Loading rates...</p>
      ) : error ? (
        <p className="text-red-600 text-sm">{error}</p>
      ) : (
        <div className="space-y-3">
          <div className="text-sm text-gray-600 mb-2">Exchange rates to INR (₹)</div>
          <div className="bg-gray-50 rounded-lg p-4 font-mono text-sm">
            {Object.entries(rates)
              .filter(([currency]) => ['USD', 'EUR', 'GBP', 'JPY', 'CAD', 'AUD'].includes(currency))
              .map(([currency, rate]) => (
                <span key={currency} className="inline-block mr-4 mb-2">
                  <span className="font-semibold text-gray-900">{currency}</span>
                  <span className="text-gray-500 mx-1">→</span>
                  <span className="text-green-600 font-semibold">₹{Number(rate).toFixed(2)}</span>
                </span>
              ))}
          </div>
          <div className="text-xs text-gray-500 text-center">
            Auto-refreshes every 5 minutes • Last updated: {new Date().toLocaleTimeString()}
          </div>
        </div>
      )}
    </div>
  );
}
