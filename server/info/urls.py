from django.urls import path, re_path
from django.contrib	import admin

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^ping/', views.ping, name='ping'),
#    path('', views.index, name='index'),
]
