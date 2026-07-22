import axios from 'axios';

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to attach JWT token securely
api.interceptors.request.use((config) => {
  // We will retrieve the token from the client-side store or cookies later
  return config;
});

export default api;
