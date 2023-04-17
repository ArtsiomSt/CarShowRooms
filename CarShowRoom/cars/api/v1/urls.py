from rest_framework import routers

from .views import CarBrandViewSet, CarViewSet

router = routers.DefaultRouter()
router.register(r"carbrand", CarBrandViewSet)
router.register(r"car", CarViewSet)

urlpatterns = router.urls
