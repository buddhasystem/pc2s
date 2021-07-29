from django.urls import path

from . import views

urlpatterns = [
    path('',            views.index, {'what':'main'},   name='index'),
  ]


