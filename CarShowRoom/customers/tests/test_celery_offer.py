import random
from datetime import timedelta
from decimal import Decimal

import pytest
from django.utils import timezone

from cars.models import CarBrand
from customers.models import Offer, TransactionHistory
from customers.tasks import process_offers
from sellers.models import (
    Balance,
    DealerCar,
    Discount,
    DiscountCar,
    ShowroomBrand,
    ShowroomCar,
)
from sellers.tasks import update_dealer_showroom_relations, update_showrooms_car

pytest_plugins = [
    "cars.tests.fixtures",
    "sellers.tests.fixtures",
    "customers.tests.fixtures",
]


@pytest.mark.django_db
def test_offer_no_discounts(customer_with_email, get_cars, get_dealers, get_showrooms):
    car_brands = [CarBrand.objects.create(title="CarBrand_0", slug="cb0", country="US")]
    cars = get_cars(1, car_brands)
    car = cars[0]
    showrooms = get_showrooms(3)
    for showroom in showrooms:
        showroom.price_category = car.price_category
        showroom.save()
        ShowroomBrand.objects.create(car_brand=car_brands[0], car_showroom=showroom)
        update_showrooms_car(showroom)
    dealers = get_dealers(3)
    highest_price = 500
    for dealer in dealers:
        assert highest_price > 0
        DealerCar.objects.create(dealer=dealer, car=car, car_price=highest_price)
        highest_price -= 100

    update_dealer_showroom_relations()

    start_car_amount = 10
    for showroom in showrooms:
        showroom_car_objects = ShowroomCar.objects.get(car=car, car_showroom=showroom)
        assert showroom_car_objects.dealer == dealers[-1]
        showroom_car_objects.car_amount = start_car_amount
        showroom_car_objects.save()

    best_showroom_offer = random.choice(showrooms)
    for showroom in showrooms:
        if showroom != best_showroom_offer:
            showroom.margin = 20
        else:
            showroom.margin = 5
        showroom.save()

    start_balance = round(Decimal(1000.00), 2)
    Balance.objects.filter(pk=customer_with_email.balance.pk).update(
        money_amount=start_balance
    )

    offer = Offer.objects.create(
        made_by_customer=customer_with_email, car=car, max_price=314
    )

    process_offers()

    assert (
        Balance.objects.get(pk=customer_with_email.balance.pk).money_amount
        == start_balance
    )
    assert len(TransactionHistory.objects.all()) == 0
    offer = Offer.objects.get(made_by_customer=customer_with_email, car=car)
    assert offer.is_processed is False

    offer.max_price = 400
    offer.save()
    process_offers()

    new_target_balance = round(Decimal(300 * (1 + best_showroom_offer.margin / 100)), 2)
    assert (
        Balance.objects.get(pk=customer_with_email.balance.pk).money_amount
        == start_balance - new_target_balance
    )
    assert (
        Balance.objects.get(pk=best_showroom_offer.balance.pk).money_amount
        == new_target_balance
    )

    worst_offer = random.choice(showrooms)
    for showroom in showrooms:
        if showroom != worst_offer:
            showroom.margin = 20
        else:
            showroom.margin = 40
        Balance.objects.filter(pk=showroom.balance.pk).update(money_amount=0)
        showroom.save()
    discount = Discount.objects.create(
        car_showroom=worst_offer,
        discount_percent=80,
        start_date=timezone.now(),
        end_date=timezone.now() + timedelta(hours=1),
    )
    discount_car_objects = DiscountCar.objects.create(car=car, discount=discount)
    assert worst_offer.margin == 40
    car_price_with_discount = round(
        Decimal(300)
        * (1 + Decimal(worst_offer.margin) / 100)
        * Decimal(1 - discount.discount_percent / 100),
        2,
    )
    Balance.objects.filter(pk=customer_with_email.balance.pk).update(
        money_amount=start_balance
    )
    offer.is_processed = False
    offer.save()

    process_offers()

    assert (
        Balance.objects.get(pk=customer_with_email.balance.pk).money_amount
        == start_balance - car_price_with_discount
    )
    assert (
        Balance.objects.get(pk=worst_offer.balance.pk).money_amount
        == car_price_with_discount
    )
