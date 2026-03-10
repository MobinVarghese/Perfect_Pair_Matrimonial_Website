import React, { useState, useEffect } from 'react';
import { getAllUsers, getAllReports, reviewReport, exportProfilesPDF, exportProfilesExcel, getExportLogs, blockUser, unblockUser, getPasswordResetRequests, approvePasswordResetRequest, rejectPasswordResetRequest } from '../api/api';
import Navbar from '../components/Navbar';

const AdminDashboard = () => {
  const [activeTab, setActiveTab] = useState('users');
  const [users, setUsers] = useState([]);
  const [reports, setReports] = useState([]);
  const [exportLogs, setExportLogs] = useState([]);
  const [passwordResets, setPasswordResets] = useState([]);
  const [loading, setLoading] = useState(false);
  const [exporting, setExporting] = useState(false);
  const [notification, setNotification] = useState('');

  useEffect(() => {
    if (activeTab === 'users') {
      fetchUsers();
    } else if (activeTab === 'reports') {
      fetchReports();
    } else if (activeTab === 'exports') {
      fetchExportLogs();
    } else if (activeTab === 'password-resets') {
      fetchPasswordResets();
    }
  }, [activeTab]);

  const fetchUsers = async () => {
    setLoading(true);
    try {
      const data = await getAllUsers();
      setUsers(Array.isArray(data) ? data : data.results || []);
    } catch (error) {
      console.error('Error fetching users:', error);
      setUsers([]);
    } finally {
      setLoading(false);
    }
  };

  const fetchReports = async () => {
    setLoading(true);
    try {
      const data = await getAllReports();
      setReports(Array.isArray(data) ? data : data.results || []);
    } catch (error) {
      console.error('Error fetching reports:', error);
      setReports([]);
    } finally {
      setLoading(false);
    }
  };

  const fetchExportLogs = async () => {
    setLoading(true);
    try {
      const data = await getExportLogs();
      setExportLogs(Array.isArray(data) ? data : data.results || []);
    } catch (error) {
      console.error('Error fetching export logs:', error);
      setExportLogs([]);
    } finally {
      setLoading(false);
    }
  };

  const fetchPasswordResets = async () => {
    setLoading(true);
    try {
      const data = await getPasswordResetRequests();
      setPasswordResets(Array.isArray(data) ? data : data.results || []);
    } catch (error) {
      console.error('Error fetching password resets:', error);
      setPasswordResets([]);
    } finally {
      setLoading(false);
    }
  };

  const handleApproveReset = async (requestId) => {
    if (!window.confirm('Approve this password reset request? A new password will be generated and sent to the user.')) {
      return;
    }

    try {
      const response = await approvePasswordResetRequest(requestId);
      showNotification(`Password reset approved! New password: ${response.new_password}`);
      fetchPasswordResets();
    } catch (error) {
      console.error('Error approving reset:', error);
      showNotification(error.response?.data?.error || 'Failed to approve reset', 'error');
    }
  };

  const handleRejectReset = async (requestId) => {
    const reason = prompt('Enter reason for rejection (optional):');
    if (reason === null) return; // User cancelled

    try {
      await rejectPasswordResetRequest(requestId, reason);
      showNotification('Password reset request rejected');
      fetchPasswordResets();
    } catch (error) {
      console.error('Error rejecting reset:', error);
      showNotification('Failed to reject reset', 'error');
    }
  };

  const handleReviewReport = async (reportId, action) => {
    try {
      await reviewReport(reportId, { action, review_notes: `Report ${action}` });
      showNotification(`Report ${action} successfully`);
      fetchReports();
    } catch (error) {
      console.error('Error reviewing report:', error);
      showNotification('Failed to review report', 'error');
    }
  };

  const handleExportPDF = async () => {
    setExporting(true);
    try {
      await exportProfilesPDF();
      showNotification('PDF exported successfully!');
      fetchExportLogs();
    } catch (error) {
      console.error('Error exporting PDF:', error);
      showNotification('Failed to export PDF', 'error');
    } finally {
      setExporting(false);
    }
  };

  const handleExportExcel = async () => {
    setExporting(true);
    try {
      await exportProfilesExcel();
      showNotification('Excel exported successfully!');
      fetchExportLogs();
    } catch (error) {
      console.error('Error exporting Excel:', error);
      showNotification('Failed to export Excel', 'error');
    } finally {
      setExporting(false);
    }
  };

  const handleBlockUser = async (userId, username) => {
    const reason = prompt(`Enter reason for blocking user "${username}":`, 'Violated terms of service');
    
    if (reason === null) {
      return; // User cancelled
    }
    
    if (!reason.trim()) {
      showNotification('Block reason cannot be empty', 'error');
      return;
    }

    try {
      await blockUser(userId, reason);
      showNotification(`User "${username}" has been blocked successfully`);
      fetchUsers(); // Refresh user list
    } catch (error) {
      console.error('Error blocking user:', error);
      showNotification(error.response?.data?.error || 'Failed to block user', 'error');
    }
  };

  const handleUnblockUser = async (userId) => {
    if (!window.confirm('Are you sure you want to unblock this user?')) {
      return;
    }

    try {
      await unblockUser(userId);
      showNotification('User has been unblocked successfully');
      fetchUsers(); // Refresh user list
    } catch (error) {
      console.error('Error unblocking user:', error);
      showNotification(error.response?.data?.error || 'Failed to unblock user', 'error');
    }
  };

  const showNotification = (message, type = 'success') => {
    setNotification({ message, type });
    setTimeout(() => setNotification(''), 3000);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />

      {/* Notification */}
      {notification && (
        <div className="fixed top-20 right-4 z-50 animate-fadeIn">
          <div className={`bg-white border-l-4 ${
            notification.type === 'error' ? 'border-red-500' : 'border-green-500'
          } rounded-lg shadow-lg p-4 max-w-md`}>
            <div className="flex">
              <div className="flex-shrink-0">
                {notification.type === 'error' ? (
                  <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                  </svg>
                ) : (
                  <svg className="h-5 w-5 text-green-400" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                )}
              </div>
              <div className="ml-3">
                <p className="text-sm text-gray-700">{notification.message}</p>
              </div>
            </div>
          </div>
        </div>
      )}

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Admin Dashboard</h1>
          <p className="text-gray-600">Manage users, reports, and export data</p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatsCard
            title="Total Users"
            value={users.length}
            icon={
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
              </svg>
            }
            bgColor="from-blue-500 to-blue-600"
          />
          <StatsCard
            title="Pending Reports"
            value={reports.filter(r => r.status === 'pending').length}
            icon={
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
            }
            bgColor="from-yellow-500 to-yellow-600"
          />
          <StatsCard
            title="Total Exports"
            value={exportLogs.length}
            icon={
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M9 19l3 3m0 0l3-3m-3 3V10" />
              </svg>
            }
            bgColor="from-green-500 to-green-600"
          />
          <StatsCard
            title="Pending Resets"
            value={passwordResets.filter(r => r.status === 'pending').length}
            icon={
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
              </svg>
            }
            bgColor="from-orange-500 to-red-600"
          />
        </div>

        {/* Tabs */}
        <div className="bg-white rounded-xl shadow-md mb-6">
          <div className="border-b border-gray-200">
            <nav className="flex -mb-px">
              <TabButton
                label="Users"
                icon={
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                  </svg>
                }
                isActive={activeTab === 'users'}
                onClick={() => setActiveTab('users')}
              />
              <TabButton
                label="Reports"
                icon={
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                  </svg>
                }
                isActive={activeTab === 'reports'}
                onClick={() => setActiveTab('reports')}
              />
              <TabButton
                label="Exports"
                icon={
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M9 19l3 3m0 0l3-3m-3 3V10" />
                  </svg>
                }
                isActive={activeTab === 'exports'}
                onClick={() => setActiveTab('exports')}
              />
              <TabButton
                label="Password Resets"
                icon={
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
                  </svg>
                }
                count={passwordResets.filter(r => r.status === 'pending').length}
                isActive={activeTab === 'password-resets'}
                onClick={() => setActiveTab('password-resets')}
              />
            </nav>
          </div>

          {/* Tab Content */}
          <div className="p-6">
            {loading ? (
              <div className="flex justify-center items-center py-12">
                <svg className="animate-spin h-8 w-8 text-red-600" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
              </div>
            ) : (
              <>
                {activeTab === 'users' && <UsersTab users={users} onBlockUser={handleBlockUser} onUnblockUser={handleUnblockUser} />}
                {activeTab === 'reports' && (
                  <ReportsTab reports={reports} onReview={handleReviewReport} />
                )}
                {activeTab === 'exports' && (
                  <ExportsTab
                    exportLogs={exportLogs}
                    onExportPDF={handleExportPDF}
                    onExportExcel={handleExportExcel}
                    exporting={exporting}
                  />
                )}
                {activeTab === 'password-resets' && (
                  <PasswordResetsTab
                    requests={passwordResets}
                    onApprove={handleApproveReset}
                    onReject={handleRejectReset}
                  />
                )}
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

// Stats Card Component
const StatsCard = ({ title, value, icon, bgColor }) => (
  <div className={`bg-gradient-to-r ${bgColor} rounded-xl shadow-md p-6 text-white`}>
    <div className="flex items-center justify-between">
      <div>
        <p className="text-white/80 text-sm font-medium mb-1">{title}</p>
        <p className="text-4xl font-bold">{value}</p>
      </div>
      <div className="bg-white/20 rounded-lg p-3">
        {icon}
      </div>
    </div>
  </div>
);

// Tab Button Component
const TabButton = ({ label, icon, isActive, onClick }) => (
  <button
    onClick={onClick}
    className={`flex items-center px-6 py-4 border-b-2 font-medium text-sm transition duration-150 ${
      isActive
        ? 'border-red-600 text-red-600'
        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
    }`}
  >
    {icon}
    <span className="ml-2">{label}</span>
  </button>
);

// Users Tab Component
const UsersTab = ({ users, onBlockUser, onUnblockUser }) => (
  <div className="overflow-x-auto">
    <table className="min-w-full divide-y divide-gray-200">
      <thead className="bg-gray-50">
        <tr>
          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">User</th>
          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Email</th>
          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Gender</th>
          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Location</th>
          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
        </tr>
      </thead>
      <tbody className="bg-white divide-y divide-gray-200">
        {users.map((user) => (
          <tr key={user.id} className={`hover:bg-gray-50 ${user.is_blocked ? 'bg-red-50' : ''}`}>
            <td className="px-6 py-4 whitespace-nowrap">
              <div className="flex items-center">
                <div className={`h-10 w-10 rounded-full flex items-center justify-center ${
                  user.is_blocked 
                    ? 'bg-gradient-to-br from-gray-200 to-gray-300' 
                    : 'bg-gradient-to-br from-pink-100 to-red-100'
                }`}>
                  <span className={`font-semibold ${user.is_blocked ? 'text-gray-600' : 'text-red-600'}`}>
                    {user.first_name?.[0] || user.username?.[0] || 'U'}
                  </span>
                </div>
                <div className="ml-4">
                  <div className="text-sm font-medium text-gray-900 flex items-center">
                    {user.first_name} {user.last_name}
                    {user.is_blocked && (
                      <span className="ml-2 text-xs text-red-600">🔒 Blocked</span>
                    )}
                    {(user.is_admin || user.is_staff) && (
                      <span className="ml-2 text-xs text-purple-600">👑 Admin</span>
                    )}
                  </div>
                  <div className="text-sm text-gray-500">@{user.username}</div>
                </div>
              </div>
            </td>
            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{user.email}</td>
            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{user.gender || 'N/A'}</td>
            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{user.location || 'N/A'}</td>
            <td className="px-6 py-4 whitespace-nowrap">
              <div className="flex flex-col gap-1">
                <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                  user.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                }`}>
                  {user.is_active ? 'Active' : 'Inactive'}
                </span>
                {user.is_blocked && (
                  <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-red-100 text-red-800">
                    Blocked
                  </span>
                )}
              </div>
            </td>
            <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
              {!user.is_admin && !user.is_staff && (
                user.is_blocked ? (
                  <button 
                    onClick={() => onUnblockUser(user.id)}
                    className="text-green-600 hover:text-green-900 font-medium"
                  >
                    ✓ Unblock
                  </button>
                ) : (
                  <button 
                    onClick={() => onBlockUser(user.id, user.username)}
                    className="text-orange-600 hover:text-orange-900 font-medium"
                  >
                    🔒 Block
                  </button>
                )
              )}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
    {users.length === 0 && (
      <div className="text-center py-12 text-gray-500">No users found</div>
    )}
  </div>
);

// Reports Tab Component
const ReportsTab = ({ reports, onReview }) => (
  <div className="space-y-4">
    {reports.map((report) => (
      <div key={report.id} className="bg-gray-50 rounded-lg p-6 border border-gray-200">
        <div className="flex justify-between items-start mb-4">
          <div className="flex-1">
            <div className="flex items-center mb-2">
              <span className={`px-3 py-1 text-xs font-semibold rounded-full ${
                report.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                report.status === 'resolved' ? 'bg-green-100 text-green-800' :
                'bg-red-100 text-red-800'
              }`}>
                {report.status}
              </span>
              <span className="ml-3 text-sm text-gray-500">
                Reported on {new Date(report.created_at).toLocaleDateString()}
              </span>
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">{report.reason}</h3>
            <p className="text-gray-700 mb-3">{report.description}</p>
            <div className="text-sm text-gray-600">
              <p><strong>Reporter:</strong> {report.reporter_name || 'Anonymous'}</p>
              <p><strong>Reported User:</strong> {report.reported_user_name || `User #${report.reported_user}`}</p>
            </div>
          </div>
        </div>
        {report.status === 'pending' && (
          <div className="flex space-x-3">
            <button
              onClick={() => onReview(report.id, 'resolved')}
              className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition duration-150 text-sm font-medium"
            >
              Mark as Resolved
            </button>
            <button
              onClick={() => onReview(report.id, 'dismissed')}
              className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition duration-150 text-sm font-medium"
            >
              Dismiss
            </button>
          </div>
        )}
      </div>
    ))}
    {reports.length === 0 && (
      <div className="text-center py-12 text-gray-500">No reports found</div>
    )}
  </div>
);

// Exports Tab Component
const ExportsTab = ({ exportLogs, onExportPDF, onExportExcel, exporting }) => (
  <div>
    {/* Export Buttons */}
    <div className="mb-8 flex space-x-4">
      <button
        onClick={onExportPDF}
        disabled={exporting}
        className="flex-1 bg-gradient-to-r from-red-600 to-pink-600 text-white px-6 py-4 rounded-lg hover:from-red-700 hover:to-pink-700 transition duration-150 font-medium disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
      >
        {exporting ? (
          <svg className="animate-spin h-5 w-5 text-white mr-2" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
        ) : (
          <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
          </svg>
        )}
        Export to PDF
      </button>
      <button
        onClick={onExportExcel}
        disabled={exporting}
        className="flex-1 bg-gradient-to-r from-green-600 to-emerald-600 text-white px-6 py-4 rounded-lg hover:from-green-700 hover:to-emerald-700 transition duration-150 font-medium disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
      >
        {exporting ? (
          <svg className="animate-spin h-5 w-5 text-white mr-2" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
        ) : (
          <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        )}
        Export to Excel
      </button>
    </div>

    {/* Export History */}
    <h3 className="text-lg font-semibold text-gray-900 mb-4">Export History</h3>
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Format</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Records</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Exported By</th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {exportLogs.map((log) => (
            <tr key={log.id} className="hover:bg-gray-50">
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {new Date(log.created_at).toLocaleString()}
              </td>
              <td className="px-6 py-4 whitespace-nowrap">
                <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                  log.format === 'PDF' ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'
                }`}>
                  {log.format}
                </span>
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{log.record_count || 0}</td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{log.exported_by || 'Admin'}</td>
            </tr>
          ))}
        </tbody>
      </table>
      {exportLogs.length === 0 && (
        <div className="text-center py-12 text-gray-500">No export history found</div>
      )}
    </div>
  </div>
);

// Password Resets Tab Component
const PasswordResetsTab = ({ requests, onApprove, onReject }) => (
  <div>
    <div className="mb-6">
      <h2 className="text-xl font-semibold text-gray-900 mb-2">Password Reset Requests</h2>
      <p className="text-gray-600">Review and process password reset requests from users</p>
    </div>

    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">User</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Email</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Reason</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Requested</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {requests.map((request) => (
            <tr key={request.id} className="hover:bg-gray-50">
              <td className="px-6 py-4 whitespace-nowrap">
                <div className="text-sm font-medium text-gray-900">{request.user_username || `User #${request.user}`}</div>
                {request.user_full_name && (
                  <div className="text-sm text-gray-500">{request.user_full_name}</div>
                )}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{request.email}</td>
              <td className="px-6 py-4 text-sm text-gray-700">
                {request.reason || <span className="text-gray-400 italic">No reason provided</span>}
              </td>
              <td className="px-6 py-4 whitespace-nowrap">
                <span className={`px-3 py-1 text-xs font-semibold rounded-full ${
                  request.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                  request.status === 'approved' ? 'bg-green-100 text-green-800' :
                  'bg-red-100 text-red-800'
                }`}>
                  {request.status.toUpperCase()}
                </span>
                {request.status === 'approved' && request.new_password && (
                  <div className="mt-2 p-3 bg-yellow-50 border-2 border-yellow-400 rounded-lg">
                    <div className="flex items-center text-sm">
                      <svg className="w-4 h-4 text-yellow-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
                      </svg>
                      <span className="font-mono font-bold text-yellow-900">{request.new_password}</span>
                    </div>
                    <p className="text-xs text-yellow-700 mt-1">New password generated</p>
                  </div>
                )}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {new Date(request.created_at).toLocaleString()}
                {request.processed_at && (
                  <div className="text-xs text-gray-400 mt-1">
                    Processed: {new Date(request.processed_at).toLocaleString()}
                  </div>
                )}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm">
                {request.status === 'pending' ? (
                  <div className="flex space-x-2">
                    <button
                      onClick={() => onApprove(request.id)}
                      className="px-3 py-1.5 bg-green-600 text-white rounded hover:bg-green-700 transition duration-150 font-medium flex items-center"
                    >
                      <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                      </svg>
                      Approve
                    </button>
                    <button
                      onClick={() => onReject(request.id)}
                      className="px-3 py-1.5 bg-red-600 text-white rounded hover:bg-red-700 transition duration-150 font-medium flex items-center"
                    >
                      <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                      </svg>
                      Reject
                    </button>
                  </div>
                ) : (
                  <div className="text-gray-500">
                    {request.processed_by_username && (
                      <span className="text-xs">By: {request.processed_by_username}</span>
                    )}
                    {request.admin_notes && (
                      <div className="text-xs text-gray-400 mt-1 italic">{request.admin_notes}</div>
                    )}
                  </div>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      {requests.length === 0 && (
        <div className="text-center py-12">
          <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
          </svg>
          <p className="mt-4 text-gray-500">No password reset requests found</p>
        </div>
      )}
    </div>
  </div>
);

export default AdminDashboard;
