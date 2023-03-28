from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from celery.schedules import crontab

from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celerypro.settings')

app = Celery('celerypro')
app.conf.enable_utc = False

app.conf.update(timezone = 'Asia/Kolkata')

app.config_from_object(settings, namespace='CELERY')

# CELERY BEAT SETTINGS
app.conf.beat_schedule = {
    'send_mail_everyday': {
    'task': 'send_mail_app.tasks.send_mail_func',
    'schedule': crontab(hour=20, minute=00, day_of_month=25, month_of_year=3),
    # 'args': (2,)
    }
}

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')