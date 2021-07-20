from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, {'what':'main'}, name='index'),
    path('test', views.index, {'what':'test'}, name='index'),    
 #    path('', views.index, name='index'),
]
