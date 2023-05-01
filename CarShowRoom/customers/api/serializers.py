from rest_framework import serializers

from cars.api.serializers import CarSerializer
from core.serializers import RegisterSerializer
from customers.models import Customer, Offer


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
    car = CarSerializer()
    car_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Offer
        fields = ("max_price", "currency", "is_processed", "car_id", "car", "details")
        read_only_fields = ("is_processed", "car", "details")
