import React from 'react';
import { Routes, Route, Outlet } from 'react-router-dom';
import Navbar from './components/Navbar.jsx';
import Footer from './components/Footer.jsx';
import Home from './pages/Home.jsx';
import Login from './pages/Login.jsx';
import Dashboard from './pages/CustDashboard.jsx';
import Services from './pages/Services';
import Analytics from './pages/Analytics';
import Support from './pages/Support';
import AdminDashboard from './pages/AdminDashboard.jsx';
import ProtectedRoute from './components/ProtectedRoute.jsx';
import Bills from './pages/Bills.jsx';
import Rewards from './pages/Rewards.jsx';
import Currency from './pages/Currency.jsx';
import ForgotPassword from './pages/ForgotPassword.jsx';
import ResetPassword from './pages/ResetPassword.jsx';

import AlertCenter from './pages/AlertCenter.jsx';
import InsightsDashboard from './components/InsightsDashboard.jsx';
import useSessionTimeout from './hooks/useSessionTimeout.js';
import SessionTimeoutWarning from './components/SessionTimeoutWarning.jsx';

function MainLayout() {
  // Initialize session timeout monitoring
  useSessionTimeout(60); // 60 minutes of inactivity

  return (
    <>
      <SessionTimeoutWarning timeoutMinutes={60} warningSeconds={300} />
      <Navbar />
      <main className="pt-20">
        <Outlet />
      </main>
      <Footer />
    </>
  );
}

export default function App() {
  return (
    <Routes>
      <Route element={<MainLayout />}>
        <Route path="/" element={<Home />} />
        <Route path="/Dashboard" element={
          <ProtectedRoute allowedRoles={["user"]}>
            <Dashboard />
          </ProtectedRoute>
        } />
        <Route path="/dashboard/bills" element={
          <ProtectedRoute allowedRoles={["user"]}>
            <Bills />
          </ProtectedRoute>
        } />
        <Route path="/dashboard/rewards" element={
          <ProtectedRoute allowedRoles={["user"]}>
            <Rewards />
          </ProtectedRoute>
        } />
        <Route path="/dashboard/currency" element={
          <ProtectedRoute allowedRoles={["user"]}>
            <Currency />
          </ProtectedRoute>
        } />
        <Route path="/dashboard/alerts" element={
          <ProtectedRoute allowedRoles={["user"]}>
            <AlertCenter />
          </ProtectedRoute>
        } />
        <Route path="/dashboard/insights" element={
          <ProtectedRoute allowedRoles={["user"]}>
            <InsightsDashboard />
          </ProtectedRoute>
        } />
        <Route path="/Services" element={<Services />} />
        <Route path="/Analytics" element={<Analytics />} />
        <Route path="/Support" element={<Support />} />
        <Route path="/AdminDashboard" element={
          <ProtectedRoute allowedRoles={["admin"]}>
            <AdminDashboard />
          </ProtectedRoute>
        } />
      </Route>

      <Route path="/login" element={<Login />} />
      <Route path="/forgot-password" element={<ForgotPassword />} />
      <Route path="/reset-password" element={<ResetPassword />} />

    </Routes>
  );
}
