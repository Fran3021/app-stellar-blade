# Generated by Django 5.1.6 on 2025-03-18 13:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notificaciones', '0017_notificacionrespuestacomentario'),
        ('publicaciones', '0012_respuestacomentario_publicacion'),
        ('usuarios', '0003_alter_follow_fecha_inicio'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificacionMeGusta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('leida', models.BooleanField(default=False, verbose_name='¿Leida?')),
                ('url', models.URLField(blank=True, null=True, verbose_name='url de la publicacion:')),
                ('destinatario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='me_gusta_destinatario', to='usuarios.perfilusuario', verbose_name='Usuario al que pertenece la publicacion que le ha dado a me gusta:')),
                ('publicacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='publicaciones.publicacion', verbose_name='Publicacion que pertenece el me gusta:')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='me_gusta_usuario', to='usuarios.perfilusuario', verbose_name='Usuario que ha dado me gusta:')),
            ],
        ),
    ]
