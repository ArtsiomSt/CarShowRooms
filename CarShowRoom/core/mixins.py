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
    """
    This mixin is used to implement different serializers for different
    methods in ViewSets, it uses mapping where the key is list of methods
    and the value is a class of serializer for this group of methods
    """

    serializer_mapping = {}

    def get_serializer_class(self):
        for action, serializer in self.serializer_mapping.items():
            if self.action == action or self.action in action:
                return serializer
        assert (
            self.serializer_class is not None
        ), "You should specify default serializer or provide mapping for all methods"
        return self.serializer_class


class DynamicPermissionMixin:
    """
    This mixin is used to implement different permissions for different
    methods in ViewSets, it uses mapping where the key is list of methods
    and the value is list of permissions for this group of methods
    """

    permission_mapping = {}

    def get_permissions(self):
        for action, permissions in self.permission_mapping.items():
            if self.action in action:
                return [permission() for permission in permissions]
        return [permission() for permission in self.permission_classes]
