import uuid

from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.cache import cache
from django.core.mail import send_mail
from rest_framework import serializers
from rest_framework.reverse import reverse_lazy

from CarShowRoom.settings import USER_CONFIRMATION_KEY, USER_CONFIRMATION_TIMEOUT
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
    email = serializers.EmailField(required=True)

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        created_user = super().create(validated_data)
        self.send_verification_email(created_user)
        return created_user

    def send_verification_email(self, instance):
        token = uuid.uuid4().hex
        redis_key = USER_CONFIRMATION_KEY.format(token=token)
        cache.set(
            redis_key, {"user_id": instance.pk}, timeout=USER_CONFIRMATION_TIMEOUT
        )
        request = self.context["request"]
        confirm_link = request.build_absolute_uri(
            reverse_lazy("tokens:email_confirm", kwargs={"token": token})
        )
        send_mail(
            "Email verifications",
            f"To verify you email use link bellow\n{confirm_link}",
            "akeonst@yandex.ru",
            [instance.email],
        )
