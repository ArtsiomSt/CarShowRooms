from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsDealerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return bool(
            request.user.user_type == "DEALER" and
            request.user.is_email_verified or
            request.method in SAFE_METHODS
        )
