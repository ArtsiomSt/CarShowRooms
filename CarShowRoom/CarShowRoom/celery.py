import os
from datetime import timedelta

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CarShowRoom.settings")

app = Celery("CarShowRoom")
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'update-showrooms-car-dealers': {
        'task': 'sellers.tasks.update_dealer_showroom_relations',
        'schedule': timedelta(minutes=60)
    },
    'supply-cars-from-dealers': {
        'task': 'sellers.tasks.supply_cars_from_dealers',
        'schedule': timedelta(minutes=10)
    }
}
