# Generated by Django 5.1.6 on 2025-03-04 19:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inicio', models.DateTimeField(verbose_name='Fecha de inicio')),
            ],
            options={
                'verbose_name': 'Seguidor',
                'verbose_name_plural': 'Seguidores',
            },
        ),
        migrations.CreateModel(
            name='PerfilUsuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen_perfil', models.ImageField(blank=True, null=True, upload_to='usuarios/img_perfil/', verbose_name='Imagen de perfil:')),
                ('biografia', models.CharField(blank=True, max_length=300, verbose_name='Biografia del ususario:')),
                ('fecha_nacimiento', models.DateField(blank=True, default='1900-01-01', null=True, verbose_name='Fecha de nacimiento:')),
                ('seguidores', models.ManyToManyField(related_name='siguiendo', through='usuarios.Follow', to='usuarios.perfilusuario', verbose_name='Seguidores')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='perfil', to=settings.AUTH_USER_MODEL, verbose_name='Usuario:')),
            ],
            options={
                'verbose_name': 'Perfil',
                'verbose_name_plural': 'Perfiles',
            },
        ),
        migrations.AddField(
            model_name='follow',
            name='seguidor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='siguiendo_set', to='usuarios.perfilusuario', verbose_name='Seguidor'),
        ),
        migrations.AddField(
            model_name='follow',
            name='siguiendo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seguidores_set', to='usuarios.perfilusuario', verbose_name='Siguiendo'),
        ),
        migrations.AlterUniqueTogether(
            name='follow',
            unique_together={('seguidor', 'siguiendo')},
        ),
    ]
