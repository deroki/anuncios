# Generated by Django 2.2 on 2019-04-24 17:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20190424_0338'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campana',
            name='creatividad',
        ),
        migrations.RemoveField(
            model_name='campana',
            name='material',
        ),
        migrations.AddField(
            model_name='campana_pdv_pdi',
            name='creatividad',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='application.Creatividad'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='campana_pdv_pdi',
            name='material',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='application.Material'),
            preserve_default=False,
        ),
    ]
