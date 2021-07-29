from django.urls import path

from . import views

urlpatterns = [
    path('',                views.index, name='index'),
    path('globaltags',      views.globaltags, name='index'),    
    path('globaltagmaps',   views.index, name='index'),
    path('tags',            views.index, name='index'),

#    path('',            views.index, {'what':'main'},   name='index'),    
  ]


