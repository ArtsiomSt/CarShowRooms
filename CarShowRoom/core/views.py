from django.core.cache import cache
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from CarShowRoom.settings import USER_CONFIRMATION_KEY

from .models import User
from .service import send_verification_email


class ConfirmEmailView(APIView):
    """View for confirming email by token from redis"""

    def get(self, request, token):
        redis_key = USER_CONFIRMATION_KEY.format(token=token)
        user_info = cache.get(redis_key)
        if user_info:
            user_id = user_info.get("user_id", "")
            if user_id:
                instance = get_object_or_404(User, id=user_info.get("user_id"))
                setattr(instance, "is_email_verified", True)
                instance.save()
                return Response(
                    {"message": "email has been successfully verified"},
                    status=status.HTTP_200_OK,
                )
        return Response(
            {"message": "this link is not active"}, status=status.HTTP_400_BAD_REQUEST
        )


class ManualConfirmEmailView(APIView):
    """View for manually sending a request for email verification"""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        send_verification_email(
            request.user, "Email verification", "To confirm email use this", request
        )
        return Response(
            {
                "message": f"we have sent you verification email, check {request.user.email}"
            },
            status=status.HTTP_200_OK,
        )
