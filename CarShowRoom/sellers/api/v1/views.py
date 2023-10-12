from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from sellers.api.permissions import IsShowRoomOwnerOrReadOnly, IsSeller
from sellers.api.serializers import (
    CarShowRoomRegisterSerializer,
    CarShowRoomSerializer,
    DealerRegisterSerializer,
    DealerSerializer,
    DiscountSerializer,
)
from sellers.models import CarShowRoom, Dealer, Discount


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


class DiscountViewSet(RetrieveModelMixin, CreateModelMixin, GenericViewSet):
    permission_classes = [IsSeller]
    queryset = Discount.objects.filter(is_active=True)
    serializer_class = DiscountSerializer

    def get_object(self):
        obj = super().get_object()
        user_id = self.request.user.pk
        if not (obj.dealer_id == user_id or obj.car_showroom_id == user_id):
            raise PermissionDenied
        return obj

    def destroy(self, request, *args, **kwargs):
        discount_instance = self.get_object()
        discount_instance.is_active = False
        discount_instance.save()

    def list(self, request, *args, **kwargs):
        user_id = request.user.id
        users_discounts = Discount.objects.filter(
            Q(Q(dealer=user_id) | Q(car_showroom=user_id)) & Q(is_active=True)
        )
        response = []
        for discount in users_discounts:
            response.append(DiscountSerializer(discount).data)
        return Response(response)
