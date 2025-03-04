from django.db import models
from usuarios.models import PerfilUsuario

class Publicacion(models.Model):
    titulo = models.CharField(verbose_name='Titulo de la publicacion:', max_length=50, blank=True, null=False)
    autor = models.ForeignKey(PerfilUsuario, verbose_name='Autor:', on_delete=models.CASCADE, related_name='publicaciones')
    imagen = models.ImageField(verbose_name='Imagen del post:', upload_to='publicaciones/img/')
    video = models.FileField(verbose_name='Video de la publicacion:', upload_to='publicaciones/video/', null=True)
    fecha_publicacion = models.DateTimeField(verbose_name='Fecha de creacion:', auto_now_add=True)
    likes = models.ManyToManyField(PerfilUsuario, verbose_name='Likes de la publicacion:', related_name='likes_publicacion')

    class Meta:
        verbose_name = 'Publicacion'
        verbose_name_plural = 'Publicaciones'

    def __str__(self):
        return f'Titulo: {self.titulo} - Autor: {self.usuario} - Fecha publicacion: {self.fecha_publicacion}'


class Comentario(models.Model):
    publicacion = models.ForeignKey(Publicacion, verbose_name='Publicacion a comentar:', on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(PerfilUsuario, verbose_name='Autor:', on_delete=models.CASCADE, related_name='comentarios')
    contenido = models.CharField(verbose_name='Comentario de la publicacion:', max_length=500)
    fecha_comentario = models.DateTimeField(verbose_name='Fecha del comentario:', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'

    def __str__(self):
        return f'Comentario creado por el ususario {self.autor} en la fecha: {self.fecha_comentario}'