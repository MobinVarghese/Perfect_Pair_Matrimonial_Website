import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { logout, getCurrentUser, isAuthenticated, getReceivedInterests } from '../api/api';

const Navbar = () => {
  const navigate = useNavigate();
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isUserMenuOpen, setIsUserMenuOpen] = useState(false);
  const [currentUser, setCurrentUser] = useState(null);
  const [pendingInterestsCount, setPendingInterestsCount] = useState(0);

  useEffect(() => {
    if (isAuthenticated()) {
      fetchCurrentUser();
      fetchPendingInterests();
      
      // Refresh pending interests every 30 seconds
      const interval = setInterval(fetchPendingInterests, 30000);
      return () => clearInterval(interval);
    }
  }, []);

  const fetchCurrentUser = async () => {
    try {
      const user = await getCurrentUser();
      setCurrentUser(user);
    } catch (error) {
      console.error('Error fetching user:', error);
    }
  };

  const fetchPendingInterests = async () => {
    try {
      const interests = await getReceivedInterests();
      const pending = interests.filter(i => i.status === 'pending');
      setPendingInterestsCount(pending.length);
    } catch (error) {
      console.error('Error fetching pending interests:', error);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="bg-white shadow-lg sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          {/* Logo and Brand */}
          <div className="flex items-center">
            <Link to="/home" className="flex items-center">
              <div className="bg-gradient-to-r from-red-600 to-pink-600 rounded-full p-2 mr-3">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                </svg>
              </div>
              <span className="text-2xl font-bold bg-gradient-to-r from-red-600 to-pink-600 bg-clip-text text-transparent">
                PerfectPair
              </span>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-4">
            <Link
              to="/home"
              className="px-3 py-2 rounded-lg text-gray-700 hover:text-red-600 hover:bg-red-50 transition duration-150 font-medium"
            >
              Browse Profiles
            </Link>
            
            {/* Favorites Icon */}
            <Link
              to="/favorites"
              className="px-3 py-2 rounded-lg text-gray-700 hover:text-red-600 hover:bg-red-50 transition duration-150 font-medium"
              title="My Favorites"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
              </svg>
            </Link>
            
            {/* Notifications Icon */}
            <Link
              to="/notifications"
              className="relative px-3 py-2 rounded-lg text-gray-700 hover:text-red-600 hover:bg-red-50 transition duration-150 font-medium"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
              </svg>
              {pendingInterestsCount > 0 && (
                <span className="absolute top-0 right-0 inline-flex items-center justify-center px-2 py-1 text-xs font-bold leading-none text-white transform translate-x-1/2 -translate-y-1/2 bg-red-600 rounded-full">
                  {pendingInterestsCount}
                </span>
              )}
            </Link>
            
            {/* Feedback Icon */}
            <Link
              to="/feedback"
              className="px-3 py-2 rounded-lg text-gray-700 hover:text-red-600 hover:bg-red-50 transition duration-150 font-medium"
              title="Feedback"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
              </svg>
            </Link>
            
            {currentUser?.is_staff && (
              <Link
                to="/admin"
                className="px-3 py-2 rounded-lg text-gray-700 hover:text-red-600 hover:bg-red-50 transition duration-150 font-medium flex items-center"
              >
                <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                Admin
              </Link>
            )}

            {/* User Menu */}
            <div className="relative">
              <button
                onClick={() => setIsUserMenuOpen(!isUserMenuOpen)}
                className="flex items-center space-x-2 px-3 py-2 rounded-lg hover:bg-gray-100 transition duration-150"
              >
                <div className="h-8 w-8 rounded-full bg-gradient-to-br from-red-400 to-pink-500 flex items-center justify-center">
                  <span className="text-white font-semibold text-sm">
                    {currentUser?.first_name?.[0] || currentUser?.username?.[0] || 'U'}
                  </span>
                </div>
                <span className="text-gray-700 font-medium">
                  {currentUser?.first_name || currentUser?.username || 'User'}
                </span>
                <svg className={`w-4 h-4 text-gray-500 transition-transform ${isUserMenuOpen ? 'rotate-180' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>

              {/* Dropdown Menu */}
              {isUserMenuOpen && (
                <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-xl py-1 border border-gray-200 animate-fadeIn">
                  <Link
                    to="/edit-profile"
                    className="block px-4 py-2 text-sm text-gray-700 hover:bg-red-50 hover:text-red-600 transition duration-150"
                    onClick={() => setIsUserMenuOpen(false)}
                  >
                    <div className="flex items-center">
                      <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                      </svg>
                      Edit Profile
                    </div>
                  </Link>
                  <Link
                    to="/feedback"
                    className="block px-4 py-2 text-sm text-gray-700 hover:bg-red-50 hover:text-red-600 transition duration-150"
                    onClick={() => setIsUserMenuOpen(false)}
                  >
                    <div className="flex items-center">
                      <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                      </svg>
                      Feedback
                    </div>
                  </Link>
                  <div className="border-t border-gray-200 my-1"></div>
                  <button
                    onClick={handleLogout}
                    className="block w-full text-left px-4 py-2 text-sm text-red-700 hover:bg-red-50 transition duration-150"
                  >
                    <div className="flex items-center">
                      <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                      </svg>
                      Logout
                    </div>
                  </button>
                </div>
              )}
            </div>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden flex items-center">
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="inline-flex items-center justify-center p-2 rounded-lg text-gray-700 hover:text-red-600 hover:bg-red-50 transition duration-150"
            >
              <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                {isMenuOpen ? (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                ) : (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16" />
                )}
              </svg>
            </button>
          </div>
        </div>

        {/* Mobile Menu */}
        {isMenuOpen && (
          <div className="md:hidden border-t border-gray-200 pb-6 animate-fadeIn bg-gradient-to-br from-gray-50 to-red-50">
            {/* User Profile Section */}
            <div className="pt-6 pb-4 px-4">
              <div className="flex flex-col items-center">
                <div className="h-20 w-20 rounded-full bg-gradient-to-br from-red-400 to-pink-500 flex items-center justify-center shadow-lg">
                  <span className="text-white font-bold text-2xl">
                    {currentUser?.first_name?.[0] || currentUser?.username?.[0] || 'U'}
                  </span>
                </div>
                <div className="mt-3 text-center">
                  <div className="text-lg font-bold text-gray-900">
                    {currentUser?.first_name || currentUser?.username || 'User'}
                  </div>
                  <div className="text-sm text-gray-600">{currentUser?.email}</div>
                </div>
              </div>
            </div>

            {/* Menu Options - Beautiful Boxes */}
            <div className="px-4 space-y-3">
              {/* Browse Profiles */}
              <Link
                to="/home"
                className="flex items-center justify-center px-6 py-4 bg-white rounded-xl shadow-md hover:shadow-lg transition duration-150 border-2 border-transparent hover:border-red-200"
                onClick={() => setIsMenuOpen(false)}
              >
                <svg className="w-6 h-6 text-red-600 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
                <span className="text-base font-semibold text-gray-800">Browse Profiles</span>
              </Link>

              {/* My Favorites */}
              <Link
                to="/favorites"
                className="flex items-center justify-center px-6 py-4 bg-white rounded-xl shadow-md hover:shadow-lg transition duration-150 border-2 border-transparent hover:border-red-200"
                onClick={() => setIsMenuOpen(false)}
              >
                <svg className="w-6 h-6 text-red-600 mr-3" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clipRule="evenodd" />
                </svg>
                <span className="text-base font-semibold text-gray-800">My Favorites</span>
              </Link>

              {/* Notifications */}
              <Link
                to="/notifications"
                className="flex items-center justify-center px-6 py-4 bg-white rounded-xl shadow-md hover:shadow-lg transition duration-150 border-2 border-transparent hover:border-red-200 relative"
                onClick={() => setIsMenuOpen(false)}
              >
                <svg className="w-6 h-6 text-red-600 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                </svg>
                <span className="text-base font-semibold text-gray-800">Notifications</span>
                {pendingInterestsCount > 0 && (
                  <span className="absolute top-2 right-2 inline-flex items-center justify-center px-2 py-1 text-xs font-bold leading-none text-white bg-red-600 rounded-full">
                    {pendingInterestsCount}
                  </span>
                )}
              </Link>

              {/* Edit Profile */}
              <Link
                to="/edit-profile"
                className="flex items-center justify-center px-6 py-4 bg-white rounded-xl shadow-md hover:shadow-lg transition duration-150 border-2 border-transparent hover:border-red-200"
                onClick={() => setIsMenuOpen(false)}
              >
                <svg className="w-6 h-6 text-red-600 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
                <span className="text-base font-semibold text-gray-800">Edit Profile</span>
              </Link>

              {/* Feedback */}
              <Link
                to="/feedback"
                className="flex items-center justify-center px-6 py-4 bg-white rounded-xl shadow-md hover:shadow-lg transition duration-150 border-2 border-transparent hover:border-red-200"
                onClick={() => setIsMenuOpen(false)}
              >
                <svg className="w-6 h-6 text-red-600 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                </svg>
                <span className="text-base font-semibold text-gray-800">Feedback</span>
              </Link>

              {/* Admin Dashboard (if staff) */}
              {currentUser?.is_staff && (
                <Link
                  to="/admin"
                  className="flex items-center justify-center px-6 py-4 bg-gradient-to-r from-purple-100 to-purple-50 rounded-xl shadow-md hover:shadow-lg transition duration-150 border-2 border-purple-200"
                  onClick={() => setIsMenuOpen(false)}
                >
                  <svg className="w-6 h-6 text-purple-600 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                  <span className="text-base font-semibold text-purple-800">Admin Dashboard</span>
                </Link>
              )}

              {/* Logout Button */}
              <button
                onClick={() => {
                  handleLogout();
                  setIsMenuOpen(false);
                }}
                className="w-full flex items-center justify-center px-6 py-4 bg-gradient-to-r from-red-500 to-pink-500 text-white rounded-xl shadow-md hover:shadow-lg transition duration-150 font-semibold"
              >
                <svg className="w-6 h-6 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                </svg>
                Logout
              </button>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
