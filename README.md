### Change image V1

The site allows you to rotate images 90 degrees to the right and left.

![Example](https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExbmJidzNrbTdpeDJrcmtkOXNmdzlnM3Z6YjNhYXY5MTF5bmY3eWU2dSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xkE6a0hjSKbrVguGAw/giphy.gif)


## Run Redis

`settings.py`
~~~python
REDIS_HOST = '0.0.0.0'
REDIS_PORT = '6379'
CELERY_BROKER_URL = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_RESULT_BACKEND = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
~~~
<br>

`terminal`
~~~linux
sudo docker run --name some-redis -d redis
~~~

## Run celery worker
Every time the user uploads a new image to edit, it is saved in the `media/` folder. To avoid storing all these images, we create a scheduled task that will clean out the `media/` folder every 5 minutes.

<br> 

`tasks.py`
~~~python
from ChangeImage.celery import app
import os


@app.task
def clear_media_folder():
    folder_path = './media'

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
        except Exception as ex:
            print(f'Fail, {ex}')
~~~

<br>

`celery.py`
~~~python
import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ChangeImage.settings')

app = Celery('ChangeImage')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule = {
    # create task name
    'clear-media-folder-every-5-minute': {
        # path to task
        'task': 'image.tasks.clear_media_folder',
        # task runs every 5 minutes
        'schedule': crontab(minute='*/5')
    }
}
~~~

#### Run worker
~~~
celery -A ChangeImage worker -l info
~~~

#### Run beat schedule
~~~
celery -A ChangeImage beat -l info
~~~

## Run flower
~~~
flower -A ChangeImage --port=5555
~~~

<br>

<br>

<p align="center">
    <img width="400" height="250" src="https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExdGNkNTRsYW5pY2RrbW1zczIxMjg4czQ5eTJlOWMyczNuNGI1dzV4NCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/cMnt7i2RykmpW/giphy.gif">
</p>
