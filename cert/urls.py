from django.urls import path

from .views import CreatePostView, create_certi, create_certi_multiple, DeleteFile

urlpatterns = [
   #path('', HomePageView, name='home'),
    path('', CreatePostView, name='add_post'), # new
    path('create_certi', create_certi, name='create_certi'),
    path('create_certi_multiple', create_certi_multiple, name='create_certi_multiple'),
    path('DeleteFile', DeleteFile, name='DeleteFile'),


]