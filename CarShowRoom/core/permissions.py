from rest_framework.permissions import BasePermission


class IsAnonymous(BasePermission):
    def has_permission(self, request, view):
        return bool(not request.user.is_authenticated)
