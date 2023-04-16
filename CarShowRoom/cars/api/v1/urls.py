from django.urls import path

from .views import (
    CreateUpdateCar,
    GetCarBrands,
    GetCarList,
    RetrieveUpdateCreateCarBrand,
)

urlpatterns = [
    path("", GetCarList.as_view(), name="cars"),
    path("changecar/", CreateUpdateCar.as_view(), name="cu_cars"),
    path(
        "carbrands/<slug:slug>",
        RetrieveUpdateCreateCarBrand.as_view(),
        name="cru_carbrand",
    ),
    path("carbrands/", GetCarBrands.as_view(), name="carbrands"),
]
