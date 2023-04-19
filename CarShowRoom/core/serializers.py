from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from sellers.models import Balance


class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Balance
        fields = ("money_amount", "currency")


class RegisterSerializer(serializers.ModelSerializer):
    """This serializer implements registration for models, that need field balance"""

    balance = BalanceSerializer(read_only=True)
    password = serializers.CharField(
        max_length=100, write_only=True, validators=[validate_password]
    )

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)
