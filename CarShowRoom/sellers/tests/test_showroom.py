import random

import pytest

from cars.api.serializers import CarBrandSerializer

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
        ("showroom_without_email", 403),
        ("dealer_with_email", 403),
        ("dealer_without_email", 403),
        ("customer_with_email", 403),
        ("customer_without_email", 403),
    ],
)
def test_showroom_update(
    user_instance,
    status_code,
    get_token,
    showroom_with_email,
    get_two_car_brands,
    client,
    request,
):
    """
    This tests checks that only showroom owner can change information about itself
    Also it checks the correct work of changing showroom's preferences in CarBrands
    """
    user_instance = request.getfixturevalue(user_instance)
    car_brand_one, car_brand_two = get_two_car_brands()
    endpoint = f"/api/v1/sellers/showroom/{showroom_with_email.id}/"
    auth_token = get_token(user_instance)
    payload = {
        "name": "string",
        "country": "AF",
        "city": "string",
        "address": "string",
        "margin": 4,
        "phone_number": "+4873874",
        "price_category": "CHEAP",
        "car_brands_slugs": [car_brand_one.slug, car_brand_two.slug],
    }
    response = client.put(
        endpoint, payload, headers={"Authorization": "JWT " + auth_token}, format="json"
    )
    assert response.status_code == status_code
    if status_code == 200:
        assert user_instance.id == showroom_with_email.id
        payload["car_brands"] = [
            CarBrandSerializer(car_brand_one).data,
            CarBrandSerializer(car_brand_two).data,
        ]
        assert payload["car_brands"] == response.data["car_brands"]


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
def test_show_showrooms_balance(
    user_instance,
    status_code,
    get_token,
    showroom_with_email,
    showroom_without_email,
    client,
    request,
):
    """
    This tests checks if only showroom owner can see its balance
    """
    if "showroom" in user_instance:
        user_instance = request.getfixturevalue(user_instance)
        endpoint = f"/api/v1/sellers/showroom/{user_instance.id}/"
        target_id = user_instance.id
    else:
        showroom_choice = random.choice([showroom_without_email, showroom_with_email])
        user_instance = request.getfixturevalue(user_instance)
        endpoint = f"/api/v1/sellers/showroom/{showroom_choice.id}/"
        target_id = showroom_choice.id
    auth_token = get_token(user_instance)
    response = client.get(endpoint, headers={"Authorization": "JWT " + auth_token})
    assert response.status_code == 200
    if user_instance.id == target_id:
        assert "balance" in response.data.keys()
    else:
        assert "balance" not in response.data.keys()
