from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from sellers.api.serializers import BalanceSerializer
from sellers.models import Balance


class RegisterSerializer(serializers.ModelSerializer):
    """This serializer implements registration for models, that need field balance"""

    balance = BalanceSerializer(read_only=True)
    password = serializers.CharField(
        max_length=100, write_only=True, validators=[validate_password]
    )

    def create(self, validated_data):
        new_balance = Balance.objects.create(money_amount=0)
        validated_data["balance"] = new_balance
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)
