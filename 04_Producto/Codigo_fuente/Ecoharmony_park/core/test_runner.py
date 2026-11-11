from django.test.runner import DiscoverRunner

from core.celery import app


class TestRunner(DiscoverRunner):
    """Corre las tareas de Celery en el momento, sin broker.

    Así los tests no necesitan Redis y el mail encolado aterriza en
    mail.outbox como cualquier otro.
    """

    def setup_test_environment(self, **kwargs):
        super().setup_test_environment(**kwargs)
        app.conf.task_always_eager = True

    def teardown_test_environment(self, **kwargs):
        app.conf.task_always_eager = False
        super().teardown_test_environment(**kwargs)
