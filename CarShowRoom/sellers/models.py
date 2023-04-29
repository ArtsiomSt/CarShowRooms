from django.core.validators import MinValueValidator
from django.db import models
from django_countries.fields import CountryField

from cars.models import Car, CarBrand
from core.enums.carenums import PriceCategory
from core.enums.moneyenums import MoneyCurrency
from core.models import CarPriceCurrency, User, DefaultTimeFields
from core.validation.validators import validate_positive, validate_discount


class CarShowRoom(User):
    name = models.CharField(max_length=40, null=False, blank=False, unique=True)
    city = models.CharField(max_length=40)
    country = CountryField()
    address = models.TextField()
    margin = models.FloatField(validators=[validate_positive])
    balance = models.OneToOneField(
        "Balance",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="car_showroom",
    )
    car_brands = models.ManyToManyField(
        CarBrand, through="ShowroomBrand", related_name="car_showrooms"
    )
    car_list = models.ManyToManyField(
        Car, through="ShowroomCar", related_name="car_showrooms"
    )
    price_category = models.CharField(
        max_length=10,
        choices=PriceCategory.choices(),
        default=PriceCategory.MEDIUM.name,
    )

    def __str__(self):
        return f"{self.name} showroom located in {self.country}"


class Dealer(User):
    name = models.CharField(max_length=40, null=False, blank=False, unique=True)
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
        related_name="dealer",
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


class ShowroomCar(models.Model):
    car_showroom = models.ForeignKey(CarShowRoom, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE, null=True, blank=True)
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


class Discount(DefaultTimeFields):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    car_showroom = models.ForeignKey(
        CarShowRoom,
        on_delete=models.CASCADE,
        related_name="discounts",
        null=True,
        blank=True,
    )
    dealer = models.ForeignKey(
        Dealer,
        on_delete=models.CASCADE,
        related_name="discounts",
        null=True,
        blank=True,
    )
    discount_percent = models.IntegerField(validators=[validate_discount])
    cars = models.ManyToManyField(Car, through="DiscountCar", related_name="discounts")

    def __str__(self):
        return f"{self.car_showroom if self.car_showroom else self.dealer} - discount"


class DiscountCar(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE)
    sold_with_discount = models.IntegerField(default=0, validators=[validate_positive])
    new_car_price = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True
    )
    currency = models.CharField(
        max_length=30, choices=MoneyCurrency.choices(), default=MoneyCurrency.USD.name
    )

    def __str__(self):
        return f"{self.car} discount"


class SupplyHistory(CarPriceCurrency):
    car_showroom = models.ForeignKey(CarShowRoom, on_delete=models.PROTECT, related_name="supplies")
    dealer = models.ForeignKey(Dealer, on_delete=models.PROTECT, related_name='supplies')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='supplies')
    cars_amount = models.IntegerField(validators=[validate_positive])
    date_of_supply = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.car} supply'
