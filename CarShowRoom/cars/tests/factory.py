import factory

from cars.models import Car


class CarFactory(factory.django.DjangoModelFactory):
    title = "string"
    car_brand = "car_brand"
    doors_amount = 3
    engine_power = 100
    engine_type = "FUEL"
    year_produced = 2010
    price_category = "CHEAP"
    length = 2
    width = 2
    height = 2
    max_speed = 300

    class Meta:
        model = Car
