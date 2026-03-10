import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { getReceivedInterests, respondToInterest } from '../api/api';
import Navbar from '../components/Navbar';

const Notifications = () => {
  const navigate = useNavigate();
  const [interests, setInterests] = useState([]);
  const [loading, setLoading] = useState(true);
  const [respondingTo, setRespondingTo] = useState(null);
  const [notification, setNotification] = useState('');

  useEffect(() => {
    fetchInterests();
  }, []);

  const fetchInterests = async () => {
    setLoading(true);
    try {
      const data = await getReceivedInterests();
      setInterests(Array.isArray(data) ? data : data.results || []);
    } catch (error) {
      console.error('Error fetching interests:', error);
      setNotification('Failed to load notifications');
      setTimeout(() => setNotification(''), 3000);
    } finally {
      setLoading(false);
    }
  };

  const handleRespond = async (interestId, status) => {
    setRespondingTo(interestId);
    try {
      await respondToInterest(interestId, status);
      setNotification(`Interest ${status} successfully!`);
      setTimeout(() => setNotification(''), 3000);
      // Refresh the list
      await fetchInterests();
    } catch (error) {
      console.error('Error responding to interest:', error);
      setNotification('Failed to respond. Try again.');
      setTimeout(() => setNotification(''), 3000);
    } finally {
      setRespondingTo(null);
    }
  };

  const pendingInterests = interests.filter(i => i.status === 'pending');
  const respondedInterests = interests.filter(i => i.status !== 'pending');

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />

      {/* Notification */}
      {notification && (
        <div className="fixed top-20 right-4 z-50 animate-fadeIn">
          <div className="bg-white border-l-4 border-green-500 rounded-lg shadow-lg p-4 max-w-md">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-green-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <p className="text-sm text-gray-700">{notification}</p>
              </div>
            </div>
          </div>
        </div>
      )}

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Notifications</h1>
          <p className="text-gray-600">Manage interest requests from other users</p>
        </div>

        {loading ? (
          <div className="flex justify-center py-20">
            <svg className="animate-spin h-12 w-12 text-red-600" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
          </div>
        ) : interests.length === 0 ? (
          <div className="bg-white rounded-xl shadow-md p-12 text-center">
            <svg className="mx-auto h-16 w-16 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
            </svg>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">No Notifications</h3>
            <p className="text-gray-600 mb-6">You don't have any interest requests yet</p>
            <Link
              to="/home"
              className="inline-block bg-gradient-to-r from-red-600 to-pink-600 text-white px-6 py-3 rounded-lg hover:from-red-700 hover:to-pink-700 transition duration-150 font-medium"
            >
              Browse Profiles
            </Link>
          </div>
        ) : (
          <div className="space-y-6">
            {/* Pending Interests */}
            {pendingInterests.length > 0 && (
              <div>
                <h2 className="text-xl font-bold text-gray-900 mb-4">
                  Pending Requests ({pendingInterests.length})
                </h2>
                <div className="space-y-4">
                  {pendingInterests.map((interest) => (
                    <InterestCard
                      key={interest.id}
                      interest={interest}
                      onRespond={handleRespond}
                      isResponding={respondingTo === interest.id}
                    />
                  ))}
                </div>
              </div>
            )}

            {/* Responded Interests */}
            {respondedInterests.length > 0 && (
              <div>
                <h2 className="text-xl font-bold text-gray-900 mb-4">
                  History ({respondedInterests.length})
                </h2>
                <div className="space-y-4">
                  {respondedInterests.map((interest) => (
                    <InterestCard
                      key={interest.id}
                      interest={interest}
                      isHistory={true}
                    />
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

const InterestCard = ({ interest, onRespond, isResponding, isHistory }) => {
  const senderProfile = interest.sender_profile || {};
  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  return (
    <div className="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-lg transition duration-150">
      <div className="p-6">
        <div className="flex items-start justify-between">
          <div className="flex items-center space-x-4 flex-1">
            {/* Profile Picture */}
            <Link to={`/profile/${senderProfile.id}`} className="flex-shrink-0">
              <div className="relative h-16 w-16 bg-gradient-to-br from-pink-100 to-red-100 rounded-full overflow-hidden">
                {senderProfile.profile_picture ? (
                  <img
                    src={senderProfile.profile_picture}
                    alt={senderProfile.name}
                    className="w-full h-full object-cover"
                  />
                ) : (
                  <div className="flex items-center justify-center h-full">
                    <svg className="w-8 h-8 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clipRule="evenodd" />
                    </svg>
                  </div>
                )}
              </div>
            </Link>

            {/* Interest Details */}
            <div className="flex-1">
              <Link
                to={`/profile/${senderProfile.id}`}
                className="text-lg font-bold text-gray-900 hover:text-red-600 transition"
              >
                {senderProfile.name || interest.sender_username}
              </Link>
              <p className="text-sm text-gray-600">
                {senderProfile.occupation && `${senderProfile.occupation} • `}
                {senderProfile.location}
              </p>
              {interest.message && (
                <p className="mt-2 text-sm text-gray-700 italic">"{interest.message}"</p>
              )}
              <p className="text-xs text-gray-500 mt-1">Sent on {formatDate(interest.created_at)}</p>
            </div>
          </div>

          {/* Status Badge */}
          {isHistory && (
            <div className="ml-4">
              {interest.status === 'accepted' ? (
                <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800">
                  ✓ Accepted
                </span>
              ) : (
                <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-red-100 text-red-800">
                  ✗ Declined
                </span>
              )}
            </div>
          )}
        </div>

        {/* Action Buttons */}
        {!isHistory && (
          <div className="mt-4 flex space-x-3">
            <button
              onClick={() => onRespond(interest.id, 'accepted')}
              disabled={isResponding}
              className="flex-1 bg-gradient-to-r from-green-600 to-green-700 text-white px-4 py-2 rounded-lg hover:from-green-700 hover:to-green-800 transition duration-150 font-medium disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
            >
              {isResponding ? (
                <svg className="animate-spin h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
              ) : (
                <>
                  <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                  </svg>
                  Accept
                </>
              )}
            </button>
            <button
              onClick={() => onRespond(interest.id, 'rejected')}
              disabled={isResponding}
              className="flex-1 bg-white border-2 border-gray-300 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-50 transition duration-150 font-medium disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
            >
              {isResponding ? (
                <svg className="animate-spin h-5 w-5 text-gray-700" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
              ) : (
                <>
                  <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                  Decline
                </>
              )}
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default Notifications;
