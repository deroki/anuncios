from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core import serializers
from django.http import HttpResponse

# Create your views here.
from main.forms import ClienteForm, ImageForm
from main.models import Cliente
from anuncios2.settings import MEDIA_URL


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
                render(request, 'main/crearCliente.html', {'form': form,
                                                           'form_image': form_image,
                                                           'exitStatus': exitStatus,
                                                           'MEDIA_URL': MEDIA_URL})

        if 'nombre' in request.POST:
            form = ClienteForm(request.POST)
            form_image = ImageForm()
            if form.is_valid():
                form.save()
                exitStatus = "Cliente guardado"
                render(request, 'main/crearCliente.html', {'form': form,
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


def clientes_asJson(request):
    clientes = Cliente.objects.all()
    clientes_json = serializers.serialize('json', clientes)
    return HttpResponse(clientes_json, content_type='application/json')
