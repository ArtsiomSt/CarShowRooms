from django.core.exceptions import ObjectDoesNotExist

from cars.models import CarBrand
from sellers.models import ShowroomBrand


class ChangeShowRoomBrandsMixin:
    """
    Mixin that provides changing showrooms preferences in car brands by the list of slugs.
    """

    @staticmethod
    def update_car_brands_by_slugs(instance, car_brands_slugs):
        """
        This method implements changing ShowRoom's brands by adding new or removing odd ones,
        Basically this method changes ShowRoom's brands to brands with slugs from car_brands_slugs
        """
        chosen_car_brands = []
        for car_brand_slug in car_brands_slugs:
            try:
                chosen_car_brands.append(CarBrand.objects.get(slug=car_brand_slug))
            except ObjectDoesNotExist:
                raise ObjectDoesNotExist(
                    f"CarBrand with slug {car_brand_slug} does not exist"
                )
        ShowroomBrand.objects.filter(car_showroom=instance).exclude(
            car_brand__slug__in=car_brands_slugs
        ).delete()
        showrooms_brands = instance.car_brands.all()
        car_brands_to_create = []
        for car_brand in chosen_car_brands:
            if car_brand not in showrooms_brands:
                car_brands_to_create.append(
                    ShowroomBrand(car_showroom=instance, car_brand=car_brand)
                )
        if car_brands_to_create:
            ShowroomBrand.objects.bulk_create(car_brands_to_create)
