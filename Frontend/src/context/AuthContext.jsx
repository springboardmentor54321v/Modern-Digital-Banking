import React, { createContext, useContext, useEffect, useState, useCallback } from "react";
import { getMe } from "../api/users";

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [loading, setLoading] = useState(true);
  const [lastActivity, setLastActivity] = useState(Date.now());

  useEffect(() => {
    const token = localStorage.getItem("access_token");

    if (token) {
      getMe()
        .then((data) => { setUser(data); setIsLoggedIn(true); })

        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  const loginUser = useCallback(async (authResponse) => {
    const { access_token, refresh_token, user } = authResponse;

    localStorage.setItem("access_token", access_token);
    localStorage.setItem("refresh_token", refresh_token);
    setIsLoggedIn(true);
    setLastActivity(Date.now()); // Reset activity timer on login
    const me = await getMe();
    setUser(me);
    localStorage.setItem("user", JSON.stringify(me));
    return me;
  }, []);

  const logoutUser = useCallback(() => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("user");

    setUser(null);
    setIsLoggedIn(false);
    setLastActivity(null);
  }, []);

  return (
    <AuthContext.Provider
      value={{
        isLoggedIn,
        user,
        loginUser,
        logoutUser,
        loading,
        lastActivity,
        setLastActivity,
      }}
    >
      {!loading && children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used inside AuthProvider");
  }
  return context;
};
