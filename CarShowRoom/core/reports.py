from django.db.models import Sum, F, Count

from sellers.models import SupplyHistory, CarShowRoom
from customers.models import TransactionHistory
from pprint import pprint


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
    sold_cars_by_showrooms = TransactionHistory.objects.values("sold_by_showroom_id", "sold_by_showroom__name", "car_id", "car__title").annotate(cars_sold=Count("car_id"))
    showroom_objects = CarShowRoom.objects.filter(is_active=True)
    for showroom in showroom_objects:
        car_by_showroom = {'car_showroom_id': showroom.pk, 'cars': []}
        for car in sold_cars_by_showrooms:
            if car['sold_by_showroom_id'] == showroom.pk:
                car_by_showroom['cars'].append({"car_id": car['car_id'], "car_title": car['car__title'], "cars_sold": car['cars_sold']})
        showrooms.append(car_by_showroom)
    return report


