from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django_countries.fields import CountryField
from core.enums.carenums import PriceCategory
from core.enums.moneyenums import MoneyCurrency
from core.validation.validators import validate_positive, validate_phone
from core.models import DefaultTimeFields, CarPriceCurrency
from cars.models import CarBrand, Car


class CarShowRoom(User):
    name = models.CharField(max_length=40)
    city = models.CharField(max_length=40)
    country = CountryField()
    address = models.TextField()
    margin = models.FloatField(validators=[validate_positive])
    balance = models.OneToOneField(
        "Balance",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="instance",
    )
    phone_number = models.CharField(
        max_length=20, null=True, blank=True, validators=[validate_phone]
    )
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
        return f"{self.name} showroom located in {self.country}"


class Dealer(User):
    name = models.CharField(max_length=40)
    phone_number = models.CharField(
        max_length=20, null=True, blank=True, validators=[validate_phone]
    )
    year_founded = models.IntegerField(
        validators=[
            MinValueValidator(
                limit_value=1800, message="Year should be greater than 1800"
            )
        ]
    )
    balance = models.OneToOneField(
        "Balance",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="instance",
    )
    car_list = models.ManyToManyField(Car, through="DealerCar", related_name="dealers")

    def __str__(self):
        return f"{self.name} dealer"


class Balance(models.Model):
    money_amount = models.DecimalField(
        max_digits=9, decimal_places=2, validators=[validate_positive]
    )
    currency = models.CharField(
        max_length=40, choices=MoneyCurrency.choices(), default=MoneyCurrency.USD.name
    )
    last_deposit = models.DateTimeField(null=True, blank=True, default=None)
    last_spent = models.DateTimeField(null=True, blank=True, default=None)


class ShowroomBrand(models.Model):
    car_showroom = models.ForeignKey(CarShowRoom, on_delete=models.CASCADE)
    car_brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.car_showroom} sells cars from {self.car_brand}"


class DealerCar(CarPriceCurrency):
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    car_sold = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.dealer} supplies {self.car}"


class ShowroomCar(CarPriceCurrency):
    car_showroom = models.ForeignKey(CarShowRoom, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE)
    car_amount = models.IntegerField(default=1)
    car_sold = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.car_showroom} sells {self.car}"


class DealerShowroom(models.Model):
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE)
    car_showroom = models.ForeignKey(CarShowRoom, on_delete=models.CASCADE)
    deals_amount = models.IntegerField(default=1)
    discount = models.FloatField(default=0)

    def __str__(self):
        return f"{self.dealer} cooperates with {self.car_showroom}"
