import os
from datetime import timedelta

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CarShowRoom.settings")

app = Celery("CarShowRoom")
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'spam-every-10-sec': {
        'task': 'sellers.tasks.print_something',
        'schedule': timedelta(seconds=6)
    }
}