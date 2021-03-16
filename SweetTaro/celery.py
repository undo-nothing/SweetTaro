import os
from celery import Celery, platforms
from celery.utils.log import get_task_logger
# from django.conf import settings

platforms.C_FORCE_ROOT = True

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SweetTaro.settings')

app = Celery('SweetTaro')
logger = get_task_logger(__name__)
# app.config_from_object('django.conf.settings')
app.config_from_object('SweetTaro.celeryconfig')
app.autodiscover_tasks()
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True, name='debug_task')
def debug_task(self, *args, **kwargs):
    logger.info('Request: {0!r}'.format(self.request))


@app.task(bind=True, name='debug_queue_task')
def debug_queue_task(self, *args, **kwargs):
    pass
