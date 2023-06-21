from celery.schedules import crontab

task_schedule = {
    "actor_process": {
        "task": "actor_process",
        "schedule": crontab(minute="*/5"),
        "enabled": True,
    },
    "actor_process_long_task": {
        "task": "actor_process_long_task",
        "schedule": crontab(minute=0, hour=1),
        "enabled": True,
    },
    "actor_process_error": {
        "task": "actor_process_error",
        "schedule": crontab(hour="*", minute=1),
        "enabled": True,
    },
    "actor_image_process": {
        "task": "actor_image_process",
        "schedule": crontab(minute="*/5"),
        "enabled": True,
    },
    "actor_image_process_long_task": {
        "task": "actor_image_process_long_task",
        "schedule": crontab(minute=0, hour=1),
        "enabled": True,
    },
    "actor_image_process_error": {
        "task": "actor_image_process_error",
        "schedule": crontab(hour="*", minute=1),
        "enabled": True,
    },
    "elasticsearch_process": {
        "task": "elasticsearch_process",
        "schedule": crontab(minute="*/5"),
        "enabled": True,
    },
    "elasticsearch_process_long_task": {
        "task": "elasticsearch_process_long_task",
        "schedule": crontab(minute=0, hour=1),
        "enabled": True,
    },
    "elasticsearch_process_error": {
        "task": "elasticsearch_process_error",
        "schedule": crontab(hour="*", minute=1),
        "enabled": True,
    },
}
