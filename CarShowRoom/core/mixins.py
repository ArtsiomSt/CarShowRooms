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
