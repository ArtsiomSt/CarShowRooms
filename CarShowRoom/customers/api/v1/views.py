from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet

from customers.api.permissions import IsCustomer
from customers.api.serializers import CustomerSerializer, OfferSerializer
from customers.models import Customer, Offer


class CustomerRegisterViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    """ViewSet that provides registration for Customer model"""

    queryset = Customer.objects.filter(is_active=True)
    serializer_class = CustomerSerializer


class OfferViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [IsCustomer]
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

    def get_queryset(self):
        return Offer.objects.filter(made_by_customer=self.request.user)
