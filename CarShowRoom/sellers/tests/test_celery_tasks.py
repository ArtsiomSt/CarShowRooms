import random

import pytest

from cars.models import CarBrand
from core.enums.carenums import PriceCategory
from sellers.models import DealerCar, ShowroomBrand, ShowroomCar
from sellers.tasks import update_dealer_showroom_relations, update_showrooms_car

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
    update_dealer_showroom_relations()
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


def random_amount_of_elements(array):
    return [random.choice(array) for _ in range(random.randrange(0, len(array)))]
