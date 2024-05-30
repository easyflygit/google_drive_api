from django.urls import path
from . import views


urlpatterns = [
    path('', views.file_list, name='file_list'),
    path('api/create/', views.create_file, name='create_file'),
]