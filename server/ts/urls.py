from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dist/<int:t>', views.dist, name='dist'),
]
