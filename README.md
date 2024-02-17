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
