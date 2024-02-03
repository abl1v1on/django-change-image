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
