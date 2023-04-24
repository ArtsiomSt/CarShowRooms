from pytest_factoryboy import register

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
