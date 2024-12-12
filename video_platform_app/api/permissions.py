from rest_framework.permissions import BasePermission, SAFE_METHODS


class ReadOnly(BasePermission):
    """
    Permission class allowing read-only access.

    Methods:
        - has_permission: Grants access if the request method is safe (e.g., GET, HEAD, OPTIONS).
        - has_object_permission: Grants access to individual objects if the request method is safe.
    """

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS
