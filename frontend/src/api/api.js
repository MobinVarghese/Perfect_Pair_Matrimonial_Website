/**
 * API Service Module
 * Centralized API calls for PerfectPair
 * 
 * Features:
 * - Axios instance with base URL configuration
 * - Automatic JWT token injection for all requests
 * - Token refresh on 401 errors
 * - Centralized error handling
 */

import axios from 'axios';

// Base URL for API - can be overridden with environment variable
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

console.log('API Base URL:', API_BASE_URL);

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 second timeout
});

// Request interceptor to add JWT token to requests
api.interceptors.request.use(
  (config) => {
    // Get JWT token from localStorage
    const token = localStorage.getItem('access_token');
    
    // Add Authorization header if token exists
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
      console.log('Added JWT token to request:', config.url);
    }
    
    return config;
  },
  (error) => {
    console.error('Request interceptor error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // If 401 error and not already retried, try to refresh token
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        if (refreshToken) {
          const response = await axios.post(`${API_BASE_URL}/api/token/refresh/`, {
            refresh: refreshToken,
          });

          const { access } = response.data;
          localStorage.setItem('access_token', access);

          // Retry original request with new token
          originalRequest.headers.Authorization = `Bearer ${access}`;
          return api(originalRequest);
        }
      } catch (refreshError) {
        // Refresh failed, logout user
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

// ===================== Authentication APIs =====================

/**
 * User Registration
 */
export const register = async (userData) => {
  const response = await api.post('/api/register/', userData);
  return response.data;
};

/**
 * User Login
 */
export const login = async (credentials) => {
  const response = await api.post('/api/token/', credentials);
  const { access, refresh } = response.data;
  
  // Store tokens
  localStorage.setItem('access_token', access);
  localStorage.setItem('refresh_token', refresh);
  
  return response.data;
};

/**
 * User Logout
 */
export const logout = () => {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  window.location.href = '/login';
};

/**
 * Verify JWT Token
 */
export const verifyToken = async (token) => {
  const response = await api.post('/api/token/verify/', { token });
  return response.data;
};

/**
 * Refresh JWT Token
 */
export const refreshToken = async (refresh) => {
  const response = await api.post('/api/token/refresh/', { refresh });
  return response.data;
};

// ===================== OTP Verification APIs =====================

/**
 * Request OTP
 */
export const requestOTP = async (email) => {
  const response = await api.post('/api/otp/request/', { email });
  return response.data;
};

/**
 * Verify OTP
 */
export const verifyOTP = async (email, otp) => {
  const response = await api.post('/api/otp/verify/', { email, otp });
  return response.data;
};

// ===================== User Profile APIs =====================

/**
 * Get Current User Profile
 */
export const getCurrentUser = async () => {
  const response = await api.get('/api/users/me/');
  return response.data;
};

/**
 * Update User Profile
 */
export const updateProfile = async (profileData) => {
  const response = await api.patch('/api/users/me/', profileData);
  return response.data;
};

/**
 * Update Profile with FormData (for file uploads)
 */
export const updateProfileWithFiles = async (formData) => {
  const response = await api.patch('/api/users/me/update/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

/**
 * Change Password
 */
export const changePassword = async (passwordData) => {
  const response = await api.put('/api/users/users/change-password/', passwordData);
  return response.data;
};

// ===================== Profile APIs =====================

/**
 * Get All Profiles
 */
export const getProfiles = async (params = {}) => {
  const response = await api.get('/api/profiles/', { params });
  return response.data;
};

/**
 * Get Profile by ID
 */
export const getProfileById = async (id) => {
  const response = await api.get(`/api/profiles/${id}/`);
  return response.data;
};

/**
 * Search Profiles
 */
export const searchProfiles = async (searchParams) => {
  const response = await api.get('/api/profiles/', { params: searchParams });
  return response.data;
};

/**
 * Get Recommended Profiles
 */
export const getRecommendedProfiles = async () => {
  const response = await api.get('/api/profiles/recommendations/');
  return response.data;
};

// ===================== Interest APIs =====================

/**
 * Send Interest to a Profile
 */
export const sendInterest = async (receiverId, message = '') => {
  const response = await api.post('/api/interests/', {
    receiver: receiverId,
    message,
  });
  return response.data;
};

/**
 * Get Sent Interests
 */
export const getSentInterests = async () => {
  const response = await api.get('/api/interests/sent/');
  return response.data;
};

/**
 * Get Received Interests
 */
export const getReceivedInterests = async () => {
  const response = await api.get('/api/interests/received/');
  return response.data;
};

/**
 * Respond to Interest (Accept/Reject)
 */
export const respondToInterest = async (interestId, status) => {
  const response = await api.post(`/api/interests/${interestId}/respond/`, { status });
  return response.data;
};

/**
 * Cancel/Withdraw Interest
 */
export const cancelInterest = async (interestId) => {
  const response = await api.delete(`/api/interests/${interestId}/`);
  return response.data;
};

/**
 * Check Interest Status with a Profile
 */
export const checkInterestStatus = async (profileId) => {
  const response = await api.get(`/api/interests/check/${profileId}/`);
  return response.data;
};

// ===================== Favorite APIs =====================

/**
 * Toggle Favorite Status (Add/Remove)
 */
export const toggleFavorite = async (profileId) => {
  const response = await api.post(`/api/favorites/toggle/${profileId}/`);
  return response.data;
};

/**
 * Check if Profile is Favorited
 */
export const checkFavoriteStatus = async (profileId) => {
  const response = await api.get(`/api/favorites/check/${profileId}/`);
  return response.data;
};

/**
 * Get My Favorites
 */
export const getMyFavorites = async () => {
  const response = await api.get('/api/favorites/my-favorites/');
  return response.data;
};

/**
 * Get All Favorites (with pagination)
 */
export const getAllFavorites = async () => {
  const response = await api.get('/api/favorites/');
  return response.data;
};

// ===================== Report APIs =====================

/**
 * Report a Profile
 */
export const reportProfile = async (reportData) => {
  const response = await api.post('/api/reports/', reportData);
  return response.data;
};

/**
 * Get My Reports
 */
export const getMyReports = async () => {
  const response = await api.get('/api/reports/my-reports/');
  return response.data;
};

// ===================== Admin APIs =====================

/**
 * Get All Users (Admin only)
 */
export const getAllUsers = async (params = {}) => {
  const response = await api.get('/api/users/', { params });
  return response.data;
};

/**
 * Get All Reports (Admin only)
 */
export const getAllReports = async (params = {}) => {
  const response = await api.get('/api/reports/', { params });
  return response.data;
};

/**
 * Review Report (Admin only)
 */
export const reviewReport = async (reportId, reviewData) => {
  const response = await api.post(`/api/reports/${reportId}/review/`, reviewData);
  return response.data;
};

/**
 * Export Profiles to PDF (Admin only)
 */
export const exportProfilesPDF = async (filters = {}) => {
  const params = new URLSearchParams(filters);
  const response = await api.get(`/api/export/profiles/pdf/?${params}`, {
    responseType: 'blob',
  });
  
  // Create blob URL and open in new tab
  const url = window.URL.createObjectURL(new Blob([response.data], { type: 'application/pdf' }));
  window.open(url, '_blank');
  
  // Clean up the URL after a short delay
  setTimeout(() => window.URL.revokeObjectURL(url), 100);
  
  return response.data;
};

/**
 * Export Profiles to Excel (Admin only)
 */
export const exportProfilesExcel = async (filters = {}) => {
  const params = new URLSearchParams(filters);
  const response = await api.get(`/api/export/profiles/excel/?${params}`, {
    responseType: 'blob',
  });
  
  // Create blob URL and open in new tab (Excel will auto-download)
  const url = window.URL.createObjectURL(new Blob([response.data], { 
    type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' 
  }));
  window.open(url, '_blank');
  
  // Clean up the URL after a short delay
  setTimeout(() => window.URL.revokeObjectURL(url), 100);
  
  return response.data;
};

/**
 * Get Export Logs (Admin only)
 */
export const getExportLogs = async (params = {}) => {
  const response = await api.get('/api/export-logs/', { params });
  return response.data;
};

/**
 * Block a user (Admin only)
 */
export const blockUser = async (userId, reason) => {
  const response = await api.post(`/api/users/${userId}/block/`, {
    action: 'block',
    reason: reason,
  });
  return response.data;
};

/**
 * Unblock a user (Admin only)
 */
export const unblockUser = async (userId) => {
  const response = await api.post(`/api/users/${userId}/block/`, {
    action: 'unblock',
  });
  return response.data;
};

// ===================== Password Reset Request APIs =====================

/**
 * Submit password reset request (User)
 */
export const submitPasswordResetRequest = async (requestData) => {
  const response = await api.post('/api/password-reset-requests/', requestData);
  return response.data;
};

/**
 * Get all password reset requests (Admin only)
 */
export const getPasswordResetRequests = async (params = {}) => {
  const response = await api.get('/api/password-reset-requests/', { params });
  return response.data;
};

/**
 * Approve password reset request (Admin only)
 */
export const approvePasswordResetRequest = async (requestId, adminNotes = '') => {
  const response = await api.post(`/api/password-reset-requests/${requestId}/approve/`, {
    admin_notes: adminNotes,
  });
  return response.data;
};

/**
 * Reject password reset request (Admin only)
 */
export const rejectPasswordResetRequest = async (requestId, adminNotes = '') => {
  const response = await api.post(`/api/password-reset-requests/${requestId}/reject/`, {
    admin_notes: adminNotes,
  });
  return response.data;
};

// ===================== Feedback APIs =====================

/**
 * Submit new feedback
 */
export const submitFeedback = async (feedbackData) => {
  const response = await api.post('/api/feedback/', feedbackData);
  return response.data;
};

/**
 * Get current user's feedback
 */
export const getUserFeedback = async () => {
  const response = await api.get('/api/feedback/');
  return response.data;
};

/**
 * Get all feedback (Admin only)
 */
export const getAllFeedback = async (params = {}) => {
  const response = await api.get('/api/feedback/', { params });
  return response.data;
};

/**
 * Respond to feedback (Admin only)
 */
export const respondToFeedback = async (feedbackId, responseData) => {
  const response = await api.post(`/api/feedback/${feedbackId}/respond/`, responseData);
  return response.data;
};

/**
 * Update feedback status (Admin only)
 */
export const updateFeedbackStatus = async (feedbackId, status) => {
  const response = await api.patch(`/api/feedback/${feedbackId}/update_status/`, { status });
  return response.data;
};

// ===================== Utility Functions =====================

/**
 * Check if user is authenticated
 */
export const isAuthenticated = () => {
  return !!localStorage.getItem('access_token');
};

/**
 * Get stored access token
 */
export const getAccessToken = () => {
  return localStorage.getItem('access_token');
};

/**
 * Get stored refresh token
 */
export const getRefreshToken = () => {
  return localStorage.getItem('refresh_token');
};

export default api;
