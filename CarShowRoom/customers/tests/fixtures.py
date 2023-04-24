from pytest_factoryboy import register

from .factory import CustomerFactory

register(CustomerFactory, "customer_without_email")
register(
    CustomerFactory,
    "customer_with_email",
    username='customer_with_email',
    email="customer_test_email@testpytest.com",
    is_email_verified=True
)
