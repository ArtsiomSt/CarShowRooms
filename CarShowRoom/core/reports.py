from django.db.models import Sum, F, Count

from sellers.models import SupplyHistory, CarShowRoom, Dealer
from customers.models import TransactionHistory, Customer


def get_supply_history_reports():
    report = {}
    return report


def get_incomes_expenses():
    report = {"showrooms": {}, "dealers": {}, "customers": {}}
    showrooms = report['showrooms']
    dealers = report['dealers']
    customers = report['customers']
    showrooms['turnover'] = SupplyHistory.objects.values("car_showroom_id", "car_showroom__name").annotate(expense=Sum(F("car_price")*F("cars_amount")))
    dealers['incomes'] = SupplyHistory.objects.values("dealer").annotate(income=Sum(F("car_price")*F("cars_amount")))
    customers['expenses'] = TransactionHistory.objects.values("made_by_customer").annotate(expense=Sum(F("deal_price")))
    showrooms_incomes = TransactionHistory.objects.values("sold_by_showroom_id", "sold_by_showroom__name").annotate(income=Sum(F("deal_price")))
    for showrooms_income in showrooms_incomes:
        for showroom in showrooms['turnover']:
            if showrooms_income['sold_by_showroom_id'] == showroom['car_showroom_id']:
                showroom['income'] = showrooms_income['income']
        else:
            stats_to_add = {"car_showroom_id": showrooms_income['sold_by_showroom_id'], "car_showroom__name": showrooms_income['sold_by_showroom__name']}
    return report


def get_cars_stats():
    report = {"showrooms": [], "dealers": [], "customers": []}
    showrooms = report['showrooms']
    dealers = report['dealers']
    customers = report['customers']
    sold_cars_by_showrooms = TransactionHistory.objects.values(
        "sold_by_showroom_id",
        "sold_by_showroom__name",
        "car_id",
        "car__title"
    ).annotate(cars_sold=Count("car_id"))
    sold_cars_by_dealers = SupplyHistory.objects.values("dealer_id", "dealer__name", "car_id", "car__title").annotate(cars_sold=Count("car_id"))
    purchased_cars_by_customers = TransactionHistory.objects.values("made_by_customer_id", "made_by_customer__username", "car_id", "car__title").annotate(cars_bought=Count("car_id"))
    showroom_objects = CarShowRoom.objects.filter(is_active=True)
    dealer_objects = Dealer.objects.filter(is_active=True)
    customer_objects = Customer.objects.filter(is_active=True)
    for showroom in showroom_objects:
        cars_by_showroom = {'car_showroom_id': showroom.pk, "car_showroom_name": showroom.name, 'cars': []}
        best_sold_car = {}
        for car in sold_cars_by_showrooms:
            if car['sold_by_showroom_id'] == showroom.pk:
                cars_by_showroom['cars'].append({"car_id": car['car_id'], "car_title": car['car__title'], "cars_sold": car['cars_sold']})
                if not best_sold_car or best_sold_car.get("cars_sold", 0) < car['cars_sold']:
                    best_sold_car = {"car_id": car["car_id"], "car_title": car["car__title"]}
                    cars_by_showroom['best_sold_car'] = best_sold_car
        showrooms.append(cars_by_showroom)
    for dealer in dealer_objects:
        cars_by_dealer = {"dealer_id": dealer.pk, "dealer_name": dealer.name, "cars": []}
        for car in sold_cars_by_dealers:
            best_sold_car = {}
            if car['dealer_id'] == dealer.pk:
                cars_by_dealer['cars'].append({"car_id": car['car_id'], "car_title": car['car__title'], "cars_sold": car['cars_sold']})
                if not best_sold_car or best_sold_car.get("cars_sold", 0) < car['cars_sold']:
                    best_sold_car = {"car_id": car['car_id'], "car_title": car["car__title"]}
                    cars_by_dealer['best_sold_car'] = best_sold_car
        dealers.append(cars_by_dealer)
    for customer in customer_objects:
        cars_by_customer = {"customer_id": customer.pk, "customer_username": customer.username, 'cars': []}
        for car in purchased_cars_by_customers:
            if car["made_by_customer_id"] == customer.pk:
                cars_by_customer['cars'].append({"car_id": car['car_id'], "car_title": car['car__title'], "cars_bought": car['cars_bought']})
        customers.append(cars_by_customer)
    return report


