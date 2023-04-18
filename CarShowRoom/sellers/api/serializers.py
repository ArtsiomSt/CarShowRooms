from core.serializers import RegisterSerializer
from sellers.models import CarShowRoom, Dealer


class CarShowRoomSerializer(RegisterSerializer):
    class Meta:
        model = CarShowRoom
        fields = (
            "username",
            "email",
            "password",
            "name",
            "country",
            "address",
            "margin",
            "balance",
            "phone_number",
            "car_brands",
            "price_category",
        )


class DealerSerializer(RegisterSerializer):
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
