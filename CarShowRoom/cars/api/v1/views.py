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

from cars.api.serializers import CarBrandSerializer, CarSerializer
from cars.models import Car, CarBrand


class RetrieveUpdateCreateCarBrand(
    UpdateModelMixin, RetrieveModelMixin, CreateModelMixin, GenericViewSet
):
    """ViewSet for retrieving, updating and creating CarBrand instances"""

    queryset = CarBrand.objects.filter(is_active=True)
    serializer_class = CarBrandSerializer
    lookup_field = "slug"
    lookup_url_kwarg = "slug"


class GetCarBrands(ListModelMixin, GenericViewSet):
    """ViewSet for getting a list of all active CarBrand instances"""

    queryset = CarBrand.objects.filter(is_active=True)
    serializer_class = CarBrandSerializer


class GetCarList(ListModelMixin, GenericViewSet):
    """ViewSet for getting a list of all active Car instances"""

    queryset = Car.objects.filter(is_active=True)
    serializer_class = CarSerializer


class CreateRetrieveUpdateCar(
    RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, GenericViewSet
):
    """ViewSet for creating, retrieving and updating Car instances"""

    queryset = Car.objects.all()
    serializer_class = CarSerializer

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
