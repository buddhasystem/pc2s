from django.urls import path

from . import views
################### CDB Monitor (Web) ##########################

urlpatterns = [
    path('',                views.index,            name='index'),
    path('globaltags',      views.globaltags,       name='globaltags'),
    path('globaltagdetail', views.globaltagdetail,  name='globaltagdetail'),
    path('globaltagmaps',   views.index,            name='globaltagmaps'),
    path('tags',            views.index,            name='tags'),

#    path('',            views.index, {'what':'main'},   name='index'),    
  ]


