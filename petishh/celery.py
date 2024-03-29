from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "petishh.settings.development")

app = Celery("petishh", broker=settings.BROKER_URL, backend=settings.BACKEND_URL)

app.config_from_object("django.conf:settings")

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
