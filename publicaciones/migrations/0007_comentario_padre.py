# Generated by Django 5.1.6 on 2025-03-11 11:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publicaciones', '0006_alter_comentario_texto'),
    ]

    operations = [
        migrations.AddField(
            model_name='comentario',
            name='padre',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='respuestas', to='publicaciones.comentario'),
        ),
    ]
