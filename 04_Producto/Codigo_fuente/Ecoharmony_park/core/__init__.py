# Carga Celery junto con Django, para que @shared_task use esta app.
from core.celery import app as celery_app

__all__ = ('celery_app',)
