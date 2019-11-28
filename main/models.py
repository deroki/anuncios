from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model."""
    # TODO añadir resto de caracteristicas o crear nuevos users asociados one2one
    objects = UserManager()
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150,
                                unique=False,
                                null=True,
                                blank=True,
                                default=None)
    is_cliente = models.BooleanField(default=False)
    is_montador = models.BooleanField(default=False)
    empresa = models.CharField(max_length=100,
                               default=None,
                               null=True,
                               blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Logo(models.Model):
    image = models.ImageField(upload_to='images/')
    datestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.image.name


COLOR = (('red', 'rojo'),
         ('blue', 'azul'),
         ('yellow', 'amarillo'),
         ('violet', 'violeta'),
         ('green', 'verde'),
         ('yellow', 'amarillo'),
         ('black', 'negro'),
         ('white', 'blanco'))


class Cliente(models.Model):
    usuario = models.OneToOneField(User,
                                   on_delete=models.CASCADE,
                                   primary_key=True,
                                   limit_choices_to={'is_cliente': True},
                                   related_name='cliente')
    created = models.DateField(auto_now_add=True)
    slug = models.SlugField(max_length=20,
                            unique=True,
                            blank=True)
    admin = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              limit_choices_to={'is_staff': True},
                              related_name='admin')
    color = models.CharField(choices=COLOR,
                             max_length=10)
    logo = models.ForeignKey(Logo,
                             on_delete=models.CASCADE,
                             default=None)

    def __str__(self):
        return self.usuario.empresa

    def get_every_two(self):
        newWord = ''
        for char in self.usuario.empresa[::2]:
            newWord += char

        return newWord[:3]

    # TODO : funcion que haga unico el slug del cliente cojo de 2 en 2, poco elegante
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.get_every_two()
        return super(Cliente, self).save()

class Zona(models.Model):
    cliente = models.ForeignKey(Cliente,
                                on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50,
                              null=True,
                              unique=False)

    class Metal:
        unique_together =('cliente', 'nombre')

    def __str__(self):
        return f'{self.cliente.usuario.empresa}//{self.nombre}'


COMUNIDADES = (
        ("AND", 'Andalucía'),
        ("ARA", 'Aragón'),
        ("AST", 'Asturias'),
        ("CAN", 'Cantabria'),
        ("CYL", 'Castilla-Leon'),
        ("CAT", 'Cataluña'),
        ("CEUTA", 'Ceuta'),
        ("EXT", 'Extremadura'),
        ("GAL", 'Galicia'),
        ("BAL", 'Islas Baleares'),
        ("RIO", 'Rioja'),
        ("MAD", 'Madrid'),
        ("MEL", 'Melilla'),
        ("MUR", 'Murcia'),
        ("NAV", 'Navarra'),
        ("VAL", 'Valencia'),
)


class Montador(models.Model):
    usuario = models.OneToOneField(User,
                                   on_delete=models.CASCADE,
                                   primary_key=True,
                                   limit_choices_to={'is_montador': True})
    dni = models.CharField(max_length=9,
                           null=True,
                           blank=True
                           )
    ciudad = models.CharField(max_length=50,
                              null=True,
                              blank=True
                              )
    provincia = models.CharField(max_length=50,
                                 null=True,
                                 blank=True
                                 )
    comunidad = models.CharField(max_length=50,
                                 choices=COMUNIDADES,
                                 null=True,
                                 blank=True
                                 )

    def __str__(self):
        return f'{self.usuario.empresa}-{self.usuario.first_name}'

TRUE_FALSE_CHOICES = (
        (True, 'Si'),
        (False, 'No')
    )
class Pdv(models.Model):
    cliente = models.ManyToManyField(Cliente)
    campanas = models.ManyToManyField('Campana', through='Campana_Pdv')
    #TODO como elgeimos el slug en el pdv?
    slug = models.SlugField(max_length=10)
    cadena = models.CharField(max_length=50,
                              null=True,
                              blank=True
                              )
    nombre = models.CharField(max_length=50)
    direccion = models.TextField(max_length=300,
                                 null=True,
                                 blank=True
                                 )
    cp = models.IntegerField(null=True,
                             blank=True)
    ciudad = models.CharField(max_length=50,
                              null=True,
                              blank=True
                              )
    provincia = models.CharField(max_length=50,
                                 null=True,
                                 blank=True
                                 )
    prioridad = models.IntegerField(null=True,
                                    blank=True
                                    )
    activo = models.BooleanField(default=False)
    zona = models.ForeignKey(Zona,
                             on_delete=models.SET_NULL,
                             null=True,
                             blank=True)
    permisos = models.BooleanField(default=True,
                                   choices=TRUE_FALSE_CHOICES)
    observaciones = models.TextField(max_length=500,
                                    null = True,
                                    blank= True)

    mail = models.EmailField(max_length = 100, null = True, blank = True)
    telefono = models.IntegerField(null = True, blank= True)
    persona_contacto = models.CharField(max_length = 100, null = True, blank = True)



    def __str__(self):
        return self.nombre




class TipoPdi(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class Pdi(models.Model):
    pdv = models.ForeignKey(Pdv, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    tipo = models.ForeignKey(TipoPdi,
                             on_delete=models.CASCADE)
    anchoTotal = models.IntegerField(null=True,
                                     blank=True
                                     )
    anchoVista = models.IntegerField(null=True,
                                     blank=True
                                     )
    altoTotal = models.IntegerField(null=True,
                                    blank=True
                                     )
    altoVista = models.IntegerField(null=True,
                                    blank=True
                                     )
    material = models.ForeignKey('Material',
                                 on_delete=models.CASCADE,
                                 default=None)
    activo = models.BooleanField(default=True)
    composicion = models.BooleanField(default=False)
    instaladores = models.IntegerField()

    def __str__(self):
        return f"{self.pdv}-{self.nombre}"


pdv_estados =(('ok', 'ok'),
              ('ko', 'ko'),
              ('incidencia', 'incidencia'),
              ('pendiente', 'pendiente'))


class Creatividad(models.Model):
    campana = models.ForeignKey("Campana", on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    imagen = models.ImageField(upload_to='images/creatividades')

    def __str__(self):
        return self.nombre

IDIOMAS = (('finalizada', 'Finalizada'),
           ('iniciada', 'Iniciada'),)

class Campana(models.Model):
    cliente = models.ForeignKey(Cliente,
                                on_delete=models.CASCADE)
    pdvs = models.ManyToManyField('Pdv', through='Campana_Pdv')
    nombre = models.CharField(max_length=50)
    comentarios = models.TextField(max_length=500,
                                   null=True,
                                   blank=True)
    estado = models.CharField(choices=pdv_estados,
                              max_length=15,
                              default="iniciada")
    activo = models.BooleanField(default=False)
    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_cambio = models.DateField(auto_now=True)
    fecha_finalizado = models.DateField(null=True,
                                        blank=True)

    def __str__(self):
        return f'{self.cliente}-{self.nombre}'


IDIOMAS = (('Español', 'Español'),
           ('Catalán', 'Catalán'),
           ('Gallego', 'Gallego'),
           ('Euskera', 'Euskera'),
           ('Inglés', 'Inglés'),)

def pdi_image_path(instance, filename):
    return f'images/{instance.Campana_Pdv.campana.nombre}/{instance.Campana_Pdv.pdv.slug}/{instance.pdi.nombre}/{filename}'


pdv_estados =(('atendida', 'atendida'),
              ('suspendida', 'suspendida'),
              ('incidencia', 'incidencia'),
              ('finalizada', 'finalizada'))

class Campana_Pdv(models.Model):
    campana = models.ForeignKey(Campana,on_delete=models.CASCADE)
    pdv = models.ForeignKey(Pdv, on_delete=models.CASCADE)
    estado = models.CharField(choices=pdv_estados,
                              max_length=15)
    idioma = models.CharField(choices=IDIOMAS,
                              max_length=10,
                              null=True,
                              blank=True)
    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_cambio = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.campana.nombre}//{self.pdv.nombre}'


class Material(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

def instalacionPdi_imagen(instance, filename):
    return f'images/{instance.CampanapdV_pdI.pdi.nombre}/{instance.CampanapdV_pdI.fecha_cambio}/{filename}'

class CampanapdV_pdI(models.Model):
    Campana_Pdv = models.ForeignKey(Campana_Pdv, on_delete=models.CASCADE)
    pdi = models.ForeignKey(Pdi, on_delete=models.CASCADE)
    creatividad = models.ForeignKey(Creatividad,
                                    on_delete=models.CASCADE,
                                    null=True,
                                    blank=True)
    user_montador = models.ManyToManyField(User,
                                 null=True,
                                 blank=True
                                 )
    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_cambio = models.DateField(auto_now=True)
    # TODO: boton para desplegar todas las datatables extendibles
    # TODO : poner el color del cliente look n feel

    def __str__(self):
        return f'{self.Campana_Pdv.campana}//{self.Campana_Pdv.pdv}//{self.pdi}'

comentarioTipo = (('ok', 'ok'),
                  ('ko', 'ko'),
                  ('incidencia', 'incidencia'),
                  ('admin', 'admin')
                  )

class Montador_images(models.Model):
    CampanapdV_pdI = models.ForeignKey(CampanapdV_pdI,
                                        on_delete=models.CASCADE)
    image = models.ImageField(upload_to=instalacionPdi_imagen,
                              null=True,
                              blank=True)
class Comments(models.Model):
    Campana_Pdv = models.ForeignKey(Campana_Pdv, on_delete=models.CASCADE)
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Comments = models.CharField(max_length=500,
                                null=True,
                                blank=True)
    tipo = models.CharField(choices=comentarioTipo,
                            max_length=10,
                            null=True,
                            blank=True)
    visible = models.BooleanField(default=False)
    fecha_creacion = models.DateField(auto_now_add=True)



