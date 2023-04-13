from django.db import models
from django.contrib.auth.models import User
from sellers.models import CarShowRoom, Car, Balance
from core.models import DefaultTimeFields
from core.validation.validators import validate_positive, validate_phone
from core.enums.moneyenums import MoneyCurrency


class Customer(User):
    phone_number = models.CharField(
        max_length=20, blank=True, null=True, validators=[validate_phone]
    )
    balance = models.OneToOneField(
        Balance,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="balance_customer",
    )
    showrooms = models.ManyToManyField(
        CarShowRoom, through="ShowroomCustomer", related_name="customers"
    )

    def __str__(self):
        return f"Customer - {self.user.username}"


class Offer(DefaultTimeFields):
    max_price = models.DecimalField(
        max_digits=7, decimal_places=2, validators=[validate_positive]
    )
    currency = models.CharField(
        max_length=20, choices=MoneyCurrency.choices(), default=MoneyCurrency.USD.name
    )
    is_processed = models.BooleanField(default=False)
    made_by_customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="offers"
    )
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="offers")

    def __str__(self):
        return f"Offer made by {self.made_by_customer} for the {self.car}"


class TransactionHistory(DefaultTimeFields):
    made_by_customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="transactions"
    )
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="transactions")
    sold_by_showroom = models.ForeignKey(
        CarShowRoom, on_delete=models.PROTECT, related_name="transactions"
    )
    deal_price = models.DecimalField(
        max_digits=7, decimal_places=2, validators=[validate_positive]
    )
    currency = models.CharField(
        max_length=40, choices=MoneyCurrency.choices(), default=MoneyCurrency.USD.name
    )

    def __str__(self):
        return "Transaction"


class ShowroomCustomer(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    car_showroom = models.ForeignKey(CarShowRoom, on_delete=models.CASCADE)
    deals_amount = models.IntegerField(default=1)
    discount = models.FloatField(default=0)

    def __str__(self):
        return f"Customer - {self.customer}, showroom - {self.car_showroom}"
