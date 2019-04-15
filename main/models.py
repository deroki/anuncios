from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Logo(models.Model):
    image = models.ImageField(upload_to='images/')
    datestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.image.name


COLOR = (('red', 'red'),
         ('blue', 'blue'),
         ('yellow', 'yellow'))


class Cliente(models.Model):
    nombre = models.CharField(max_length=20)
    created = models.DateField(auto_now_add=True)
    slug = models.SlugField(max_length=20,
                            unique= True,
                            blank= True)
    admin = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              limit_choices_to={'is_staff': True})
    color = models.CharField(choices=COLOR,
                             max_length=10)
    logo = models.ForeignKey(Logo,
                             on_delete=models.CASCADE,
                             default= None)

    def get_every_two(self):
        newWord = ''
        for char in self.nombre[::2]:
            newWord += char

        return newWord[:3]

# TODO : funcion que haga unico el slug del cliente cojo de 2 en 2, poco elegante
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.get_every_two()
        return super(Cliente,self).save()