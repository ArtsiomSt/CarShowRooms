from django.contrib.auth.models import AbstractUser
from django.db import models

from .enums.moneyenums import MoneyCurrency
from .enums.userenums import UserType
from .validation.validators import validate_phone, validate_positive


class DefaultTimeFields(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class CarPriceCurrency(models.Model):
    car_price = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[validate_positive]
    )
    currency = models.CharField(
        max_length=40, choices=MoneyCurrency.choices(), default=MoneyCurrency.USD.name
    )

    class Meta:
        abstract = True


class User(AbstractUser):
    email = models.EmailField(blank=False, null=False, unique=True)
    phone_number = models.CharField(
        max_length=20, blank=True, null=True, validators=[validate_phone]
    )
    is_email_verified = models.BooleanField(default=False)
    user_type = models.CharField(
        blank=False,
        null=False,
        choices=UserType.choices(),
        default=UserType.CUSTOMER.name,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
