from django.db import models
from django.contrib.auth.models import AbstractUser


class Perfil(models.Model):
    nombre = models.CharField(max_length=35)

    class Meta:
        verbose_name_plural = 'Perfiles'

    def __str__(self):
        return self.nombre


class Usuario(AbstractUser):
    perfil = models.ForeignKey(Perfil, related_name="usuarios",on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return self.username
    
    def sectores_permitidos(self):
        if self.perfil:
            return self.perfil.perfiles_sectores.first().sectores.all()



class PerfilSector(models.Model):
    perfil = models.ForeignKey(Perfil, related_name="perfiles_sectores", on_delete=models.CASCADE)
    sectores = models.ManyToManyField('chat.Sector', related_name='perfiles_sectores')

    class Meta:
        verbose_name = 'Perfil sector'
        verbose_name_plural = 'Perfiles sectores'