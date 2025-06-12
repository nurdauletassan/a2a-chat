from celery import Celery
from celery.schedules import crontab
from .config import get_settings

settings = get_settings()

# Initialize Celery
celery_app = Celery(
    "backend",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["backend.tasks.daily_task"]
)

# Configure Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

# Configure Celery Beat schedule
celery_app.conf.beat_schedule = {
    "daily-timestamp-task": {
        "task": "backend.tasks.daily_task.write_timestamp",
        "schedule": crontab(hour=0, minute=0),  # Run at midnight
    }
} 