from rest_framework import routers

from .views import CustomerViewSet

router = routers.DefaultRouter()
router.register("register", CustomerViewSet)

urlpatterns = router.urls
