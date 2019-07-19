from django.shortcuts import render
from .models import Session
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.core.files.storage import FileSystemStorage

def data_list(request):
	resultado = Session.objects.all().order_by('user')
	return render(request, 'siteEM/data_list.html', {'rst' : resultado})

def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'siteEM/data_list.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'siteEM/data_list.html')