from django.urls import path

from . import views

urlpatterns = [
    path('',            views.index, {'what':'main'},   name='index'),
    path('test',        views.index, {'what':'test'},   name='index'),

    # Global Tags
    path('globaltag',       views.globaltag,            name='globaltag'),
    path('globaltag/list',  views.gtlist,               name='gtlist'),
    path('globaltag/taglist',views.gttaglist,           name='gttaglist'),
    path('globaltag/create',views.gtcreate,             name='gtcreate'),
    path('globaltag/delete',views.gtdelete,             name='gtdelete'),

    # Global Tag Maps
    path('gtm',             views.gtm,                  name='gtm'),
    path('gtm/create',      views.gtmcreate,            name='gtmcreate'),
    path('gtm/delete',      views.gtmdelete,            name='gtmdelete'),

    # Tags
    path('tag',             views.tag,                  name='tag'),
    path('tag/create',      views.tagcreate,            name='tagcreate'),
    path('tag/delete',      views.tagdelete,            name='tagdelete'),

    # Payloads
    path('payload',         views.payload,              name='payload'),
    path('payload/create',  views.payloadcreate,        name='payloadcreate'),
    path('payload/delete',  views.payloaddelete,        name='payloaddelete'),    
]


