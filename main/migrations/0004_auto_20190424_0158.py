# Generated by Django 2.2 on 2019-04-24 01:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20190424_0133'),
    ]

    operations = [
        migrations.RenameField(
            model_name='campana_pdv_pdi',
            old_name='idioma',
            new_name='idiom',
        ),
    ]