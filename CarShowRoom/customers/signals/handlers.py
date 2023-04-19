from django.db.models.signals import post_save
from django.dispatch import receiver
from customers.models import Balance, Customer


@receiver(post_save, sender=Customer)
def link_balance(sender, instance, **kwargs):
    if kwargs.get('created', False):
        new_balance = Balance.objects.create(money_amount=0)
        setattr(instance, "balance", new_balance)
        instance.save()
