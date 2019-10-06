import re
from pipes import stepkinds

from dal import autocomplete
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.db.models import Q, Count
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, render_to_response
from django.core import serializers
from django.http import HttpResponse
from django.db.models.functions import TruncMonth
from django.utils import timezone


# Create your views here.
from django.template import RequestContext

from main.forms import ClienteForm, ImageForm, UserForm, MontadorForm, CampanaForm, PdvForm, PdiForm, CreatividadForm, \
    MaterialForm
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
                    return HttpResponseRedirect('dashboard')

    return render(request, 'registration/login.html')

def index(request):
    clientes = Cliente.objects.all()
    return render(request, 'main/clientes.html', {'clientes' : clientes,
                                                  'MEDIA_URL' : MEDIA_URL})


def crear_cliente(request):
    if request.method == 'POST':
        if 'image' in request.FILES:
            print(request.FILES)
            form_image = ImageForm(request.POST, request.FILES)
            form = ClienteForm()
            if form_image.is_valid():
                form_image.save()
                exitStatus = "Imagen enviada"
                return render(request, 'main/crear_usuario.html', {'form': form,
                                                           'form_image': form_image,
                                                           'exitStatus': exitStatus,
                                                           'MEDIA_URL': MEDIA_URL})

        if 'nombre' in request.POST:
            form = ClienteForm(request.POST)
            form_image = ImageForm()
            if form.is_valid():
                form.save()
                exitStatus = "Cliente guardado"
                return render(request, 'main/crear_usuario.html', {'form': form,
                                                           'form_image': form_image,
                                                           'exitStatus': exitStatus,
                                                           'MEDIA_URL': MEDIA_URL})

    else:
        form = ClienteForm()
        form_image = ImageForm()
        exitStatus = None
    return render(request, 'main/crear_usuario.html', {'form': form,
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


def crear_usuario(request,pk=None):
    accion = 'Crear'
    instance = None
    cliente_instance = None
    montador_instance = None
    if pk:
        instance = User.objects.get(pk=pk)
        accion = 'Editar'
        if instance.is_cliente == True:
            cliente_instance = Cliente.objects.get(usuario = instance)
        if instance.is_montador == True:
            montador_instance = Montador.objects.get(usuario = instance)
    else:
        instance = None

    exitStatus = None
    form_image = ImageForm()
    form = UserForm()
    form_cliente = ClienteForm()
    form_montador = MontadorForm()
    #en caso de que subamos una imagen solo...
    if request.method == 'POST':
        if 'image' in request.FILES:
            form = UserForm()
            form_cliente = ClienteForm()
            form_montador = MontadorForm()
            form_image = ImageForm(request.POST, request.FILES)
            if form_image.is_valid():
                form_image.save()
                exitStatus = "Imagen enviada"
                return render(request, 'main/crear_usuario.html', {'form': form,
                                                                  'form_montador': form_montador,
                                                                  'form_image': form_image,
                                                                  'form_cliente': form_cliente,
                                                                  'exitStatus': exitStatus,
                                                                  'MEDIA_URL': MEDIA_URL,
                                                                  'accion' : accion})
        # en caso de que subamos un usuario
        if 'color' in request.POST:
            form_image = ImageForm()
            form = UserForm(request.POST, instance=instance)
            form_cliente = ClienteForm(request.POST, instance=cliente_instance)
            form_montador = MontadorForm(request.POST, instance=montador_instance)
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
                                                                   'form_image': form_image,
                                                                   'form_cliente': form_cliente,
                                                                   'exitStatus': exitStatus,
                                                                   'MEDIA_URL': MEDIA_URL,
                                                                   'accion' : accion})

    else:
        form_image = ImageForm()
        form = UserForm(instance= instance)
        form_cliente = ClienteForm(instance = cliente_instance)
        form_montador = MontadorForm(instance = montador_instance)
        exitStatus = None
    return render(request, 'main/crear_usuario.html', {'form': form,
                                                      'form_montador': form_montador,
                                                      'form_image': form_image,
                                                      'form_cliente': form_cliente,
                                                      'exitStatus': exitStatus,
                                                      'MEDIA_URL': MEDIA_URL,
                                                      'accion' : accion})


