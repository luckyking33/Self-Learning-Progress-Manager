import axios from "axios";

import { clearAccessToken, getAccessToken } from "@/utils/auth";

const client = axios.create({
  baseURL: "/api/v1",
  timeout: 6000,
});

client.interceptors.request.use((config) => {
  const token = getAccessToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

client.interceptors.response.use(
  (response) => response,
  (error) => {
    const status = error.response?.status as number | undefined;
    const message =
      error.response?.data?.detail ??
      error.response?.data?.message ??
      error.message ??
      "请求失败，请稍后重试。";

    if (status === 401) {
      clearAccessToken();
      const currentPath = `${window.location.pathname}${window.location.search}`;
      const needsRedirect =
        currentPath.startsWith("/learning") || currentPath.startsWith("/settings");

      if (
        needsRedirect &&
        !window.location.pathname.startsWith("/login") &&
        !window.location.pathname.startsWith("/register")
      ) {
        const redirect = encodeURIComponent(currentPath);
        window.location.assign(`/login?redirect=${redirect}`);
      }
    }

    const wrappedError = new Error(message) as Error & { status?: number };
    wrappedError.status = status;
    return Promise.reject(wrappedError);
  },
);

export default client;
