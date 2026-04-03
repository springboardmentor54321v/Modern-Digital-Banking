import React, { useState } from "react";
import { forgotPassword } from "../api/auth.js";
import toast from "react-hot-toast";
import { Mail } from "lucide-react";

export default function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [resetUrl, setResetUrl] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await forgotPassword(email);
      setResetUrl(response.reset_url);
      toast.success("Reset link generated successfully.");
    } catch (err) {
      toast.error(
        typeof err === "string" ? err : err.detail || err.message || "Error"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-100 via-blue-50 to-white">
      <div className="w-full max-w-md bg-white rounded-3xl shadow-xl p-8">
        <h2 className="text-2xl font-bold text-center mb-6">
          Forgot Password
        </h2>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Email Address
            </label>
            <div className="relative">
              <Mail className="absolute left-3 top-3 text-gray-400 w-5 h-5" />
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="you@example.com"
                disabled={loading}
                className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent disabled:opacity-50 disabled:cursor-not-allowed"
              />
            </div>
          </div>
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-purple-600 hover:bg-purple-700 text-white py-3 rounded-xl font-semibold disabled:opacity-50"
          >
            {loading ? "Generating..." : "Generate Reset Link"}
          </button>
        </form>
        {resetUrl && (
          <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded-xl">
            <p className="text-green-800 font-medium mb-2">Reset Link Generated:</p>
            <a
              href={resetUrl}
              className="text-blue-600 hover:underline break-all"
              target="_blank"
              rel="noopener noreferrer"
            >
              {resetUrl}
            </a>
            <p className="text-sm text-gray-600 mt-2">
              Click the link above to reset your password. The link expires in 3 minutes.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
