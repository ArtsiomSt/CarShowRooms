from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsShowRoomOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        request_kwargs = request.parser_context["kwargs"]
        if not request.user.is_authenticated:
            return False
        return bool(
            request.user.user_type == "CARSHOWROOM"
            and request.user.is_email_verified
            and request_kwargs.get("pk", None) == str(request.user.pk)
            or request.method in SAFE_METHODS
        )
