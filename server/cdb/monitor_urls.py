from django.urls import path

from . import views
################### CDB Monitor (Web) ##########################
#    path('',                views.index,            name='index'),
urlpatterns = [
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
            {'what':'/clients.md', 'header':'PC2S CLI Clients'},
            name='clients'),
            
        path('cpp',
            views.documentation,
            {'what':'/cpp.md', 'header':'C++ Interface'},
            name='cpp'),

        path('examples',
            views.documentation,
            {'what':'/examples.md', 'header':'Examples of PC2S use'},
            name='examples'),

    path('stats',           views.stats,            name='stats'),
    path('test',            views.test,             name='test'),

#    path('',            views.index, {'what':'main'},   name='index'),    
  ]


