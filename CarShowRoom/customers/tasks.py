from decimal import Decimal

from django.db import transaction
from django.db.models import F, Q
from django.utils import timezone

from CarShowRoom.celery import app
from customers.models import Offer, TransactionHistory
from sellers.models import Balance, CarShowRoom, DealerCar, DiscountCar, ShowroomCar


@app.task
def process_offers():
    """This function processes all unprocessed offers"""

    offers = Offer.objects.filter(is_processed=False).select_related(
        "made_by_customer", "car", "made_by_customer__balance"
    )
    for offer in offers:
        available_offers_from_showrooms = ShowroomCar.objects.filter(
            Q(car=offer.car) & Q(car_amount__gt=0) & ~Q(dealer=None)
        ).select_related("car_showroom", "dealer", "car_showroom__balance", "car")
        if available_offers_from_showrooms:
            minimal_price_offer = min(
                available_offers_from_showrooms, key=get_car_price_from_showroomcar
            )
            best_price_offer = get_car_price_from_showroomcar(minimal_price_offer)
            if offer.max_price >= best_price_offer:
                commit_offer(offer, minimal_price_offer.car_showroom, best_price_offer)
            else:
                continue  # process if there is no offer for such requirements
        else:
            continue  # process if there is no such currently available


def get_car_price_from_showroomcar(showroom_car: ShowroomCar):
    """This function finds the best offer from showroom about this car"""

    dealers_offer = DealerCar.objects.get(
        Q(dealer=showroom_car.dealer) & Q(car=showroom_car.car)
    )
    discounts_from_showroom = DiscountCar.objects.filter(
        car=showroom_car.car,
        discount__dealer=None,
        discount__car_showroom=showroom_car.car_showroom,
        discount__end_date__gt=timezone.now(),
    ).select_related("discount")
    if discounts_from_showroom:
        best_discount = max(
            discounts_from_showroom,
            key=lambda discount_car: discount_car.discount.discount_percent,
        )
        return round(
            best_discount.new_car_price
            * (1 + round(Decimal(showroom_car.car_showroom.margin / 100), 2)),
            2,
        )
    return round(
        dealers_offer.car_price
        * (1 + round(Decimal(showroom_car.car_showroom.margin / 100), 2)),
        2,
    )


def commit_offer(offer: Offer, showroom: CarShowRoom, price: Decimal):
    with transaction.atomic():
        if offer.made_by_customer.balance.money_amount < price:
            return  # Process if customer does not have enough money
        Balance.objects.filter(pk=offer.made_by_customer.balance.pk).update(
            money_amount=F("money_amount") - price, last_spent=timezone.now()
        )
        Balance.objects.filter(pk=showroom.balance.pk).update(
            money_amount=F("money_amount") + price, last_deposit=timezone.now()
        )
        ShowroomCar.objects.filter(car_showroom=showroom, car=offer.car).update(
            car_amount=F("car_amount") - 1, car_sold=F("car_sold") + 1
        )
        offer.is_processed = True
        offer.save()
        TransactionHistory.objects.create(
            made_by_customer=offer.made_by_customer,
            car=offer.car,
            deal_price=price,
            sold_by_showroom=showroom,
        )
