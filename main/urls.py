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
    path('usuarios/', views.usuarios, name='usuarios'),
    path('crear_usuario', views.crear_usuario, name='crear_usuario'),
    path('delete_usuario/<int:pk>/', views.delete_usuario, name = "delete_usuario"),
    path('delete_usuario/', views.delete_usuario, name = "delete_usuario"),
    path('edit_usuario/<int:pk>/', views.crear_usuario, name = "edit_usuario"),
    path('edit_usuario/', views.crear_usuario, name = "edit_usuario"),
    path('clientes/', views.index, name='clientes'),
    path('formulario_ok/', views.formulario_ok, name='formulario_ok'),
    path('crear_cliente/', views.crear_cliente, name='crear_cliente'),
    path('campana_pdvs', views.campana_pdvs, name = 'campana_pdvs'),
    # admin pdvs
    path('pdvs/', views.pdvs, name="pdvs"),
    path('all_pdis_json/', views.all_pdis_json, name='all_pdis_json'),
    path('get_creatividad_imagen/', views.get_creatividad_image, name = 'get_creatividad_imagen'),
    path('crear_pdv/', views.crear_pdv, name='crear_pdv'),
    path('edit_pdv/<int:pk>/', views.crear_pdv, name='edit_pdv'),
    path('delete_pdv/<int:pk>/', views.delete_pdv, name='delete_pdv'),
    path('delete_pdv/', views.delete_pdv, name='delete_pdv'),
    path('crear_pdi/', views.crear_pdi, name='crear_pdi'),
    path('crear_material', views.crear_material, name='crear_material'),
    path('creatividades', views.creatividades, name='creatividades'),
    path('delete_creatividad/<int:creatividad_pk>/', views.delete_creatividad, name='delete_creatividad'),
    path('delete_creatividad/', views.delete_creatividad, name='delete_creatividad'),
    path('edit_creatividad/<int:pk>/', views.crear_creatividad, name="edit_creatividad"),
    path('crear_creatividad/', views.crear_creatividad, name='crear_creatividad'),
    path('materiales/', views.materiales, name="materiales"),
    path('delete_material/<int:pk>/', views.delete_material, name='delete_material'),
    path('delete_material/', views.delete_material, name='delete_material'),
    path('edit_material/<int:pk>/', views.crear_material, name="edit_material"),
    path('crear_material/', views.crear_material, name='crear_material'),
    path('instalaciones', views.instalaciones, name='instalaciones'),
    path('incidencias/<int:pk>/', views.incidencias, name="incidencias"),
    path('zonas/', views.zonas, name="zonas"),
    path('add_zonas/', views.add_zonas, name='add_zonas'),
    path('guardar_config_pdvs/', views.guardar_config_pdvs, name='guardar_config_pdvs'),
    path('finalizarCampana/', views.finalizarCampana, name='finalizarCampana'),
    # cliente
    path('campanas_del_cliente/', views.campanas_del_cliente, name='campanas_del_cliente'),
    path('campanas_del_cliente/<int:cliente_id>/', views.campanas_del_cliente, name='campanas_del_cliente'),
    path('crear_campana', views.crear_campana, name='crear_campana'),
    path('elegir_pdvs/<int:campana_pk>/', views.elegir_pdvs, name ='elegir_pdvs'),
    path('pdis_json/', views.pdis_json, name = 'pdis_json'),
    path('guardar_config_campana/', views.guardar_config_campana, name='guardar_config_campana'),
    path('estadisticas/', views.estadisticas, name='estadisticas'),
    #autocomplete
    path('campanasAutocomplete/', views.CampanasAutocomplete.as_view(), name="CampanasAutocomplete"),
    path('clientesAutocomplete/', views.ClientesAutocomplete.as_view(), name="ClientesAutocomplete"),
    path('zonasAutocomplete/', views.ZonasAutocomplete.as_view(), name="ZonasAutocomplete"),
    path('pdvsAutocomplete/', views.PdvAutocomplete.as_view(),  name="PdvAutocomplete"),
    #montador
    path('montadores_json/', views.montadores_json, name="montadores_json"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('pdis_instalacion_json/', views.pdis_instalacion_json, name="pdis_instalacion_json"),
    path('instalacion_config/', views.instalacion_config, name= "instalacion_config")


]
