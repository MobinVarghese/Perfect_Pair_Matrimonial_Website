"""
Custom permission classes for the matrimonial website.
Implements role-based access control and ownership checks.
"""

from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    Read permissions are allowed to any authenticated user.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any authenticated request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner
        if hasattr(obj, 'user'):
            return obj.user == request.user
        return obj == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins to edit objects.
    Read permissions are allowed to any authenticated user.
    """
    
    def has_permission(self, request, view):
        # Authenticated users can read
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        # Only admins can write
        return request.user and request.user.is_authenticated and request.user.is_admin


class IsReportOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission for reports.
    - Reporter can view their own reports
    - Admins can view and manage all reports
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Admins have full access
        if request.user.is_admin:
            return True
        
        # Reporter can view their own reports
        if hasattr(obj, 'reporter'):
            return obj.reporter == request.user
        
        return False


class IsProfileOwner(permissions.BasePermission):
    """
    Custom permission to only allow profile owners to edit their profile.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any authenticated request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the profile owner
        return obj.user == request.user


class IsInterestParticipant(permissions.BasePermission):
    """
    Custom permission for interests.
    - Sender can view and cancel
    - Receiver can view and respond
    """
    
    def has_object_permission(self, request, view, obj):
        # Both sender and receiver can view
        if request.method in permissions.SAFE_METHODS:
            return obj.sender == request.user or obj.receiver == request.user
        
        # Sender can delete (cancel)
        if request.method == 'DELETE':
            return obj.sender == request.user
        
        # Receiver can update (respond)
        if request.method in ['PUT', 'PATCH']:
            return obj.receiver == request.user
        
        return False


class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow access to admin users.
    Checks the custom is_admin field.
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_admin


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to access it.
    """
    
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'user'):
            return obj.user == request.user
        return obj == request.user
