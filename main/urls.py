"""anuncios2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.login_user, name='login'),
    path('usuarios', views.usuarios, name='usuarios'),
    path('crear_usuario', views.crear_usuario, name='crear_usuario'),
    path('clientes/', views.index, name='clientes'),
    path('formulario_ok/', views.formulario_ok, name='formulario_ok'),
    path('crear_cliente/', views.crear_cliente, name='crear_cliente'),
    path('campana_pdvs', views.campana_pdvs, name = 'campana_pdvs'),
    path('campanas_del_cliente/', views.campanas_del_cliente, name='campanas_del_cliente'),
    path('crear_campana', views.crear_campana, name='crear_campana'),
    path('elegir_pdvs/<int:campana_pk>/', views.elegir_pdvs, name ='elegir_pdvs'),
    path('pdis_json/', views.pdis_json, name = 'pdis_json'),
    path('guardar_config_campana/', views.guardar_config_campana, name='guardar_config_campana')



]
