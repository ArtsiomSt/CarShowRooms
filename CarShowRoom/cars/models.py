import datetime
from django.db import models
from django_countries.fields import CountryField


class CarBrand(models.Model):
    title = models.CharField(max_length=30)
    country = CountryField
    date_created = models.DateTimeField(default=datetime.datetime.now())
    date_modified = models.DateTimeField(default=datetime.datetime.now())
    is_active = models.BooleanField(default=True)


class Car(models.Model):
    class EngineType(models.TextChoices):
        FUEL = 'F', 'Fuel'
        DIESEL = 'D', 'Diesel'
        HYBRID = 'H', 'Hybrid'
        GAS = 'G', 'Gas'

    title = models.CharField(max_length=40)
    car_brand = models.ForeignKey(CarBrand, on_delete=models.PROTECT, null=True, blank=True)
    doors_amount = models.IntegerField(default=3)
    engine_power = models.IntegerField()
    engine_type = models.CharField(max_length=20, choices=EngineType.choices, default=EngineType.FUEL)
    year_produced = models.IntegerField(default=datetime.datetime.now().year)
    length = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()
    max_speed = models.IntegerField()
    date_created = models.DateTimeField(default=datetime.datetime.now())
    date_modified = models.DateTimeField(default=datetime.datetime.now())
    is_active = models.BooleanField(default=True)
