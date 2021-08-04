from django.urls import path

from . import views
################### CDB Monitor (Web) ##########################

urlpatterns = [
#    path('',                views.index,            name='index'),
    path('',
        views.documentation,
        {'what':'/welcome.md', 'header':'Welcome to PC2S'}, name='index'),

    path('globaltags',      views.globaltags,       name='globaltags'),
    path('globaltagdetail', views.globaltagdetail,  name='globaltagdetail'),
    path('globaltagmaps',   views.index,            name='globaltagmaps'),

    path('tags',            views.tags,             name='tags'),
    path('tagdetail',       views.tagdetail,        name='tagdetail'),

    path('about',
            views.documentation,
            {'what':'/about.md', 'header':'About'},
            name='about'),
    path('clients',
            views.documentation,
            {'what':'/clients.md', 'header':'PC2S CLI Clients'},name='clients'),
#    path('',            views.index, {'what':'main'},   name='index'),    
  ]


