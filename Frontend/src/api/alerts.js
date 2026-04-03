import axiosClient from "../utils/axiosClient";
import { getUserIdFromAuth } from "../utils/authUser";

export const getAlerts = async () => {
  const userId = getUserIdFromAuth();
  try {
    const response = await axiosClient.get(`/alerts/?user_id=${userId}`);
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

export const markAlertRead = async (alertId) => {
  const userId = getUserIdFromAuth();
  try {
    const response = await axiosClient.post("/alerts/mark-read", { user_id: userId, alert_ids: [alertId], mark_all: false });
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

export const getUnreadCount = async () => {
  const userId = getUserIdFromAuth();
  try {
    const response = await axiosClient.get(`/alerts/unread?user_id=${userId}`);
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};