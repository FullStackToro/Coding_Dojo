from django.urls import path
from . import views

urlpatterns = [

    path('', views.home),

    #Registro de nuevo Usuario
    path('registro', views.registrar),
    path('registrado', views.registrado),

    #Login de Usuarios
    path('login', views.login),
    path('exito', views.logeado),


    path('logout', views.logout),
]