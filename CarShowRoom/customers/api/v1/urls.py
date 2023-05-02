from rest_framework import routers

from .views import CustomerRegisterViewSet, OfferViewSet

router = routers.DefaultRouter()
router.register("register", CustomerRegisterViewSet)
router.register("offers", OfferViewSet)

urlpatterns = router.urls
