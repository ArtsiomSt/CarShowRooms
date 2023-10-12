from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from CarShowRoom.settings import USER_CONFIRMATION_KEY

from .mixins import DynamicPermissionMixin
from .models import User
from .permissions import IsAnonymous
from .reports import get_incomes_expenses, get_cars_stats
from .serializers import ChangeCredsDataSerializer, ForgotPasswordSerializer
from .service import send_change_credentials_email, send_verification_email


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


class ManualConfirmEmailViewSet(DynamicPermissionMixin, ViewSet):
    """View for manually sending a request for email verification"""

    permission_mapping = {
        ("verify_email", "creds_change"): [IsAuthenticated],
        ("forgot_password",): [IsAnonymous],
    }

    @action(detail=True, methods=["get"])
    def verify_email(self, request):
        send_verification_email(
            request.user, "Email verification", "To confirm email use this", request
        )
        return Response(
            {
                "message": f"we have sent you verification email, check {request.user.email}"
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["get"])
    def creds_change(self, request):
        send_change_credentials_email(
            request.user,
            "Email verification",
            "To change your credentials use this link",
            request,
        )
        return Response(
            {
                "message": f"we have sent you a link for changing credentials, check {request.user.email}"
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"])
    def forgot_password(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        users_email = serializer.validated_data["email"]
        try:
            serializer.send_reset_password_email(users_email, request)
        except ObjectDoesNotExist:
            return Response({"message": "there is no user with such email"})
        return Response(
            {
                "message": f"we have sent you a link for changing credentials, check {users_email}"
            },
            status=status.HTTP_200_OK,
        )


class ChangePasswordViewSet(ViewSet):
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        redis_key = USER_CONFIRMATION_KEY.format(token=kwargs["token"])
        user_info = cache.get(redis_key)
        if user_info:
            user_id = user_info.get("user_id", "")
            if user_id:
                instance = get_object_or_404(User, id=user_info.get("user_id"))
                serializer = ChangeCredsDataSerializer(
                    instance, data=request.data, partial=partial
                )
                serializer.is_valid(raise_exception=True)
                serializer.validated_data["reset"] = bool(
                    request.GET.get("reset", False)
                )
                serializer.save()
                return Response(
                    {"message": "credentials changed successfully"},
                    status=status.HTTP_200_OK,
                )
        return Response(
            {"message": "You can not change your password using this link"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)


class ReportViewSet(ViewSet):
    """This ViewSet stands for creating and sending reports about system"""

    permission_classes = [IsAdminUser]

    @action(detail=False, methods=["get"])
    def turnover_reports(self, request):
        reports = get_incomes_expenses()
        return Response(reports)

    @action(detail=False, methods=["get"])
    def car_reports(self, request):
        reports = get_cars_stats()
        return Response(reports)
