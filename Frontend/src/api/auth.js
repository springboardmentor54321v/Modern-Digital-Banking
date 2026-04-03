import axiosClient from "../utils/axiosClient";

export const register = async (name, email, password, phone = "", role) => {
  try {
    const response = await axiosClient.post("/auth/register", {
      name,
      email,
      password,
      phone,
      role
    });
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

export const login = async (email, password) => {
  try {
    const formData = new URLSearchParams();
    formData.append("username", email);
    formData.append("password", password);

    const response = await axiosClient.post("/auth/login", formData, {
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
    });
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

export const forgotPassword = async (email) => {
  try {
    const response = await axiosClient.post("/auth/forgot-password", { email });
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

export const resetPassword = async (token, newPassword) => {
  try {
    const response = await axiosClient.post("/auth/reset-password", {
      token,
      new_password: newPassword,
    });
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};
