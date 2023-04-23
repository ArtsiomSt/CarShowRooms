from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from cars.api.serializers import CarBrandSerializer, CarSerializer
from cars.models import Car, CarBrand
from core.mixins import AddBalanceIfOwnerMixin
from core.serializers import CarPriceCurrencySerializer, RegisterSerializer
from sellers.models import CarShowRoom, Dealer, DealerCar, ShowroomBrand
from django.db.utils import IntegrityError



class CarShowRoomRegisterSerializer(RegisterSerializer):
    class Meta:
        model = CarShowRoom
        fields = (
            "id",
            "username",
            "email",
            "password",
            "name",
            "country",
            "city",
            "address",
            "margin",
            "balance",
            "phone_number",
            "car_brands",
            "price_category",
        )
        read_only_fields = ("id",)


class DealerRegisterSerializer(RegisterSerializer):
    class Meta:
        model = Dealer
        fields = (
            "username",
            "email",
            "password",
            "name",
            "phone_number",
            "year_founded",
            "balance",
            "car_list",
        )


class CarShowRoomSerializer(AddBalanceIfOwnerMixin, serializers.ModelSerializer):
    car_brands = CarBrandSerializer(many=True, read_only=True)
    car_brands_slugs = serializers.ListSerializer(
        write_only=True, child=serializers.SlugField(max_length=30)
    )

    def update(self, instance, validated_data):
        if "car_brands_slugs" in validated_data.keys():
            car_brands_slugs = validated_data.pop("car_brands_slugs")
            self.update_car_brands_by_slugs(instance, car_brands_slugs)
        return super().update(instance, validated_data)

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

    class Meta:
        model = CarShowRoom
        fields = (
            "id",
            "name",
            "city",
            "country",
            "address",
            "margin",
            "car_brands",
            "phone_number",
            "price_category",
            "car_brands_slugs",
        )
        read_only_fields = ("id",)


class DealerSerializer(AddBalanceIfOwnerMixin, serializers.ModelSerializer):
    car_list = CarSerializer(many=True, read_only=True)

    class Meta:
        model = Dealer
        fields = (
            "id",
            "email",
            "name",
            "phone_number",
            "year_founded",
            "car_list",
        )


class DealerCarSerializer(serializers.ModelSerializer):
    """This serializer provides adding car to dealers, where dealer is taken from request"""

    def create(self, validated_data):
        request = self.context["request"]
        request_kwargs = request.parser_context["kwargs"]
        car_id = request_kwargs["car_id"]
        if not DealerCar.objects.filter(car=car_id, dealer=request.user.id):
            try:
                validated_data["car"] = Car.objects.get(pk=car_id)
            except ObjectDoesNotExist:
                raise ObjectDoesNotExist("there is no such car")
            validated_data["dealer"] = Dealer.objects.get(pk=request.user.id)
            return super().create(validated_data)
        else:
            raise IntegrityError("This dealer has already added this car to his list")

    class Meta:
        model = DealerCar
        fields = ("car_price", "currency")
