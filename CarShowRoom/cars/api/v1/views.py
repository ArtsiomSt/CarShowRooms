from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from rest_framework import status
from rest_framework.decorators import action
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
from core.mixins import DynamicSerializerMixin
from core.service import return_message
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
    DynamicSerializerMixin,
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    GenericViewSet,
):
    """ViewSet for creating, retrieving, updating, getting all Car instances"""

    queryset = Car.objects.filter(is_active=True)
    permission_classes = [IsDealerOrReadOnly]
    serializer_class = CarSerializer
    serializer_mapping = {
        ("get_dealer_car", "add_car_to_dealer", "delete_car_from_dealer"): DealerCarSerializer,
        ("create", "update", "list", "retrieve"): CarSerializer,
    }

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

    @action(detail=True, methods=["get"])
    def get_dealer_car(self, request, *args, **kwargs):
        dealer_with_car_id = DealerCar.objects.filter(
            dealer=request.user.id, car=kwargs["pk"]
        )
        return Response({"exists": True if dealer_with_car_id else False})

    @action(detail=True, methods=["post"])
    def add_car_to_dealer(self, request, *args, **kwargs):
        try:
            result = super().create(request, *args, **kwargs)
        except IntegrityError as e:
            return return_message(str(e), status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist as e:
            return return_message(str(e), status.HTTP_400_BAD_REQUEST)
        return result

    @action(detail=True, methods=["delete"])
    def delete_car_from_dealer(self, request, *args, **kwargs):
        dealer_with_car_id = DealerCar.objects.filter(
            dealer=request.user.id, car=kwargs["pk"]
        )
        if dealer_with_car_id:
            dealer_with_car_id.delete()
            return return_message("Car has been successfully deleted from your list")
        return return_message(
            "there is no such car in your list", status.HTTP_400_BAD_REQUEST
        )
