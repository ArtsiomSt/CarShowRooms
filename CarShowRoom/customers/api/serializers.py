from core.serializers import RegisterSerializer
from customers.models import Customer


class CustomerSerializer(RegisterSerializer):
    class Meta:
        model = Customer
        fields = (
            "phone_number",
            "balance",
            "showrooms",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
        )
