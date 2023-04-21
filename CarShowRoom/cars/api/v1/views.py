from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from cars.api.permissions import IsDealerOrReadOnly
from cars.api.serializers import CarBrandSerializer, CarSerializer
from cars.models import Car, CarBrand
from sellers.api.serializers import DealerCarSerializer
from sellers.models import DealerCar


class CarBrandViewSet(
    ListModelMixin,
    UpdateModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    GenericViewSet,
):
    """ViewSet for retrieving, updating, creating and getting all CarBrand instances"""

    queryset = CarBrand.objects.filter(is_active=True)
    serializer_class = CarBrandSerializer
    lookup_field = "slug"
    lookup_url_kwarg = "slug"
    permission_classes = [IsDealerOrReadOnly]


class CarViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    GenericViewSet,
):
    """ViewSet for creating, retrieving, updating, getting all Car instances"""

    queryset = Car.objects.filter(is_active=True)
    serializer_class = CarSerializer
    permission_classes = [IsDealerOrReadOnly]

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return Response(
                {"car_brand_slug": "Brand with that slug does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return response

    def update(self, request, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return Response(
                {"car_brand_slug": "Brand with that slug does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return response


class AddCarForDealer(CreateModelMixin, GenericAPIView):
    queryset = DealerCar.objects.all()
    serializer_class = DealerCarSerializer
    permission_classes = [IsDealerOrReadOnly]

    def post(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def delete(self, request, car_id):
        DealerCar.objects.filter(dealer=request.user.id, car=car_id).delete()
        return Response({"message": "Car has been successfully deleted from your list"})
