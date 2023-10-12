from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from rest_framework import serializers

from cars.models import Car, CarBrand
from core.serializers import CarPriceCurrencySerializer
from sellers.models import Dealer, DealerCar


class CarBrandSerializer(serializers.ModelSerializer):
    """Serializer for CarBrand model"""

    class Meta:
        model = CarBrand
        fields = ("title", "country", "slug")


class CarSerializer(serializers.ModelSerializer):
    """Serializer for CarModel with custom creation and updating methods"""

    car_brand = CarBrandSerializer(read_only=True)
    car_brand_slug = serializers.SlugField(max_length=30, write_only=True)
    car_price = CarPriceCurrencySerializer(write_only=True)

    def create(self, validated_data):
        chosen_brand = validated_data.pop("car_brand_slug")
        brand_instance = CarBrand.objects.get(slug=chosen_brand)
        if not brand_instance.is_active:
            raise ObjectDoesNotExist("There is no such CarBrand instance")
        serialized_car_price = validated_data.pop("car_price")
        validated_data["car_brand"] = brand_instance
        instance = super().create(validated_data)
        request = self.context["request"]
        dealer = Dealer.objects.get(pk=request.user.pk)
        DealerCar.objects.create(
            dealer=dealer,
            car=instance,
            car_price=serialized_car_price["car_price"],
            currency=serialized_car_price["currency"],
        )
        return instance

    def update(self, instance, validated_data):
        request = self.context["request"]
        if "car_brand_slug" in validated_data.keys():
            chosen_brand = validated_data.pop("car_brand_slug")
            brand_instance = CarBrand.objects.get(slug=chosen_brand)
            if not brand_instance.is_active:
                raise ObjectDoesNotExist("There is no such CarBrand instance")
            setattr(instance, "car_brand", brand_instance)
        if "car_price" in validated_data.keys():
            serialized_car_price = validated_data.pop("car_price")
            dealer = Dealer.objects.get(pk=request.user.pk)
            DealerCar.objects.filter(Q(dealer=dealer) & Q(car=instance)).update(
                car_price=serialized_car_price["car_price"],
                currency=serialized_car_price["currency"],
            )
        return super().update(instance, validated_data)

    class Meta:
        model = Car
        fields = (
            "id",
            "title",
            "car_brand",
            "doors_amount",
            "engine_power",
            "engine_type",
            "year_produced",
            "price_category",
            "length",
            "width",
            "height",
            "max_speed",
            "car_brand_slug",
            "car_price",
        )
        read_only_fields = ("id",)
