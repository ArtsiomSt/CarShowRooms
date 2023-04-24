from inspect import stack

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
    serializer_mapping = None

    def get_serializer_class(self):
        assert self.serializer_mapping is not None
        for methods, serializer_class in self.serializer_mapping.items():
            called_from = stack()[1].function
            if called_from != "get_serializer":
                raise ValueError("get_serializer_class should be called from get_serializer")
            for depth in range(len(stack())):
                function_of_that_level = stack()[depth].function
                if function_of_that_level in methods:
                    return serializer_class
        raise ValueError("Bad serializer mapping")
