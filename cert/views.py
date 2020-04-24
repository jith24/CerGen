from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from .forms import PostForm
from django.http import FileResponse
from django.utils.encoding import smart_str
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from django.http import HttpResponse
import os, xlrd, mimetypes, logging
from zipfile import ZipFile
from pdf2image import convert_from_path

logger = logging.getLogger(__name__)


def DeleteFile(request):
    file_name = request.POST.get('file_url')
    os.remove(file_name[1:])
    return HttpResponse(file_name)

def CreatePostView(request): # new
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return render(request, 'home.html', {'post':post})
    else:
        form = PostForm()
    return render(request, 'post.html', {'form': form})

def create_certi(request):
    temp_path=request.POST.get('url')
    img = Image.open(temp_path[1:])
    draw = ImageDraw.Draw(img)
    path="static/fonts/DejaVuSans-Oblique.ttf"
    h = int(request.POST.get('h'))
    selectFont = ImageFont.truetype(path, size = h)
    name = request.POST.get('name')
    W, H = draw.textsize(name, selectFont)
    x1 = int(request.POST.get('x1'))
    y1 = int(request.POST.get('y1'))
    w = int(request.POST.get('w'))
    draw.text((x1+(w-W)/2,y1+(h-H)/2), name, (0,0,0), font=selectFont)
    img.save( 'media/certificate/'+name+'.pdf', "PDF", resolution=100.0)
    os.remove(temp_path[1:])
    file_name = name+'.pdf'
    path_to_file = 'certificate\\'
    response = path_to_file+file_name
    return HttpResponse('/media/certificate/'+file_name)


def create_certi_indi(name,x1,y1,h,w,temp_path,zipname):
    img = Image.open(temp_path[1:])
    draw = ImageDraw.Draw(img)
    path="static/fonts/DejaVuSans-Oblique.ttf"
    selectFont = ImageFont.truetype(path, size = h)
    W, H = draw.textsize(name, selectFont)
    draw.text((x1+(w-W)/2,y1+(h-H)/2),name, (0,0,0), font=selectFont)
    zipObj = ZipFile('media/certificate/'+zipname+'.zip', 'a')
    img.save('media/certificate/'+name+'.pdf', "PDF", resolution=100.0)
    zipObj.write('media/certificate/'+name+'.pdf')
    os.remove('media/certificate/'+name+'.pdf')
    zipObj.close()
    #html = "Success!"
    return zipname

def create_certi_multiple(request):
    temp_path=request.POST.get('url')
    xl_path_temp=request.POST.get('file_url')
    xl_path=xl_path_temp[1:]
    Book = xlrd.open_workbook(xl_path)
    WorkSheet = Book.sheet_by_name('Sheet1')
    num_row = WorkSheet.nrows - 1
    row = 0
    x1 = request.POST.get('x1')
    y1 = request.POST.get('y1')
    h = request.POST.get('h')
    w = request.POST.get('w')
    zipname = request.POST.get('name')


    while row < num_row:
        row += 1
        
        name = WorkSheet.cell_value(row,1)
        
        
        # Make certificate and check if it was successful
        filename = create_certi_indi(name,int(x1),int(y1),int(h),int(w),temp_path,zipname)
    
    return HttpResponse('/media/certificate/'+filename+'.zip')