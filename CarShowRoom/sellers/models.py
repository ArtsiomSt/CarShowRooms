from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from core.models import DefaultFields
from core.enums.carenums import PriceCategory
from cars.models import CarBrand, Car


class CarShowRoom(User):
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
        max_length=10, choices=PriceCategory.choices(), default=PriceCategory.MEDIUM
    )

    def __str__(self):
        return f'{self.name} showroom located in {self.country}'


class Dealer(User):
    name = models.CharField(max_length=40)
    year_founded = models.IntegerField()
    money_turnover = models.DecimalField(max_digits=8, decimal_places=2)
    car_list = models.ManyToManyField(Car, through="DealerCar", related_name="dealers")

    def __str__(self):
        return f'{self.name} dealer'


class ShowroomBrand(models.Model):
    car_showroom = models.ForeignKey(CarShowRoom, on_delete=models.CASCADE)
    car_brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.car_showroom} sells cars from {self.car_brand}'


class DealerCar(models.Model):
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    car_price = models.DecimalField(max_digits=6, decimal_places=2)
    car_sold = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.dealer} supplies {self.car}'


class ShowroomCar(models.Model):
    car_showroom = models.ForeignKey(CarShowRoom, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE)
    car_price = models.DecimalField(max_digits=6, decimal_places=2)
    car_amount = models.IntegerField(default=1)
    car_sold = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.car_showroom} sells {self.car}'


class DealerShowroom(models.Model):
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE)
    car_showroom = models.ForeignKey(CarShowRoom, on_delete=models.CASCADE)
    deals_amount = models.IntegerField(default=1)
    discount = models.FloatField(default=0)

    def __str__(self):
        return f'{self.dealer} cooperates with {self.car_showroom}'
