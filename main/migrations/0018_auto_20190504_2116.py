# Generated by Django 2.2 on 2019-05-04 21:16

from django.db import migrations, models
import django.db.models.deletion
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_auto_20190504_1952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campanapdv_pdi',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=main.models.pdi_image_path),
        ),
        migrations.AlterField(
            model_name='campanapdv_pdi',
            name='montador',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Montador'),
        ),
    ]