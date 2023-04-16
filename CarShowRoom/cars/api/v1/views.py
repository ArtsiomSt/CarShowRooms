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

from cars.api.serializers import CarBrandSerializer, CarSerializer
from cars.models import Car, CarBrand


class RetrieveUpdateCreateCarBrand(
    UpdateModelMixin, RetrieveModelMixin, CreateModelMixin, GenericAPIView
):
    queryset = CarBrand.objects.filter()
    serializer_class = CarBrandSerializer
    lookup_field = "slug"
    lookup_url_kwarg = "slug"

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class GetCarBrands(ListModelMixin, GenericAPIView):
    queryset = CarBrand.objects.filter(is_active=True)
    serializer_class = CarBrandSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class GetCarList(ListModelMixin, GenericAPIView):
    queryset = Car.objects.filter(is_active=True)
    serializer_class = CarSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class CreateUpdateCar(CreateModelMixin, UpdateModelMixin, GenericAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    def create_with_brand(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
        except ObjectDoesNotExist:
            return Response(
                {"car_brand_slug": "Such brand with that slug does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def post(self, request, *args, **kwargs):
        return self.create_with_brand(request, *args, **kwargs)
