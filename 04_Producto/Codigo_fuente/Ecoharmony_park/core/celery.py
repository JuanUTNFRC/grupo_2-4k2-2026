import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')
# Toda la configuración sale del settings, con el prefijo CELERY_.
app.config_from_object('django.conf:settings', namespace='CELERY')
# Busca un módulo tasks.py en cada app instalada.
app.autodiscover_tasks()
