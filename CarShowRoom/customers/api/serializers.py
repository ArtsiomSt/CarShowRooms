from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from cars.api.serializers import CarSerializer
from cars.models import Car
from core.serializers import RegisterSerializer
from customers.models import Customer, Offer
from customers.tasks import process_offers
from core.exceptions import NoSuchObjectException


class CustomerSerializer(RegisterSerializer):
    class Meta:
        model = Customer
        fields = (
            "phone_number",
            "balance",
            "showrooms",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
        )


class OfferSerializer(serializers.ModelSerializer):
    car = CarSerializer(read_only=True)
    car_id = serializers.IntegerField(write_only=True)

    def create(self, validated_data):
        request = self.context['request']
        validated_data['made_by_customer'] = Customer.objects.get(pk=request.user.pk)
        car_id = validated_data.pop('car_id')
        try:
            validated_data['car'] = Car.objects.get(pk=car_id)
        except ObjectDoesNotExist:
            raise NoSuchObjectException({"car_id": "there is no car with such id"})
        instance = super().create(validated_data)
        process_offers.delay()
        return instance
    
    def update(self, instance, validated_data):
        if "car_id" in validated_data.keys():
            car_id = validated_data.pop("car_id")
            try:
                validated_data['car'] = Car.objects.get(pk=car_id)
            except ObjectDoesNotExist:
                raise NoSuchObjectException({"car_id": "there is no car with such id"})
        instance = super().update(instance, validated_data)
        process_offers.delay()
        return instance

    class Meta:
        model = Offer
        fields = ("id", "max_price", "currency", "is_processed", "car_id", "car", "details")
        read_only_fields = ("is_processed", "car", "details", "id")
