from django.db import models
from usuarios.models import PerfilUsuario
from thumbnails.fields import ImageField

class Publicacion(models.Model):
    titulo = models.CharField(verbose_name='Titulo de la publicacion:', max_length=50, blank=True, null=False)
    autor = models.ForeignKey(PerfilUsuario, verbose_name='Autor:', on_delete=models.CASCADE, related_name='publicaciones')
    imagen = ImageField(verbose_name='Imagen del post:', upload_to='publicaciones/img/')
    video = models.FileField(verbose_name='Video de la publicacion:', upload_to='publicaciones/video/', null=True)
    contenido = models.TextField(verbose_name='Contenido de la publicacion', max_length=300, blank=True)
    fecha_publicacion = models.DateTimeField(verbose_name='Fecha de creacion:', auto_now_add=True)
    likes = models.ManyToManyField(PerfilUsuario, verbose_name='Likes de la publicacion:', related_name='likes_publicacion')

    def like(self, usuario):    
        self.likes.add(usuario)

    def unlike(self, usuario):
        self.likes.remove(usuario)

    def total_comentarios(self):
        comentarios = Comentario.objects.filter(publicacion=self).count()
        respuestas = RespuestaComentario.objects.filter(publicacion=self).count()
        return comentarios + respuestas

    class Meta:
        verbose_name = 'Publicacion'
        verbose_name_plural = 'Publicaciones'

    def __str__(self):
        return f'{self.titulo}'


class Comentario(models.Model):
    publicacion = models.ForeignKey(Publicacion, verbose_name='Publicacion a comentar:', on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(PerfilUsuario, verbose_name='Autor:', on_delete=models.CASCADE, related_name='comentarios')
    texto = models.TextField(verbose_name='Nuevo comentario:', max_length=500)
    fecha_comentario = models.DateTimeField(verbose_name='Fecha del comentario:', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'

    def __str__(self):
        return f'{self.texto}'


class RespuestaComentario(models.Model):
    publicacion = models.ForeignKey(Publicacion, verbose_name='Publicacion:', on_delete=models.CASCADE, related_name='respuestas_publicacion')
    comentario = models.ForeignKey(Comentario, verbose_name='Comentario a responder:', on_delete=models.CASCADE, related_name='respuestas')
    autor = models.ForeignKey(PerfilUsuario, verbose_name="Autor:", on_delete=models.CASCADE, related_name='respuestas')
    respuesta = models.TextField(verbose_name='Responder comentario:', max_length=300)
    fecha_respuesta = models.DateTimeField(verbose_name='Fecha de respuesta:', auto_now_add=True)

    class Meta:
        verbose_name= 'Respuesta'
        verbose_name_plural = 'Respuestas'

    def __str__(self):
        return f'{self.respuesta}'