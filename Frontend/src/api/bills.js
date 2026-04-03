import axiosClient from "../utils/axiosClient";

const BASE_URL = "/bills/";

export const getBills = async () => {
  const { data } = await axiosClient.get(BASE_URL);
  return data;
};

export const getUpcomingBills = async () => {
  try {
    const { data } = await axiosClient.get(BASE_URL);
    // Filter to only upcoming bills
    return Array.isArray(data) ? data.filter(b => b.status === "upcoming") : [];
  } catch (error) {
    throw error.response?.data?.detail || error.message;
  }
};


export const addBill = async (payload) => {
  const { data } = await axiosClient.post(BASE_URL, payload);
  return data;
};

export const updateBill = async (id, payload) => {
  const { data } = await axiosClient.put(
    `${BASE_URL}${id}`,
    payload
  );
  return data;
};


export const deleteBill = async (id) => {
  await axiosClient.delete(`${BASE_URL}${id}`);
};

export const markPaid = async (id) => {
  const { data } = await axiosClient.post(`${BASE_URL}${id}/mark-paid`);
  return data;
};
