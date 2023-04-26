import os

from celery import Celery
from django.core.mail import send_mail

from CarShowRoom.celery import app
from sellers.models import CarShowRoom


@app.task
def print_something():
    print("something from celery")
    print(CarShowRoom.objects.all())
