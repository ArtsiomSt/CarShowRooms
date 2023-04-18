from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet

from sellers.api.serializers import CarShowRoomSerializer, DealerSerializer
from sellers.models import CarShowRoom, Dealer


class CarShowRoomRegisterViewSet(CreateModelMixin, GenericViewSet):
    """ViewSet that provides registration for CarShowRoom model"""

    queryset = CarShowRoom.objects.filter(is_active=True)
    serializer_class = CarShowRoomSerializer


class DealerRegisterViewSet(CreateModelMixin, GenericViewSet):
    """ViewSet that provides registration for Dealer model"""

    queryset = Dealer.objects.filter(is_active=True)
    serializer_class = DealerSerializer
