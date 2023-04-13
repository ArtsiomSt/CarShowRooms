from django.db import models
from django_countries.fields import CountryField
from django.core.validators import MinValueValidator
from core.models import DefaultTimeFields
from core.enums.carenums import PriceCategory, EngineType
from core.validation.validators import validate_positive


class CarBrand(DefaultTimeFields):
    title = models.CharField(max_length=30)
    country = CountryField()

    def __str__(self):
        return f"{self.title}"


class Car(DefaultTimeFields):
    title = models.CharField(max_length=40)
    car_brand = models.ForeignKey(
        CarBrand, on_delete=models.PROTECT, null=True, blank=True, related_name="cars"
    )
    doors_amount = models.IntegerField(default=3, validators=[validate_positive])
    engine_power = models.IntegerField(validators=[validate_positive])
    engine_type = models.CharField(
        max_length=20, choices=EngineType.choices(), default=EngineType.FUEL.name
    )
    year_produced = models.IntegerField(
        validators=[
            MinValueValidator(
                limit_value=1900, message="Year should be greater than 1900"
            )
        ]
    )
    price_category = models.CharField(
        max_length=20,
        choices=PriceCategory.choices(),
        default=PriceCategory.MEDIUM.name,
    )
    length = models.FloatField(validators=[validate_positive])
    width = models.FloatField(validators=[validate_positive])
    height = models.FloatField(validators=[validate_positive])
    max_speed = models.IntegerField(validators=[validate_positive])

    def __str__(self):
        return f"{self.car_brand} {self.title}"
