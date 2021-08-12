from django.urls import path

from . import views
################### CDB Monitor (Web) ##########################

urlpatterns = [
        path('globaltags',      views.globaltags,       name='globaltags'),
        path('globaltagdetail', views.globaltagdetail,  name='globaltagdetail'),
        path('globaltagmaps',   views.index,            name='globaltagmaps'),

        path('tags',            views.tags,             name='tags'),
        path('tagdetail',       views.tagdetail,        name='tagdetail'),

        path('stats',           views.stats,            name='stats'),

        # Test area is not exposed in the menu
        path('test',            views.test,             name='test'),

        # Documentation:
        path('',                views.documentation,    {'what':'/welcome.md',},        name='index'),
        path('about',           views.documentation,    {'what':'/about.md',},          name='about'),
        path('clients',         views.documentation,    {'what':'/clients.md',},        name='clients'),
        path('cpp',             views.documentation,    {'what':'/cpp.md',},            name='cpp'),
        path('examples',        views.documentation,    {'what':'/examples.md',},       name='examples'),
  ]

# ATTIC
#    path('', views.index, {'what':'main'}, name='index'), 
#    path('',  views.index, name='index'),
