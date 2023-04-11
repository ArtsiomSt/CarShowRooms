import datetime
from django.db import models
from django_countries.fields import CountryField
from cars.models import CarBrand, Car


class CarShowRoom(models.Model):
    class PriceCategory(models.TextChoices):
        CHEAP = "C", "Cheap"
        MEDIUM = "M", "Medium"
        LUXURY = "L", "Luxury"

    name = models.CharField(max_length=40)
    city = models.CharField(max_length=40)
    country = CountryField()
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    car_brands = models.ManyToManyField(CarBrand, through='ShowroomBrand')
    dealers = models.ManyToManyField('Dealer', through='DealerShowroom')
    price_category = models.CharField(
        max_length=10, choices=PriceCategory.choices, default=PriceCategory.MEDIUM
    )
    date_created = models.DateTimeField(default=datetime.datetime.now())
    date_modified = models.DateTimeField(default=datetime.datetime.now())
    is_active = models.BooleanField(default=True)


class Dealer(models.Model):
    name = models.CharField(max_length=40)
    year_founded = models.IntegerField(default=datetime.datetime.now().year)
    money_turnover = models.DecimalField(max_digits=8, decimal_places=2)
    car_list = models.ManyToManyField(Car, through='DealerCar')
    date_created = models.DateTimeField(default=datetime.datetime.now())
    date_modified = models.DateTimeField(default=datetime.datetime.now())
    is_active = models.BooleanField(default=True)


class ShowroomBrand(models.Model):
    car_showroom = models.ForeignKey(CarShowRoom, on_delete=models.CASCADE)
    car_brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE)


class DealerCar(models.Model):
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    cars_amount = models.IntegerField(default=1)
    cars_sold = models.IntegerField(default=0)


class DealerShowroom(models.Model):
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE)
    car_showroom = models.ForeignKey(CarShowRoom, on_delete=models.CASCADE)

