from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('registro/', views.registro, name='registro'),
    path('', views.home, name='home'),
    path('sobre_nosotros/', views.sobre_nosotros, name='sobre_nosotros'), 
]
