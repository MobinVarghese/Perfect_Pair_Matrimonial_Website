import React from 'react';
import { Navigate } from 'react-router-dom';
import { isAuthenticated } from '../api/api';

const ProtectedRoute = ({ children, adminOnly = false }) => {
  const authenticated = isAuthenticated();

  if (!authenticated) {
    return <Navigate to="/login" replace />;
  }

  // For admin-only routes, you might want to check user role
  // This would require fetching the current user or storing role in localStorage
  if (adminOnly) {
    // You can add admin check logic here
    // For now, we'll allow if authenticated
  }

  return children;
};

export default ProtectedRoute;
