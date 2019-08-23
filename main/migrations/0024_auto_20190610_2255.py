# Generated by Django 2.2.1 on 2019-06-10 22:55

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_auto_20190607_2015'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campanapdv_pdi',
            name='montador',
        ),
        migrations.AddField(
            model_name='campanapdv_pdi',
            name='user_montador',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
