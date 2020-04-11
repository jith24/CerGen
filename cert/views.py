from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from .forms import PostForm
from django.utils.encoding import smart_str
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from django.http import HttpResponse
import os, xlrd
from zipfile import ZipFile

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
    #selecting the required font and text size
    path="static/fonts/DejaVuSans-Oblique.ttf"
    h = int(request.POST.get('h'))
    selectFont = ImageFont.truetype(path, size = h)
    name = request.POST.get('name')
    W, H = draw.textsize(name, selectFont)
    x1 = int(request.POST.get('x1'))
    #x2 = request.POST.get('x2')
    y1 = int(request.POST.get('y1'))
    #y2 = request.POST.get('y2')
    w = int(request.POST.get('w'))
    draw.text((x1+(w-W)/2,y1+(h-H)/2), name, (0,0,0), font=selectFont)

    img.save( 'certificate\\'+name+'.pdf', "PDF", resolution=100.0)
    os.remove(temp_path[1:])

    file_name = name+'.pdf'
    path_to_file = 'certificate\\'
    response = HttpResponse(content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_name)
    response['X-Sendfile'] = smart_str(path_to_file)
    os.remove(path_to_file+file_name)
    return response

    #html = "Success!"
    #return HttpResponse(html)

def create_certi_indi(name,x1,y1,h,w,temp_path,zipname):
    img = Image.open(temp_path[1:])
    draw = ImageDraw.Draw(img)
    path="static/fonts/DejaVuSans-Oblique.ttf"
    selectFont = ImageFont.truetype(path, size = int(h))
    W, H = draw.textsize(name, selectFont)
    draw.text((x1+(w-W)/2,y1+(h-H)/2),name, (0,0,0), font=selectFont)
    zipObj = ZipFile('certificate\\'+zipname+'.zip', 'a')
    img.save('certificate\\'+name+'.pdf', "PDF", resolution=100.0)
    zipObj.write('certificate/'+name+'.pdf')
    os.remove('certificate\\'+name+'.pdf')
    zipObj.close()


    
    html = "Success!"
    return HttpResponse(html)

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
