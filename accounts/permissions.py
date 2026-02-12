from rest_framework.permissions import BasePermission


class IsCreator(BasePermission):
    # Allows access only to authenticated users with role "creator"
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "creator"


class IsViewer(BasePermission):
    # Allows access only to authenticated users with role "viewer"
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "viewer"
