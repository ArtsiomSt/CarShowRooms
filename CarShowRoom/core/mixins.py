from core.serializers import BalanceSerializer


class AddBalanceIfOwnerMixin:
    """Adds balance field in serializer for retrieving instances, if instance is logged as owner"""

    @property
    def data(self):
        res = super().data
        request = self.context["request"]
        if res.get("id", None) == request.user.id:
            instances_balance = self.instance.balance
            res["balance"] = BalanceSerializer(instances_balance).data
        return res


class DynamicSerializerMixin:
    serializer_mapping = {}

    def get_serializer_class(self):
        for action, serializer in self.serializer_mapping.items():
            if self.action == action or self.action in action:
                return serializer
        assert (
            self.serializer_class is not None
        ), "You should specify default serializer or provide mapping for all methods"
        return self.serializer_class
