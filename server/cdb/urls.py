from django.urls import path

from . import views

urlpatterns = [
    path('',            views.index, {'what':'main'},   name='index'),
    path('test',        views.index, {'what':'test'},   name='index'),

    # Global Tags
    path('gtcreate',    views.gtcreate,                 name='gtcreate'),
    path('gtdelete',    views.gtdelete,                 name='gtdelete'),

    # Global Tag Maps
    path('gtmcreate',   views.gtmcreate,                name='gtmcreate'),
    path('gtmdelete',   views.gtmdelete,                name='gtmdelete'),

    # Tags
    path('tag',             views.tag,                  name='tag'),
    path('tag/create',      views.tagcreate,            name='tagcreate'),
    path('tag/delete',      views.tagdelete,            name='tagdelete'),

    # Payloads
    path('payload/create',  views.payloadcreate,        name='payloadcreate'),
    path('payload/delete',  views.payloaddelete,        name='payloaddelete'),    
]
#################
# path('gtstatus', views.gtstatus, name='gtstatus'),
# path('', views.index, name='index'),

