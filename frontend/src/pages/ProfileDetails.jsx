import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { getProfileById, sendInterest, getCurrentUser, checkInterestStatus, reportProfile } from '../api/api';
import Navbar from '../components/Navbar';

const ProfileDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [profile, setProfile] = useState(null);
  const [currentUser, setCurrentUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [sendingInterest, setSendingInterest] = useState(false);
  const [notification, setNotification] = useState('');
  const [interestStatus, setInterestStatus] = useState(null);
  const [canViewContact, setCanViewContact] = useState(false);
  const [reportSent, setReportSent] = useState(false);
  const [sendingReport, setSendingReport] = useState(false);
  const [showReportModal, setShowReportModal] = useState(false);
  const [reportReason, setReportReason] = useState('inappropriate_content');
  const [reportDescription, setReportDescription] = useState('');

  useEffect(() => {
    fetchProfile();
    fetchCurrentUser();
    fetchInterestStatus();
  }, [id]);

  const fetchProfile = async () => {
    try {
      const data = await getProfileById(id);
      setProfile(data);
    } catch (error) {
      console.error('Error fetching profile:', error);
      setNotification('Failed to load profile');
    } finally {
      setLoading(false);
    }
  };

  const fetchCurrentUser = async () => {
    try {
      const user = await getCurrentUser();
      setCurrentUser(user);
    } catch (error) {
      console.error('Error fetching current user:', error);
    }
  };

  const fetchInterestStatus = async () => {
    try {
      const status = await checkInterestStatus(id);
      setInterestStatus(status);
      setCanViewContact(status.can_view_contact);
    } catch (error) {
      console.error('Error fetching interest status:', error);
    }
  };

  const calculateAge = (dob) => {
    if (!dob) return 'N/A';
    const birthDate = new Date(dob);
    const today = new Date();
    let age = today.getFullYear() - birthDate.getFullYear();
    const monthDiff = today.getMonth() - birthDate.getMonth();
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
      age--;
    }
    return age;
  };

  const handleSendInterest = async () => {
    setSendingInterest(true);
    try {
      // Send interest using USER ID, not PROFILE ID
      await sendInterest(profile.user);
      setNotification('Interest sent successfully! Wait for them to accept.');
      setTimeout(() => setNotification(''), 3000);
      // Refresh interest status
      await fetchInterestStatus();
    } catch (error) {
      console.error('Error sending interest:', error);
      if (error.response?.data?.error) {
        setNotification(error.response.data.error);
      } else {
        setNotification('Failed to send interest. Try again.');
      }
      setTimeout(() => setNotification(''), 3000);
    } finally {
      setSendingInterest(false);
    }
  };

  const handleReportClick = () => {
    if (reportSent) return;
    setShowReportModal(true);
  };

  const handleReportSubmit = async () => {
    if (reportSent || sendingReport) return;
    
    // Validate description
    if (!reportDescription.trim() || reportDescription.trim().length < 20) {
      setNotification('Please provide a detailed reason (at least 20 characters).');
      setTimeout(() => setNotification(''), 3000);
      return;
    }
    
    setSendingReport(true);
    try {
      // Send report with USER ID
      await reportProfile({
        reported_user: profile.user,
        reason: reportReason,
        description: reportDescription.trim()
      });
      setReportSent(true);
      setShowReportModal(false);
      setNotification('Report submitted successfully. Admin will review it.');
      setTimeout(() => setNotification(''), 3000);
    } catch (error) {
      console.error('Error sending report:', error);
      if (error.response?.data?.error) {
        setNotification(error.response.data.error);
      } else if (error.response?.data) {
        // Show detailed error message
        const errorMsg = JSON.stringify(error.response.data);
        setNotification(`Failed to submit report: ${errorMsg}`);
      } else {
        setNotification('Failed to submit report. Try again.');
      }
      setTimeout(() => setNotification(''), 3000);
    } finally {
      setSendingReport(false);
    }
  };

  const handleReportCancel = () => {
    setShowReportModal(false);
    setReportDescription('');
    setReportReason('inappropriate_content');
  };

  const isOwnProfile = currentUser && profile && currentUser.id === profile.user;

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <div className="flex justify-center items-center py-20">
          <svg className="animate-spin h-12 w-12 text-red-600" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
        </div>
      </div>
    );
  }

  if (!profile) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <div className="max-w-4xl mx-auto px-4 py-20 text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Profile Not Found</h2>
          <Link to="/home" className="text-red-600 hover:text-red-700 font-medium">
            ← Back to Home
          </Link>
        </div>
      </div>
    );
  }

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

      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Back Button */}
        <button
          onClick={() => navigate(-1)}
          className="mb-6 flex items-center text-gray-600 hover:text-gray-900 transition duration-150"
        >
          <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
          Back
        </button>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - Profile Image & Quick Actions */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-xl shadow-md overflow-hidden sticky top-6">
              {/* Profile Image */}
              <div className="relative h-80 bg-gradient-to-br from-pink-100 to-red-100">
                {profile.profile_picture ? (
                  <img
                    src={profile.profile_picture}
                    alt={profile.first_name}
                    className="w-full h-full object-cover"
                  />
                ) : (
                  <div className="flex items-center justify-center h-full">
                    <svg className="w-32 h-32 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clipRule="evenodd" />
                    </svg>
                  </div>
                )}
              </div>

              {/* Quick Info */}
              <div className="p-6">
                <h1 className="text-2xl font-bold text-gray-900 mb-1">
                  {profile.first_name} {profile.last_name}
                </h1>
                <p className="text-gray-600 mb-4">{calculateAge(profile.date_of_birth)} years old</p>

                {/* Action Buttons */}
                {isOwnProfile ? (
                  <Link
                    to="/edit-profile"
                    className="w-full bg-gradient-to-r from-red-600 to-pink-600 text-white px-4 py-3 rounded-lg hover:from-red-700 hover:to-pink-700 transition duration-150 font-medium text-center block"
                  >
                    Edit Profile
                  </Link>
                ) : (
                  <div className="space-y-3">
                    {/* Interest Status Display */}
                    {interestStatus?.has_interest && interestStatus.status === 'pending' && (
                      <div className="bg-blue-50 border-l-4 border-blue-500 p-3 rounded">
                        <p className="text-sm text-blue-800 font-medium">
                          {interestStatus.is_sender ? '⏳ Interest Sent - Waiting for Response' : '📬 You have a pending interest from this user'}
                        </p>
                      </div>
                    )}
                    
                    {interestStatus?.has_interest && interestStatus.status === 'accepted' && (
                      <div className="bg-green-50 border-l-4 border-green-500 p-3 rounded">
                        <p className="text-sm text-green-800 font-medium">
                          ✅ Interest Accepted - You can now contact each other!
                        </p>
                      </div>
                    )}
                    
                    {interestStatus?.has_interest && interestStatus.status === 'rejected' && (
                      <div className="bg-red-50 border-l-4 border-red-500 p-3 rounded">
                        <p className="text-sm text-red-800 font-medium">
                          ❌ Interest was not accepted
                        </p>
                      </div>
                    )}

                    {/* Interest Button - Shows different states based on interest status */}
                    {!interestStatus?.has_interest ? (
                      // No interest sent yet - Show Send Interest button
                      <button
                        onClick={handleSendInterest}
                        disabled={sendingInterest}
                        className="w-full bg-gradient-to-r from-red-600 to-pink-600 text-white px-4 py-3 rounded-lg hover:from-red-700 hover:to-pink-700 transition duration-150 font-medium disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
                      >
                        {sendingInterest ? (
                          <svg className="animate-spin h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                          </svg>
                        ) : (
                          <>
                            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                            </svg>
                            Send Interest
                          </>
                        )}
                      </button>
                    ) : interestStatus.status === 'accepted' ? (
                      // Interest accepted - Show success state
                      <button
                        disabled
                        className="w-full bg-gradient-to-r from-green-600 to-emerald-600 text-white px-4 py-3 rounded-lg font-medium cursor-not-allowed flex items-center justify-center"
                      >
                        <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        Interest Accepted
                      </button>
                    ) : (
                      // Interest sent (pending or rejected) - Show Request Sent (disabled, cannot resend)
                      <button
                        disabled
                        className="w-full bg-gradient-to-r from-gray-500 to-gray-600 text-white px-4 py-3 rounded-lg font-medium cursor-not-allowed flex items-center justify-center"
                      >
                        <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        Request Sent
                      </button>
                    )}
                    {!reportSent ? (
                      <button
                        onClick={handleReportClick}
                        disabled={sendingReport}
                        className="w-full border-2 border-gray-300 text-gray-700 px-4 py-3 rounded-lg hover:bg-gray-50 transition duration-150 font-medium flex items-center justify-center"
                      >
                        <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                        </svg>
                        Report Profile
                      </button>
                    ) : (
                      <button
                        disabled
                        className="w-full bg-gradient-to-r from-orange-500 to-orange-600 text-white px-4 py-3 rounded-lg font-medium cursor-not-allowed flex items-center justify-center"
                      >
                        <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        Report Sent
                      </button>
                    )}
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Right Column - Detailed Information */}
          <div className="lg:col-span-2 space-y-6">
            {/* Basic Information */}
            <div className="bg-white rounded-xl shadow-md p-6">
              <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
                <svg className="w-6 h-6 mr-2 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
                Basic Information
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <InfoItem label="Gender" value={profile.gender} />
                <InfoItem label="Age" value={profile.age ? `${profile.age} years` : 'N/A'} />
                <InfoItem label="Height" value={profile.height ? `${profile.height} ft` : 'N/A'} />
              </div>
            </div>

            {/* Professional Information */}
            <div className="bg-white rounded-xl shadow-md p-6">
              <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
                <svg className="w-6 h-6 mr-2 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
                Professional & Educational Details
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <InfoItem label="Education" value={profile.education} />
                <InfoItem label="Occupation" value={profile.occupation} />
              </div>
            </div>

            {/* Contact & Location */}
            <div className="bg-white rounded-xl shadow-md p-6">
              <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
                <svg className="w-6 h-6 mr-2 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                Location & Contact
              </h2>
              <div className="space-y-4">
                <InfoItem label="Location" value={profile.location} />
                
                {/* Mobile Number - Only visible if interest is accepted or own profile */}
                {isOwnProfile ? (
                  <InfoItem label="Mobile Number" value={profile.mobile_number} />
                ) : canViewContact ? (
                  <div>
                    <div className="bg-green-50 border-l-4 border-green-500 p-4 rounded">
                      <div className="flex items-center">
                        <svg className="w-5 h-5 text-green-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                        </svg>
                        <div>
                          <p className="text-sm text-green-800 font-medium">Contact Information Available</p>
                          <p className="text-lg text-green-900 font-semibold">{profile.mobile_number || 'Not provided'}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                ) : (
                  <div>
                    <div className="bg-yellow-50 border-l-4 border-yellow-500 p-4 rounded">
                      <div className="flex items-center">
                        <svg className="w-5 h-5 text-yellow-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                        </svg>
                        <div>
                          <p className="text-sm text-yellow-800 font-medium">Contact Information Hidden</p>
                          <p className="text-xs text-yellow-700">Send an interest request and wait for acceptance to view contact details</p>
                        </div>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* About */}
            {profile.about && (
              <div className="bg-white rounded-xl shadow-md p-6">
                <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
                  <svg className="w-6 h-6 mr-2 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  About
                </h2>
                <p className="text-gray-700 leading-relaxed whitespace-pre-line">{profile.about}</p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Report Modal */}
      {showReportModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl shadow-2xl max-w-md w-full p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Report Profile</h2>
            
            {/* Reason Selection */}
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Reason for Reporting *
              </label>
              <select
                value={reportReason}
                onChange={(e) => setReportReason(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-red-500"
              >
                <option value="inappropriate_content">Inappropriate Content</option>
                <option value="fake_profile">Fake Profile</option>
                <option value="harassment">Harassment</option>
                <option value="spam">Spam</option>
                <option value="other">Other</option>
              </select>
            </div>

            {/* Description */}
            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Description * (minimum 20 characters)
              </label>
              <textarea
                value={reportDescription}
                onChange={(e) => setReportDescription(e.target.value)}
                placeholder="Please provide details about why you're reporting this profile..."
                rows="4"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-red-500 resize-none"
              />
              <p className="text-sm text-gray-500 mt-1">
                {reportDescription.length}/20 characters minimum
              </p>
            </div>

            {/* Buttons */}
            <div className="flex space-x-3">
              <button
                onClick={handleReportCancel}
                disabled={sendingReport}
                className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition duration-150 font-medium"
              >
                Cancel
              </button>
              <button
                onClick={handleReportSubmit}
                disabled={sendingReport || reportDescription.trim().length < 20}
                className={`flex-1 px-4 py-2 rounded-lg transition duration-150 font-medium ${
                  sendingReport || reportDescription.trim().length < 20
                    ? 'bg-gray-400 text-white cursor-not-allowed'
                    : 'bg-gradient-to-r from-red-600 to-red-700 text-white hover:from-red-700 hover:to-red-800'
                }`}
              >
                {sendingReport ? 'Submitting...' : 'Submit Report'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

const InfoItem = ({ label, value }) => (
  <div>
    <p className="text-sm text-gray-600 mb-1">{label}</p>
    <p className="text-gray-900 font-medium">{value || 'Not specified'}</p>
  </div>
);

export default ProfileDetails;
