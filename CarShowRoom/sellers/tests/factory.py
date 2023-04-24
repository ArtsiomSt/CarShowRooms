import factory

from core.enums.userenums import UserType
from sellers.models import CarShowRoom, Dealer


class CarShowRoomFactory(factory.django.DjangoModelFactory):
    email = "showroom_for_no_email_test@testpytest.com"
    name = "showroom_for_test_no_email"
    username = "showroom_no_email"
    country = "RU"
    city = "CityTest"
    address = "string"
    user_type = UserType.CARSHOWROOM.name
    margin = 1
    phone_number = "+36482734"
    is_email_verified = False
    password = "zxcvbnm1234567890"

    class Meta:
        model = CarShowRoom


class DealerFactory(factory.django.DjangoModelFactory):
    email = "dealer_without_email@testexample.com"
    password = "zxcvbnm1234567890"
    username = "dealer_no_email"
    name = "dealer_without_email_test"
    phone_number = "+37529623542"
    year_founded = 2023
    is_email_verified = False
    user_type = UserType.DEALER.name

    class Meta:
        model = Dealer
