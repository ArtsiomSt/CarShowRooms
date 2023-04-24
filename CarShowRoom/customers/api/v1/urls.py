from rest_framework import routers

from .views import CustomerRegisterViewSet

router = routers.DefaultRouter()
router.register("register", CustomerRegisterViewSet)

urlpatterns = router.urls
