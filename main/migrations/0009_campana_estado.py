# Generated by Django 2.2 on 2019-04-25 01:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20190424_1758'),
    ]

    operations = [
        migrations.AddField(
            model_name='campana',
            name='estado',
            field=models.CharField(choices=[('ok', 'ok'), ('pendiente', 'pendiente'), ('incidencia', 'incidencia')], default='pendiente', max_length=15),
            preserve_default=False,
        ),
    ]
