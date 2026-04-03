import axios from "axios";

// pick up base URL from environment (Vite) or fall back to localhost for dev
// NOTE: when running the production build the backend should be reachable at
// the same host/port as the frontend (hence a relative `/api` URL). During
// local development configure VITE_API_BASE_URL in an .env file or let the
// default below point at your local FastAPI server.
const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  (import.meta.env.MODE === "production" ? "" : "http://localhost:8000");

const axiosClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

axiosClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");
    if (token) {
      config.headers = config.headers || {};
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

const refreshAccessToken = async () => {
  const refresh = localStorage.getItem("refresh_token");

  if (!refresh) throw new Error("No refresh token");

  const response = await axios.post(
    // explicit URL because this request is outside of axiosClient instance
    `${API_BASE_URL.replace(/\/$$/, "")}/auth/refresh`,
    { refresh_token: refresh }
  );

  const newAccess = response.data.access_token;
  localStorage.setItem("access_token", newAccess);
  localStorage.setItem("refresh_token", response.data.refresh_token)
  return newAccess;
};

axiosClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // Only try to refresh once, and not on auth endpoints themselves
    if (
      error.response?.status === 401 &&
      !originalRequest._retry &&
      !originalRequest.url.includes("/auth/")
    ) {
      originalRequest._retry = true;

      try {
        const newAccessToken = await refreshAccessToken();
        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
        return axiosClient(originalRequest);
      } catch (refreshError) {
        // Refresh failed — clear everything and force re-login
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        localStorage.removeItem("user");
        window.location.href = "/";
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default axiosClient;
