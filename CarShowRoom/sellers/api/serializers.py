from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.db import transaction
from rest_framework import serializers

from cars.api.serializers import CarBrandSerializer, CarSerializer
from cars.models import Car
from core.exceptions import CreationException
from core.mixins import AddBalanceIfOwnerMixin
from core.enums.userenums import UserType
from core.serializers import RegisterSerializer
from sellers.mixins import ChangeShowRoomBrandsMixin
from sellers.models import (
    CarShowRoom,
    Dealer,
    DealerCar,
    ShowroomCar,
    Discount,
    DiscountCar,
)
from sellers.tasks import update_cars_suppliers


class CarShowRoomRegisterSerializer(ChangeShowRoomBrandsMixin, RegisterSerializer):
    """
    This serializer is used in registration process for showrooms.
    It also provides adding CarBrand preferences while creating instance
    and finds cars that fit showroom's preferences.
    """

    car_brands = CarBrandSerializer(many=True, read_only=True)
    car_brands_slugs = serializers.ListSerializer(
        write_only=True, child=serializers.SlugField(max_length=30)
    )

    def create(self, validated_data):
        car_brands_slugs = validated_data.pop("car_brands_slugs")
        instance = super().create(validated_data)
        self.update_car_brands_by_slugs(instance, car_brands_slugs)
        cars_that_fit_showroom = Car.objects.filter(
            car_brand__slug__in=car_brands_slugs, price_category=instance.price_category
        )
        showroomcar_to_create = []
        for car in cars_that_fit_showroom:
            showroomcar_to_create.append(ShowroomCar(car_showroom=instance, car=car))
        ShowroomCar.objects.bulk_create(showroomcar_to_create)
        update_cars_suppliers(instance)
        return instance

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
            "car_brands_slugs",
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


class CarShowRoomSerializer(
    AddBalanceIfOwnerMixin, ChangeShowRoomBrandsMixin, serializers.ModelSerializer
):
    """
    This serializer is used to provide different actions
    with showroom instances after registration
    """

    car_brands = CarBrandSerializer(many=True, read_only=True)
    car_brands_slugs = serializers.ListSerializer(
        write_only=True, child=serializers.SlugField(max_length=30)
    )

    def update(self, instance, validated_data):
        if "car_brands_slugs" in validated_data.keys():
            car_brands_slugs = validated_data.pop("car_brands_slugs")
            self.update_car_brands_by_slugs(instance, car_brands_slugs)
        return super().update(instance, validated_data)

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
    """
    This serializer is used to provide different actions
    with dealer instances after registration
    """

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
        car_id = request_kwargs["pk"]
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


class DiscountSerializer(serializers.ModelSerializer):
    dealer = DealerSerializer(read_only=True)
    car_showroom = CarShowRoomSerializer(read_only=True)
    car_ids = serializers.ListSerializer(
        child=serializers.IntegerField(), write_only=True
    )

    @property
    def data(self):
        res = super().data
        if res["dealer"] is None:
            res.pop("dealer")
        elif res["car_showroom"] is None:
            res.pop("car_showroom")
            res["dealer"].pop("car_list")
        else:
            res["details"] = "This discount seems to have no owner"
        return res

    def create(self, validated_data):
        request = self.context["request"]
        user_id = request.user.pk
        with transaction.atomic():
            car_ids = validated_data.pop("car_ids")
            if request.user.user_type == UserType.CARSHOWROOM.name:
                validated_data["car_showroom"] = CarShowRoom.objects.get(pk=user_id)
                owners_cars = validated_data["car_showroom"].car_list.filter(
                    is_active=True
                )
            elif request.user.user_type == UserType.DEALER.name:
                validated_data["dealer"] = Dealer.objects.get(pk=user_id)
                owners_cars = validated_data["dealer"].car_list.filter(is_active=True)
            else:
                raise CreationException(
                    {"message": "impossible to create discount from this account"}
                )
            instance = super().create(validated_data)
            discount_car_objects = []
            for car_id in car_ids:
                try:
                    car = Car.objects.get(pk=car_id)
                except ObjectDoesNotExist:
                    raise CreationException(
                        {"message": f"there is no such car with id {car_id}"}
                    )
                if car in owners_cars:
                    discount_car_objects.append(DiscountCar(car=car, discount=instance))
                else:
                    raise CreationException(
                        {"message": f"you dont sell car with id {car_id}"}
                    )
            if discount_car_objects:
                DiscountCar.objects.bulk_create(discount_car_objects)
            return instance

    class Meta:
        model = Discount
        fields = (
            "id",
            "start_date",
            "end_date",
            "discount_percent",
            "dealer",
            "car_showroom",
            "car_ids",
        )
        read_only_fields = ("id",)
