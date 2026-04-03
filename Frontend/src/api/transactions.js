import axiosClient from "../utils/axiosClient";

export const getTransactions = async (accountId, skip = 0, limit = 100) => {
  try {
    const response = await axiosClient.get(
      `/accounts/transactions/`,
      { params: { account_id: accountId, skip, limit } }
    );
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

export const getTransaction = async (accountId, transactionId) => {
  // Note: Backend doesn't have a specific GET /accounts/transactions/{id} yet,
  // but we align the path for consistency if needed later.
  try {
    const response = await axiosClient.get(
      `/accounts/transactions/${transactionId}`
    );
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

export const createTransaction = async (accountId, transactionData) => {
  try {
    const response = await axiosClient.post(
      `/accounts/transactions/`,
      { ...transactionData, account_id: accountId }
    );
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

export const importCSV = async (accountId, file) => {
  try {
    const formData = new FormData();
    formData.append("file", file);

    const response = await axiosClient.post(
      `/transactions/${accountId}/import-csv`,
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      }
    );

    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};
