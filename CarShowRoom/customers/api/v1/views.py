from django.core.cache import cache
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from rest_framework.response import Response

from CarShowRoom.settings import USER_CONFIRMATION_KEY
from customers.api.serializers import CustomerSerializer
from customers.models import Customer


class CustomerRegisterViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    """ViewSet that provides registration for Customer model"""

    queryset = Customer.objects.filter(is_active=True)
    serializer_class = CustomerSerializer


class ConfirmEmailView(APIView):
    def get(self, request, token):
        redis_key = USER_CONFIRMATION_KEY.format(token=token)
        user_info = cache.get(redis_key)
        if user_info:
            user_id = user_info.get("user_id", "")
            if user_id:
                instance = get_object_or_404(Customer, id=user_info.get("user_id"))
                setattr(instance, "is_email_verified", True)
                instance.save()
                print(user_id, "email is now activated")
                return Response({"message": "email has been successfully verified"}, status=status.HTTP_200_OK)
        return Response({"message": "this link is not active"}, status=status.HTTP_400_BAD_REQUEST)
