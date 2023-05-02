from decimal import Decimal

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver

from sellers.models import DealerCar, DiscountCar, ShowroomCar


@receiver(post_save, sender=DiscountCar)
def get_new_car_price(sender, instance, **kwargs):
    """This signal is used to calculate new_cars_price with discount"""

    discount = instance.discount
    if kwargs.get("created", False):
        if discount.car_showroom_id is None and discount.dealer_id is not None:
            try:
                dealercar_object = DealerCar.objects.get(
                    dealer=discount.dealer_id, car=instance.car_id
                )
            except ObjectDoesNotExist:
                instance.delete()
                raise ValueError(
                    "You do not sell this car"
                )  # Soon will make it APIException(when there will be api to create discounts)
        if discount.car_showroom_id is not None and discount.dealer_id is None:
            try:
                showroom_car = ShowroomCar.objects.get(
                    Q(car_showroom=discount.car_showroom_id)
                    & Q(car=instance.car_id)
                    & ~Q(dealer=None)
                )
                dealercar_object = DealerCar.objects.get(
                    Q(car=instance.car_id) & Q(dealer=showroom_car.dealer_id)
                )
            except ObjectDoesNotExist:
                instance.delete()
                raise ValueError(
                    "You do not sell this car or there is no dealer for it"
                )  # Soon will make it APIException
        instance.new_car_price = dealercar_object.car_price * (
            1 - round(Decimal(instance.discount.discount_percent / 100), 2)
        )
        instance.save()


@receiver(post_save, sender=DealerCar)
def update_car_prices(sender, instance, **kwargs):
    """This signal is used to update field new_car_price in existing DiscountCar objects"""

    existing_discountcar_objects = instance.car.discountcar_set.all()
    for discountcar in existing_discountcar_objects:
        cars_discount = discountcar.discount
        sold_with_discount = discountcar.sold_with_discount
        discountcar.delete()
        DiscountCar.objects.create(
            car=instance.car,
            discount=cars_discount,
            sold_with_discount=sold_with_discount,
        )
