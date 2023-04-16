from rest_framework import serializers

from ..models import Car, CarBrand


class CarBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarBrand
        fields = ("title", "country", "slug")


class CarSerializer(serializers.ModelSerializer):
    car_brand = CarBrandSerializer(read_only=True)
    car_brand_slug = serializers.SlugField(max_length=30, write_only=True)

    def create(self, validated_data):
        validated_data = self.validated_data
        chosen_brand = validated_data.pop("car_brand_slug", "default_brand")
        brand_instance = CarBrand.objects.get(slug=chosen_brand)
        created_car = Car.objects.create(**validated_data, car_brand=brand_instance)
        return created_car

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
