from decimal import Decimal

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import F, Q
from django.utils import timezone

from cars.models import Car
from CarShowRoom.celery import app
from sellers.models import (
    Balance,
    CarShowRoom,
    Dealer,
    DealerCar,
    ShowroomCar,
    SupplyHistory,
)


@app.task
def update_dealer_showroom_relations():
    """
    This tasks update dealers for showrooms, so they buy cars
    for the best available price
    """

    showrooms = CarShowRoom.objects.all()
    for showroom in showrooms:
        update_cars_suppliers(showroom)


def update_cars_suppliers(showroom: CarShowRoom):
    """This function checks if there are better dealers for showroom's cars"""

    for showrooms_car in ShowroomCar.objects.filter(
        car_showroom=showroom
    ).select_related("car_showroom", "car", "dealer"):
        update_car_supplier(showrooms_car)


def update_car_supplier(showrooms_car: ShowroomCar):
    """This function checks if there are better dealers for showroom's car"""

    try:
        current_dealers_offer = DealerCar.objects.get(
            car=showrooms_car.car, dealer=showrooms_car.dealer
        )
    except ObjectDoesNotExist:
        current_dealers_offer = None
    available_offer = DealerCar.objects.filter(car=showrooms_car.car).select_related(
        "dealer"
    )
    if available_offer:
        min_price_offer = min(available_offer, key=lambda offer: offer.car_price)
    else:
        return  # process if there is no active dealers for this car
    if current_dealers_offer is not None:
        if min_price_offer.car_price < current_dealers_offer.car_price:
            showrooms_car.dealer = min_price_offer.dealer
    else:
        showrooms_car.dealer = min_price_offer.dealer
    showrooms_car.save()


@app.task
def supply_cars_from_dealers():
    """
    This task buys cars from dealers for showrooms
    """

    target_amount = 10
    showrooms = CarShowRoom.objects.all().select_related("balance")
    for showroom in showrooms:
        update_showrooms_car(showroom)
        for showrooms_car in (
            ShowroomCar.objects.filter(car_showroom=showroom)
            .select_related("car_showroom", "car", "dealer")
            .order_by("car_sold")
        ):
            if showrooms_car.dealer is None:
                continue  # process if showroom do not have dealer for this car
            discounts_on_this_car = showrooms_car.car.discountcar_set.filter(
                Q(discount__car_showroom=None)
                & Q(discount__end_date__gt=timezone.now())
                & ~Q(discount__dealer=None)
            ).select_related("discount", "discount__dealer")
            current_dealers_offer = DealerCar.objects.get(
                dealer=showrooms_car.dealer, car=showrooms_car.car
            )
            if discounts_on_this_car:
                minimal_offer_with_discount = min(
                    discounts_on_this_car, key=lambda discount: discount.new_car_price
                )
                if (
                    minimal_offer_with_discount.new_car_price
                    < current_dealers_offer.car_price
                ):
                    supply_cars_from_dealer(
                        showroom,
                        minimal_offer_with_discount.discount.dealer,
                        showrooms_car.car,
                        minimal_offer_with_discount.new_car_price,
                        target_amount,
                    )
                    continue
            supply_cars_from_dealer(
                showroom,
                showrooms_car.dealer,
                showrooms_car.car,
                current_dealers_offer.car_price,
                target_amount,
            )


def update_showrooms_car(showroom: CarShowRoom):
    """
    This checks if there are new cars that fit showroom's
    requirements and then adds them to showroom
    """

    cars_that_fit_showroom = Car.objects.filter(
        Q(car_brand__in=showroom.car_brands.all())
        & Q(price_category=showroom.price_category)
        & ~Q(pk__in=showroom.car_list.all())
    )
    created_showrooms_cars = ShowroomCar.objects.bulk_create(
        [ShowroomCar(car_showroom=showroom, car=car) for car in cars_that_fit_showroom]
    )
    for car in created_showrooms_cars:
        update_car_supplier(car)


def supply_cars_from_dealer(
    showroom: CarShowRoom,
    dealer: Dealer,
    car: Car,
    price_for_one_car: Decimal,
    car_amount: int,
):
    """This function makes a transaction between showroom and dealer"""

    with transaction.atomic():
        money_amount = price_for_one_car * car_amount
        if Balance.objects.get(pk=showroom.balance.pk).money_amount < money_amount:
            SupplyHistory.objects.create(
                car_showroom=showroom,
                dealer=dealer,
                car_price=price_for_one_car,
                car=car,
                cars_amount=car_amount,
                details="Impossible to supply cars, showroom doesn't have enough money"
            )
            return  # process if showroom does not have enough money
        Balance.objects.filter(pk=showroom.balance.pk).update(
            money_amount=F("money_amount") - money_amount, last_spent=timezone.now()
        )
        Balance.objects.filter(pk=dealer.balance.pk).update(
            money_amount=F("money_amount") + money_amount, last_deposit=timezone.now()
        )
        ShowroomCar.objects.filter(car_showroom=showroom, car=car).update(
            car_amount=F("car_amount") + car_amount
        )
        SupplyHistory.objects.create(
            car_showroom=showroom,
            dealer=dealer,
            car_price=price_for_one_car,
            car=car,
            cars_amount=car_amount,
            details="Successful supply"
        )
