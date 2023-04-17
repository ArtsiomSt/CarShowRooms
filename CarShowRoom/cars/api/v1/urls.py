from rest_framework import routers

from .views import (
    CreateRetrieveUpdateCar,
    GetCarBrands,
    GetCarList,
    RetrieveUpdateCreateCarBrand,
)

router = routers.DefaultRouter()
router.register(r"carbrands", GetCarBrands)
router.register(r"carbrand", RetrieveUpdateCreateCarBrand)
router.register(r"", GetCarList)
router.register(r"car", CreateRetrieveUpdateCar)

urlpatterns = []

urlpatterns += router.urls
