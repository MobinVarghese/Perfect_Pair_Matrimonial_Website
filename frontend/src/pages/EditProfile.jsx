import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getCurrentUser, updateProfileWithFiles, changePassword } from '../api/api';
import Navbar from '../components/Navbar';

const EditProfile = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    mobile_number: '',
    gender: '',
    date_of_birth: '',
    height: '',
    education: '',
    occupation: '',
    location: '',
    bio: '',
  });
  const [profilePicture, setProfilePicture] = useState(null);
  const [previewUrl, setPreviewUrl] = useState('');
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [errors, setErrors] = useState({});
  const [success, setSuccess] = useState('');

  // Password change state
  const [passwordData, setPasswordData] = useState({
    old_password: '',
    new_password: '',
    new_password2: ''
  });
  const [passwordLoading, setPasswordLoading] = useState(false);
  const [passwordSuccess, setPasswordSuccess] = useState(false);
  const [passwordErrors, setPasswordErrors] = useState({});

  useEffect(() => {
    fetchCurrentUser();
  }, []);

  const fetchCurrentUser = async () => {
    try {
      const user = await getCurrentUser();
      console.log('📥 Fetched user data:', user);
      
      // Extract profile data from nested profile object
      const profile = user.profile || {};
      
      // Calculate date_of_birth from age if not available
      let dateOfBirth = profile.date_of_birth || '';
      if (!dateOfBirth && profile.age) {
        const currentYear = new Date().getFullYear();
        const birthYear = currentYear - profile.age;
        dateOfBirth = `${birthYear}-01-01`;
      }
      
      setFormData({
        first_name: user.first_name || '',
        last_name: user.last_name || '',
        mobile_number: profile.mobile_number || '',
        gender: profile.gender || '',
        date_of_birth: dateOfBirth,
        height: profile.height || '',
        education: profile.education || '',
        occupation: profile.occupation || '',
        location: profile.location || '',
        bio: profile.about || profile.bio || '', // 'about' field in Profile model
      });
      
      // Set profile picture preview
      if (profile.profile_picture || profile.photo_url) {
        setPreviewUrl(profile.profile_picture || profile.photo_url);
      }
      
      console.log('✅ Form data populated:', {
        first_name: user.first_name,
        mobile_number: profile.mobile_number,
        gender: profile.gender,
        location: profile.location
      });
    } catch (error) {
      console.error('❌ Error fetching user:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
    if (errors[name]) {
      setErrors({ ...errors, [name]: '' });
    }
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (file.size > 5 * 1024 * 1024) {
        setErrors({ profile_picture: 'File size must be less than 5MB' });
        return;
      }
      setProfilePicture(file);
      setPreviewUrl(URL.createObjectURL(file));
      if (errors.profile_picture) {
        setErrors({ ...errors, profile_picture: '' });
      }
    }
  };

  const validateRequiredFields = () => {
    const requiredFields = {
      first_name: 'First Name',
      last_name: 'Last Name',
      mobile_number: 'Mobile Number',
      // gender and date_of_birth are read-only, set during registration
    };

    const newErrors = {};
    let missingFields = [];

    Object.keys(requiredFields).forEach(field => {
      if (!formData[field] || formData[field].trim() === '') {
        newErrors[field] = `${requiredFields[field]} is required`;
        missingFields.push(requiredFields[field]);
      }
    });

    if (missingFields.length > 0) {
      newErrors.general = `Please fill in the following required fields: ${missingFields.join(', ')}`;
      setErrors(newErrors);
      return false;
    }

    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log('🔵 Form submitted - Initial states:', { saving, saved });
    setErrors({});
    setSuccess('');
    setSaved(false);

    // Validate required fields
    if (!validateRequiredFields()) {
      console.log('❌ Validation failed');
      // Scroll to top to show error message
      window.scrollTo({ top: 0, behavior: 'smooth' });
      return;
    }

    console.log('✅ Validation passed, starting save...');
    setSaving(true);
    console.log('🔵 Set saving to true');

    const formDataToSend = new FormData();
    Object.keys(formData).forEach(key => {
      // Exclude gender and date_of_birth from update (read-only after registration)
      if (formData[key] && key !== 'gender' && key !== 'date_of_birth') {
        formDataToSend.append(key, formData[key]);
      }
    });

    if (profilePicture) {
      formDataToSend.append('profile_picture', profilePicture);
    }

    try {
      await updateProfileWithFiles(formDataToSend);
      console.log('✅ API call successful - Profile updated!');
      setSaving(false);
      setSuccess('Profile updated successfully!');
      setSaved(true);
      console.log('✅ Profile saved! Refreshing user data...');
      
      // Refetch user data to show updated profile picture
      await fetchCurrentUser();
      
      // Clear the file input so user can upload again if needed
      setProfilePicture(null);
      
      // Scroll to top to show success message
      window.scrollTo({ top: 0, behavior: 'smooth' });
      
      // Reset saved state after 3 seconds to allow more edits
      setTimeout(() => {
        setSaved(false);
      }, 3000);
    } catch (error) {
      console.error('❌ Error updating profile:', error);
      setSaving(false);
      if (error.response?.data) {
        setErrors(error.response.data);
        // Scroll to top to show error
        window.scrollTo({ top: 0, behavior: 'smooth' });
      } else {
        setErrors({ general: 'Failed to update profile. Please try again.' });
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
    }
  };

  const handlePasswordChange = (e) => {
    setPasswordData({
      ...passwordData,
      [e.target.name]: e.target.value
    });
    setPasswordErrors({});
    setPasswordSuccess(false);
  };

  const handlePasswordSubmit = async (e) => {
    e.preventDefault();
    setPasswordLoading(true);
    setPasswordErrors({});
    setPasswordSuccess(false);

    try {
      await changePassword(passwordData);
      setPasswordSuccess(true);
      setPasswordData({
        old_password: '',
        new_password: '',
        new_password2: ''
      });
      
      // Reset success message after 5 seconds
      setTimeout(() => {
        setPasswordSuccess(false);
      }, 5000);
    } catch (error) {
      console.error('❌ Error changing password:', error);
      if (error.response?.data) {
        setPasswordErrors(error.response.data);
      } else {
        setPasswordErrors({ general: 'Failed to change password. Please try again.' });
      }
    } finally {
      setPasswordLoading(false);
    }
  };

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

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />

      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <button
            onClick={() => navigate(-1)}
            className="mb-4 flex items-center text-gray-600 hover:text-gray-900 transition duration-150"
          >
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            Back
          </button>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Edit Profile</h1>
          <p className="text-gray-600">Update your information to help others know you better</p>
        </div>

        {/* Success Message */}
        {success && (
          <div className="mb-6 bg-green-50 border-l-4 border-green-500 p-4 rounded animate-fadeIn">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-green-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <p className="text-sm text-green-700">{success}</p>
              </div>
            </div>
          </div>
        )}

        {/* Error Message */}
        {errors.general && (
          <div className="mb-6 bg-red-50 border-l-4 border-red-500 p-4 rounded">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <p className="text-sm text-red-700">{errors.general}</p>
              </div>
            </div>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Profile Picture Section */}
          <div className="bg-white rounded-xl shadow-md p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Profile Picture</h2>
            <div className="flex items-center space-x-6">
              <div className="relative">
                <div className="h-32 w-32 rounded-full bg-gradient-to-br from-pink-100 to-red-100 flex items-center justify-center overflow-hidden">
                  {previewUrl ? (
                    <img src={previewUrl} alt="Profile" className="h-full w-full object-cover" />
                  ) : (
                    <svg className="h-16 w-16 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clipRule="evenodd" />
                    </svg>
                  )}
                </div>
              </div>
              <div className="flex-1">
                <label className="block">
                  <span className="sr-only">Choose profile photo</span>
                  <input
                    type="file"
                    accept="image/*"
                    onChange={handleFileChange}
                    className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-red-50 file:text-red-700 hover:file:bg-red-100 cursor-pointer"
                  />
                </label>
                <p className="mt-2 text-xs text-gray-500">PNG, JPG, GIF up to 5MB</p>
                {errors.profile_picture && (
                  <p className="mt-2 text-sm text-red-600">{errors.profile_picture}</p>
                )}
              </div>
            </div>
          </div>

          {/* Personal Information */}
          <div className="bg-white rounded-xl shadow-md p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
              <svg className="w-5 h-5 mr-2 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
              Personal Information
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <FormInput
                label="First Name"
                name="first_name"
                value={formData.first_name}
                onChange={handleChange}
                error={errors.first_name}
                required
              />
              <FormInput
                label="Last Name"
                name="last_name"
                value={formData.last_name}
                onChange={handleChange}
                error={errors.last_name}
                required
              />
              <FormInput
                label="Mobile Number"
                name="mobile_number"
                type="tel"
                value={formData.mobile_number}
                onChange={handleChange}
                error={errors.mobile_number}
                placeholder="+1234567890"
                required
              />
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Gender
                </label>
                <input
                  type="text"
                  value={formData.gender ? (formData.gender.charAt(0).toUpperCase() + formData.gender.slice(1)) : ''}
                  disabled
                  className="block w-full px-4 py-3 border border-gray-200 rounded-lg bg-gray-50 text-gray-600 cursor-not-allowed"
                />
                <p className="mt-1 text-xs text-gray-500">
                  ⚠️ Gender cannot be changed after registration
                </p>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Date of Birth
                </label>
                <input
                  type="date"
                  value={formData.date_of_birth}
                  disabled
                  className="block w-full px-4 py-3 border border-gray-200 rounded-lg bg-gray-50 text-gray-600 cursor-not-allowed"
                />
                <p className="mt-1 text-xs text-gray-500">
                  ⚠️ Date of birth cannot be changed after registration
                </p>
              </div>
              <FormInput
                label="Height (feet)"
                name="height"
                type="number"
                step="0.01"
                value={formData.height}
                onChange={handleChange}
                error={errors.height}
                placeholder="5.6"
              />
            </div>
          </div>

          {/* Professional Information */}
          <div className="bg-white rounded-xl shadow-md p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
              <svg className="w-5 h-5 mr-2 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
              Professional Details
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <FormInput
                label="Education"
                name="education"
                value={formData.education}
                onChange={handleChange}
                error={errors.education}
                placeholder="Bachelor's, Master's, etc."
              />
              <FormInput
                label="Occupation"
                name="occupation"
                value={formData.occupation}
                onChange={handleChange}
                error={errors.occupation}
                placeholder="Software Engineer, Doctor, etc."
              />
            </div>
          </div>

          {/* Location Information */}
          <div className="bg-white rounded-xl shadow-md p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
              <svg className="w-5 h-5 mr-2 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              Location
            </h2>
            <div className="grid grid-cols-1 gap-6">
              <FormInput
                label="Location"
                name="location"
                value={formData.location}
                onChange={handleChange}
                error={errors.location}
                placeholder="City, State, Country (e.g., New York, NY, USA)"
              />
            </div>
          </div>

          {/* About/Bio */}
          <div className="bg-white rounded-xl shadow-md p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
              <svg className="w-5 h-5 mr-2 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              About Yourself
            </h2>
            <textarea
              name="bio"
              value={formData.bio}
              onChange={handleChange}
              rows="5"
              className="block w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent transition resize-none"
              placeholder="Tell others about yourself, your interests, what you're looking for in a partner..."
            />
            {errors.bio && (
              <p className="mt-2 text-sm text-red-600">{errors.bio}</p>
            )}
          </div>

          {/* Action Buttons */}
          <div className="flex space-x-4">
            <button
              type="button"
              onClick={() => navigate(-1)}
              disabled={saving || saved}
              className="flex-1 bg-white border-2 border-gray-300 text-gray-700 px-6 py-3 rounded-lg hover:bg-gray-50 transition duration-150 font-medium disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={saving || saved}
              className={`flex-1 px-6 py-3 rounded-lg transition-all duration-300 font-medium disabled:cursor-not-allowed flex items-center justify-center ${
                saved
                  ? 'bg-green-600 hover:bg-green-700 text-white'
                  : 'bg-gradient-to-r from-red-600 to-pink-600 hover:from-red-700 hover:to-pink-700 text-white disabled:opacity-50'
              }`}
            >
              {(() => {
                console.log('🎨 Button rendering - States:', { saving, saved });
                console.log('🎨 Button class should be:', saved ? 'GREEN (bg-green-600)' : 'RED-PINK gradient');
              })()}
              {saving ? (
                <>
                  <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Saving Changes...
                </>
              ) : saved ? (
                <>
                  <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                  </svg>
                  Saved Changes!
                </>
              ) : (
                <>
                  <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4" />
                  </svg>
                  Save Changes
                </>
              )}
            </button>
          </div>
        </form>
      </div>

      {/* Change Password Section */}
      <div className="max-w-2xl mx-auto px-4 pb-12">
        <div className="bg-white rounded-xl shadow-md p-8">
          <div className="mb-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-2 flex items-center">
              <svg className="w-7 h-7 text-red-600 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
              </svg>
              Change Password
            </h2>
            <p className="text-gray-600 ml-10">Update your password to keep your account secure</p>
          </div>

          {/* Success Message */}
          {passwordSuccess && (
            <div className="mb-6 p-4 bg-green-50 border-l-4 border-green-500 rounded-lg">
              <div className="flex items-center">
                <svg className="w-6 h-6 text-green-500 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <p className="text-green-700 font-medium">Password changed successfully! You can now use your new password to login.</p>
              </div>
            </div>
          )}

          {/* Error Messages */}
          {passwordErrors.general && (
            <div className="mb-6 p-4 bg-red-50 border-l-4 border-red-500 rounded-lg">
              <p className="text-red-700">{passwordErrors.general}</p>
            </div>
          )}

          {passwordErrors.old_password && (
            <div className="mb-6 p-4 bg-red-50 border-l-4 border-red-500 rounded-lg">
              <p className="text-red-700">{passwordErrors.old_password}</p>
            </div>
          )}

          {/* Info Banner */}
          <div className="mb-6 p-4 bg-blue-50 border-l-4 border-blue-500 rounded-lg">
            <div className="flex items-start">
              <svg className="w-5 h-5 text-blue-500 mr-3 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <div className="text-sm text-blue-700">
                <p className="font-semibold mb-1">Password Requirements:</p>
                <ul className="list-disc list-inside space-y-1">
                  <li>At least 8 characters long</li>
                  <li>Must contain letters and numbers</li>
                  <li>Should be different from your old password</li>
                </ul>
              </div>
            </div>
          </div>

          <form onSubmit={handlePasswordSubmit} className="space-y-6">
            {/* Old Password */}
            <div>
              <label htmlFor="old_password" className="block text-sm font-medium text-gray-700 mb-2">
                Current Password <span className="text-red-500">*</span>
              </label>
              <input
                type="password"
                id="old_password"
                name="old_password"
                value={passwordData.old_password}
                onChange={handlePasswordChange}
                className={`block w-full px-4 py-3 border ${
                  passwordErrors.old_password ? 'border-red-300' : 'border-gray-300'
                } rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent transition`}
                placeholder="Enter your current password"
                required
              />
              {passwordErrors.old_password && (
                <p className="mt-2 text-sm text-red-600">{passwordErrors.old_password}</p>
              )}
            </div>

            {/* New Password */}
            <div>
              <label htmlFor="new_password" className="block text-sm font-medium text-gray-700 mb-2">
                New Password <span className="text-red-500">*</span>
              </label>
              <input
                type="password"
                id="new_password"
                name="new_password"
                value={passwordData.new_password}
                onChange={handlePasswordChange}
                className={`block w-full px-4 py-3 border ${
                  passwordErrors.new_password ? 'border-red-300' : 'border-gray-300'
                } rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent transition`}
                placeholder="Enter your new password"
                required
              />
              {passwordErrors.new_password && (
                <p className="mt-2 text-sm text-red-600">{passwordErrors.new_password}</p>
              )}
            </div>

            {/* Confirm New Password */}
            <div>
              <label htmlFor="new_password2" className="block text-sm font-medium text-gray-700 mb-2">
                Confirm New Password <span className="text-red-500">*</span>
              </label>
              <input
                type="password"
                id="new_password2"
                name="new_password2"
                value={passwordData.new_password2}
                onChange={handlePasswordChange}
                className={`block w-full px-4 py-3 border ${
                  passwordErrors.new_password2 ? 'border-red-300' : 'border-gray-300'
                } rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent transition`}
                placeholder="Confirm your new password"
                required
              />
              {passwordErrors.new_password2 && (
                <p className="mt-2 text-sm text-red-600">{passwordErrors.new_password2}</p>
              )}
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={passwordLoading || passwordSuccess}
              className={`w-full px-6 py-3 rounded-lg transition-all duration-300 font-medium disabled:cursor-not-allowed flex items-center justify-center ${
                passwordSuccess
                  ? 'bg-green-600 hover:bg-green-700 text-white'
                  : 'bg-gradient-to-r from-red-600 to-pink-600 hover:from-red-700 hover:to-pink-700 text-white disabled:opacity-50'
              }`}
            >
              {passwordLoading ? (
                <>
                  <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Changing Password...
                </>
              ) : passwordSuccess ? (
                <>
                  <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                  </svg>
                  Password Changed!
                </>
              ) : (
                <>
                  <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
                  </svg>
                  Change Password
                </>
              )}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

// Reusable Form Components
const FormInput = ({ label, name, type = 'text', value, onChange, error, required, placeholder }) => (
  <div>
    <label htmlFor={name} className="block text-sm font-medium text-gray-700 mb-2">
      {label} {required && <span className="text-red-500">*</span>}
    </label>
    <input
      type={type}
      id={name}
      name={name}
      value={value}
      onChange={onChange}
      className={`block w-full px-4 py-3 border ${
        error ? 'border-red-300' : 'border-gray-300'
      } rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent transition`}
      placeholder={placeholder}
      required={required}
    />
    {error && <p className="mt-2 text-sm text-red-600">{error}</p>}
  </div>
);

const FormSelect = ({ label, name, value, onChange, error, options, required }) => (
  <div>
    <label htmlFor={name} className="block text-sm font-medium text-gray-700 mb-2">
      {label} {required && <span className="text-red-500">*</span>}
    </label>
    <select
      id={name}
      name={name}
      value={value}
      onChange={onChange}
      className={`block w-full px-4 py-3 border ${
        error ? 'border-red-300' : 'border-gray-300'
      } rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent transition`}
      required={required}
    >
      <option value="">Select {label}</option>
      {options.map(option => (
        <option key={option} value={option}>
          {option}
        </option>
      ))}
    </select>
    {error && <p className="mt-2 text-sm text-red-600">{error}</p>}
  </div>
);

export default EditProfile;
