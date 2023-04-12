from django.db import models
from django_countries.fields import CountryField
from core.models import DefaultFields
from core.enums.carenums import PriceCategory, EngineType


class CarBrand(DefaultFields):
    title = models.CharField(max_length=30)
    country = CountryField()

    def __str__(self):
        return f'{self.title}'


class Car(DefaultFields):
    title = models.CharField(max_length=40)
    car_brand = models.ForeignKey(
        CarBrand, on_delete=models.PROTECT, null=True, blank=True, related_name="cars"
    )
    doors_amount = models.IntegerField(default=3)
    engine_power = models.IntegerField()
    engine_type = models.CharField(
        max_length=20, choices=EngineType.choices(), default=EngineType.FUEL
    )
    year_produced = models.IntegerField()
    price_category = models.CharField(
        max_length=20, choices=PriceCategory.choices(), default=PriceCategory.MEDIUM
    )
    length = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()
    max_speed = models.IntegerField()

    def __str__(self):
        return f'{self.car_brand} {self.title}'
