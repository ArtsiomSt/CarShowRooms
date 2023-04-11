import datetime
from django.db import models


class Customer(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True)
    money_balance = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    date_register = models.DateTimeField(default=datetime.datetime.now())
    date_modified = models.DateTimeField(default=datetime.datetime.now())
    is_active = models.BooleanField(default=True)


class Offer(models.Model):
    max_price = models.DecimalField(max_digits=7, decimal_places=2)
    is_processed = models.BooleanField(default=False)
    made_by_customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=datetime.datetime.now())
    date_modified = models.DateTimeField(default=datetime.datetime.now())
    is_active = models.BooleanField(default=True)
