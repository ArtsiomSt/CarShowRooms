from rest_framework import routers

from .views import (
    CarShowRoomRegisterViewSet,
    CarShowRoomViewSet,
    DealerRegisterViewSet,
    DealerViewSet,
    DiscountViewSet,
)

router = routers.DefaultRouter()
router.register(r"showroom", CarShowRoomViewSet)
router.register(r"dealer", DealerViewSet)
router.register(r"register/showroom", CarShowRoomRegisterViewSet)
router.register(r"register/dealer", DealerRegisterViewSet)
router.register(r"discount", DiscountViewSet)

urlpatterns = router.urls
