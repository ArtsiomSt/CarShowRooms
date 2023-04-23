import pytest
from customers.models import Customer


@pytest.fixture
def password():
    return "zxcvbnm1234567890"


@pytest.fixture
def customer_with_email(password):
    return Customer.objects.create(
        first_name="customer_test",
        last_name="customer_test",
        email="customer_test_email@testpytest.com",
        username="customer_email",
        password=password,
        is_email_verified=True,
    )


@pytest.fixture()
def customer_without_email(password):
    return Customer.objects.create(
        first_name="customer_test",
        last_name="customer_test",
        username="customer_no_email",
        email="customer_test_no_email@testpytest.com",
        password=password,
        is_email_verified=False,
    )