def delete_usuario(request,pk):
    usuario = User.objects.get(pk=pk)
    usuario.delete()
    return redirect('usuarios')


def pdvs(request):
    user = request.user
    if user.is_superuser:
        pdvs = Pdv.objects.all()
        print(pdvs)
    return render(request, 'main/pdvs.html', {'pdvs': pdvs})

def guardar_config_pdvs(request):
    post = request.POST
    pdvs = Pdv.objects.all().update(activo=False)
    for pdv in request.POST.keys():
        if pdv.startswith("pdv"):
            pdv_id = pdv[4:]
            pdv_status = request.POST[pdv]
            pdv = Pdv.objects.get(pk=pdv_id)
            pdv.activo = pdv_status
            pdv.save()


    return redirect('pdvs')



class ClientesAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Cliente.objects.none()

        clientes = Cliente.objects.all()

        if self.q:
            seleccion = clientes.filter(usuario__empresa__startswith = self.q)
        else:
            seleccion = clientes

        return seleccion

class PdvAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Pdv.objects.none()

        
        pdvs = Pdv.objects.all()
        
        if self.q:
            seleccion = pdvs.filter(nombre__startswith = self.q)
        else:
            seleccion = pdvs

        return seleccion

class ZonasAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Zona.objects.none()

        zonas = Zona.objects.all()
        if self.q:
            seleccion = zonas.filter(cliente__usuario__empresa__startswith = self.q)
        else:
            seleccion = zonas


        return seleccion


def all_pdis_json(request):

    """
    GET: pdv_pk
    :param request:
    :return: (datos del pdi) (path de la ultima imagen del campana_pdv_pdi donde la fecha de cambio sea la ultima
    """

    pdv_pk = request.GET.get('pdv_pk', None)
    pdis = Pdi.objects.filter(pdv=pdv_pk)
    pdis_ = list(pdis.values())

    for pdi, pdi_ in zip(pdis, pdis_):
        try:
            image = CampanapdV_pdI.objects.filter(pdi=pdi).latest('fecha_cambio').image.name
            pdi_['image'] = image
        except:
            pass



    return JsonResponse({'data': pdis_,
                         'pdv_pk': pdv_pk,
                         'MEDIA_URL': MEDIA_URL})

def get_creatividad_image(request):
    pdv_name = request.GET.get('pdv', None)
    pdi_name = request.GET.get('pdi', None)
    creatividad_name = request.GET.get('creatividad', None)
    campana_name = request.GET.get('campana_name', None)
    campana = campana_name.lower()

    campana = Campana.objects.get(nombre=campana)
    creatividad = Creatividad.objects.get(campana = campana, nombre = creatividad_name)
    imagepath = MEDIA_URL + creatividad.imagen.name

    return JsonResponse({'imagen': imagepath})




def crear_pdv(request, pk=None):
    if pk:
        accion = "Editar"
        instance = Pdv.objects.get(pk=pk)
    else:
        accion = "Crear"
        instance = None

    if request.method == 'POST':
        pdv_form = PdvForm(request.POST, instance=instance)
        if pdv_form.is_valid():
            pdv_form.save()
            return redirect('pdvs')
    else:
        pdv_form = PdvForm(instance=instance)
    return render(request, 'main/crear_pdv.html',{'form': pdv_form,
                                                  'accion' : accion})


def delete_pdv(request, pk=None):
    pdv = Pdv.objects.filter(pk = pk)
    pdv.delete()
    return redirect('pdvs')

def crear_pdi(request, pk=None):
    if pk:
        accion = "Editar"
        instance = Pdi.objects.get(pk=pk)
    else:
        accion = "Crear"
        instance = None

    if request.method == 'POST':
        pdi_form = PdiForm(request.POST, instance=instance)
        if pdi_form.is_valid():
            pdi_form.save()
            return redirect('pdvs')
    else:
        pdi_form = PdiForm(instance=instance)
    return render(request, 'main/crear_pdi.html',{'form': pdi_form,
                                                'accion' : accion})


def campana_pdvs(request):
    pass


def pdis_por_pdv(request):
    if request.POST:
        pdvSlug = request.POST['pdvSlug']
        pdis = Pdi.objects.filter(pdv=pdvSlug)


