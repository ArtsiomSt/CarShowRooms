import factory

from customers.models import Customer


class CustomerFactory(factory.django.DjangoModelFactory):
    first_name = "customer_test"
    last_name = "customer_test"
    email = "customer_without_email@testpytest.com"
    username = "customer_without_email"
    password = "zxcvbnm1234567890"
    is_email_verified = False

    class Meta:
        model = Customer
