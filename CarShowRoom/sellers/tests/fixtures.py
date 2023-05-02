import random

import pytest
from pytest_factoryboy import register

from core.enums.carenums import PriceCategory

from .factory import CarShowRoomFactory, DealerFactory

register(DealerFactory, "dealer_without_email")
register(
    DealerFactory,
    "dealer_with_email",
    email="dealer_with_email@pytesttest.com",
    username="dealer_with_email",
    is_email_verified=True,
    name="dealer_with_email",
)

register(CarShowRoomFactory, "showroom_without_email")
register(
    CarShowRoomFactory,
    "showroom_with_email",
    email="showroom_with_email@testpytest.com",
    name="showroom_with_email",
    username="showroom_with_email",
    is_email_verified=True,
)


@pytest.fixture
def get_showrooms():
    def result_function(amount):
        showrooms = [
            CarShowRoomFactory(
                email=f"showroom_dealer_relations@test{counter}.com",
                name=f"showroom{counter}",
                username=f"showroom{counter}",
                price_category=random.choice(PriceCategory.names()),
            )
            for counter in range(amount)
        ]
        return showrooms

    return result_function


@pytest.fixture
def get_dealers():
    def result_function(amount):
        dealers = [
            DealerFactory(
                email=f"dealer_showroom_relations@test{counter}.com",
                name=f"dealer{counter}",
                username=f"dealer{counter}",
            )
            for counter in range(amount)
        ]
        return dealers

    return result_function
