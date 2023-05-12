CELERY_TASK_ROUTES = {
    "textgen.tasks.*": {"queue": "textgen"}
}