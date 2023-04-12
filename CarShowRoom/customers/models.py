from django.db import models
from django.contrib.auth.models import User
from sellers.models import CarShowRoom, Car
from core.models import DefaultFields


class Customer(User):
    phone_number = models.CharField(max_length=20, blank=True)
    money_balance = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    showrooms = models.ManyToManyField(
        CarShowRoom, through="ShowroomCustomer", related_name="customers"
    )

    def __str__(self):
        return f'{self.last_name} {self.first_name}'


class Offer(DefaultFields):
    max_price = models.DecimalField(max_digits=7, decimal_places=2)
    is_processed = models.BooleanField(default=False)
    made_by_customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="offers")

    def __str__(self):
        return f'Offer made by {self.made_by_customer} for the {self.car}'


class TransactionHistory(DefaultFields):
    offer = models.ForeignKey(
        Offer, on_delete=models.CASCADE, related_name="transactions"
    )
    resulted_price = models.DecimalField(max_digits=6, decimal_places=2)
    car_showroom = models.ForeignKey(CarShowRoom, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.offer}'.replace('Offer', 'Transaction')


class ShowroomCustomer(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    car_showroom = models.ForeignKey(CarShowRoom, on_delete=models.CASCADE)
    deals_amount = models.IntegerField(default=1)
    discount = models.FloatField(default=0)

    def __str__(self):
        return f'Customer - {self.customer}, showroom - {self.car_showroom}'
