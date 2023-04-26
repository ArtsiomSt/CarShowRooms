from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from CarShowRoom.celery import app
from cars.models import Car
from sellers.models import CarShowRoom, DealerCar, ShowroomCar


@app.task  # I need this one to test different options in celery
def print_something():
    print("something from celery")
    print(CarShowRoom.objects.all())


@app.task
def update_dealer_showroom_relations():
    """
    This tasks update dealers for showrooms, so they buy cars
    for the best available price. Also, this tasks updated showroom's
    car list using it preferences.
    """

    showrooms = CarShowRoom.objects.all()
    print('update_dealer_showroom_relations task')
    for showroom in showrooms:
        cars_that_fit_showroom = Car.objects.filter(
            Q(car_brand__in=showroom.car_brands.all())
            & Q(price_category=showroom.price_category)
            & ~Q(pk__in=showroom.car_list.all())
        )
        ShowroomCar.objects.bulk_create(
            [
                ShowroomCar(car_showroom=showroom, car=car)
                for car in cars_that_fit_showroom
            ]
        )
        for showrooms_car in ShowroomCar.objects.filter(
            car_showroom=showroom
        ).select_related("car_showroom", "car", "dealer"):
            try:
                current_dealers_offer = DealerCar.objects.get(
                    car=showrooms_car.car, dealer=showrooms_car.dealer
                )
            except ObjectDoesNotExist:
                current_dealers_offer = None
            available_offer = DealerCar.objects.filter(
                car=showrooms_car.car
            ).select_related("dealer")
            if available_offer:
                min_price_offer = min(
                    available_offer, key=lambda offer: offer.car_price
                )
            else:
                continue
            if current_dealers_offer is not None:
                if min_price_offer.car_price < current_dealers_offer.car_price:
                    showrooms_car.dealer = min_price_offer.dealer
                    showrooms_car.save()
            else:
                showrooms_car.dealer = min_price_offer.dealer
                showrooms_car.save()
