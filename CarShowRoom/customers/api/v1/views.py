from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet

from customers.api.permissions import IsCustomer
from customers.api.serializers import CustomerSerializer, OfferSerializer
from customers.models import Customer, Offer
from core.service import return_message


class CustomerRegisterViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    """ViewSet that provides registration for Customer model"""

    queryset = Customer.objects.filter(is_active=True)
    serializer_class = CustomerSerializer


class OfferViewSet(ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    permission_classes = [IsCustomer]
    queryset = Offer.objects.filter(is_active=True)
    serializer_class = OfferSerializer

    def destroy(self, request, *args, **kwargs):
        offer = self.get_object()
        offer.is_active = False
        offer.save()
        return return_message("your offer was successfully destroyed")

    def get_queryset(self):
        return Offer.objects.filter(made_by_customer=self.request.user, is_active=True)
