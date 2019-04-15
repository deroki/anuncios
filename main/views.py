from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from main.forms import ClienteForm, ImageForm


def index(request):
    return render(request, 'main/clientes.html')

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
                                                           'exitStatus': exitStatus})

        if 'nombre' in request.POST:
            form = ClienteForm(request.POST)
            form_image = ImageForm()
            if form.is_valid():
                form.save()
                exitStatus = "Cliente guardado"
                render(request, 'main/crearCliente.html', {'form': form,
                                                           'form_image': form_image,
                                                           'exitStatus': exitStatus})

    else:
        form = ClienteForm()
        form_image = ImageForm()
        exitStatus = None
    return render(request, 'main/crearCliente.html', {'form': form,
                                                      'form_image': form_image,
                                                      'exitStatus': exitStatus})

def formulario_ok(request):
    return render(request, 'main/formulario_ok.html')