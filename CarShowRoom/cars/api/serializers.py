from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from cars.models import Car, CarBrand


class CarBrandSerializer(serializers.ModelSerializer):
    """Serializer for CarBrand model"""

    class Meta:
        model = CarBrand
        fields = ("title", "country", "slug")


class CarSerializer(serializers.ModelSerializer):
    """Serializer for CarModel with custom creation and updating methods"""

    car_brand = CarBrandSerializer(read_only=True)
    car_brand_slug = serializers.SlugField(max_length=30, write_only=True)

    def create(self, validated_data):
        chosen_brand = validated_data.pop("car_brand_slug")
        brand_instance = CarBrand.objects.get(slug=chosen_brand)
        if not brand_instance.is_active:
            raise ObjectDoesNotExist("There is no such CarBrand instance")
        validated_data["car_brand"] = brand_instance
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if "car_brand_slug" in validated_data.keys():
            chosen_brand = validated_data.pop("car_brand_slug")
            brand_instance = CarBrand.objects.get(slug=chosen_brand)
            if not brand_instance.is_active:
                raise ObjectDoesNotExist("There is no such CarBrand instance")
            setattr(instance, "car_brand", brand_instance)
        return super().update(instance, validated_data)

    class Meta:
        model = Car
        fields = (
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
        )
