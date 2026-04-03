import axiosClient from "../utils/axiosClient";
import { getUserIdFromAuth } from "../utils/authUser";

export const getCashFlow = async () => {
  const userId = getUserIdFromAuth();
  try {
    const response = await axiosClient.get(`/insights/cashflow?user_id=${userId}`);
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

export const getCategorySpend = async () => {
  const userId = getUserIdFromAuth();
  try {
    const response = await axiosClient.get(`/insights/category-spend?user_id=${userId}`);
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

export const getTopMerchants = async () => {
  const userId = getUserIdFromAuth();
  try {
    const response = await axiosClient.get(`/insights/top-merchants?user_id=${userId}`);
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

export const getBudgetBurnRate = async () => {
  const userId = getUserIdFromAuth();
  try {
    const response = await axiosClient.get(`/insights/burn-rate?user_id=${userId}`);
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};