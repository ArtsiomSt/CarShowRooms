from rest_framework import routers

from .views import CustomerRegisterViewSet

router = routers.DefaultRouter()
router.register("register", CustomerRegisterViewSet)

urlpatterns = router.urls

from rest_framework.urls import path
from .views import CeleryView


urlpatterns += [
    path("celery/", CeleryView.as_view())
]
