from PIL import Image
import uuid

from django.http import FileResponse

def return_image(image, file_name, rotate: int):
    image = Image.open(image).rotate(rotate)
    image_path = f'./media/{uuid.uuid4()}_{file_name}'
    image.save(image_path)
    
    responce = FileResponse(open(image_path, 'rb'))
    return responce
