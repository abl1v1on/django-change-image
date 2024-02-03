import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ChangeImage.settings')

app = Celery('ChangeImage')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое подцепление тасков
app.autodiscover_tasks()


# Рассылка на почту каждые пять минут

# app.conf.beat_schedule = {
#     # Имя таска
#     'send-spam-every-5-minute': {
#         # Путь до нужной таски
#         'task': 'image.tasks.send_beat_email',
#         # Переодичность, с которой мы будет отправлять письма
#         'schedule': crontab(minute='*/20')
#     }
# }