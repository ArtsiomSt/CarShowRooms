from rest_framework import routers

from .views import CarShowRoomRegisterViewSet, DealerRegisterViewSet

router = routers.DefaultRouter()
router.register(r"register/showroom", CarShowRoomRegisterViewSet)
router.register(r"register/dealer", DealerRegisterViewSet)

urlpatterns = router.urls
