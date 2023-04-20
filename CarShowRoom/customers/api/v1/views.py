from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet

from customers.api.serializers import CustomerSerializer
from customers.models import Customer


class CustomerRegisterViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    """ViewSet that provides registration for Customer model"""

    queryset = Customer.objects.filter(is_active=True)
    serializer_class = CustomerSerializer
