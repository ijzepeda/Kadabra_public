from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from ms_data_mining.tasks import celebrity_task, movie_task
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ms_data_mining.settings")

app = Celery("ms_data_mining")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.task_default_queue = "default"

app.conf.task_routes = {
    "tasks.*": {"queue": "default"},
}

app.autodiscover_tasks()

task_schedule = {
    "redis-flush_all": {
        "task": "redis-flush_all",
        "schedule": crontab(minute="*/60"),
        "enabled": False,
    }
}

app.conf.beat_schedule = (celebrity_task.task_schedule | movie_task.task_schedule)


@app.task(bind=True, name="redis-flush_all")
def flush_all_cache_redis(self):
    from ms_data_mining.redis_tools import Utils as rd

    rd().flush_all()
