from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet

from customers.api.serializers import CustomerSerializer
from customers.models import Customer


class CustomerRegisterViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    """ViewSet that provides registration for Customer model"""

    queryset = Customer.objects.filter(is_active=True)
    serializer_class = CustomerSerializer


from rest_framework.views import APIView
from sellers.tasks import print_something, update_dealer_showroom_relations, supply_cars_from_dealers, update_cars_suppliers
from rest_framework.response import Response
from sellers.models import CarShowRoom, Dealer


class CeleryView(APIView):
    def get(self, request):
        print('test_method')
        #supply_cars_from_dealers()
        #update_dealer_showroom_relations.delay()
        showroom = CarShowRoom.objects.all()[0]
        update_cars_suppliers(showroom)
        return Response({"answer": "success"})
