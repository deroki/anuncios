from django.contrib.auth import login, authenticate, logout, get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response
from django.core import serializers
from django.http import HttpResponse

# Create your views here.
from django.template import RequestContext

from main.forms import ClienteForm, ImageForm, UserForm, MontadorForm
from main.models import Cliente
from main.models import *
from anuncios2.settings import MEDIA_URL

def login_user(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if user.is_staff:
                    return HttpResponseRedirect('clientes')
                elif user.is_cliente:
                    return HttpResponseRedirect('campanas_del_cliente')
                elif user.is_montador:
                    return HttpResponseRedirect()

    return render(request, 'registration/login.html')

def index(request):
    clientes = Cliente.objects.all()
    context = {'clientes' : clientes}
    return render(request, 'main/clientes.html', context)


def crear_cliente(request):
    if request.method == 'POST':
        if 'image' in request.FILES:
            print(request.FILES)
            form_image = ImageForm(request.POST, request.FILES)
            form = ClienteForm()
            if form_image.is_valid():
                form_image.save()
                exitStatus = "Imagen enviada"
                return render(request, 'main/crearCliente.html', {'form': form,
                                                           'form_image': form_image,
                                                           'exitStatus': exitStatus,
                                                           'MEDIA_URL': MEDIA_URL})

        if 'nombre' in request.POST:
            form = ClienteForm(request.POST)
            form_image = ImageForm()
            if form.is_valid():
                form.save()
                exitStatus = "Cliente guardado"
                return render(request, 'main/crearCliente.html', {'form': form,
                                                           'form_image': form_image,
                                                           'exitStatus': exitStatus,
                                                           'MEDIA_URL': MEDIA_URL})

    else:
        form = ClienteForm()
        form_image = ImageForm()
        exitStatus = None
    return render(request, 'main/crearCliente.html', {'form': form,
                                                      'form_image': form_image,
                                                      'exitStatus': exitStatus,
                                                      'MEDIA_URL': MEDIA_URL})


def formulario_ok(request):
    return render(request, 'main/formulario_ok.html')


def usuarios(request):
    User = get_user_model()
    users = User.objects.all()
    for user in users:
        if user.is_staff:
            user.role = 'STAFF'
        elif user.is_cliente:
            user.role = 'CLIENTE'
        elif user.is_montador:
            user.role = 'MONTADOR'

    context = {'users': users}
    return render(request, 'main/usuarios.html', context)

def crear_usuario(request):
        exitStatus = None
        if request.POST:
            # TODO: si el form no es valido meterlo en exitstatus
            form = UserForm(request.POST)
            form_cliente = ClienteForm(request.POST)
            form_montador = MontadorForm(request.POST)
            if form.is_valid():
                form.save()
                exitStatus = "Usuario guardado"
                user = User.objects.get(email=request.POST.get('email'))
                if request.POST.get('is_cliente'):
                    if form_cliente.is_valid():
                        preform = form_cliente.save(commit=False)
                        preform.usuario = user
                        preform.save()
                        exitStatus = "Usuario cliente guardado"
                elif request.POST.get('is_montador'):
                    if form_montador.is_valid():
                        preform = form_montador.save(commit=False)
                        preform.usuario = user
                        preform.save()
                        exitStatus = "Usuario montador guardado"
                return render(request, 'main/crear_usuario.html', {'form': form,
                                                           'form_montador': form_montador,
                                                           'form_cliente': form_cliente,
                                                            'exitStatus': exitStatus})
        else:
            form = UserForm()
            form_montador = MontadorForm()
            form_cliente = ClienteForm()
            exitStatus = None
        return render(request, 'main/crear_usuario.html', {'form': form,
                                                           'form_montador': form_montador,
                                                           'form_cliente': form_cliente,
                                                            'exitStatus': exitStatus})


def campana_pdvs(request):
    campanaPdvs = Campana_pdV_pdI.objects.all()
    return render(request, 'main/campana_pdvs.html', {'campanaPdvs': campanaPdvs})


def pdis_por_pdv(request):
    if request.POST:
        pdvSlug = request.POST['pdvSlug']
        pdis = Pdi.objects.filter(pdv=pdvSlug)


def campanas_del_cliente(request):
    user = request.user
    campanas = Campana.objects.filter(user=user)
    return render(request, 'main/campanas_del_cliente.html', {'campanas': campanas})

