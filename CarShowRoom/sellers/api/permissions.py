from rest_framework.permissions import SAFE_METHODS, BasePermission

from core.enums.userenums import UserType


class IsShowRoomOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        request_kwargs = request.parser_context["kwargs"]
        if not request.user.is_authenticated:
            return False
        return bool(
            request.user.user_type == UserType.CARSHOWROOM.name
            and request.user.is_email_verified
            and request_kwargs.get("pk", None) == str(request.user.pk)
            or request.method in SAFE_METHODS
        )


class IsSeller(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return bool(
            request.user.user_type == UserType.CARSHOWROOM.name
            or request.user.user_type == UserType.DEALER.name
            and request.user.is_email_verified
        )
