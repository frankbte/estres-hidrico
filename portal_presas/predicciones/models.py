from django.db import models

# Create your models here.


class predicciones(models.Model):
    presa = models.CharField(max_length=30)
    imagen = models.ImageField(upload_to='predicciones/imagenes/')

    def __str__(self):
        return self.presa