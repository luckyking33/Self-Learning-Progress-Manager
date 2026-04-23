import axios from "axios";

const client = axios.create({
  baseURL: "/api/mock",
  timeout: 6000,
});

client.interceptors.response.use(
  (response) => response,
  (error) => {
    const message =
      error.response?.data?.message ??
      error.message ??
      "请求失败，请稍后重试。";
    return Promise.reject(new Error(message));
  },
);

export default client;
