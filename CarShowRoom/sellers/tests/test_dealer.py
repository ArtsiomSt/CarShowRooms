import random

import pytest

pytest_plugins = [
    "cars.tests.fixtures",
    "sellers.tests.fixtures",
    "customers.tests.fixtures",
]


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_instance,status_code",
    [
        ("showroom_with_email", 200),
        ("showroom_without_email", 200),
        ("dealer_with_email", 200),
        ("dealer_without_email", 200),
        ("customer_with_email", 200),
        ("customer_without_email", 200),
    ],
)
def test_show_dealers_balance(
    user_instance,
    status_code,
    get_token,
    dealer_with_email,
    dealer_without_email,
    client,
    request,
):
    """
    This tests checks if only dealer owner can see its balance
    """

    if "dealer" in user_instance:
        user_instance = request.getfixturevalue(user_instance)
        endpoint = f"/api/v1/sellers/dealer/{user_instance.id}/"
        target_id = user_instance.id
    else:
        dealer_choice = random.choice([dealer_without_email, dealer_with_email])
        user_instance = request.getfixturevalue(user_instance)
        endpoint = f"/api/v1/sellers/dealer/{dealer_choice.id}/"
        target_id = dealer_choice.id
    auth_token = get_token(user_instance)
    response = client.get(endpoint, headers={"Authorization": "JWT " + auth_token})
    assert response.status_code == 200
    if user_instance.id == target_id:
        assert "balance" in response.data.keys()
    else:
        assert "balance" not in response.data.keys()
