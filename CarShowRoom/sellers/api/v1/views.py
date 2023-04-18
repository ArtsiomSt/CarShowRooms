from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet

from sellers.api.serializers import CarShowRoomSerializer, DealerSerializer
from sellers.models import CarShowRoom, Dealer


class CarShowRoomRegisterViewSet(CreateModelMixin, GenericViewSet):
    queryset = CarShowRoom.objects.filter(is_active=True)
    serializer_class = CarShowRoomSerializer


class DealerRegisterViewSet(CreateModelMixin, GenericViewSet):
    queryset = Dealer.objects.filter(is_active=True)
    serializer_class = DealerSerializer
