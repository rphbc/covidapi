from __future__ import absolute_import

import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'covidapi.settings')

app = Celery('covidapi', broker=settings.CELERY_BROKER_URL, )

app.config_from_object('django.conf:settings', )
app.autodiscover_tasks(settings.COVID19_APPS)
task_routes = {
    '*.*.*': {
        'queue': 'covidapi'
    }
}


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
