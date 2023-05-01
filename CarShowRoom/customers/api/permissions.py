from rest_framework.permissions import BasePermission

from core.enums.userenums import UserType


class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return bool(
            request.user.user_type == UserType.CUSTOMER.name
            and request.user.is_email_verified
        )
