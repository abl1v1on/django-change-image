import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ChangeImage.settings')

app = Celery('ChangeImage')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое подцепление тасков
app.autodiscover_tasks()


app.conf.beat_schedule = {
    # Имя таска
    'clear-media-folder-every-5-minute': {
        # Путь до нужной таски
        'task': 'image.tasks.clear_media_folder',
        # Переодичность
        'schedule': crontab(minute='*/5')
    }
}
