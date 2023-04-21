from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from sellers.models import Balance

from .enums.moneyenums import MoneyCurrency
from .service import send_verification_email
from .validation.validators import validate_positive


class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Balance
        fields = ("money_amount", "currency")


class RegisterSerializer(serializers.ModelSerializer):
    """This serializer implements registration with email verification for models"""

    balance = BalanceSerializer(read_only=True)
    password = serializers.CharField(
        max_length=100, write_only=True, validators=[validate_password]
    )

    def create(self, validated_data):
        if hasattr(self, "Meta"):
            validated_data["user_type"] = self.Meta.model.__name__.upper()
        validated_data["password"] = make_password(validated_data["password"])
        created_user = super().create(validated_data)
        send_verification_email(
            created_user,
            "Email verification",
            "To confirm your email use this link",
            self.context["request"],
        )
        return created_user


class CarPriceCurrencySerializer(serializers.ModelSerializer):
    car_price = serializers.DecimalField(
        max_digits=6, decimal_places=2, validators=[validate_positive]
    )
    currency = serializers.ChoiceField(choices=MoneyCurrency.choices())
