from django.urls import path
from rest_framework import routers

from .views import AddCarForDealerView, CarBrandViewSet, CarViewSet

router = routers.DefaultRouter()
router.register(r"carbrand", CarBrandViewSet)
router.register(r"car", CarViewSet)

urlpatterns = router.urls

urlpatterns += [
    path("car/<int:car_id>/add/", AddCarForDealerView.as_view()),
]
