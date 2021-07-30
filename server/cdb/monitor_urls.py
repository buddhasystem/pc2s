from django.urls import path

from . import views
################### CDB Monitor (Web) ##########################

urlpatterns = [
    path('',                views.index,            name='index'),
    path('globaltags',      views.globaltags,       name='globaltags'),
    path('globaltagdetail', views.globaltagdetail,  name='globaltagdetail'),
    path('globaltagmaps',   views.index,            name='globaltagmaps'),

    path('tags',            views.index,            name='tags'),
    path('tagdetail',       views.tagdetail,        name='tagdetail'),

    path('documentation',   views.documentation,    name='documentation'),

#    path('',            views.index, {'what':'main'},   name='index'),    
  ]


