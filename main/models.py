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


COLOR = (('red', 'red'),
         ('blue', 'blue'),
         ('yellow', 'yellow'))


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


class Montador(models.Model):
    usuario = models.OneToOneField(User,
                                   on_delete=models.CASCADE,
                                   primary_key=True,
                                   limit_choices_to={'is_montador': True})
    dni = models.CharField(max_length=9)
    ciudad = models.CharField(max_length=50)
    provincia = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.usuario.empresa}-{self.usuario.first_name}'


class Pdv(models.Model):
    campanas = models.ManyToManyField('Campana', through='Campana_Pdv')
    slug = models.SlugField(max_length=10)
    cadena = models.CharField(max_length=50)
    nombre = models.CharField(max_length=50)
    direccion = models.TextField(max_length=300)
    cp = models.IntegerField()
    ciudad = models.CharField(max_length=50)
    provincia = models.CharField(max_length=50)
    prioridad = models.IntegerField()
    activo = models.BooleanField(default=False)

    def __str__(self):
        return self.slug


class TipoPdi(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class Pdi(models.Model):
    pdv = models.ForeignKey(Pdv, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    tipo = models.ForeignKey(TipoPdi,
                             on_delete=models.CASCADE)
    anchoTotal = models.IntegerField()
    anchoVista = models.IntegerField()
    altoTotal = models.IntegerField()
    altoVista = models.IntegerField()
    activo = models.BooleanField()
    composicion = models.BooleanField()
    instaladores = models.IntegerField()

    def __str__(self):
        return f"{self.pdv}-{self.nombre}"


pdv_estados =(('ok', 'ok'),
              ('ko', 'ko'),
              ('incidencia', 'incidencia'))


class Creatividad(models.Model):
    campana = models.ForeignKey("Campana", on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    imagen = models.ImageField(upload_to='images/creatividades')

    def __str__(self):
        return self.nombre


class Campana(models.Model):
    cliente = models.ForeignKey(Cliente,
                                on_delete=models.CASCADE)
    pdvs = models.ManyToManyField('Pdv', through='Campana_Pdv')
    nombre = models.CharField(max_length=50)
    comentarios = models.TextField(max_length=500)
    estado = models.CharField(choices=pdv_estados,
                              max_length=15)
    activo = models.BooleanField()
    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_cambio = models.DateField(auto_now=True)
    fecha_finalizado = models.DateField(null=True,
                                        blank=True)

    def __str__(self):
        return f'{self.cliente}-{self.nombre}'


IDIOMAS = (('esp', 'Español'),
           ('cat', 'Catalán'),
           ('gal', 'Gallego'),
           ('eu', 'Euskera'),
           ('eng', 'Inglés'),)

def pdi_image_path(instance, filename):
    return f'images/{instance.Campana_Pdv.campana.nombre}/{instance.Campana_Pdv.pdv.slug}/{instance.pdi.nombre}/{filename}'

class Campana_Pdv(models.Model):
    campana = models.ForeignKey(Campana,on_delete=models.CASCADE)
    pdv = models.ForeignKey(Pdv, on_delete=models.CASCADE)
    estado = models.CharField(choices=pdv_estados,
                              max_length=15)
    idioma = models.CharField(choices=IDIOMAS, max_length=10)
    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_cambio = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.campana.nombre}//{self.pdv.nombre}'


class Material(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

def instalacionPdi_imagen(instance, filename):
    return f'images/{instance.pdi.nombre}/{instance.fecha_camio}/{filename}'

class CampanapdV_pdI(models.Model):
    Campana_Pdv = models.ForeignKey(Campana_Pdv, on_delete=models.CASCADE)
    pdi = models.ForeignKey(Pdi, on_delete=models.CASCADE)
    creatividad = models.ForeignKey(Creatividad,
                                    on_delete=models.CASCADE,
                                    null=True,
                                    blank=True)
    material = models.ForeignKey(Material,on_delete=models.CASCADE)
    image = models.ImageField(upload_to=instalacionPdi_imagen,
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
class Comments(models.Model):
    Campana_Pdv = models.ForeignKey(Campana_Pdv, on_delete=models.CASCADE)
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Comments = models.CharField(max_length=500)
    tipo = models.CharField(choices=comentarioTipo,
                            max_length=10)
    visible = models.BooleanField(default=False)
    fecha_creacion = models.DateField(auto_now_add=True)



