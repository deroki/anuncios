import re
from pipes import stepkinds

from django.contrib.auth import login, authenticate, logout, get_user_model
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, render_to_response
from django.core import serializers
from django.http import HttpResponse

# Create your views here.
from django.template import RequestContext

from main.forms import ClienteForm, ImageForm, UserForm, MontadorForm, CampanaForm
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
        if request.method == 'POST':
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

# Vistar de Cliente


def campanas_del_cliente(request):
    user = request.user
    cliente = Cliente.objects.get(usuario=user)
    logo_path = cliente.logo.image.name
    campanas = Campana.objects.filter(cliente=cliente)
    return render(request, 'main/cliente/campanas_del_cliente.html', {'campanas': campanas,
                                                                      'MEDIA_URL' : MEDIA_URL,
                                                                      'logo_path' : logo_path,
                                                                      'cliente': cliente
                                                                      })


def crear_campana(request):
    user = request.user
    cliente = Cliente.objects.get(usuario=user)
    logo_path = cliente.logo.image.name
    if request.method == 'POST':
        user = request.user
        cliente = Cliente.objects.get(usuario=user)
        form_campana = CampanaForm(request.POST)
        if form_campana.is_valid():
            preform = form_campana.save(commit=False)
            preform.cliente = cliente
            preform.save()
            return HttpResponseRedirect('campanas_del_cliente')
    else:
        form_campana = CampanaForm()

    return render(request, 'main/cliente/crear_campana.html', {'form_campana': form_campana,
                                                               'MEDIA_URL': MEDIA_URL,
                                                               'logo_path': logo_path,
                                                               })


def elegir_pdvs(request,campana_pk):
    user = request.user
    selected_campana = Campana.objects.get(pk = campana_pk)
    cliente = Cliente.objects.get(usuario = user)
    logo_path = cliente.logo.image.name

    pdvs = Pdv.objects.filter(cliente=cliente)

    for pdv in pdvs:
        campanas_del_pdv = pdv.campana_pdv_set
        try:
            campana_pdv = campanas_del_pdv.get(campana=selected_campana)
            pdv.estado = campana_pdv.estado
            pdv.idioma = campana_pdv.idioma
            pdv.checked = True
            print(f'{pdv.nombre}   {pdv.estado}')
        except:
            pass

    return render(request,'main/cliente/pdvs_cliente.html', {'pdvs': pdvs,
                                                             'selected_campana': selected_campana,
                                                             'MEDIA_URL' : MEDIA_URL,
                                                              'logo_path' : logo_path,
                                                             'cliente': cliente})


def pdis_json(request):
    str = request.META['HTTP_REFERER']
    CampanaNum = re.findall(r'/\d+/', str)[0][1:-1]
    campana = Campana.objects.filter(pk = CampanaNum).get()
    pdv_pk = request.GET.get('pdv_pk', None)
    pdv = Pdv.objects.get(pk=pdv_pk)
    pdis = pdv.pdi_set.all()
    creatividades = list(Creatividad.objects.all().values())
    materiales = list(Material.objects.all().values())
    try:
        campana_pdv = pdv.campana_pdv_set.filter(campana = CampanaNum).get()
        print(campana_pdv)
        pdis_ = pdis.values()
        for pdi, pdi_ in zip(pdis,pdis_):
                try:
                    campanapdv_pdi = pdi.campanapdv_pdi_set.all()
                    campanapdv_pdi = pdi.campanapdv_pdi_set.filter(Campana_Pdv = campana_pdv).get()
                    pdi_['creatividad'] = campanapdv_pdi.creatividad.id
                    pdi_['material'] = campanapdv_pdi.material.id
                    pdi_['checked'] = True
                    pdi_['tipo'] = pdi.tipo.nombre
                    pdi_['image'] = campanapdv_pdi.image.name

                except Exception as Err:
                    print(Err)
                    # pdi_['creatividad'] = ""
                    # pdi_['material'] = ""
                    pdi_['checked'] = False

        pdis_ = list(pdis_)
        return JsonResponse({'data': pdis_,
                             'creatividades': creatividades,
                             'materiales': materiales,
                             'pdv_pk': pdv_pk,
                             'MEDIA_URL' : MEDIA_URL})


    except Exception as Err:
        print(Err)
        pdis_ = pdis.values()
        for pdi, pdi_ in zip(pdis, pdis_):
            pdi_['creatividad'] = ""
            pdi_['material'] = ""
            pdi_['checked'] = True
            pdi_['tipo'] = pdi.tipo.nombre

    pdis_ = list(pdis_)
    return JsonResponse({'data': pdis_,
                         'creatividades': creatividades,
                         'materiales' : materiales,
                         'pdv_pk': pdv_pk})


def guardar_config_campana(request):
    request = request
    str = request.META['HTTP_REFERER']
    CampanaNum = re.findall(r'/\d+/', str)[0][1:-1]
    campana = Campana.objects.get(pk=CampanaNum)
    # borrar all
    campanaPdv = Campana_Pdv.objects.filter(campana=campana).delete()
    params = request.POST

    for key in params.keys():
        z = re.match(r'^pdi_\d+$', key)
        if z:
            material = key + '_material'
            creatividad = key + '_creatividad'
            print(z.group())
            pdi_pk = key[4:]
            pdi = Pdi.objects.get(pk = pdi_pk)
            pdv = pdi.pdv
            #TODO idioma español por defecto cambiar al elegido en request
            campana_Pdv, created = Campana_Pdv.objects.get_or_create(campana=campana,
                                                            pdv=pdv,
                                                            idioma=params[f'pdv_{pdv.id}_idioma'],
                                                            estado='pendiente')
            campanaPdv_Pdi = CampanapdV_pdI.objects.get_or_create(Campana_Pdv = campana_Pdv,
                                                                  pdi = pdi,
                                                                  material_id= params[material],
                                                                  creatividad_id= params[creatividad])
    return redirect('campanas_del_cliente')