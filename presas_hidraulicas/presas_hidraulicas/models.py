from django.db import models

class Presa(models.Model):
    clave_presa = models.CharField(max_length=10, primary_key=True)  # Clave primaria
    nombre_completo = models.CharField(max_length=255)
    nombre_comun = models.CharField(max_length=255, null=True, blank=True)
    estado = models.CharField(max_length=100)
    municipio = models.CharField(max_length=100)
    rio = models.CharField(max_length=100)
    latitud = models.DecimalField(max_digits=10, decimal_places=8)
    longitud = models.DecimalField(max_digits=11, decimal_places=8)
    altitud = models.DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        managed = False  # Evita que Django intente crear esta tabla automáticamente
        db_table = 'presas'  # Especifica el nombre de la tabla en la base de datos

    def __str__(self):
        return self.nombre_completo


class DatosClima(models.Model):
    id_clima = models.AutoField(primary_key=True)  # Agrega id_clima como clave primaria
    clave_presa = models.ForeignKey(Presa, on_delete=models.CASCADE, db_column='clave_clima')  # Cambiar a clave_presa
    fecha_lectura = models.DateField()
    almacenamiento = models.DecimalField(max_digits=10, decimal_places=2)
    temp = models.DecimalField(max_digits=5, decimal_places=2)
    humidity = models.DecimalField(max_digits=5, decimal_places=2)
    precip = models.DecimalField(max_digits=5, decimal_places=2)
    preciptype = models.IntegerField()
    uvindex = models.DecimalField(max_digits=5, decimal_places=2)
    conditions_clear = models.DecimalField(max_digits=5, decimal_places=2)
    conditions_overcast = models.DecimalField(max_digits=5, decimal_places=2)
    conditions_partially_cloudy = models.DecimalField(max_digits=5, decimal_places=2)
    conditions_rain = models.DecimalField(max_digits=5, decimal_places=2)
    conditions_rain_overcast = models.DecimalField(max_digits=5, decimal_places=2)
    conditions_rain_partially_cloudy = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        managed = False  # Evita que Django intente crear esta tabla automáticamente
        db_table = 'datos_clima'  # Especifica el nombre de la tabla en la base de datos

    def __str__(self):
        return f"Clima para {self.clave_presa} en {self.fecha_lectura}"


class Almacenamiento(models.Model):
    id_almacenamiento = models.AutoField(primary_key=True)  # Define id_almacenamiento como clave primaria
    clave_presa = models.ForeignKey(Presa, on_delete=models.CASCADE, db_column='clave_presa')  # Relación con la tabla presas
    fecha = models.DateField()
    nivel_agua = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False  # Evita que Django intente crear esta tabla automáticamente
        db_table = 'almacenamiento'  # Especifica el nombre de la tabla en la base de datos

    def __str__(self):
        return f"Nivel de agua de {self.clave_presa} en {self.fecha}"
