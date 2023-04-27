from decimal import Decimal

from django.db.models.signals import post_save
from django.dispatch import receiver

from sellers.models import DealerCar, DiscountCar


@receiver(post_save, sender=DiscountCar)
def link_balance(sender, instance, **kwargs):
    """This signal is used to calculate new_cars_price with discount"""

    discount = instance.discount
    if (
        discount.car_showroom_id is None
        and discount.dealer_id is not None
        and instance.new_car_price is None
    ):
        dealercar_object = DealerCar.objects.get(
            dealer=discount.dealer_id, car=instance.car_id
        )
        instance.new_car_price = dealercar_object.car_price * (
            1 - round(Decimal(instance.discount.discount_percent / 100), 2)
        )
        instance.save()
