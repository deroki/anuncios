# Generated by Django 2.2.1 on 2019-07-15 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0033_pdv_cliente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zona',
            name='nombre',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
