# Generated by Django 5.1.6 on 2025-03-31 15:52

import thumbnails.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0003_alter_follow_fecha_inicio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfilusuario',
            name='imagen_perfil',
            field=thumbnails.fields.ImageField(blank=True, null=True, upload_to='usuarios/img_perfil/', verbose_name='Imagen de perfil:'),
        ),
    ]
