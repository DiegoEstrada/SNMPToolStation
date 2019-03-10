from django.db import models

# Create your models here.
class Agent(models.Model):
    name = models.CharField(primary_key=True, max_length=50)
    hostname = models.TextField(max_length=20, null=False)
    version = models.PositiveSmallIntegerField(null=False)
    puerto = models.IntegerField(null=False)
    grupo = models.TextField(max_length=50, null=False)
    

class Image(models.Model):
    location = models.TextField(max_length=1000, null=False)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)