# def get_cliente_pk(request):
#     return pk


def campanas_del_cliente(request, cliente_id = None):
    user = request.user
    if user.is_cliente:
        cliente = Cliente.objects.get(usuario=user)
    elif cliente_id == None:
        cliente_id = request.COOKIES.get('cliente_id')
        cliente = Cliente.objects.get(pk=cliente_id)
    elif user.is_staff:
        cliente = Cliente.objects.get(pk=cliente_id)

    logo_path = cliente.logo.image.name
    campanas = Campana.objects.filter(cliente=cliente)
    response = render(request, 'main/cliente/campanas_del_cliente.html', {'campanas': campanas,
                                                                      'MEDIA_URL' : MEDIA_URL,
                                                                      'logo_path' : logo_path,
                                                                      'cliente': cliente
                                                                      })

    response.set_cookie('cliente_id', cliente_id)
    return response


def crear_campana(request):
    cliente_id = ""
    user = request.user
    if user.is_staff:
        cliente_id = request.COOKIES.get('cliente_id')
        cliente = Cliente.objects.get(pk=cliente_id)
    else:
        cliente = Cliente.objects.get(usuario=user)
    logo_path = cliente.logo.image.name
    if request.method == 'POST':
        user = request.user
        form_campana = CampanaForm(request.POST)
        if form_campana.is_valid():
            preform = form_campana.save(commit=False)
            preform.cliente = cliente
            preform.save()
            return redirect('campanas_del_cliente', cliente_id =cliente_id)
    else:
        form_campana = CampanaForm()

    return render(request, 'main/cliente/crear_campana.html', {'form_campana': form_campana,
                                                               'MEDIA_URL': MEDIA_URL,
                                                               'logo_path': logo_path,
                                                               })


def elegir_pdvs(request,campana_pk):
    user = request.user
    if user.is_staff:
        cliente_id = request.COOKIES.get('cliente_id')
        cliente = Cliente.objects.get(pk=cliente_id)
    else:
        cliente = Cliente.objects.get(usuario=user)
    selected_campana = Campana.objects.get(pk = campana_pk)
    logo_path = cliente.logo.image.name

    pdvs = Pdv.objects.filter(cliente=cliente, activo=True)

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


