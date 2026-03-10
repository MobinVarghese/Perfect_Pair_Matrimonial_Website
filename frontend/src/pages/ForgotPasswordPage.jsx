import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { submitPasswordResetRequest } from '../api/api';

const ForgotPasswordPage = () => {
  const [formData, setFormData] = useState({
    email: '',
    reason: ''
  });
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      await submitPasswordResetRequest(formData);
      setSuccess(true);
    } catch (err) {
      console.error('Password reset request error:', err);
      setError(
        err.response?.data?.detail ||
        err.response?.data?.error ||
        'Failed to submit request. Please try again.'
      );
    } finally {
      setLoading(false);
    }
  };

  if (success) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-pink-50 via-red-50 to-orange-50 flex items-center justify-center px-4">
        <div className="max-w-md w-full bg-white p-10 rounded-2xl shadow-2xl">
          <div className="text-center">
            <div className="mx-auto h-20 w-20 bg-green-100 rounded-full flex items-center justify-center mb-4">
              <svg className="h-12 w-12 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
              </svg>
            </div>
            <h2 className="text-3xl font-extrabold text-gray-900 mb-4">Request Submitted!</h2>
            <div className="bg-green-50 border-l-4 border-green-500 p-4 rounded-lg mb-6">
              <p className="text-sm text-green-800">
                Your password reset request has been sent to our admin team.
              </p>
            </div>
            <div className="text-left space-y-3 mb-6">
              <h3 className="font-semibold text-gray-900">What happens next?</h3>
              <ul className="space-y-2 text-sm text-gray-600">
                <li>1. Admin will review your request</li>
                <li>2. New password will be sent to your email</li>
                <li>3. Login and change your password</li>
              </ul>
            </div>
            <Link
              to="/login"
              className="inline-flex w-full justify-center py-3 px-4 rounded-lg text-white bg-gradient-to-r from-red-600 to-pink-600 hover:from-red-700 hover:to-pink-700"
            >
              Back to Login
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-50 via-red-50 to-orange-50 flex items-center justify-center px-4">
      <div className="max-w-md w-full bg-white p-10 rounded-2xl shadow-2xl">
        <div className="text-center mb-8">
          <div className="mx-auto h-16 w-16 bg-gradient-to-br from-red-100 to-pink-100 rounded-full flex items-center justify-center mb-4">
            <svg className="h-10 w-10 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z"></path>
            </svg>
          </div>
          <h2 className="text-3xl font-extrabold text-gray-900 mb-2">Forgot Password?</h2>
          <p className="text-sm text-gray-600">Submit a request and our admin will help reset your password.</p>
        </div>

        {error && (
          <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded-lg mb-6">
            <p className="text-sm text-red-700">{error}</p>
          </div>
        )}

        <div className="bg-blue-50 border-l-4 border-blue-500 p-4 rounded-lg mb-6">
          <p className="text-sm text-blue-700">
            <strong>How it works:</strong> Admin will review your request and send a new password to your email.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
              Registered Email Address *
            </label>
            <input
              id="email"
              name="email"
              type="email"
              value={formData.email}
              onChange={handleChange}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
              placeholder="Enter your registered email"
              required
            />
          </div>

          <div>
            <label htmlFor="reason" className="block text-sm font-medium text-gray-700 mb-2">
              Reason (Optional)
            </label>
            <textarea
              id="reason"
              name="reason"
              rows="3"
              value={formData.reason}
              onChange={handleChange}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent resize-none"
              placeholder="E.g., Forgot password"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 px-4 rounded-lg text-white bg-gradient-to-r from-red-600 to-pink-600 hover:from-red-700 hover:to-pink-700 disabled:opacity-50 transition"
          >
            {loading ? 'Submitting...' : 'Submit Request'}
          </button>

          <div className="text-center">
            <Link to="/login" className="text-sm text-red-600 hover:text-red-500">
               Back to Login
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ForgotPasswordPage;