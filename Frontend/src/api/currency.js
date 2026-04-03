import axiosClient from "../utils/axiosClient";

const BASE_URL = "/currency-rates";

export const getExchangeRates = async () => {
  try {
    const { data } = await axiosClient.get(BASE_URL);
    return data;
  } catch (error) {
    throw error.response?.data?.detail || error.message;
  }
};
