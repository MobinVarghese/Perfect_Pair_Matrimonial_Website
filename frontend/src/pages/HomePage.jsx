import React, { useState, useEffect, useCallback } from 'react';
import { Link } from 'react-router-dom';
import { searchProfiles, sendInterest, toggleFavorite, checkFavoriteStatus, checkInterestStatus } from '../api/api';
import Navbar from '../components/Navbar';

// ProfileCard Component with Favorite Button
const ProfileCard = ({ profile, calculateAge, handleSendInterest, sendingInterest }) => {
  const [isFavorited, setIsFavorited] = useState(false);
  const [togglingFavorite, setTogglingFavorite] = useState(false);
  const [interestStatus, setInterestStatus] = useState(null);

  useEffect(() => {
    // Check if profile is favorited when component mounts
    const checkFavorite = async () => {
      try {
        const { is_favorited } = await checkFavoriteStatus(profile.id);
        setIsFavorited(is_favorited);
      } catch (error) {
        console.error('Error checking favorite status:', error);
      }
    };
    
    // Check interest status
    const checkInterest = async () => {
      try {
        const status = await checkInterestStatus(profile.id);
        setInterestStatus(status);
      } catch (error) {
        console.error('Error checking interest status:', error);
      }
    };
    
    checkFavorite();
    checkInterest();
  }, [profile.id]);

  const handleToggleFavorite = async (e) => {
    e.preventDefault();
    e.stopPropagation();
    setTogglingFavorite(true);
    try {
      const { is_favorited } = await toggleFavorite(profile.id);
      setIsFavorited(is_favorited);
    } catch (error) {
      console.error('Error toggling favorite:', error);
    } finally {
      setTogglingFavorite(false);
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-md overflow-hidden card-hover">
      {/* Profile Image */}
      <div className="relative h-64 bg-gradient-to-br from-pink-100 to-red-100">
        {profile.profile_picture ? (
          <img
            src={profile.profile_picture}
            alt={profile.first_name}
            className="w-full h-full object-cover"
          />
        ) : (
          <div className="flex items-center justify-center h-full">
            <svg className="w-24 h-24 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clipRule="evenodd" />
            </svg>
          </div>
        )}
        
        {/* Age Badge */}
        <div className="absolute top-3 right-3 bg-white rounded-full px-3 py-1 text-xs font-semibold text-gray-700">
          {calculateAge(profile.date_of_birth)} yrs
        </div>

        {/* Favorite Button */}
        <button
          onClick={handleToggleFavorite}
          disabled={togglingFavorite}
          className="absolute top-3 left-3 bg-white rounded-full p-2 shadow-lg hover:bg-gray-50 transition duration-150 disabled:opacity-50"
          title={isFavorited ? 'Remove from favorites' : 'Add to favorites'}
        >
          {togglingFavorite ? (
            <svg className="animate-spin h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
          ) : isFavorited ? (
            <svg className="w-5 h-5 text-red-600" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clipRule="evenodd" />
            </svg>
          ) : (
            <svg className="w-5 h-5 text-gray-400 hover:text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
            </svg>
          )}
        </button>
      </div>

      {/* Profile Info */}
      <div className="p-5">
        <h3 className="text-xl font-bold text-gray-900 mb-1">
          {profile.first_name} {profile.last_name}
        </h3>
        
        <div className="space-y-2 text-sm text-gray-600 mb-4">
          {profile.location && (
            <div className="flex items-center">
              <svg className="w-4 h-4 mr-2 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              <span>{profile.location}</span>
            </div>
          )}
          {profile.occupation && (
            <div className="flex items-center">
              <svg className="w-4 h-4 mr-2 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
              <span>{profile.occupation}</span>
            </div>
          )}
          {profile.education && (
            <div className="flex items-center">
              <svg className="w-4 h-4 mr-2 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path d="M12 14l9-5-9-5-9 5 9 5z" />
                <path d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 14l9-5-9-5-9 5 9 5zm0 0l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14zm-4 6v-7.5l4-2.222" />
              </svg>
              <span className="truncate">{profile.education}</span>
            </div>
          )}
        </div>

        {/* Action Buttons */}
        <div className="flex space-x-2">
          <Link
            to={`/profile/${profile.id}`}
            className="flex-1 bg-white border-2 border-red-600 text-red-600 px-4 py-2 rounded-lg hover:bg-red-50 transition duration-150 text-center font-medium"
          >
            View Profile
          </Link>
          
          {/* Interest Button - Shows different states based on interest status */}
          {!interestStatus?.has_interest ? (
            // No interest sent yet
            <button
              onClick={() => handleSendInterest(profile, setInterestStatus)}
              disabled={sendingInterest === profile.id}
              className="flex-1 bg-gradient-to-r from-red-600 to-pink-600 text-white px-4 py-2 rounded-lg hover:from-red-700 hover:to-pink-700 transition duration-150 font-medium disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
            >
              {sendingInterest === profile.id ? (
                <svg className="animate-spin h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
              ) : (
                <>
                  <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                  </svg>
                  Interest
                </>
              )}
            </button>
          ) : interestStatus.status === 'accepted' ? (
            // Interest accepted
            <button
              disabled
              className="flex-1 bg-gradient-to-r from-green-600 to-emerald-600 text-white px-4 py-2 rounded-lg font-medium cursor-not-allowed flex items-center justify-center text-sm"
            >
              <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Accepted
            </button>
          ) : (
            // Interest sent (pending or rejected)
            <button
              disabled
              className="flex-1 bg-gradient-to-r from-gray-500 to-gray-600 text-white px-4 py-2 rounded-lg font-medium cursor-not-allowed flex items-center justify-center text-sm"
            >
              <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Sent
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

const HomePage = () => {
  const [profiles, setProfiles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [filters, setFilters] = useState({
    gender: '',
    min_age: '',
    max_age: '',
    location: '',
    occupation: '',
    education: '',
    marital_status: '',
  });
  const [showAdvancedFilters, setShowAdvancedFilters] = useState(false);
  const [sendingInterest, setSendingInterest] = useState(null);
  const [notification, setNotification] = useState('');
  const [resultCount, setResultCount] = useState(0);
  const [currentUser, setCurrentUser] = useState(null);
  const [initialLoadComplete, setInitialLoadComplete] = useState(false);

  const fetchProfiles = useCallback(async (searchFilters = {}, userForFilter = null) => {
    setLoading(true);
    try {
      const filters = { ...searchFilters };

      if (userForFilter) {
        const userGender = userForFilter.profile?.gender;
        if (userGender) {
          // Use lowercase for API consistency (database stores 'male'/'female' in lowercase)
          filters.gender = userGender.toLowerCase() === 'male' ? 'female' : 'male';
          console.log(`User is ${userGender}, showing ${filters.gender} profiles.`);
        } else {
          console.log('User gender not found, defaulting to show female profiles.');
          filters.gender = 'female';
        }
      } else {
        console.log('No user specified for filtering.');
      }

      const data = await searchProfiles(filters);
      const profileList = Array.isArray(data) ? data : data.results || [];
      console.log('Fetched profiles:', profileList.length);
      if (profileList.length > 0) {
        console.log('Sample profile data:', profileList[0]);
      }
      setProfiles(profileList);
      setResultCount(data.count || profileList.length);
    } catch (error) {
      console.error('Error fetching profiles:', error);
      setProfiles([]);
      setResultCount(0);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (initialLoadComplete) return;
    
    const fetchInitialData = async () => {
      try {
        const { getCurrentUser } = await import('../api/api');
        const user = await getCurrentUser();
        console.log('Current user:', user);
        setCurrentUser(user);
        await fetchProfiles({}, user); // Pass user directly to fetchProfiles
      } catch (error) {
        console.error('Error fetching current user:', error);
        await fetchProfiles({}, null);
      } finally {
        setInitialLoadComplete(true);
      }
    };

    fetchInitialData();
  }, [initialLoadComplete, fetchProfiles]);

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters({ ...filters, [name]: value });
  };

  const handleSearchQueryChange = (e) => {
    setSearchQuery(e.target.value);
  };

  const handleQuickSearch = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleSearch(e);
    }
  };

  const handleSearch = (e) => {
    if (e) e.preventDefault();
    
    const searchFilters = {};
    
    // Add general search query
    if (searchQuery.trim()) {
      searchFilters.q = searchQuery.trim();
    }
    
    // Add specific filters
    Object.keys(filters).forEach(key => {
      if (filters[key]) searchFilters[key] = filters[key];
    });
    
    fetchProfiles(searchFilters, currentUser);
  };

  const handleClearFilters = () => {
    setSearchQuery('');
    setFilters({
      gender: '',
      min_age: '',
      max_age: '',
      location: '',
      occupation: '',
      education: '',
      marital_status: '',
    });
    fetchProfiles({}, currentUser);
  };

  const handleSendInterest = async (profile, setInterestStatusCallback) => {
    setSendingInterest(profile.id);
    try {
      // Send interest using USER ID, not PROFILE ID
      await sendInterest(profile.user);
      setNotification('Interest sent successfully!');
      setTimeout(() => setNotification(''), 3000);
      
      // Refresh interest status for this profile
      if (setInterestStatusCallback) {
        try {
          const status = await checkInterestStatus(profile.id);
          setInterestStatusCallback(status);
        } catch (error) {
          console.error('Error refreshing interest status:', error);
        }
      }
    } catch (error) {
      console.error('Error sending interest:', error);
      // Show backend error message if available
      if (error.response?.data?.error) {
        setNotification(error.response.data.error);
      } else {
        setNotification('Failed to send interest. Try again.');
      }
      setTimeout(() => setNotification(''), 3000);
    } finally {
      setSendingInterest(null);
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

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Discover Your Match</h1>
          <p className="text-gray-600">Browse through profiles and find your perfect partner</p>
        </div>

        {/* Search Bar */}
        <div className="bg-white rounded-xl shadow-md p-6 mb-6">
          <div className="flex items-center space-x-4">
            <div className="flex-1 relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg className="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </div>
              <input
                type="text"
                value={searchQuery}
                onChange={handleSearchQueryChange}
                onKeyPress={handleQuickSearch}
                placeholder="Search by name, occupation, location, education..."
                className="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent transition duration-150"
              />
            </div>
            <button
              onClick={handleSearch}
              className="bg-gradient-to-r from-red-600 to-pink-600 text-white px-6 py-3 rounded-lg hover:from-red-700 hover:to-pink-700 transition duration-150 font-medium flex items-center"
            >
              <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              Search
            </button>
            <button
              onClick={() => setShowAdvancedFilters(!showAdvancedFilters)}
              className="border-2 border-gray-300 text-gray-700 px-4 py-3 rounded-lg hover:bg-gray-50 transition duration-150 font-medium flex items-center"
            >
              <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4" />
              </svg>
              {showAdvancedFilters ? 'Hide Filters' : 'Advanced Filters'}
            </button>
          </div>

          {/* Results Count */}
          {!loading && (
            <div className="mt-4 text-sm text-gray-600">
              Found <span className="font-semibold text-red-600">{resultCount}</span> profiles
            </div>
          )}
        </div>

        {/* Advanced Filters */}
        {showAdvancedFilters && (
          <div className="bg-white rounded-xl shadow-md p-6 mb-6 animate-fadeIn">
            <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
              <svg className="w-5 h-5 mr-2 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
              </svg>
              Advanced Filters
            </h2>
            <form onSubmit={handleSearch}>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                {/* Gender Filter */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Gender</label>
                  <select
                    name="gender"
                    value={filters.gender}
                    onChange={handleFilterChange}
                    className="block w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
                  >
                    <option value="">All</option>
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                    <option value="Other">Other</option>
                  </select>
                </div>

                {/* Min Age */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Min Age</label>
                  <input
                    type="number"
                    name="min_age"
                    value={filters.min_age}
                    onChange={handleFilterChange}
                    placeholder="18"
                    min="18"
                    max="100"
                    className="block w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
              />
            </div>

            {/* Max Age */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Max Age</label>
              <input
                type="number"
                name="max_age"
                value={filters.max_age}
                onChange={handleFilterChange}
                placeholder="60"
                min="18"
                max="100"
                className="block w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
              />
            </div>

            {/* Location */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Location</label>
              <input
                type="text"
                name="location"
                value={filters.location}
                onChange={handleFilterChange}
                placeholder="City, State"
                className="block w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
              />
            </div>

            {/* Occupation */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Occupation</label>
              <input
                type="text"
                name="occupation"
                value={filters.occupation}
                onChange={handleFilterChange}
                placeholder="e.g., Engineer, Doctor"
                className="block w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
              />
            </div>

            {/* Education */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Education</label>
              <input
                type="text"
                name="education"
                value={filters.education}
                onChange={handleFilterChange}
                placeholder="e.g., Bachelor's, Master's"
                className="block w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
              />
            </div>

            {/* Marital Status */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Marital Status</label>
              <select
                name="marital_status"
                value={filters.marital_status}
                onChange={handleFilterChange}
                className="block w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
              >
                <option value="">All</option>
                <option value="Single">Single</option>
                <option value="Married">Married</option>
                <option value="Divorced">Divorced</option>
                <option value="Widowed">Widowed</option>
              </select>
            </div>
              </div>

              {/* Buttons */}
              <div className="flex items-center space-x-4 mt-6">
                <button
                  type="submit"
                  className="bg-gradient-to-r from-red-600 to-pink-600 text-white px-6 py-2 rounded-lg hover:from-red-700 hover:to-pink-700 transition duration-150 font-medium"
                >
                  Apply Filters
                </button>
                <button
                  type="button"
                  onClick={handleClearFilters}
                  className="px-6 py-2 border-2 border-gray-300 rounded-lg hover:bg-gray-50 transition duration-150 font-medium text-gray-700"
                >
                  Clear All
                </button>
              </div>
            </form>
          </div>
        )}

        {/* Profiles Grid */}
        {loading ? (
          <div className="flex justify-center items-center py-20">
            <svg className="animate-spin h-12 w-12 text-red-600" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
          </div>
        ) : profiles.length === 0 ? (
          <div className="text-center py-20">
            <svg className="mx-auto h-16 w-16 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">No Profiles Found</h3>
            <p className="text-gray-600">Try adjusting your search filters</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {profiles.map((profile) => (
              <ProfileCard
                key={profile.id}
                profile={profile}
                calculateAge={calculateAge}
                handleSendInterest={handleSendInterest}
                sendingInterest={sendingInterest}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default HomePage;
