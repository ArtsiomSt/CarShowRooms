from copy import deepcopy

import pytest

from cars.models import Car
from sellers.models import DealerCar

pytest_plugins = [
    "cars.tests.fixtures",
    "sellers.tests.fixtures",
    "customers.tests.fixtures",
]


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_instance,status_code",
    [
        ("dealer_with_email", 201),
        ("dealer_without_email", 403),
        ("showroom_with_email", 403),
        ("showroom_without_email", 403),
        ("customer_with_email", 403),
        ("customer_without_email", 403),
    ],
)
def test_create_car(user_instance, status_code, get_token, car_brand, client, request):
    """
    This test check the process of creating car instance
     with adding this car to dealer's list
    """

    user_instance = request.getfixturevalue(user_instance)
    endpoint = "/api/v1/cars/car/"
    auth_token = get_token(user_instance)
    payload = {
        "title": "string",
        "car_brand_slug": car_brand.slug,
        "doors_amount": 3,
        "engine_power": 100,
        "engine_type": "FUEL",
        "year_produced": 2010,
        "price_category": "CHEAP",
        "length": 2,
        "width": 2,
        "height": 2,
        "max_speed": 300,
        "car_price": {"car_price": 100.55, "currency": "USD"},
    }
    response = client.post(
        endpoint, payload, format="json", headers={"Authorization": "JWT " + auth_token}
    )
    assert response.status_code == status_code
    if status_code == 201:
        payload["car_brand"] = {
            "title": car_brand.title,
            "slug": car_brand.slug,
            "country": car_brand.country,
        }
        payload.pop("car_brand_slug")
        payload.pop("car_price")
        payload["id"] = 1
        assert response.data == payload
        assert Car.objects.count() == 1
        assert DealerCar.objects.count() == 1


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_instance,status_code",
    [
        ("dealer_with_email", 200),
        ("dealer_without_email", 403),
        ("showroom_with_email", 403),
        ("showroom_without_email", 403),
        ("customer_with_email", 403),
        ("customer_without_email", 403),
    ],
)
def test_update_car(
    user_instance, status_code, get_token, car_brand, car, client, request
):
    """
    This test checks the process of updating car by dealer.
    Also it controls that script changes information about
    car price in DealerCar model. Also it checks exception
    when we are trying to change cars brand to brand that not exists.
    """
    user_instance = request.getfixturevalue(user_instance)
    endpoint = f"/api/v1/cars/car/{car.id}/"
    auth_token = get_token(user_instance)
    payload = {
        "title": "put",
        "car_brand_slug": car_brand.slug,
        "doors_amount": 4,
        "engine_power": 500,
        "engine_type": "DIESEL",
        "year_produced": 2010,
        "price_category": "CHEAP",
        "length": 2,
        "width": 2,
        "height": 2,
        "max_speed": 300,
        "car_price": {"car_price": 100.55, "currency": "USD"},
    }
    response = client.put(
        endpoint, payload, format="json", headers={"Authorization": "JWT " + auth_token}
    )
    assert response.status_code == status_code
    if status_code == 200:
        payload_copy = deepcopy(payload)
        payload["car_brand"] = {
            "title": car_brand.title,
            "slug": car_brand.slug,
            "country": car_brand.country,
        }
        payload.pop("car_brand_slug")
        car_price_dict = payload.pop("car_price")
        payload["id"] = car.id
        dealercar_instance = DealerCar.objects.get(dealer=user_instance, car=car)
        assert response.data == payload
        assert float(dealercar_instance.car_price) == round(
            car_price_dict["car_price"], 2
        )
        assert dealercar_instance.currency == car_price_dict["currency"]
        payload_copy["car_brand_slug"] += "brand_that_not_exists"
        response = client.put(
            endpoint,
            payload_copy,
            format="json",
            headers={"Authorization": "JWT " + auth_token},
        )
        assert response.status_code == 400
