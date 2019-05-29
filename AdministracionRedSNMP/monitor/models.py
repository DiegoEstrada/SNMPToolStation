from django.db import models

# Create your models here.
class Agent(models.Model):
    name = models.CharField(primary_key=True, max_length=50)
    hostname = models.TextField(max_length=20, null=False)
    version = models.PositiveSmallIntegerField(null=False)
    puerto = models.IntegerField(null=False)
    grupo = models.TextField(max_length=50, null=False)
    email = models.EmailField(max_length=254, null=False, default="samplemail@hotmail.com")
    

class Image(models.Model):
    location = models.TextField(max_length=1000, null=False)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)


class Router(models.Model):
    ip = models.CharField(primary_key=True, max_length=200, null=False)
    getway = models.CharField( max_length=200, null=False,)
    hostname = models.CharField(max_length=100, null=True)
    version = models.PositiveSmallIntegerField(null=True)
    puerto = models.IntegerField(null=True)
    grupo = models.CharField(max_length=50, null=True)
    os = models.CharField(max_length=250, null=True)
    interfaces = models.PositiveSmallIntegerField(null=True)
    ubicacion = models.TextField(null=True)
    contacto = models.TextField(null=True)
    # Cadena con el contenido del archivo de configuración
    archivo = models.TextField(null=True, default="")