from django.conf import settings
from celery.schedules import crontab
from kombu import Queue
# from celery.schedules import crontab


# Timezone setting
# timezone = tzlocal.get_localzone().zone
timezone = settings.TIME_ZONE
# enable_utc = True

# Broker Settings
broker_url = settings.BROKER_URL

# Task settings
task_serializer = 'pickle'
task_ignore_resul = True
accept_content = ['pickle', 'json', 'msgpack', 'yaml']

# Task result backend settings
result_backend = settings.CELERY_RESULT_BACKEND
result_serializer = 'json'
result_expires = 60 * 5
if not settings.DEBUG:
    task_ignore_result = True

# Logging
worker_log_format = "[%(asctime)s: %(levelname)s/%(processName)s] %(message)s"
worker_task_log_format = "[%(asctime)s: %(levelname)s/%(processName)s] [%(task_name)s(%(task_id)s)] %(message)s"

# Queue
# if debug worker will run this task_queues tasks
if settings.DEBUG:
    task_queues = (
        Queue('celery', routing_key='celery'),
    )

# Routing
task_routes = {}

# Worker
worker_max_tasks_per_child = 100
worker_concurrency = 3

# Beat Settings
DJANGO_CELERY_BEAT_TZ_AWARE = False
beat_scheduler = 'django_celery_beat.schedulers.DatabaseScheduler'


beat_schedule = {
    'check_bingwapper_data_task': {
        'task': 'apps.bing_wapper.task.check_bingwapper_data_task',
        'schedule': crontab(minute=5, hour=0),
    },
}
