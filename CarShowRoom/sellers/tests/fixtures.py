import pytest

from sellers.models import CarShowRoom, Dealer


@pytest.fixture
def password():
    return "zxcvbnm1234567890"


@pytest.fixture
def dealer_with_email(password):
    return Dealer.objects.create(
        email="dealer_with_email@testexample.com",
        password=password,
        username="dealer_email",
        name="dealer_with_email_test",
        phone_number="+37529623542",
        year_founded=2023,
        is_email_verified=True,
        user_type="DEALER",
    )


@pytest.fixture
def dealer_without_email(password):
    return Dealer.objects.create(
        email="dealer_without_email@testexample.com",
        password=password,
        username="dealer_no_email",
        name="dealer_without_email_test",
        phone_number="+37529623542",
        year_founded=2023,
        is_email_verified=False,
        user_type="DEALER",
    )


@pytest.fixture
def showroom_with_email(password):
    return CarShowRoom.objects.create(
        email="showroom_for_test@testpytest.com",
        name="showroom_for_test",
        username="showroom_email",
        country="RU",
        city="CityTest",
        address="string",
        user_type="CARSHOWROOM",
        margin=1,
        phone_number="+36482734",
        is_email_verified=True,
        password=password,
    )


@pytest.fixture
def showroom_without_email():
    return CarShowRoom.objects.create(
        email="showroom_for_no_email_test@testpytest.com",
        name="showroom_for_test_no_email",
        username="showroom_no_email",
        country="RU",
        city="CityTest",
        address="string",
        user_type="CARSHOWROOM",
        margin=1,
        phone_number="+36482734",
        is_email_verified=False,
        password=password,
    )
