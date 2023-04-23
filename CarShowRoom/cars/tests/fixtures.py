from rest_framework.test import APIClient
from cars.models import CarBrand, Car
from sellers.models import DealerCar
from rest_framework_simplejwt.tokens import RefreshToken
import pytest


pytest_plugins = [
    "sellers.tests.fixtures",
]


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def password():
    return "zxcvbnm1234567890"


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
    car_instance = Car.objects.create(
        title="string",
        car_brand=car_brand,
        doors_amount=3,
        engine_power=100,
        engine_type="FUEL",
        year_produced=2010,
        price_category="CHEAP",
        length=2,
        width=2,
        height=2,
        max_speed=300,
    )
    DealerCar.objects.create(dealer=dealer_with_email, car=car_instance, car_price=0)
    return car_instance
