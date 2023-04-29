import random

import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from cars.models import CarBrand
from core.enums.carenums import PriceCategory
from sellers.models import DealerCar

from .factory import CarFactory

pytest_plugins = [
    "sellers.tests.fixtures",
]


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def get_token(client):
    def make_token(instance):
        refresh = RefreshToken.for_user(instance)
        return str(refresh.access_token)

    return make_token


@pytest.fixture
def car_brand():
    return CarBrand.objects.create(title="wolkswager", slug="wolks", country="BY")


@pytest.fixture
def car(dealer_with_email, car_brand):
    car_instance = CarFactory(car_brand=car_brand)
    DealerCar.objects.create(dealer=dealer_with_email, car=car_instance, car_price=0)
    return car_instance


@pytest.fixture
def get_two_car_brands():
    def two_car_brands():
        car_brand_one = CarBrand(title="TestOne", slug="to", country="BY")
        car_brand_two = CarBrand(title="TestTwo", slug="tw", country="US")
        return CarBrand.objects.bulk_create([car_brand_one, car_brand_two])

    return two_car_brands


@pytest.fixture
def get_cars():
    def result_function(amount, car_brands):
        cars = [
            CarFactory(
                car_brand=random.choice(car_brands),
                title=f"car{counter}",
                price_category=random.choice(PriceCategory.names()),
            )
            for counter in range(amount)
        ]
        return cars

    return result_function
