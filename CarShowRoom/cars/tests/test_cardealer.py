import pytest

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
        ("dealer_with_email", 200),
        ("dealer_without_email", 403),
        ("showroom_with_email", 403),
        ("showroom_without_email", 403),
        ("customer_with_email", 403),
        ("customer_without_email", 403),
    ],
)
def test_cardealer_add_remove(
    user_instance, status_code, get_token, car, client, request
):
    endpoint = f"/api/v1/cars/car/{car.id}/add/"
    payload = {"car_price": 1000, "currency": "RUB"}
    user_instance = request.getfixturevalue(user_instance)
    auth_token = get_token(user_instance)
    auth_headers = {"Authorization": "JWT " + auth_token}
    response = client.delete(endpoint, headers=auth_headers)
    assert response.status_code == status_code
    if status_code == 200:
        assert DealerCar.objects.count() == 0
        response = client.post(endpoint, payload, format="json", headers=auth_headers)
        assert response.status_code == 201
        assert DealerCar.objects.count() == 1
