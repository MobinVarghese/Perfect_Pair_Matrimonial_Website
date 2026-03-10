import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// User API calls
export const userAPI = {
  // Register a new user
  register: (userData) => api.post('/register/', userData),
  
  // Get all users
  getUsers: () => api.get('/users/',),
  
  // Get user by ID
  getUser: (id) => api.get(`/users/${id}/`),
  
  // Get current user
  getCurrentUser: () => api.get('/users/me/'),
  
  // Update user profile
  updateProfile: (profileData) => api.put('/users/profile/', profileData),
  
  // Update user
  updateUser: (id, userData) => api.put(`/users/${id}/`, userData),
  
  // Delete user
  deleteUser: (id) => api.delete(`/users/${id}/`),
};

export default api;
