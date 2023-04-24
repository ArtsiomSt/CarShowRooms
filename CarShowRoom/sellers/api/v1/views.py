from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from sellers.api.permissions import IsShowRoomOwnerOrReadOnly
from sellers.api.serializers import (
    CarShowRoomRegisterSerializer,
    CarShowRoomSerializer,
    DealerRegisterSerializer,
    DealerSerializer,
)
from sellers.models import CarShowRoom, Dealer


class CarShowRoomRegisterViewSet(CreateModelMixin, GenericViewSet):
    """ViewSet that provides registration for CarShowRoom model"""

    queryset = CarShowRoom.objects.filter(is_active=True)
    serializer_class = CarShowRoomRegisterSerializer

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
        except ObjectDoesNotExist as e:
            return Response(
                {"car_brands_slugs": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return response


class DealerRegisterViewSet(CreateModelMixin, GenericViewSet):
    """ViewSet that provides registration for Dealer model"""

    queryset = Dealer.objects.filter(is_active=True)
    serializer_class = DealerRegisterSerializer


class CarShowRoomViewSet(
    ListModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet
):
    """ViewSet for retrieving, updating and getting all instances of CarShowRoom model"""

    queryset = CarShowRoom.objects.filter(is_active=True)
    serializer_class = CarShowRoomSerializer
    permission_classes = [IsShowRoomOwnerOrReadOnly]

    def update(self, request, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)
        except ObjectDoesNotExist as e:
            return Response(
                {"car_brand_slug": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return response


class DealerViewSet(
    ListModelMixin, UpdateModelMixin, RetrieveModelMixin, GenericViewSet
):
    queryset = Dealer.objects.filter(is_active=True)
    serializer_class = DealerSerializer
