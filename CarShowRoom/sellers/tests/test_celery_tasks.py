import random
from datetime import timedelta
from decimal import Decimal

import pytest
from django.db.models import F, Sum
from django.utils import timezone

from cars.models import CarBrand
from core.enums.carenums import PriceCategory
from sellers.models import (
    Balance,
    CarShowRoom,
    Dealer,
    DealerCar,
    Discount,
    DiscountCar,
    ShowroomBrand,
    ShowroomCar,
    SupplyHistory,
)
from sellers.tasks import (
    supply_cars_from_dealers,
    update_dealer_showroom_relations,
    update_showrooms_car,
)

pytest_plugins = [
    "cars.tests.fixtures",
    "sellers.tests.fixtures",
    "customers.tests.fixtures",
]


@pytest.mark.django_db
def test_showroom_car_relations(get_showrooms, get_dealers, get_cars):
    """This test checks function that updates showroom's car list"""

    showrooms = get_showrooms(10)
    get_dealers(10)
    car_brands = [
        CarBrand.objects.create(
            title=f"car_brand_t{counter}", slug=f"slug{counter}", country="US"
        )
        for counter in range(5)
    ]
    cars = get_cars(100, car_brands)
    for showroom in showrooms:
        generated_brands = random_amount_of_elements(car_brands)
        if generated_brands:
            ShowroomBrand.objects.bulk_create(
                ShowroomBrand(car_showroom=showroom, car_brand=brand)
                for brand in generated_brands
            )
    for showroom in showrooms:
        update_showrooms_car(showroom)
    for showroom in showrooms:
        for showrooms_car in ShowroomCar.objects.filter(
            car_showroom=showroom
        ).select_related("car"):
            assert showrooms_car.car.car_brand in showroom.car_brands.all()
            assert showrooms_car.dealer is None
            assert showrooms_car.car.price_category == showroom.price_category
    for car in cars:
        for showroom in showrooms:
            if (
                car.car_brand in showroom.car_brands.all()
                and car.price_category == showroom.price_category
            ):
                assert car in showroom.car_list.all()


@pytest.mark.django_db
def test_showroom_car_dealer_relations_hard(get_showrooms, get_dealers, get_cars):
    showrooms = get_showrooms(10)
    dealers = get_dealers(10)
    car_brands = [
        CarBrand.objects.create(
            title=f"car_brand{counter}", slug=f"slug{counter}", country="US"
        )
        for counter in range(100)
    ]
    cars = get_cars(1000, car_brands)
    cheapest_car_dealers = {}
    for car in cars:
        dealer_for_this_car = random_amount_of_elements(dealers)
        if dealer_for_this_car:
            created_relations = DealerCar.objects.bulk_create(
                [
                    DealerCar(
                        car_price=random.randrange(20, 1000), car=car, dealer=dealer
                    )
                    for dealer in dealer_for_this_car
                ]
            )
            min_offer = min(
                created_relations, key=lambda dealercar: dealercar.car_price
            )
            cheapest_car_dealers[car] = min_offer.dealer
        else:
            cheapest_car_dealers[car] = None
    for showroom in showrooms:
        update_showrooms_car(showroom)
    for showroom in showrooms:
        for showrooms_car in ShowroomCar.objects.filter(
            car_showroom=showroom
        ).select_related("car", "dealer"):
            dealercar_object = DealerCar.objects.filter(
                car=showrooms_car.car, dealer=showrooms_car.dealer
            )
            if not dealercar_object:
                assert cheapest_car_dealers[showrooms_car.car] is None
                assert showrooms_car.dealer is None
            assert len(dealercar_object) == 1
            assert showrooms_car.dealer == cheapest_car_dealers[showrooms_car.car]


