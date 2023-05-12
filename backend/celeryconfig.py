CELERY_TASK_ROUTES = {
    "backend.tasks.*": {"queue": "backend"}
}