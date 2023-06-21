from celery.schedules import crontab

task_schedule = {
    "movie_process": {
        "task": "movie_process",
        "schedule": crontab(minute="*/5"),
        "enabled": True,
    },
    "movie_process_long_task": {
        "task": "movie_process_long_task",
        "schedule": crontab(minute=0, hour=1),
        "enabled": True,
    },
    "movie_process_error": {
        "task": "movie_process_error",
        "schedule": crontab(hour="*", minute=1),
        "enabled": True,
    },
}