@pytest.mark.django_db
def test_showroom_car_dealer_relations_easy(get_showrooms, get_dealers, get_cars):
    """
    This test provides one case: we have two showrooms, three
    dealers, 6 cars. First showroom sells first 4 cars, second
    showroom sells last 4 cars.
    """

    showrooms = get_showrooms(2)
    for showroom in showrooms:
        showroom.price_category = PriceCategory.CHEAP.name
        showroom.save()
    dealers = get_dealers(3)
    car_brands = [
        CarBrand.objects.create(
            title=f"car_brand{counter}", slug=f"slug{counter}", country="US"
        )
        for counter in range(4)
    ]
    cars = get_cars(6, car_brands)
    for car in cars:
        car.price_category = PriceCategory.CHEAP.name
        car.save()
    cars[0].car_brand = car_brands[0]
    cars[1].car_brand = car_brands[0]
    cars[2].car_brand = car_brands[1]
    cars[3].car_brand = car_brands[1]
    cars[4].car_brand = car_brands[2]
    cars[5].car_brand = car_brands[2]
    for car in cars:
        car.save()
    ShowroomBrand.objects.bulk_create(
        [
            ShowroomBrand(car_showroom=showrooms[0], car_brand=brand)
            for brand in car_brands[:2]
        ]
    )
    ShowroomBrand.objects.bulk_create(
        [
            ShowroomBrand(car_showroom=showrooms[1], car_brand=brand)
            for brand in car_brands[1:3]
        ]
    )
    for showroom in showrooms:
        update_showrooms_car(showroom)

    #  This part if all cars that fit showrooms were added to their car list
    assert cars[0] in showrooms[0].car_list.all()
    assert cars[1] in showrooms[0].car_list.all()
    assert cars[2] in showrooms[0].car_list.all()
    assert cars[3] in showrooms[0].car_list.all()
    assert cars[4] not in showrooms[0].car_list.all()
    assert cars[5] not in showrooms[0].car_list.all()
    assert cars[0] not in showrooms[1].car_list.all()
    assert cars[1] not in showrooms[1].car_list.all()
    assert cars[2] in showrooms[1].car_list.all()
    assert cars[3] in showrooms[1].car_list.all()
    assert cars[4] in showrooms[1].car_list.all()
    assert cars[5] in showrooms[1].car_list.all()
    DealerCar.objects.bulk_create(
        [
            DealerCar(
                car_price=100, dealer=dealers[0], car=cars[0]
            ),  # this one is best for car[0]
            DealerCar(car_price=200, dealer=dealers[1], car=cars[0]),
            DealerCar(car_price=300, dealer=dealers[2], car=cars[0]),
            DealerCar(car_price=300, dealer=dealers[0], car=cars[1]),
            DealerCar(
                car_price=100, dealer=dealers[1], car=cars[1]
            ),  # this one is best for car[1]
            DealerCar(car_price=200, dealer=dealers[2], car=cars[1]),
            DealerCar(car_price=300, dealer=dealers[0], car=cars[2]),
            DealerCar(car_price=200, dealer=dealers[1], car=cars[2]),
            DealerCar(
                car_price=100, dealer=dealers[2], car=cars[2]
            ),  # this one is best for car[2]
            DealerCar(
                car_price=100, dealer=dealers[0], car=cars[3]
            ),  # this one is best for car[3]
            DealerCar(car_price=200, dealer=dealers[1], car=cars[3]),
            DealerCar(
                car_price=50, dealer=dealers[1], car=cars[4]
            ),  # this one is best for car[4]
        ]
    )

    update_dealer_showroom_relations()  # this function is USED in CELERY

    assert (
        ShowroomCar.objects.get(car_showroom=showrooms[0], car=cars[0]).dealer
        == dealers[0]
    )
    assert (
        ShowroomCar.objects.get(car_showroom=showrooms[0], car=cars[1]).dealer
        == dealers[1]
    )
    assert (
        ShowroomCar.objects.get(car_showroom=showrooms[0], car=cars[2]).dealer
        == dealers[2]
    )
    assert (
        ShowroomCar.objects.get(car_showroom=showrooms[1], car=cars[2]).dealer
        == dealers[2]
    )
    assert (
        ShowroomCar.objects.get(car_showroom=showrooms[0], car=cars[3]).dealer
        == dealers[0]
    )
    assert (
        ShowroomCar.objects.get(car_showroom=showrooms[1], car=cars[3]).dealer
        == dealers[0]
    )
    assert (
        ShowroomCar.objects.get(car_showroom=showrooms[1], car=cars[4]).dealer
        == dealers[1]
    )
    assert (
        ShowroomCar.objects.get(car_showroom=showrooms[1], car=cars[5]).dealer is None
    )
    start_money_amount = Decimal(100000)
    for showroom in showrooms:
        showroom.balance.money_amount = start_money_amount
        showroom.balance.save()

    supply_cars_from_dealers()  # This function is used in CELERY

    # Now we will check that all supplied cars were bought properly(every one received his money and gotten cars)
    showrooms = CarShowRoom.objects.all()
    for showroom in showrooms:
        for car in showroom.car_list.all():
            showroom_car_object = ShowroomCar.objects.get(
                car_showroom=showroom, car=car
            )
            if showroom_car_object.dealer is not None:
                supply_history = SupplyHistory.objects.get(
                    car=car, car_showroom=showroom
                )
                dealer_car_object = DealerCar.objects.get(
                    dealer=showroom_car_object.dealer, car=car
                )
                assert supply_history.car_price == dealer_car_object.car_price
                assert (
                    showroom_car_object.car_amount == 1 + supply_history.cars_amount
                ), "1 because default car_amount is 1(will fix it soon)"
            else:
                assert (
                    len(SupplyHistory.objects.filter(car=car, car_showroom=showroom))
                    == 0
                ), "If there is no dealer there should be no deal"
        showrooms_supply_history = SupplyHistory.objects.filter(
            car_showroom=showroom
        ).aggregate(showrooms_spents=Sum(F("car_price") * F("cars_amount")))[
            "showrooms_spents"
        ]
        assert (
            showroom.balance.money_amount
            == start_money_amount - showrooms_supply_history
        )
    dealers = Dealer.objects.all().order_by("pk")
    for dealer in dealers:
        dealers_supply_history = SupplyHistory.objects.filter(dealer=dealer).aggregate(
            dealers_spents=Sum(F("car_price") * F("cars_amount"))
        )["dealers_spents"]
        assert (
            dealer.balance.money_amount == dealers_supply_history
        ), "Dealer didn't recieve his money"
    SupplyHistory.objects.all().delete()

    # Now we will check the ability of showroom to buy car by discount
    # We will create a discount for dealer[1] for car[0], so it will
    # better to buy this car from this dealer

    discount = Discount.objects.create(
        dealer=dealers[1],
        discount_percent=75,
        start_date=timezone.now(),
        end_date=timezone.now() + timedelta(hours=2),
    )  # so new cost should be 75% from 200
    discount_car_object = DiscountCar.objects.create(car=cars[0], discount=discount)
    target_dealer_car_object = DealerCar.objects.get(car=cars[0], dealer=dealers[1])
    calculated_price = round(Decimal(0.25), 2) * target_dealer_car_object.car_price
    assert discount_car_object.new_car_price == calculated_price
    showroom = ShowroomCar.objects.get(car=cars[0]).car_showroom
    showroom_car_object = ShowroomCar.objects.get(car_showroom=showroom, car=cars[0])
    current_dealer_car_object = DealerCar.objects.get(
        car=cars[0], dealer=showroom_car_object.dealer
    )
    start_balance = showroom.balance.money_amount
    start_dealer0_balance = dealers[0].balance.money_amount
    start_dealer1_balance = dealers[1].balance.money_amount
    assert showroom_car_object.dealer == dealers[0]
    assert current_dealer_car_object.car_price > discount_car_object.new_car_price

    supply_cars_from_dealers()

    showroom = ShowroomCar.objects.get(car=cars[0]).car_showroom
    supply_history = SupplyHistory.objects.get(car=cars[0])
    assert supply_history.dealer != showroom_car_object.dealer
    assert supply_history.dealer == dealers[1]
    assert supply_history.car_price == discount_car_object.new_car_price
    new_showrooms_target_balance = (
        start_balance - supply_history.cars_amount * discount_car_object.new_car_price
    )
    other_spents = (
        SupplyHistory.objects.filter(car_showroom=showroom)
        .exclude(car=cars[0])
        .aggregate(not_target_car=Sum(F("car_price") * F("cars_amount")))[
            "not_target_car"
        ]
    )
    assert showroom.balance.money_amount + other_spents == new_showrooms_target_balance
    assert (
        len(SupplyHistory.objects.filter(car=cars[0]).exclude(dealer=dealers[1])) == 0
    )
    new_dealer0_balance = Balance.objects.get(pk=dealers[0].balance.pk).money_amount
    new_dealer1_balance = Balance.objects.get(pk=dealers[1].balance.pk).money_amount
    dealer1_profit = new_dealer1_balance - start_dealer1_balance
    dealer0_profit = new_dealer0_balance - start_dealer0_balance
    assert (
        dealer0_profit
        + current_dealer_car_object.car_price * supply_history.cars_amount
        == start_dealer0_balance
    ), "This test checked if dealer0 gained less profit since last car_supply action"
    assert (
        dealer1_profit
        == start_dealer1_balance + supply_history.cars_amount * supply_history.car_price
    ), "This test checked if dealer1 got more profit since last car_supply action"


def random_amount_of_elements(array):
    return [random.choice(array) for _ in range(random.randrange(0, len(array)))]
