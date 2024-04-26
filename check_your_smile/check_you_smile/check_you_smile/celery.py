import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'check_you_smile.settings.prod')
app = Celery('check_you_smile')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
