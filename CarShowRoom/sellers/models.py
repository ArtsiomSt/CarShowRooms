from django.db import models
from django.utils import timezone
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
    margin = models.FloatField()
    money_balance = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    car_brands = models.ManyToManyField(
        CarBrand, through="ShowroomBrand", related_name="car_showrooms"
    )
    car_list = models.ManyToManyField(
        Car, through="ShowroomCar", related_name="showrooms"
    )
    price_category = models.CharField(
        max_length=10, choices=PriceCategory.choices, default=PriceCategory.MEDIUM
    )
    date_created = models.DateTimeField(default=timezone.now())
    date_modified = models.DateTimeField(default=timezone.now())
    is_active = models.BooleanField(default=True)


class Dealer(models.Model):
    name = models.CharField(max_length=40)
    year_founded = models.IntegerField()
    money_turnover = models.DecimalField(max_digits=8, decimal_places=2)
    car_list = models.ManyToManyField(Car, through="DealerCar", related_name="dealers")
    date_created = models.DateTimeField(default=timezone.now())
    date_modified = models.DateTimeField(default=timezone.now())
    is_active = models.BooleanField(default=True)


class ShowroomBrand(models.Model):
    car_showroom = models.ForeignKey(CarShowRoom, on_delete=models.CASCADE)
    car_brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE)


class DealerCar(models.Model):
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    car_price = models.DecimalField(max_digits=6, decimal_places=2)
    car_sold = models.IntegerField(default=0)


class ShowroomCar(models.Model):
    car_showroom = models.ForeignKey(CarShowRoom, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE)
    car_price = models.DecimalField(max_digits=6, decimal_places=2)
    car_amount = models.IntegerField(default=1)
    car_sold = models.IntegerField(default=0)


class DealerShowroom(models.Model):
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE)
    car_showroom = models.ForeignKey(CarShowRoom, on_delete=models.CASCADE)
    deals_amount = models.IntegerField(default=1)
    discount = models.FloatField(default=0)
