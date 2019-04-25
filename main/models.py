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


class Material(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class Creatividad(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class Pdi(models.Model):
    pdv = models.ForeignKey(Pdv,
                            on_delete=models.CASCADE,
                            )
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


campana_estados =(('ok', 'ok'),
                  ('pendiente', 'pendiente'),
                  ('incidencia', 'incidencia'))

class Campana(models.Model):
    cliente = models.ForeignKey(Cliente,
                                on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    # TODO: creatividad depende del pdi, y los materiales tb
    comentarios = models.TextField(max_length=500)
    estado = models.CharField(choices=campana_estados,
                              max_length=15)
    activo = models.BooleanField()
    fecha_creaccion = models.DateField(auto_now_add=True)
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
    return f'images/{instance.campana.nombre}/{instance.pdv.slug}/{instance.pdi.nombre}/{filename}'


class Campana_pdV_pdI(models.Model):
    campana = models.ForeignKey(Campana, on_delete=models.CASCADE)
    pdv = models.ForeignKey(Pdv, on_delete=models.CASCADE)
    pdi = models.ForeignKey(Pdi, on_delete=models.CASCADE)
    material = models.ForeignKey(Material,on_delete=models.CASCADE)
    creatividad = models.ForeignKey(Creatividad,on_delete=models.CASCADE)
    image = models.ImageField(upload_to=pdi_image_path)
    idioma = models.CharField(choices=IDIOMAS, max_length=10)
    montador = models.ForeignKey(Montador,on_delete=models.CASCADE)
    fecha_creaccion = models.DateField(auto_now_add=True)
    fecha_cambio = models.DateField(auto_now=True)
    # TODO: boton para desplegar todas las datatables extendibles
    # TODO : poner el color del cliente look n feel