def estadisticas(request,pk):

    def generate_list(queryset):
        months = ['Enero','Febrero','Marzo','Abril','Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        lista = []
        try:
            line = queryset[0]
        except:
            return []

        for key in line.keys():
            if key in months:
                lista.append(line[key])

        return lista

    today_date = timezone.now()
    year = today_date.year
    user = request.user
    if user.is_staff:
        cliente_id = request.COOKIES.get('cliente_id')
        cliente = Cliente.objects.get(pk=cliente_id)
    else:
        cliente = Cliente.objects.get(usuario=user)

    logo_path = cliente.logo.image.name


    #query para hacer la agregacion
    campana = Campana.objects.get(pk = pk)
    campanas_pdv_ok = Campana_Pdv.objects.filter(Q(estado='atendida') & Q(fecha_cambio__year=year)).values('estado','fecha_cambio') \
                                        .annotate(Enero=Count('estado', filter=Q(fecha_cambio__month=1))) \
                                        .annotate(Febrero=Count('estado', filter=Q(fecha_cambio__month=2))) \
                                        .annotate(Marzo=Count('estado', filter=Q(fecha_cambio__month=3))) \
                                        .annotate(Abril=Count('estado', filter=Q(fecha_cambio__month=4))) \
                                        .annotate(Mayo=Count('estado', filter=Q(fecha_cambio__month=5))) \
                                        .annotate(Junio=Count('estado', filter=Q(fecha_cambio__month=6))) \
                                        .annotate(Julio=Count('estado', filter=Q(fecha_cambio__month=7))) \
                                        .annotate(Agosto=Count('estado', filter=Q(fecha_cambio__month=8))) \
                                        .annotate(Septiembre=Count('estado', filter=Q(fecha_cambio__month=9))) \
                                        .annotate(Octubre=Count('estado', filter=Q(fecha_cambio__month=10))) \
                                        .annotate(Noviembre=Count('estado', filter=Q(fecha_cambio__month=11))) \
                                        .annotate(Diciembre=Count('estado', filter=Q(fecha_cambio__month=12))) \

    campanas_pdv_ko = Campana_Pdv.objects.filter(Q(estado='suspendida') & Q(fecha_cambio__year=year)).values('estado','fecha_cambio') \
                                        .annotate(Enero=Count('estado', filter=Q(fecha_cambio__month=1))) \
                                        .annotate(Febrero=Count('estado', filter=Q(fecha_cambio__month=2))) \
                                        .annotate(Marzo=Count('estado', filter=Q(fecha_cambio__month=3))) \
                                        .annotate(Abril=Count('estado', filter=Q(fecha_cambio__month=4))) \
                                        .annotate(Mayo=Count('estado', filter=Q(fecha_cambio__month=5))) \
                                        .annotate(Junio=Count('estado', filter=Q(fecha_cambio__month=6))) \
                                        .annotate(Julio=Count('estado', filter=Q(fecha_cambio__month=7))) \
                                        .annotate(Agosto=Count('estado', filter=Q(fecha_cambio__month=8))) \
                                        .annotate(Septiembre=Count('estado', filter=Q(fecha_cambio__month=9))) \
                                        .annotate(Octubre=Count('estado', filter=Q(fecha_cambio__month=10))) \
                                        .annotate(Noviembre=Count('estado', filter=Q(fecha_cambio__month=11))) \
                                        .annotate(Diciembre=Count('estado', filter=Q(fecha_cambio__month=12))) \

    campanas_pdv_incidencia = Campana_Pdv.objects.filter(Q(estado='incidencia') & Q(fecha_cambio__year=year)).values('estado','fecha_cambio') \
                                        .annotate(Enero=Count('estado', filter=Q(fecha_cambio__month=1))) \
                                        .annotate(Febrero=Count('estado', filter=Q(fecha_cambio__month=2))) \
                                        .annotate(Marzo=Count('estado', filter=Q(fecha_cambio__month=3))) \
                                        .annotate(Abril=Count('estado', filter=Q(fecha_cambio__month=4))) \
                                        .annotate(Mayo=Count('estado', filter=Q(fecha_cambio__month=5))) \
                                        .annotate(Junio=Count('estado', filter=Q(fecha_cambio__month=6))) \
                                        .annotate(Julio=Count('estado', filter=Q(fecha_cambio__month=7))) \
                                        .annotate(Agosto=Count('estado', filter=Q(fecha_cambio__month=8))) \
                                        .annotate(Septiembre=Count('estado', filter=Q(fecha_cambio__month=9))) \
                                        .annotate(Octubre=Count('estado', filter=Q(fecha_cambio__month=10))) \
                                        .annotate(Noviembre=Count('estado', filter=Q(fecha_cambio__month=11))) \
                                        .annotate(Diciembre=Count('estado', filter=Q(fecha_cambio__month=12))) \

    ok_list = generate_list(campanas_pdv_ok)
    ko_list = generate_list(campanas_pdv_ko)
    incidencia_list = generate_list(campanas_pdv_incidencia)


    return render(request, 'main/cliente/estadisticas.html', {'cliente': cliente,
                                                              'logo_path': logo_path,
                                                              'MEDIA_URL' : MEDIA_URL,
                                                              'selected_campana' : campana,
                                                              'ok' : ok_list,
                                                              'ko' : ko_list,
                                                              'incidencia' : incidencia_list})

def pdis_json(request):
    '''
    Si falta por ejemplo el material ya no funciona bien y no salen las fotos subidas por el mntador

    :param request:
    :return:
    '''
    str = request.META['HTTP_REFERER']
    CampanaNum = re.findall(r'/\d+/', str)[0][1:-1]
    campana = Campana.objects.filter(pk = CampanaNum).get()
    pdv_pk = request.GET.get('pdv_pk', None)
    pdv = Pdv.objects.get(pk=pdv_pk)
    pdis = pdv.pdi_set.all()
    montadores = None
    first_pdi = pdis.first()
    #montadores = first_pdi
    creatividades = list(Creatividad.objects.filter(campana=campana).values())
    materiales = list(Material.objects.all().values())

    try:
        # en caso de que este el pdv sleccionado para la campaña
        pdis_ = pdis.values()
        for pdi, pdi_ in zip(pdis,pdis_):
                try:
                    campana_pdv = pdv.campana_pdv_set.filter(campana=CampanaNum).get()
                    campanapdv_pdi = pdi.campanapdv_pdi_set.all()
                    campanapdv_pdi = pdi.campanapdv_pdi_set.filter(Campana_Pdv = campana_pdv).get()
                    pdi_['creatividad'] = campanapdv_pdi.creatividad.id
                    pdi_['material'] = pdi.material.nombre
                    pdi_['checked'] = True
                    pdi_['tipo'] = pdi.tipo.nombre
                    pdi_['image'] = campanapdv_pdi.image.name
                    montadores = [k['email'] for k in campanapdv_pdi.user_montador.all().values()]

                except Exception as Err:
                    print(Err)
                    # pdi_['creatividad'] = ""
                    pdi_['material'] = pdi.material.nombre
                    pdi_['checked'] = False

        pdis_ = list(pdis_)

        return JsonResponse({'data': pdis_,
                             'creatividades': creatividades,
                             'materiales': materiales,
                             'pdv_pk': pdv_pk,
                             'MEDIA_URL' : MEDIA_URL,
                             'montadores': montadores})


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
    cliente_id = campana.cliente.pk
    # borrar all
    campanaPdv = Campana_Pdv.objects.filter(campana=campana).delete()
    params = request.POST

    for key in params.keys():
        z = re.match(r'^pdi_\d+$', key)
        if z:
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

            #si no hay creatividad que seleccionar
            try:
                creatividad_id = params[creatividad]
            except:
                creatividad_id = None


            campanaPdv_Pdi, created = CampanapdV_pdI.objects.get_or_create(Campana_Pdv = campana_Pdv,
                                                                  pdi = pdi,
                                                                  creatividad_id= creatividad_id)
            montadores_list = request.POST.getlist(f'montadores_{pdv.pk}')
            if montadores_list:
                for user_pk in montadores_list:
                    campanaPdv_Pdi.user_montador.add(User.objects.get(pk=user_pk))
                    campanaPdv_Pdi.save()

    return reporte(request, CampanaNum)



def reporte(request, campana_pk):
    from django.core.files.storage import FileSystemStorage
    from django.http import HttpResponse
    from django.template.loader import render_to_string


    user = request.user
    if user.is_staff:
        cliente_id = request.COOKIES.get('cliente_id')
        cliente = Cliente.objects.get(pk=cliente_id)
    else:
        cliente = Cliente.objects.get(usuario=user)
    logo_path = cliente.logo.image.name
    
    pdvs = []
    campana = Campana.objects.get(pk=campana_pk)
    campana_pdv_items = Campana_Pdv.objects.filter(campana=campana)

    for item in campana_pdv_items:
        pdv = {}
        pdv['id'] = item.pdv.id
        pdv['nombre'] = item.pdv.nombre
        pdv['cadena'] = item.pdv.cadena
        pdv['idioma'] = item.idioma
        pdv['ciudad'] = item.pdv.ciudad
        pdv['provincia'] = item.pdv.id
        pdv['estado'] = item.estado
        # get the pdi info of this pdv
        campanaPdvPdis = CampanapdV_pdI.objects.filter(Campana_Pdv=item)
        if campanaPdvPdis != None:
            pdv['pdis'] = []
            for campanaPdvPdi in campanaPdvPdis:
                pdi = {}
                pdi['nombre'] = campanaPdvPdi.pdi.nombre
                pdi['tipo'] = campanaPdvPdi.pdi.tipo
                pdi['anchoT'] = campanaPdvPdi.pdi.anchoTotal
                pdi['anchoV'] = campanaPdvPdi.pdi.anchoVista
                pdi['altoT'] = campanaPdvPdi.pdi.altoTotal
                pdi['altoV'] = campanaPdvPdi.pdi.altoVista
                pdi['composicion'] = campanaPdvPdi.pdi.composicion
                pdi['instaladores'] = campanaPdvPdi.pdi.instaladores
                pdi['material'] = campanaPdvPdi.pdi.material
                pdi['creatividad'] = campanaPdvPdi.creatividad.imagen
                pdi['montadores'] = campanaPdvPdi.user_montador.all()
                
                pdv['pdis'].append(pdi)


        pdvs.append(pdv)


    return html_to_pdf_view(request, "main/cliente/reporte.html", {'cliente' : cliente,
                                                                    'pdvs' : pdvs,
                                                                    "MEDIA_URL": MEDIA_URL,
                                                                    'logo_path' : logo_path})
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template.loader import render_to_string

from weasyprint import HTML

def html_to_pdf_view(request, template, context):
    html_string = render_to_string(template, context)

    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    html.write_pdf(target='/tmp/mypdf.pdf')

    fs = FileSystemStorage('/tmp')
    with fs.open('mypdf.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
        return response

    return response


def finalizarCampana(request):
    request = request
    url = request.META['HTTP_REFERER']
    for key in request.POST.keys():
        if key.startswith("EndCamp"):
            campana_pk = key[8:]
            campana = Campana.objects.get(pk=campana_pk)
            campana.estado = "finalizada"
            campana.activo = False
            campana.fecha_finalizado = timezone.now()
            campana.save()



    return redirect(url)




def creatividades(request):
    creatividades = Creatividad.objects.all()

    return render(request,'main/creatividades.html', context={'creatividades': creatividades})


def crear_creatividad(request, pk=None):
    if pk:
        accion = "Editar"
        instance = Creatividad.objects.get(pk=pk)
    else:
        accion = "Crear"
        instance = None

    if request.method == 'POST':
        creatividad_form = CreatividadForm(request.POST, request.FILES, instance=instance,)
        if creatividad_form.is_valid():
            creatividad_form.save()
            return redirect('creatividades')
    else:
        creatividad_form = CreatividadForm(instance = instance)
    return render(request, 'main/crear_creatividad.html',{'form': creatividad_form,
                                                          'accion':  accion})


def delete_creatividad(request, creatividad_pk = None):
    creatividad = Creatividad.objects.filter(pk=creatividad_pk)
    creatividad.delete()
    return redirect('creatividades')


class CampanasAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Campana.objects.none()

        qs = Campana.objects.all()

        if self.q:
            qs = qs.filter(cliente__usuario__empresa__istartswith=self.q)

        return qs


def materiales(request):
    materiales = Material.objects.all()
    return render(request,'main/materiales.html', context={'materiales' : materiales})


def crear_material(request, pk=None):
    if pk:
        instance = Material.objects.get(pk=pk)
    else:
        instance = None

    if request.method == 'POST':
        material_form = MaterialForm(request.POST, instance=instance)
        if material_form.is_valid():
            material_form.save()
            return redirect('materiales')
    else:
        material_form = MaterialForm(instance=instance)
    return render(request, 'main/crear_material.html',{'form': material_form})


def delete_material(request,pk):
    material = Material.objects.get(pk=pk)
    material.delete()
    return redirect('materiales')


def instalaciones(request):
    instalaciones = Campana_Pdv.objects.all().order_by('-fecha_cambio')
    return render(request,'main/instalaciones.html', context={'instalaciones': instalaciones})



def incidencias(request,pk):
    instalacion = Campana_Pdv.objects.get(pk=pk)
    incidencias = Comments.objects.filter(Campana_Pdv = instalacion)
    return render(request,'main/incidencias.html', context={'incidencias' : incidencias,
                                                            'instalacion_pk' : instalacion.pk})


def zonas(request):
    clientes = Cliente.objects.all()
    clientes_dict = {}
    for cliente in clientes:
        clientes_dict[cliente.usuario.empresa] = ''
        zonas = Zona.objects.filter(cliente=cliente)
        for zona in zonas:
            try:
                if clientes_dict[cliente.usuario.empresa] == '':
                    clientes_dict[cliente.usuario.empresa] = clientes_dict[cliente.usuario.empresa] + zona.nombre
                else:
                    clientes_dict[cliente.usuario.empresa] = clientes_dict[cliente.usuario.empresa] + " - " + zona.nombre
            except Exception as err:
                print(err)
                clientes_dict[cliente.usuario.empresa] = ""

    return render(request, 'main/zonas.html', context={'clientes_dict' : clientes_dict})


def add_zonas(request):
    clientes = Cliente.objects.all()
    if request.method =='POST':
        post = request.POST
        cliente_pk = post['cliente']
        cliente = Cliente.objects.get(pk=cliente_pk)
        # borrar todas las zonas del cliente
        Zona.objects.filter(cliente=cliente).delete()
        #crearlas
        zonas = post['zonas']
        zonas_list= zonas.replace(' ','').split(",")
        for zona in zonas_list:
            newZona = Zona.objects.get_or_create(cliente=cliente, nombre=zona)

        return redirect('zonas')
    else:

        return render(request, 'main/zonas_form.html', context={'clientes': clientes })




# Montador


def montadores_json(request):
    montadores = Montador.objects.all()
    jsonList = []
    for montador in montadores:
        montadorDict = {'id' : montador.usuario.pk,
                        'text': montador.usuario.email}
        jsonList.append(montadorDict)


    return JsonResponse({'results' : jsonList })

def dashboard(request):
    """
    Coje todas las instalacionesPDI del montador, devuelve todas las instalacionesPDV por cada instalacion PDI que esté pendiente.
    :param request:
    :return:
    """
    user = request.user
    instalaciones_pdi = CampanapdV_pdI.objects.filter(user_montador= user)
    instalaciones_pdv = []

    for instalacion_pdi in instalaciones_pdi:
        instalacion_pdv =instalacion_pdi.Campana_Pdv
        if instalacion_pdv not in instalaciones_pdv and instalacion_pdv.estado == 'pendiente' and instalacion_pdv.estado == 'pendiente':
            instalaciones_pdv.append(instalacion_pdi.Campana_Pdv)

    return render(request, 'main/montador/dasboard.html', context= {'instalaciones_pdv': instalaciones_pdv})


def pdis_instalacion_json(request):
    instalacionPdv_pk = request.GET.get('instalacionPdv_pk', None)
    instalacionPdv = Campana_Pdv.objects.get(pk = instalacionPdv_pk)
    instalacionesPdi = CampanapdV_pdI.objects.filter(Campana_Pdv = instalacionPdv)
    jsonDict = {'data': [] }

    for instalacionPdi in instalacionesPdi:
        lastImage = CampanapdV_pdI.objects.filter(pdi=instalacionPdi.pdi).order_by('-fecha_cambio').first()
        jsonDict['data'].append({'nombre' : instalacionPdi.pdi.nombre,
                                 'tipo' : instalacionPdi.pdi.tipo.nombre,
                                 'anchoTotal' : instalacionPdi.pdi.anchoTotal,
                                 'anchoVista': instalacionPdi.pdi.anchoVista,
                                 'altoVista' : instalacionPdi.pdi.altoVista,
                                 'altoTotal' : instalacionPdi.pdi.altoTotal,
                                 'composicion': instalacionPdi.pdi.composicion,
                                 'pdi_pk' : instalacionPdi.pk, # se trata del pk de la instalacion no del pdi
                                 'imagenNow' : lastImage.image.name,
                                 "MEDIA_URL": MEDIA_URL,
                                 'campanaPdv_pk' : instalacionPdi.Campana_Pdv.pk
                                })

    return JsonResponse(jsonDict)


def instalacion_config(request):
    params = request.POST
    files = request.FILES
    user = request.user

    if files is not None:
        for imageinput in files.keys():
            pk =imageinput[6:]
            instance = CampanapdV_pdI.objects.get(pk=pk)
            instance.image= files[imageinput]
            instance.save()



    for key in params.keys():
        word = re.match(r'^comment_\d+$', key)
        if word:
            pk = key[8:]
            instalacion = Campana_Pdv.objects.get(pk=pk)
            comentario = params[f'comment_{pk}']

            tipo = params['options']

            Comment = Comments(Campana_Pdv=instalacion,
                               User= user,
                               Comments = comentario,
                               tipo= tipo,
                               visible= False)
            Comment.save()
            # Aqui el estado del ultimo comentario en el pdi, se utiliza para marcar el ultimo estado del pdv , aqui llamado instalacion
            instalacion.estado = tipo
            instalacion.save()
            if user.is_staff:
                return redirect('incidencias', pk=pk)

    return redirect('dashboard')

