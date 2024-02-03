from django.http import FileResponse, HttpResponse
from django.shortcuts import render

from .forms import ImageForm
from .servise import return_image


def index(request):
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            file_name = cd['image']

            if '90-left' in request.POST:
                return return_image(cd['image'], file_name, 90)
            
            elif '90-right' in request.POST:
                return return_image(cd['image'], file_name, 270)
            
    else:
        form = ImageForm
    return render(request, 'index.html', {'form': form})
