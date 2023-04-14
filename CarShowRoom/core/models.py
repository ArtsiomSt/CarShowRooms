from django.db import models
from django.utils import timezone

from .enums.moneyenums import MoneyCurrency
from .validation.validators import validate_positive


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
