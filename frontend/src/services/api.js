import axios from "axios";

const API_BASE_URL = process.env.REACT_APP_API_URL || "http://127.0.0.1:8000/api";

const api = axios.create({ baseURL: API_BASE_URL });

// Attach the access token to every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// On a 401, try refreshing the access token once, then retry the original request
let isRefreshing = false;
let queue = [];

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      const refreshToken = localStorage.getItem("refresh_token");
      if (!refreshToken) {
        localStorage.clear();
        window.location.href = "/login";
        return Promise.reject(error);
      }

      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          queue.push({ resolve, reject });
        }).then((token) => {
          originalRequest.headers.Authorization = `Bearer ${token}`;
          return api(originalRequest);
        });
      }

      originalRequest._retry = true;
      isRefreshing = true;
      try {
        const { data } = await axios.post(`${API_BASE_URL}/auth/token/refresh/`, {
          refresh: refreshToken,
        });
        localStorage.setItem("access_token", data.access);
        queue.forEach((p) => p.resolve(data.access));
        queue = [];
        originalRequest.headers.Authorization = `Bearer ${data.access}`;
        return api(originalRequest);
      } catch (refreshError) {
        queue.forEach((p) => p.reject(refreshError));
        queue = [];
        localStorage.clear();
        window.location.href = "/login";
        return Promise.reject(refreshError);
      } finally {
        isRefreshing = false;
      }
    }
    return Promise.reject(error);
  }
);

export default api;
