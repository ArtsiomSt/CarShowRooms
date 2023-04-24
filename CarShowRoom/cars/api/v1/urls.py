from django.urls import path
from rest_framework import routers

from .views import CarBrandViewSet, CarViewSet

router = routers.DefaultRouter()
router.register(r"carbrand", CarBrandViewSet)
router.register(r"car", CarViewSet)

urlpatterns = router.urls

urlpatterns += [
    path(
        "car/<int:pk>/add/",
        CarViewSet.as_view(
            {
                "get": "get_dealer_car",
                "post": "add_car_to_dealer",
                "delete": "delete_car_from_dealer",
            }
        ),
    ),
]
