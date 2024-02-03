from django import forms
from PIL import Image
import os


def get_image_size(image_path):
    image = Image.open(image_path)
    image_size = os.path.getsize(image_path)
    return image_size


class ImageForm(forms.Form):
    image = forms.ImageField(label='', widget=forms.FileInput(attrs={'class': 'form-control file-input',
                                                           'accept': 'image/png, image/gif, image/jpeg'}))
    
    # def clean_image(self):
    #     image = self.cleaned_data['image']

    #     if image:
    #         image_size = image.size
    #         if image_size > 2:
    #             raise forms.ValidationError(f"Максимальный размер изобраения 2MB. Вы пытаетесь загрузить {image.size}")
    #         return image
    #     else:
    #         raise forms.ValidationError("Загрузите изображжение!")
    