from django.db import models
from django.utils import timezone
from sellers.models import CarShowRoom, Car


class Customer(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True)
    money_balance = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    date_register = models.DateTimeField(default=timezone.now())
    date_modified = models.DateTimeField(default=timezone.now())
    is_active = models.BooleanField(default=True)
    showrooms = models.ManyToManyField(
        CarShowRoom, through="ShowroomCustomer", related_name="customers"
    )


class Offer(models.Model):
    max_price = models.DecimalField(max_digits=7, decimal_places=2)
    is_processed = models.BooleanField(default=False)
    made_by_customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="offers")
    date_created = models.DateTimeField(default=timezone.now())
    date_modified = models.DateTimeField(default=timezone.now())
    is_active = models.BooleanField(default=True)


class TransactionHistory(models.Model):
    offer = models.ForeignKey(
        Offer, on_delete=models.CASCADE, related_name="transactions"
    )
    resulted_price = models.DecimalField(max_digits=6, decimal_places=2)
    car_showroom = models.ForeignKey(CarShowRoom, on_delete=models.PROTECT)
    date_created = models.DateTimeField(default=timezone.now())
    date_modified = models.DateTimeField(default=timezone.now())
    is_active = models.BooleanField(default=True)


class ShowroomCustomer(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    car_showroom = models.ForeignKey(CarShowRoom, on_delete=models.CASCADE)
    deals_amount = models.IntegerField(default=1)
    discount = models.FloatField(default=0)
